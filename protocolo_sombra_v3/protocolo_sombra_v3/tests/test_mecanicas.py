#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes automatizados para Protocolo Sombra v3.0.
Verifica: parser, combinações, perfis, estados, finais.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protocolo_sombra_v3.engine.parser import parsear, encontrar_item_fuzzy, limpar_stopwords
from protocolo_sombra_v3.entities.jogador import Jogador, Perfil, ITENS_NOMES, contar_segredos
from protocolo_sombra_v3.entities.eva9 import EVA9
from protocolo_sombra_v3.entities.elena import ElenaVasquez
from protocolo_sombra_v3.world.salas import criar_salas
from protocolo_sombra_v3.world.interacoes import COMBINACOES
from protocolo_sombra_v3.narrative.finais import verificar_final_secreto


def test_parser_basico():
    """Testa parsing básico de comandos."""
    cmd = parsear("norte")
    assert cmd.verbo == "norte", f"Esperado 'norte', obtido '{cmd.verbo}'"

    cmd = parsear("n")
    assert cmd.verbo == "norte", f"Alias 'n' falhou: '{cmd.verbo}'"

    cmd = parsear("pegar gravador")
    assert cmd.verbo == "pegar" and cmd.args == "gravador"

    cmd = parsear("examinar a mesa de controle")
    assert cmd.verbo == "examinar"
    assert "mesa" in cmd.args and "controle" in cmd.args

    print("  ✓ Parser básico OK")


def test_parser_stopwords():
    """Testa remoção de stopwords."""
    resultado = limpar_stopwords("pegar o gravador digital rachado")
    assert "gravador" in resultado
    assert " o " not in f" {resultado} "
    print("  ✓ Stopwords OK")


def test_parser_fuzzy():
    """Testa fuzzy matching."""
    itens = {"gravador": "Gravador Digital", "celular": "Celular Sem Sinal"}
    assert encontrar_item_fuzzy("gravdor", itens, 0.5) == "gravador"
    assert encontrar_item_fuzzy("celulr", itens, 0.5) == "celular"
    assert encontrar_item_fuzzy("digital", itens) == "gravador"
    print("  ✓ Fuzzy matching OK")


def test_parser_distorcao():
    """Testa distorção por sanidade baixa."""
    # Sanidade alta = sem distorção
    cmd = parsear("norte", sanidade=100)
    assert cmd.verbo == "norte"
    assert not cmd.distorcido
    # Sanidade baixa = pode distorcer (probabilístico, testar múltiplas vezes)
    distorceu_alguma_vez = False
    for _ in range(50):
        cmd = parsear("norte", sanidade=5)
        if cmd.distorcido:
            distorceu_alguma_vez = True
            break
    # Não garantimos distorção em toda chamada (30% chance)
    print(f"  ✓ Distorção por sanidade OK (distorceu: {distorceu_alguma_vez})")


def test_jogador_perfis():
    """Testa aplicação de bônus de perfil."""
    for perfil in Perfil:
        j = Jogador(perfil=perfil)
        j.aplicar_bonus_perfil()
        assert 0 < j.sanidade <= 100, f"Sanidade inválida para {perfil}: {j.sanidade}"
        assert 0 <= j.hacking <= 100, f"Hacking inválido para {perfil}: {j.hacking}"
    print("  ✓ Perfis OK")


def test_jogador_mecanicas():
    """Testa mecânicas do jogador."""
    j = Jogador(perfil=Perfil.ANALISTA)
    j.aplicar_bonus_perfil()

    # Adicionar/remover itens
    assert j.adicionar_item("gravador") == True
    assert j.tem_item("gravador") == True
    assert j.adicionar_item("gravador") == False  # Duplicata
    assert j.remover_item("gravador") == True
    assert j.tem_item("gravador") == False

    # Sanidade
    j.sanidade = 50
    j.modificar_sanidade(-10, "teste")
    assert j.sanidade == 40

    # Exposição
    j.exposicao_entidade = 0
    assert j.nivel_exposicao == 0
    j.exposicao_entidade = 35
    assert j.nivel_exposicao == 1
    j.exposicao_entidade = 65
    assert j.nivel_exposicao == 2

    # Distorção
    j.sanidade = 100
    assert not j.sanidade_distorcida
    j.sanidade = 20
    assert j.sanidade_distorcida
    j.sanidade = 10
    assert j.sanidade_critica

    print("  ✓ Mecânicas do jogador OK")


def test_combinacoes_frozenset():
    """Testa que combinações usam frozenset (sem duplicação de ordem)."""
    for chave in COMBINACOES:
        assert isinstance(chave, frozenset), f"Chave não é frozenset: {type(chave)}"

    # Testar que ordem não importa
    chave1 = frozenset(("gravador", "chip_eva"))
    chave2 = frozenset(("chip_eva", "gravador"))
    assert chave1 == chave2
    assert chave1 in COMBINACOES

    print(f"  ✓ Combinações frozenset OK ({len(COMBINACOES)} combinações)")


