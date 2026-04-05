#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Save/Load com validação de schema e meta-progressão.
Persiste ações entre runs para criar narrativa emergente.
"""

import json
import os
import logging
from protocolo_sombra_v3.ui.terminal import C
from protocolo_sombra_v3.entities.jogador import Perfil

logger = logging.getLogger("protocolo_sombra.save")

SAVE_FILE = "save_protocolo_sombra.json"
META_FILE = "meta_protocolo_sombra.json"
SAVE_VERSION = "3.0"

# Schema de validação
CAMPOS_OBRIGATORIOS = {
    "versao": str,
    "nome": str,
    "perfil": str,
    "sanidade": int,
    "confianca_eva": int,
    "integridade_dados": int,
    "exposicao_entidade": int,
    "hacking": int,
    "inventario": list,
    "flags": dict,
    "sala_atual": str,
    "turnos": int,
}

RANGES_VALIDOS = {
    "sanidade": (0, 100),
    "confianca_eva": (0, 100),
    "integridade_dados": (0, 100),
    "exposicao_entidade": (0, 100),
    "hacking": (0, 100),
    "turnos": (0, 10000),
}


def validar_save(dados):
    """Valida dados de save contra o schema."""
    erros = []

    # Versão
    if dados.get("versao") != SAVE_VERSION:
        erros.append(f"Versão incompatível: {dados.get('versao')} (esperado: {SAVE_VERSION})")

    # Campos obrigatórios
    for campo, tipo in CAMPOS_OBRIGATORIOS.items():
        if campo not in dados:
            erros.append(f"Campo ausente: {campo}")
        elif not isinstance(dados[campo], tipo):
            erros.append(f"Tipo inválido para {campo}: {type(dados[campo]).__name__} (esperado: {tipo.__name__})")

    # Ranges
    for campo, (minimo, maximo) in RANGES_VALIDOS.items():
        if campo in dados and isinstance(dados[campo], (int, float)):
            if not (minimo <= dados[campo] <= maximo):
                erros.append(f"Valor fora do range para {campo}: {dados[campo]} ({minimo}-{maximo})")

    # Perfil válido
    if "perfil" in dados:
        try:
            Perfil(dados["perfil"])
        except ValueError:
            erros.append(f"Perfil inválido: {dados['perfil']}")

    return erros


def salvar_jogo(jogador, salas, eva9, elena, silencioso=False):
    """Salva o estado completo do jogo."""
    try:
        dados = {
            "versao": SAVE_VERSION,
            "nome": jogador.nome,
            "perfil": jogador.perfil.value if jogador.perfil else "analista",
            "sanidade": jogador.sanidade,
            "confianca_eva": jogador.confianca_eva,
            "integridade_dados": jogador.integridade_dados,
            "exposicao_entidade": jogador.exposicao_entidade,
            "hacking": jogador.hacking,
            "inventario": jogador.inventario,
            "flags": jogador.flags,
            "sala_atual": jogador.sala_atual,
            "turnos": jogador.turnos,
            "mensagens_lidas": jogador.mensagens_lidas,
            "logs_encontrados": jogador.logs_encontrados,
            "eventos_ocorridos": jogador.eventos_ocorridos,
            "combinacoes_feitas": jogador.combinacoes_feitas,
            "conquistas": jogador.conquistas,
            "notas_pessoais": getattr(jogador, 'notas_pessoais', []),
            "run_numero": jogador.run_numero,
            "encontros_elena": jogador.encontros_elena,
            # Estado das salas
            "salas_visitadas": {k: v.visitada for k, v in salas.items()},
            "salas_trancadas": {k: v.trancada for k, v in salas.items()},
            "salas_escuras": {k: v.escura for k, v in salas.items()},
            "salas_itens": {k: v.itens for k, v in salas.items()},
            "salas_estado": {k: v.estado for k, v in salas.items()},
            # Estado da EVA-9
            "eva9": eva9.to_dict(),
            # Estado de Elena
            "elena": elena.to_dict(),
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        if not silencioso:
            print(f"{C.VERDE}  Jogo salvo com sucesso.{C.RESET}")
        logger.info(f"Jogo salvo no turno {jogador.turnos}")
        return True

    except Exception as e:
        if not silencioso:
            print(f"{C.VERM_CLARO}  Erro ao salvar: {e}{C.RESET}")
        logger.error(f"Erro ao salvar: {e}")
        return False


def carregar_jogo(jogador, salas, eva9, elena):
    """Carrega estado do jogo com validação."""
    try:
        if not os.path.exists(SAVE_FILE):
            print(f"{C.AMARELO}  Nenhum save encontrado.{C.RESET}")
            return False

        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Validar
        erros = validar_save(dados)
        if erros:
            print(f"{C.VERM_CLARO}  Save com problemas:{C.RESET}")
            for e in erros[:3]:  # Mostrar até 3 erros
                print(f"{C.VERM_CLARO}    • {e}{C.RESET}")

            # Tentar carregar mesmo com erros não-críticos
            if any("Versão incompatível" in e for e in erros):
                print(f"{C.AMARELO}  Save incompatível com versão atual.{C.RESET}")
                return False

        # Restaurar jogador
        jogador.nome = dados["nome"]
        jogador.perfil = Perfil(dados["perfil"])
        jogador.sanidade = dados["sanidade"]
        jogador.confianca_eva = dados["confianca_eva"]
        jogador.integridade_dados = dados["integridade_dados"]
        jogador.exposicao_entidade = dados["exposicao_entidade"]
        jogador.hacking = dados["hacking"]
        jogador.inventario = dados["inventario"]
        jogador.flags = dados["flags"]
        jogador.sala_atual = dados["sala_atual"]
        jogador.turnos = dados["turnos"]
        jogador.mensagens_lidas = dados.get("mensagens_lidas", [])
        jogador.logs_encontrados = dados.get("logs_encontrados", [])
        jogador.eventos_ocorridos = dados.get("eventos_ocorridos", [])
        jogador.combinacoes_feitas = dados.get("combinacoes_feitas", [])
        jogador.conquistas = dados.get("conquistas", [])
        jogador.notas_pessoais = dados.get("notas_pessoais", [])
        jogador.run_numero = dados.get("run_numero", 1)
        jogador.encontros_elena = dados.get("encontros_elena", 0)

        # Restaurar salas
        for sala_id, visitada in dados.get("salas_visitadas", {}).items():
            if sala_id in salas:
                salas[sala_id].visitada = visitada
        for sala_id, trancada in dados.get("salas_trancadas", {}).items():
            if sala_id in salas:
                salas[sala_id].trancada = trancada
        for sala_id, escura in dados.get("salas_escuras", {}).items():
            if sala_id in salas:
                salas[sala_id].escura = escura
        for sala_id, itens in dados.get("salas_itens", {}).items():
            if sala_id in salas:
                salas[sala_id].itens = itens
        for sala_id, estado in dados.get("salas_estado", {}).items():
            if sala_id in salas:
                salas[sala_id].estado = estado

        # Restaurar EVA-9
        if "eva9" in dados:
            eva9.from_dict(dados["eva9"])

        # Restaurar Elena
        if "elena" in dados:
            elena.from_dict(dados["elena"])

        print(f"{C.VERDE}  Jogo carregado. Turno {jogador.turnos}. Sala: {salas[jogador.sala_atual].nome}{C.RESET}")
        logger.info(f"Jogo carregado do turno {jogador.turnos}")
        return True

    except json.JSONDecodeError:
        print(f"{C.VERM_CLARO}  Arquivo de save corrompido.{C.RESET}")
        return False
    except Exception as e:
        print(f"{C.VERM_CLARO}  Erro ao carregar: {e}{C.RESET}")
        logger.error(f"Erro ao carregar: {e}")
        return False


# ═══════════════════════════════════════════════════════════
# META-PROGRESSÃO ENTRE RUNS (NOVO)
# ═══════════════════════════════════════════════════════════

def salvar_meta(jogador, final_alcancado):
    """Salva dados que persistem entre runs."""
    try:
        meta = carregar_meta()

        run_data = {
            "run": meta.get("total_runs", 0) + 1,
            "nome": jogador.nome,
            "perfil": jogador.perfil.value if jogador.perfil else "analista",
            "final": final_alcancado,
            "turnos": jogador.turnos,
            "sanidade_final": jogador.sanidade,
            "segredos": list(jogador.flags.keys()),
            "acoes_marcantes": [],
        }

        # Registrar ações marcantes
        if jogador.flags.get("abriu_geladeira"):
            run_data["acoes_marcantes"].append("abriu_geladeira")
        if jogador.flags.get("usou_capacete"):
            run_data["acoes_marcantes"].append("usou_capacete")
        if jogador.flags.get("moveu_corpo"):
            run_data["acoes_marcantes"].append("moveu_corpo")
        if jogador.flags.get("pendrive_conectado"):
            run_data["acoes_marcantes"].append("pendrive_conectado")

        meta["total_runs"] = run_data["run"]
        if "runs" not in meta:
            meta["runs"] = []
        meta["runs"].append(run_data)

        # Guardar finais alcançados
        if "finais_alcancados" not in meta:
            meta["finais_alcancados"] = []
        if final_alcancado and final_alcancado not in meta["finais_alcancados"]:
            meta["finais_alcancados"].append(final_alcancado)

        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        logger.info(f"Meta-progressão salva: run {run_data['run']}")

    except Exception as e:
        logger.error(f"Erro ao salvar meta: {e}")


def carregar_meta():
    """Carrega dados de meta-progressão."""
    try:
        if os.path.exists(META_FILE):
            with open(META_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {"total_runs": 0, "runs": [], "finais_alcancados": []}


def obter_ecos_run_anterior():
    """Retorna vestígios de runs anteriores para inserir na narrativa."""
    meta = carregar_meta()
    ecos = []

    if meta["total_runs"] == 0:
        return ecos

    ultima_run = meta["runs"][-1] if meta["runs"] else None
    if not ultima_run:
        return ecos

    # Bilhete baseado na última run
    if "abriu_geladeira" in ultima_run.get("acoes_marcantes", []):
        ecos.append({
            "sala": "sala_medica",
            "texto": f"Há um bilhete com sua letra na maca: 'NÃO abra a geladeira. Confie em mim. — {ultima_run['nome']}'",
            "flag": "meta_nota_encontrada",
        })

    if "usou_capacete" in ultima_run.get("acoes_marcantes", []):
        ecos.append({
            "sala": "sala_secreta",
            "texto": f"Rabiscado na cadeira: 'O capacete mostra a verdade. Mas a verdade tem um custo. — {ultima_run['nome']}, Iteração #{ultima_run['run']}'",
            "flag": "meta_nota_encontrada",
        })

    if ultima_run.get("final") == "morte":
        ecos.append({
            "sala": "sala_terminal",
            "texto": f"Na tela do terminal, uma mensagem residual: 'EU FALHEI. NÃO REPITA MEUS ERROS. — {ultima_run['nome']}'",
            "flag": "meta_nota_encontrada",
        })

    if ultima_run.get("final") == "fusao":
        ecos.append({
            "sala": "nucleo_servidores",
            "texto": f"O terminal CRT mostra brevemente: 'EU ESTOU AQUI DENTRO AGORA. {ultima_run['nome']} SE FOI. OU SE ENCONTROU. — Iteração #{ultima_run['run']}'",
            "flag": "meta_nota_encontrada",
        })

    return ecos