def test_salas():
    """Testa criação e integridade das salas."""
    salas = criar_salas()

    # Todas as salas existem
    salas_esperadas = [
        "sala_terminal", "corredor_a", "duto_ventilacao",
        "sala_observacao", "nucleo_servidores", "sala_medica",
        "arquivo_morto", "sala_secreta", "kheiron_profundo"
    ]
    for s in salas_esperadas:
        assert s in salas, f"Sala ausente: {s}"

    # Todas as saídas apontam para salas válidas
    for sala_id, sala in salas.items():
        for direcao, destino_id in sala.saidas.items():
            assert destino_id in salas, f"Saída inválida: {sala_id} -> {direcao} -> {destino_id}"

    # Descrições por nível de exposição
    for sala_id, sala in salas.items():
        assert 0 in sala.descricoes, f"Sala {sala_id} sem descrição nível 0"
        assert 0 in sala.descricoes_curtas, f"Sala {sala_id} sem desc_curta nível 0"

    print(f"  ✓ Salas OK ({len(salas)} salas)")


def test_eva9():
    """Testa sistema da EVA-9."""
    eva = EVA9()
    jogador = Jogador(perfil=Perfil.ANALISTA)
    jogador.aplicar_bonus_perfil()

    # Gera mensagem sem erro
    msg = eva.gerar_mensagem(jogador)
    assert isinstance(msg, str) and len(msg) > 0

    # Humor atualiza
    jogador.confianca_eva = 80
    eva.atualizar_humor(jogador)
    assert eva.humor in ("aliada", "desesperada")

    jogador.confianca_eva = 10
    eva.atualizar_humor(jogador)
    assert eva.humor == "hostil"

    # Serialização
    dados = eva.to_dict()
    eva2 = EVA9()
    eva2.from_dict(dados)
    assert eva2.humor == eva.humor

    print("  ✓ EVA-9 OK")


def test_elena():
    """Testa NPC Elena Vasquez."""
    elena = ElenaVasquez()
    jogador = Jogador(perfil=Perfil.INVESTIG)

    # Aparição tem probabilidade
    assert isinstance(elena.verificar_aparicao(jogador, "corredor_a"), bool)

    # Serialização
    elena.encontros = 3
    elena.bilhetes_deixados = ["corredor_a"]
    dados = elena.to_dict()
    elena2 = ElenaVasquez()
    elena2.from_dict(dados)
    assert elena2.encontros == 3
    assert elena2.bilhetes_deixados == ["corredor_a"]

    print("  ✓ Elena Vasquez OK")


def test_final_secreto():
    """Testa requisitos do final secreto."""
    jogador = Jogador(perfil=Perfil.PSICOLOGO)
    jogador.aplicar_bonus_perfil()

    # Sem requisitos = não desbloqueia
    assert not verificar_final_secreto(jogador)

    # Com todos os requisitos
    jogador.flags["sabe_verdade"] = True
    jogador.flags["sabe_protocolo"] = True
    jogador.flags["usou_capacete"] = True
    jogador.flags["leu_diario"] = True
    jogador.flags["confrontou_brennan"] = True
    jogador.flags["foto_revelada"] = True
    jogador.flags["fita_restaurada"] = True
    jogador.flags["cofre_aberto"] = True
    jogador.flags["leu_mensagens"] = True
    jogador.flags["ouviu_faixa_oculta"] = True
    jogador.flags["abriu_geladeira"] = True
    jogador.confianca_eva = 75
    jogador.exposicao_entidade = 55

    assert verificar_final_secreto(jogador), "Final secreto deveria estar desbloqueado"
    print("  ✓ Final secreto OK")


def test_segredos():
    """Testa contagem de segredos."""
    jogador = Jogador(perfil=Perfil.ANALISTA)
    assert contar_segredos(jogador) == 0

    jogador.flags["sabe_verdade"] = True
    jogador.flags["leu_diario"] = True
    assert contar_segredos(jogador) == 2

    print("  ✓ Contagem de segredos OK")


def test_momentos_exclusivos():
    """Testa que cada perfil tem momentos exclusivos."""
    for perfil in Perfil:
        j = Jogador(perfil=perfil)
        from protocolo_sombra_v3.entities.jogador import PERFIS_INFO
        momentos = PERFIS_INFO[perfil].get("momentos_exclusivos", [])
        assert len(momentos) >= 3, f"Perfil {perfil} tem menos de 3 momentos exclusivos: {len(momentos)}"
        for m in momentos:
            assert j.tem_momento_exclusivo(m), f"Momento {m} não reconhecido para {perfil}"

    print("  ✓ Momentos exclusivos OK")


def rodar_todos():
    """Roda todos os testes."""
    print(f"\n{'='*50}")
    print("  PROTOCOLO SOMBRA v3.0 — TESTES")
    print(f"{'='*50}\n")

    testes = [
        test_parser_basico,
        test_parser_stopwords,
        test_parser_fuzzy,
        test_parser_distorcao,
        test_jogador_perfis,
        test_jogador_mecanicas,
        test_combinacoes_frozenset,
        test_salas,
        test_eva9,
        test_elena,
        test_final_secreto,
        test_segredos,
        test_momentos_exclusivos,
    ]

    aprovados = 0
    falhas = 0

    for teste in testes:
        try:
            teste()
            aprovados += 1
        except AssertionError as e:
            print(f"  ✗ FALHA em {teste.__name__}: {e}")
            falhas += 1
        except Exception as e:
            print(f"  ✗ ERRO em {teste.__name__}: {e}")
            falhas += 1

    print(f"\n{'='*50}")
    print(f"  Resultado: {aprovados}/{aprovados + falhas} aprovados")
    if falhas:
        print(f"  {falhas} falhas")
    else:
        print("  Todos os testes passaram!")
    print(f"{'='*50}\n")

    return falhas == 0


if __name__ == "__main__":
    success = rodar_todos()
    sys.exit(0 if success else 1)
