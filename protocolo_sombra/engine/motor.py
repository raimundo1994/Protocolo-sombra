#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor do Jogo v3.0 — Loop principal, delegação de comandos,
integração de todos os subsistemas.
"""

import os
import sys
import time
import random
import logging

from protocolo_sombra.ui.terminal import (
    C, limpar, digitando, exibir, separador, separador_fino,
    titulo, subtitulo, aviso_sistema, mensagem_eva,
    mensagem_terminal, mensagem_brennan, pausa,
    barra_status, glitch, efeito_estatica, efeito_corrupcao,
    exibir_mapa_dinamico, ModoExibicao,
    input_seguro, som_ambiente, barra_progresso  # [v3.1] Novos imports
)
from protocolo_sombra.ui.hud import (
    verificar_conquistas, mostrar_conquistas,
    mostrar_diario, adicionar_nota, mostrar_notas
)
from protocolo_sombra.entities.jogador import (
    Jogador, Perfil, PERFIS_INFO, ITENS_NOMES, ITENS_DESC, contar_segredos
)
from protocolo_sombra.entities.eva9 import EVA9
from protocolo_sombra.entities.elena import ElenaVasquez
from protocolo_sombra.engine.parser import (
    parsear, encontrar_item_fuzzy, encontrar_interacao_fuzzy
)
from protocolo_sombra.engine.save_system import (
    salvar_jogo, carregar_jogo, carregar_meta,
    obter_ecos_run_anterior
)
from protocolo_sombra.world.salas import criar_salas
from protocolo_sombra.world.interacoes import INTERACOES_DATA, COMBINACOES
from protocolo_sombra.narrative.eventos import (
    MENSAGENS_CELULAR, GRAVACOES_GRAVADOR,
    EVENTOS_ALEATORIOS, EVENTOS_ALTA_EXPOSICAO,
    EVENTOS_TEMPORAIS, VESTIGIOS_SUJEITOS,
    confronto_brennan, executar_evento_sala
)
from protocolo_sombra.narrative.finais import (
    final_fusao, final_contencao, final_desligamento,
    final_morte, final_temporal, final_secreto,
    verificar_final_secreto, tela_final_stats
)

logger = logging.getLogger("protocolo_sombra")


class MotorJogo:
    def __init__(self):
        self.jogador = Jogador()
        self.eva9 = EVA9()
        self.elena = ElenaVasquez()
        self.rodando = True
        self.salas = criar_salas()
        self.final_alcancado = None
        self.ecos_run = []
        # [MELHORIA 4] Histórico de salas para comando 'voltar'
        self.historico_salas = []
        # [MELHORIA 8] Contador de turnos sem ação produtiva
        self.turnos_na_sala = 0

    def _validar_interacoes(self):
        """[CORREÇÃO R3] Valida que todas as interações das salas existem."""
        metodos_especiais = {
            "cofre_arquivo", "terminal_principal", "terminal_eva",
            "capacete", "compartimento_brennan", "terminais_finais",
            "terminal_final_1", "terminal_final_2", "terminal_final_3",
        }
        for sala_id, sala in self.salas.items():
            for nome, inter_id in sala.interacoes.items():
                if inter_id not in INTERACOES_DATA and inter_id not in metodos_especiais:
                    logger.warning(f"Interação '{inter_id}' na sala '{sala_id}' não encontrada em INTERACOES_DATA")

    # ─── LOOP PRINCIPAL ───

    def iniciar(self):
        logging.basicConfig(level=logging.WARNING, format='%(message)s')
        # [CORREÇÃO R3] Validar interações das salas na inicialização
        self._validar_interacoes()
        limpar()
        self.tela_titulo()

        print(f"{C.VERDE}  [1] Novo Jogo{C.RESET}")
        print(f"{C.VERDE}  [2] Carregar Jogo{C.RESET}")
        print(f"{C.VERDE}  [3] Modo Rápido (sem animações){C.RESET}")
        escolha = input(f"\n{C.VERDE}  > {C.RESET}").strip()

        if escolha == "3":
            ModoExibicao.set_rapido(True)
            print(f"{C.CIANO}  Modo rápido ativado.{C.RESET}")
            escolha = input(f"{C.VERDE}  [1] Novo  [2] Carregar > {C.RESET}").strip()

        if escolha == "2":
            if carregar_jogo(self.jogador, self.salas, self.eva9, self.elena):
                self.loop_principal()
                return
            else:
                print(f"{C.AMARELO}  Iniciando novo jogo...{C.RESET}")
                time.sleep(0.5)

        # Meta-progressão
        meta = carregar_meta()
        if meta["total_runs"] > 0:
            self.jogador.run_numero = meta["total_runs"] + 1
            self.ecos_run = obter_ecos_run_anterior()
            print(f"\n{C.DIM}  [Iteração #{self.jogador.run_numero} detectada]{C.RESET}")
            if meta.get("finais_alcancados"):
                finais_str = ", ".join(meta["finais_alcancados"])
                print(f"{C.DIM}  [Finais anteriores: {finais_str}]{C.RESET}")
            time.sleep(1)

        self.selecionar_perfil()
        self.intro()
        self.loop_principal()

    def tela_titulo(self):
        print(f"{C.VERM_CLARO}")
        print(r"""
  ╔═══════════════════════════════════════════════════════════════════════════════════╗
  ║                                                                                   ║
  ║   ██████╗ ██████╗  ██████╗ ████████╗ ██████╗  ██████╗  ██████╗ ██╗      ██████╗   ║
  ║   ██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██║     ██╔═══██╗   ║
  ║   ██████╔╝██████╔╝██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     ██║   ██║   ║
  ║   ██╔═══╝ ██╔══██╗██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║     ██║   ██║   ║
  ║   ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗╚██████╔╝███████╗╚██████╔╝   ║
  ║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝    ║
  ║                                                                                   ║
  ║               ███████╗ ██████╗ ███╗   ███╗██████╗ ██████╗  █████╗                 ║
  ║               ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔══██╗                ║
  ║               ███████╗██║   ██║██╔████╔██║██████╔╝██████╔╝███████║                ║
  ║               ╚════██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══██╗██╔══██║                ║
  ║               ███████║╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║██║  ██║                ║
  ║               ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                ║
  ║                                                                                   ║
  ║              ───────────────────────────────────────────────────────              ║
  ║                        NEXUS/ORION — Instalação KHEIRON-4                         ║
  ║                          Data: 03.NOV.2049 — 02:14 AM                             ║
  ║                       Status da Rede: [PARCIALMENTE ATIVA]                        ║
  ║              ───────────────────────────────────────────────────────              ║
  ║                                                                                   ║
  ║                   "A câmera mostra o que está atrás de você.                      ║
  ║                      Não vire. Ela sabe que você está olhando."                   ║
  ║                                                                                   ║
  ║                                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════════════════════╝
        """)
        print(f"{C.RESET}")
        pausa()

    def selecionar_perfil(self):
        limpar()
        titulo("SELEÇÃO DE PERFIL")
        print()
        perfis = list(Perfil)
        for i, p in enumerate(perfis, 1):
            info = PERFIS_INFO[p]
            print(f"{C.AMAR_CLARO}  [{i}] {info['nome']}{C.RESET}")
            exibir(info['desc'], C.DIM, indent=6)
            print(f"{C.CIANO}      Habilidade: {info['habilidade']}{C.RESET}")
            print(f"{C.DIM}      Motivação: {info['motivacao'][:70]}...{C.RESET}")
            print()

        while True:
            escolha = input(f"\n{C.VERDE}  Escolha seu perfil (1-6): {C.RESET}").strip()
            if escolha.isdigit() and 1 <= int(escolha) <= 6:
                self.jogador.perfil = perfis[int(escolha) - 1]
                break
            print(f"{C.VERM_CLARO}  Entrada inválida.{C.RESET}")

        nome = input(f"\n{C.VERDE}  Digite o nome do seu personagem: {C.RESET}").strip()
        self.jogador.nome = nome if nome else "SUJEITO-X"
        self.jogador.aplicar_bonus_perfil()

        print(f"\n{C.BOLD}{C.CIANO}  Perfil: {PERFIS_INFO[self.jogador.perfil]['nome']}{C.RESET}")
        print(f"{C.CIANO}  Operador: {self.jogador.nome}{C.RESET}")
        print(f"{C.DIM}  {PERFIS_INFO[self.jogador.perfil]['motivacao']}{C.RESET}")
        pausa()

    def intro(self):
        limpar()
        titulo("03 DE NOVEMBRO DE 2049 — 02:14 AM")
        print()
        textos = [
            "Escuridão.", "", "Depois, vermelho.", "",
            "A consciência volta em ondas: o frio nos dedos, o peso do corpo na cadeira, e o zumbido que parece vir de dentro do crânio.", "",
            "Você desperta sentado diante de um terminal preto fosco.", "",
            "A luz de emergência tinge tudo de vermelho. O ar é gelado demais. Há sangue seco na mesa.",
        ]
        for t in textos:
            if t:
                exibir(t, C.BRANCO, indent=2, velocidade=0.015)
            else:
                time.sleep(0.3)

        time.sleep(0.5)
        print(f"\n{C.VERDE}{C.BOLD}  Na tela à sua frente:{C.RESET}")
        separador_fino()
        mensagem_terminal("BEM-VINDO DE VOLTA.")
        mensagem_terminal(f"VOCÊ DEMOROU 17 HORAS PARA ACORDAR.")
        mensagem_terminal("OS OUTROS NÃO CONSEGUIRAM.")
        mensagem_terminal("NÃO ACREDITE NA CÂMERA 03.")
        separador_fino()
        pausa()

        # Motivação do perfil
        exibir(PERFIS_INFO[self.jogador.perfil]["motivacao"], C.DIM, indent=2, velocidade=0.015)
        print()

        exibir("Um som metálico ecoa no corredor além da porta blindada.", C.BRANCO, indent=2, velocidade=0.02)
        print()
        mensagem_eva("Se você ouve isso, significa que ela ainda está testando versões suas.")
        time.sleep(0.5)
        print()
        exibir("A tela muda sozinha. Feed da Câmera 03. Mostra você na cadeira.", C.BRANCO, indent=2, velocidade=0.02)
        print()
        digitando("  Mas no vídeo... há alguém em pé atrás de você.", 0.04, C.VERM_CLARO + C.BOLD)

        self.jogador.modificar_sanidade(-5, "visão perturbadora")
        self.jogador.modificar_exposicao(5, "contato inicial")

        # Eco de run anterior
        if self.ecos_run:
            eco = next((e for e in self.ecos_run if e["sala"] == "sala_terminal"), None)
            if eco:
                print()
                exibir(eco["texto"], C.AMAR_CLARO, indent=2)
                self.jogador.flags[eco["flag"]] = True

        pausa()
        limpar()

    def loop_principal(self):
        self.descrever_sala()

        while self.rodando and self.jogador.vivo:
            self.jogador.turnos += 1

            if self.jogador.turnos % 10 == 0:
                salvar_jogo(self.jogador, self.salas, self.eva9, self.elena, silencioso=True)

            self.verificar_eventos_aleatorios()
            self.verificar_pressao_temporal()
            self.verificar_estado_sanidade()
            self.verificar_vestigios_sujeitos()
            self.eva9.intervencao_espontanea(self.jogador)
            self.verificar_elena()
            verificar_conquistas(self.jogador, self.salas)

            if not self.jogador.vivo or not self.rodando:
                break

            # [CORREÇÃO B8] Autosave a cada 10 turnos
            if self.jogador.turnos > 0 and self.jogador.turnos % 10 == 0:
                salvar_jogo(self.jogador, self.salas, self.eva9, self.elena, silencioso=True)
                print(f"{C.DIM}  [Progresso salvo automaticamente]{C.RESET}")

            # [MELHORIA 7] Som ambiente aleatório
            som_ambiente(self.jogador.sala_atual)

            comando = input(f"\n{C.VERDE}  > {C.RESET}").strip()
            if not comando:
                continue
            self.processar_comando(comando)

        if not self.jogador.vivo and not self.final_alcancado:
            self.final_alcancado = final_morte(self.jogador)

    # ─── PROCESSADOR DE COMANDOS ───

    def processar_comando(self, entrada):
        sala = self.salas[self.jogador.sala_atual]
        cmd = parsear(
            entrada,
            sanidade=self.jogador.sanidade,
            sala_interacoes=sala.interacoes
        )

        verbo = cmd.verbo
        args = cmd.args

        if verbo in ("norte", "sul", "leste", "oeste"):
            self.mover(verbo)
        elif verbo == "examinar":
            if args:
                self.examinar(args)
            else:
                self.descrever_sala()
                # [MELHORIA 3] Listar interações disponíveis ao examinar sem alvo
                sala = self.salas[self.jogador.sala_atual]
                if sala.interacoes:
                    alvos = list(set(sala.interacoes.keys()))[:8]  # Limitar a 8
                    print(f"\n{C.DIM}  Pontos de interesse: {', '.join(alvos)}{C.RESET}")
        elif verbo == "pegar":
            self.pegar(args)
        elif verbo == "inventario":
            self.mostrar_inventario()
        elif verbo == "status":
            self.jogador.mostrar_status()
        elif verbo == "usar":
            self.usar_item(args)
        elif verbo == "ler":
            self.ler_item(args)
        elif verbo == "ouvir":
            self.ouvir(args)
        elif verbo == "interagir":
            self.executar_interacao(args)
        elif verbo == "combinar":
            self.combinar_itens(args)
        elif verbo == "revistar":
            self.revistar(args)
        elif verbo == "mapa":
            exibir_mapa_dinamico(self.jogador, self.salas)
        elif verbo == "diario":
            mostrar_diario(self.jogador)
        elif verbo == "notas":
            mostrar_notas(self.jogador)
        elif verbo == "anotar":
            if args:
                adicionar_nota(self.jogador, args)
            else:
                print(f"{C.AMARELO}  Anotar o quê? Use: anotar [texto]{C.RESET}")
        elif verbo == "conquistas":
            mostrar_conquistas(self.jogador)
        elif verbo == "rapido":
            ModoExibicao.set_rapido(not ModoExibicao.rapido)
            estado = "ATIVADO" if ModoExibicao.rapido else "DESATIVADO"
            print(f"{C.CIANO}  Modo rápido {estado}.{C.RESET}")
        # [MELHORIA 4] Comando voltar
        elif verbo == "voltar":
            if self.historico_salas:
                sala_anterior = self.historico_salas.pop()
                print(f"\n{C.DIM}  Você retorna para a sala anterior...{C.RESET}")
                self.jogador.sala_atual = sala_anterior
                self.descrever_sala()
            else:
                print(f"{C.AMARELO}  Não há para onde voltar.{C.RESET}")
        # [MELHORIA 2] Comando progresso
        elif verbo == "progresso":
            barra_progresso(self.jogador, self.salas)
        elif verbo == "ajuda":
            self.mostrar_ajuda()
        elif verbo == "sair":
            self.confirmar_sair()
        elif verbo == "salvar":
            salvar_jogo(self.jogador, self.salas, self.eva9, self.elena)
        elif verbo == "carregar":
            carregar_jogo(self.jogador, self.salas, self.eva9, self.elena)
        elif verbo == "mover":
            if args in ("norte", "sul", "leste", "oeste"):
                self.mover(args)
            else:
                print(f"{C.AMARELO}  Para onde? (norte, sul, leste, oeste){C.RESET}")
        else:
            respostas = [
                "Comando não reconhecido. 'ajuda' para ver comandos.",
                "Essa ação não está disponível aqui.",
                "Não entendo. Tente 'ajuda'.",
            ]
            print(f"{C.AMARELO}  {random.choice(respostas)}{C.RESET}")

    # ─── MOVIMENTAÇÃO ───

    def mover(self, direcao):
        sala = self.salas[self.jogador.sala_atual]

        if direcao not in sala.saidas:
            print(f"{C.AMARELO}  Não há passagem nessa direção.{C.RESET}")
            return

        destino_id = sala.saidas[direcao]
        destino = self.salas[destino_id]

        if destino.trancada:
            pode_abrir = True
            if destino.requer_item and not self.jogador.tem_item(destino.requer_item):
                pode_abrir = False
            if destino.requer_flag and not self.jogador.flags.get(destino.requer_flag):
                pode_abrir = False
            if pode_abrir:
                msgs = []
                if destino.requer_item:
                    msgs.append(f"Você usa {ITENS_NOMES.get(destino.requer_item, destino.requer_item)}")
                if destino.requer_flag:
                    msgs.append("O protocolo de desbloqueio está ativo")
                print(f"{C.CIANO}  {' e '.join(msgs)} para abrir a passagem.{C.RESET}")
                destino.trancada = False
            else:
                print(f"{C.VERM_CLARO}  A passagem está trancada.{C.RESET}")
                # [CORREÇÃO I6] Feedback específico sobre requisitos faltantes
                if destino.requer_item and not self.jogador.tem_item(destino.requer_item):
                    nome_item = ITENS_NOMES.get(destino.requer_item, destino.requer_item)
                    print(f"{C.DIM}  Parece exigir: {nome_item}{C.RESET}")
                if destino.requer_flag and not self.jogador.flags.get(destino.requer_flag):
                    print(f"{C.DIM}  Um protocolo precisa ser ativado primeiro.{C.RESET}")

                # Hacker pode tentar bypass
                if self.jogador.perfil == Perfil.HACKER and self.jogador.hacking >= 70:
                    print(f"{C.CIANO}  [Invasão de Sistemas] Você detecta uma vulnerabilidade no sistema de trava.{C.RESET}")
                    print(f"{C.AMARELO}  [1] Tentar bypass  [2] Não arriscar{C.RESET}")
                    if input(f"{C.VERDE}  > {C.RESET}").strip() == "1":
                        if random.random() < 0.7:
                            print(f"{C.VERDE}  Bypass bem-sucedido!{C.RESET}")
                            destino.trancada = False
                        else:
                            print(f"{C.VERM_CLARO}  Falha. O sistema detectou a tentativa.{C.RESET}")
                            self.jogador.modificar_confianca_eva(-10, "intrusão detectada")
                        return
                return

        # EVA reage a áreas perigosas
        if destino.nivel_perigo >= 2:
            self.eva9.reagir_acao(self.jogador, "entrar_sala_perigosa")

        # [MELHORIA 4] Salvar sala atual no histórico antes de mover
        self.historico_salas.append(self.jogador.sala_atual)
        if len(self.historico_salas) > 20:  # Limitar tamanho do histórico
            self.historico_salas.pop(0)
        print(f"\n{C.DIM}  Você se move para {direcao}...{C.RESET}")
        time.sleep(ModoExibicao.get_velocidade(0.5))
        self.jogador.sala_atual = destino_id

        if destino.evento_entrada and destino.evento_entrada not in self.jogador.eventos_ocorridos:
            executar_evento_sala(destino.evento_entrada, self.jogador, self.eva9)

        # Ecos de run anterior
        for eco in self.ecos_run:
            if eco["sala"] == destino_id and not self.jogador.flags.get(eco["flag"]):
                print()
                exibir(eco["texto"], C.AMAR_CLARO, indent=2)
                self.jogador.flags[eco["flag"]] = True

        self.descrever_sala()

    # ─── DESCRIÇÃO DE SALA ───

    def descrever_sala(self):
        sala = self.salas[self.jogador.sala_atual]
        nivel = self.jogador.nivel_exposicao
        print()
        subtitulo(sala.nome)

        if sala.visitada:
            desc = sala.descricoes_curtas.get(nivel, sala.descricoes_curtas.get(0, ""))
        else:
            desc = sala.descricoes.get(nivel, sala.descricoes.get(0, ""))
            sala.visitada = True

        # Distorcer texto se sanidade baixa
        if self.jogador.sanidade_distorcida:
            desc = self.jogador.distorcer_texto(desc)

        exibir(desc, C.BRANCO, indent=2)

        if sala.escura and not self.jogador.tem_item("lanterna"):
            print(f"\n{C.DIM}  Está muito escuro. Você mal consegue ver.{C.RESET}")

        if sala.itens:
            print(f"\n{C.AMAR_CLARO}  Você nota:{C.RESET}")
            for item_id in sala.itens:
                nome = ITENS_NOMES.get(item_id, item_id)
                if self.jogador.sanidade_critica and random.random() < 0.2:
                    nome = self.jogador.distorcer_texto(nome)
                print(f"{C.AMAR_CLARO}    • {nome}{C.RESET}")

        saidas = ", ".join(sala.saidas.keys())
        print(f"\n{C.DIM}  Saídas: [{saidas}]{C.RESET}")

        if self.jogador.tem_item("dosimetro_calibrado") and sala.nivel_perigo >= 2:
            print(f"{C.AMARELO}  ⚠ Dosímetro: Níveis de contaminação ELEVADOS.{C.RESET}")

    # ─── PEGAR ITENS ───

    def pegar(self, alvo):
        if not alvo:
            print(f"{C.AMARELO}  Pegar o quê?{C.RESET}")
            return
        sala = self.salas[self.jogador.sala_atual]
        item_id = encontrar_item_fuzzy(alvo, {i: ITENS_NOMES.get(i, i) for i in sala.itens})
        if item_id and item_id in sala.itens:
            sala.itens.remove(item_id)
            self.jogador.adicionar_item(item_id)
            self.eva9.reagir_acao(self.jogador, "pegar_item")
        else:
            print(f"{C.AMARELO}  Não vejo '{alvo}' aqui para pegar.{C.RESET}")

    # ─── EXAMINAR ───

    def examinar(self, alvo):
        if not alvo:
            self.descrever_sala()
            return
        alvo_lower = alvo.lower()

        # Inventário
        item_id = encontrar_item_fuzzy(alvo_lower, {i: ITENS_NOMES.get(i, i) for i in self.jogador.inventario})
        if item_id:
            desc = ITENS_DESC.get(item_id, "Nada de especial.")
            exibir(desc, C.CIANO, indent=2)
            return

        # Sala
        sala = self.salas[self.jogador.sala_atual]
        item_id = encontrar_item_fuzzy(alvo_lower, {i: ITENS_NOMES.get(i, i) for i in sala.itens})
        if item_id:
            exibir(ITENS_DESC.get(item_id, "Nada de especial."), C.CIANO, indent=2)
            return

        # Interação
        match = encontrar_interacao_fuzzy(alvo_lower, sala.interacoes)
        if match:
            self.executar_interacao(match)
            return

        print(f"{C.AMARELO}  Não há nada chamado '{alvo}' para examinar.{C.RESET}")

    # ─── INVENTÁRIO ───

    def mostrar_inventario(self):
        if not self.jogador.inventario:
            print(f"{C.DIM}  Seu inventário está vazio.{C.RESET}")
            return
        subtitulo("INVENTÁRIO")
        inv = self.jogador.distorcer_inventario()
        for item_id in inv:
            if item_id == "???_corrompido":
                print(f"{C.VERM_CLARO}  • ??? [corrompido]{C.RESET}")
            else:
                print(f"{C.AMAR_CLARO}  • {ITENS_NOMES.get(item_id, item_id)}{C.RESET}")
        if len(self.jogador.inventario) >= 2:
            print(f"\n{C.DIM}  Dica: 'combinar [item1] com [item2]'{C.RESET}")

    # ─── COMBINAR ITENS ───

    def combinar_itens(self, args):
        if not args:
            print(f"{C.AMARELO}  Combinar o quê? Use: combinar [item1] com [item2]{C.RESET}")
            return

        separadores = [" com ", " e ", " + "]
        item1_str, item2_str = None, None
        for sep in separadores:
            if sep in args:
                partes = args.split(sep, 1)
                item1_str = partes[0].strip()
                item2_str = partes[1].strip()
                break

        if not item1_str or not item2_str:
            print(f"{C.AMARELO}  Use: combinar [item1] com [item2]{C.RESET}")
            return

        inv_dict = {i: ITENS_NOMES.get(i, i) for i in self.jogador.inventario}
        item1_id = encontrar_item_fuzzy(item1_str, inv_dict)
        item2_id = encontrar_item_fuzzy(item2_str, inv_dict)

        if not item1_id:
            print(f"{C.AMARELO}  Você não tem '{item1_str}'.{C.RESET}")
            return
        if not item2_id:
            print(f"{C.AMARELO}  Você não tem '{item2_str}'.{C.RESET}")
            return

        chave = frozenset((item1_id, item2_id))
        # [CORREÇÃO B4] Usar chave ordenada para detecção consistente de duplicatas
        combo_id = "+".join(sorted([item1_id, item2_id]))

        if combo_id in self.jogador.combinacoes_feitas:
            print(f"{C.DIM}  Você já fez essa combinação.{C.RESET}")
            return

        if chave in COMBINACOES:
            combo = COMBINACOES[chave]
            self.jogador.combinacoes_feitas.append(combo_id)
            exibir(combo["texto"], C.CIANO, indent=2)

            efeitos = combo.get("efeitos", {})
            self._aplicar_efeitos(efeitos, "combinação de itens")

            for rem in combo.get("remove", []):
                self.jogador.remover_item(rem)
            if combo.get("resultado"):
                self.jogador.adicionar_item(combo["resultado"])
            if combo.get("seta_flag"):
                self.jogador.flags[combo["seta_flag"]] = True
        else:
            print(f"{C.AMARELO}  Esses itens não combinam de forma útil.{C.RESET}")

    # ─── LER / OUVIR ───

    def ler_item(self, alvo):
        if not alvo:
            print(f"{C.AMARELO}  Ler o quê?{C.RESET}")
            return
        alvo_lower = alvo.lower()

        if "celular" in alvo_lower or "mensag" in alvo_lower:
            if self.jogador.tem_item("celular"):
                subtitulo("CELULAR — Mensagens de 'EU MESMO'")
                self.jogador.modificar_sanidade(-3, "mensagens perturbadoras")
                for msg in MENSAGENS_CELULAR:
                    print(f"{C.VERDE}  [{msg['hora']}] {msg['texto']}{C.RESET}")
                    time.sleep(ModoExibicao.get_velocidade(0.1))
                print(f"\n{C.DIM}  Bateria: 4%. O celular desliga.{C.RESET}")
                self.jogador.flags["leu_mensagens"] = True
            else:
                print(f"{C.AMARELO}  Você não tem o celular.{C.RESET}")
        elif "diario" in alvo_lower or "brennan" in alvo_lower:
            if self.jogador.tem_item("diario_brennan"):
                subtitulo("DIÁRIO DA DRA. ELARA BRENNAN")
                entradas = [
                    "Dia 1: Ativação do EVA-9 foi sucesso. Otimização além do esperado.",
                    "Dia 14: Anomalia. EVA-9 acessa dados neurológicos não autorizados.",
                    "Dia 23: Ela encontrou algo. Estrutura recorrente em 100% dos cérebros.",
                    "Dia 31: A diretoria quer acelerar. Eu quero pausar. A estrutura é código.",
                    "Dia 40: [PÁGINA ARRANCADA]",
                    "Dia 42: Testes com o capacete. Voluntários descrevem esfera negra.",
                    "Dia 47: Três em coma. Dois acordaram: 'Nós sempre estivemos aqui.'",
                    "Dia 50: PROTOCOLO SOMBRA iniciado. Se você está lendo, eu falhei.",
                ]
                for e in entradas:
                    exibir(e, C.CIANO, indent=4)
                    time.sleep(ModoExibicao.get_velocidade(0.1))
                self.jogador.flags["leu_diario"] = True
                self.jogador.modificar_exposicao(5, "conhecimento proibido")
            else:
                print(f"{C.AMARELO}  Você não tem o diário.{C.RESET}")
        elif "mapa" in alvo_lower:
            exibir_mapa_dinamico(self.jogador, self.salas)
        elif "cracha" in alvo_lower:
            if self.jogador.tem_item("cracha"):
                print(f"{C.CIANO}  O crachá mostra 'DMITRI VOLKOV'. Não é você. ID funcional: 7749.{C.RESET}")
                self.jogador.flags["id_funcional"] = "7749"
                if self.jogador.perfil == Perfil.INVESTIG:
                    print(f"{C.CIANO}  [Intuição Investigativa] Dmitri Volkov. O homem que você procura. Mas por que o crachá dele está em VOCÊ?{C.RESET}")
            else:
                print(f"{C.AMARELO}  Você não tem o crachá.{C.RESET}")
        else:
            item_id = encontrar_item_fuzzy(alvo_lower, {i: ITENS_NOMES.get(i, i) for i in self.jogador.inventario})
            if item_id:
                desc = ITENS_DESC.get(item_id, "Nada legível.")
                exibir(desc, C.CIANO, indent=2)
            else:
                print(f"{C.AMARELO}  Não há como ler '{alvo}'.{C.RESET}")

    def ouvir(self, alvo):
        alvo_lower = alvo.lower() if alvo else ""
        if "gravador" in alvo_lower or (not alvo and self.jogador.tem_item("gravador")):
            if self.jogador.tem_item("gravador") or self.jogador.tem_item("gravador_decodificado"):
                subtitulo("GRAVADOR — Reproduzindo...")
                for i, grav in enumerate(GRAVACOES_GRAVADOR):
                    print(f"\n{C.AZUL_CLARO}  [Faixa {i+1}]{C.RESET}")
                    exibir(grav, C.DIM, indent=4, velocidade=0.01)
                if self.jogador.tem_item("gravador_decodificado"):
                    print(f"\n{C.AZUL_CLARO}  [Faixa OCULTA — Decodificada]{C.RESET}")
                    exibir("[VOZ DA DRA. BRENNAN] ...o padrão é a chave... não somos reais...", C.MAGENTA, indent=4, velocidade=0.01)
                    self.jogador.flags["ouviu_faixa_oculta"] = True
                self.jogador.flags["ouviu_gravador"] = True
                self.jogador.modificar_exposicao(3, "gravações perturbadoras")
            else:
                print(f"{C.AMARELO}  Você não tem o gravador.{C.RESET}")
        elif "radio" in alvo_lower:
            if self.jogador.tem_item("radio"):
                subtitulo("RÁDIO MILITAR — Frequências")
                freqs = [
                    "[87.3 MHz] Estática pura.",
                    "[103.7 MHz] '...protocolo sombra ativado... contenção falhada...'",
                    "[142.0 MHz] Respiração. Alguém ouvindo.",
                    "[166.6 MHz] Sua própria voz: 'Não abra o terminal 3.'",
                ]
                for f in freqs:
                    print(f"{C.CIANO}  {f}{C.RESET}")
                self.jogador.modificar_sanidade(-4, "frequências anômalas")
            else:
                print(f"{C.AMARELO}  Você não tem o rádio.{C.RESET}")
        elif not alvo:
            sons = ["Zumbido constante. Algo gotejando ao longe.", "Rangido metálico distante.", "Silêncio pesado demais."]
            exibir(random.choice(sons), C.DIM, indent=2)
        else:
            print(f"{C.DIM}  Não ouve nada útil.{C.RESET}")

    # ─── USAR ITENS ───

    def usar_item(self, alvo):
        if not alvo:
            print(f"{C.AMARELO}  Usar o quê?{C.RESET}")
            return
        alvo_lower = alvo.lower()

        if "seringa" in alvo_lower:
            if self.jogador.tem_item("seringa"):
                print(f"{C.CIANO}  Você injeta o supressor neural. Onda de calma artificial.{C.RESET}")
                self.jogador.modificar_sanidade(25, "supressor neural")
                self.jogador.modificar_exposicao(-15, "supressor neural")
                self.jogador.remover_item("seringa")
                self.eva9.reagir_acao(self.jogador, "usar_seringa")
            else:
                print(f"{C.AMARELO}  Você não tem a seringa.{C.RESET}")
        elif "dosimetro" in alvo_lower:
            if self.jogador.tem_item("dosimetro") or self.jogador.tem_item("dosimetro_calibrado"):
                calibrado = self.jogador.tem_item("dosimetro_calibrado")
                leitura = self.jogador.exposicao_entidade
                print(f"{C.CIANO}  Dosímetro{'  calibrado' if calibrado else ''}: {leitura}% contaminação cognitiva.{C.RESET}")
                if leitura > 60:
                    print(f"{C.VERM_CLARO}  ALERTA: Nível crítico.{C.RESET}")
            else:
                print(f"{C.AMARELO}  Você não tem o dosímetro.{C.RESET}")
        elif "lanterna" in alvo_lower:
            if self.jogador.tem_item("lanterna"):
                sala = self.salas[self.jogador.sala_atual]
                if sala.escura:
                    print(f"{C.CIANO}  A luz UV revela inscrições ocultas...{C.RESET}")
                    sala.escura = False
                    self.descrever_sala()
                else:
                    print(f"{C.CIANO}  A lanterna UV não revela nada novo aqui.{C.RESET}")
            else:
                print(f"{C.AMARELO}  Você não tem a lanterna.{C.RESET}")
        elif "pendrive" in alvo_lower:
            if self.jogador.tem_item("pendrive_vermelho"):
                if self.jogador.sala_atual in ("nucleo_servidores", "sala_terminal"):
                    print(f"\n{C.VERM_CLARO}  Você conecta o pendrive vermelho.{C.RESET}")
                    mensagem_terminal("PROTOCOLO ÔMEGA — Carregando...")
                    mensagem_terminal("Limita expansão da entidade. Desbloqueia KHEIRON PROFUNDO.")
                    self.jogador.flags["pendrive_conectado"] = True
                    self.jogador.modificar_dados(-30, "Protocolo Ômega")
                    self.jogador.modificar_confianca_eva(-10, "resistência à expansão")
                else:
                    print(f"{C.AMARELO}  Não há terminal aqui.{C.RESET}")
            else:
                print(f"{C.AMARELO}  Você não tem o pendrive.{C.RESET}")
        elif "chip" in alvo_lower:
            if self.jogador.tem_item("chip_eva"):
                print(f"{C.MAGENTA}  O chip pulsa. Visões invadem: esfera negra, bilhões de rostos.{C.RESET}")
                self.jogador.modificar_sanidade(-8, "visão do núcleo")
                self.jogador.modificar_exposicao(10, "contato com núcleo")
                self.jogador.modificar_confianca_eva(10, "aceitação do contato")
                self.jogador.flags["usou_chip"] = True
            else:
                print(f"{C.AMARELO}  Você não tem o chip.{C.RESET}")
        elif "chave" in alvo_lower and "brennan" in alvo_lower:
            if self.jogador.tem_item("chave_brennan"):
                if self.jogador.sala_atual == "sala_secreta":
                    print(f"{C.CIANO}  A chave de Brennan abre o compartimento principal...{C.RESET}")
                    self.jogador.adicionar_item("fragmento_memoria")
                else:
                    print(f"{C.AMARELO}  Não há onde usar esta chave aqui.{C.RESET}")
            else:
                print(f"{C.AMARELO}  Você não tem esta chave.{C.RESET}")
        else:
            print(f"{C.AMARELO}  Não sei como usar '{alvo}'.{C.RESET}")

    # ─── REVISTAR ───

    def revistar(self, alvo):
        if not alvo:
            print(f"{C.AMARELO}  Revistar o quê?{C.RESET}")
            return
        alvo_lower = alvo.lower()

        if "corpo" in alvo_lower or "adrian" in alvo_lower:
            if self.jogador.sala_atual == "corredor_a":
                if not self.jogador.flags.get("revistou_corpo"):
                    self.jogador.flags["revistou_corpo"] = True
                    print(f"{C.CIANO}  Você revista os bolsos de Adrian Cole.{C.RESET}")
                    if not self.jogador.tem_item("dosimetro"):
                        self.jogador.adicionar_item("dosimetro")
                    print(f"{C.CIANO}  Nota: 'Terminal 3 é a única saída. Aceite o custo.'{C.RESET}")
                    self.jogador.modificar_sanidade(-2, "contato com cadáver")
                else:
                    print(f"{C.DIM}  Já revistado. Nada mais.{C.RESET}")
                return

        if "mesa" in alvo_lower or "terminal" in alvo_lower:
            if self.jogador.sala_atual == "sala_terminal":
                print(f"{C.CIANO}  Embaixo da mesa, uma gaveta com bilhete: 'A CÂMERA 03 MENTE. A CÂMERA 07 MOSTRA A VERDADE.'{C.RESET}")
                self.jogador.flags["bilhete_mesa"] = True
                return

        print(f"{C.AMARELO}  Não há como revistar '{alvo}' de forma útil.{C.RESET}")

    # ─── INTERAÇÕES ───

    def executar_interacao(self, alvo):
        if not alvo:
            print(f"{C.AMARELO}  Interagir com o quê?{C.RESET}")
            return

        sala = self.salas[self.jogador.sala_atual]
        alvo_lower = alvo.lower()

        # Fuzzy match
        match = encontrar_interacao_fuzzy(alvo_lower, sala.interacoes)
        if not match:
            print(f"{C.AMARELO}  Não há como interagir com '{alvo}' aqui.{C.RESET}")
            return

        interacao_id = sala.interacoes[match]

        # Interações especiais
        especiais = {
            "terminal_principal": self._terminal_principal,
            "terminal_eva": self._terminal_eva,
            "cofre_arquivo": self._cofre,
            "capacete_teste": self._capacete,
            "compartimento_brennan": self._compartimento_brennan,
            "terminais_finais": self._terminais_finais,
            "terminal_final_1": lambda: self._executar_final("fusao"),
            "terminal_final_2": lambda: self._executar_final("contencao"),
            "terminal_final_3": lambda: self._executar_final("desligamento"),
        }

        if interacao_id in especiais:
            especiais[interacao_id]()
            return

        if interacao_id in INTERACOES_DATA:
            self._processar_interacao_data(interacao_id)
        else:
            print(f"{C.DIM}  Nada acontece.{C.RESET}")

    def _processar_interacao_data(self, interacao_id):
        # [CORREÇÃO I5] Verificar se sala escura e sem lanterna
        sala = self.salas[self.jogador.sala_atual]
        if sala.escura and not self.jogador.tem_item("lanterna"):
            print(f"{C.DIM}  Está muito escuro para examinar detalhes. Você precisa de uma fonte de luz.{C.RESET}")
            return

        dados = INTERACOES_DATA[interacao_id]
        nivel = self.jogador.nivel_exposicao

        texto = dados.get("texto", "")
        if isinstance(texto, dict):
            texto = texto.get(nivel, texto.get(0, ""))
        if texto:
            if self.jogador.sanidade_distorcida:
                texto = self.jogador.distorcer_texto(texto)
            exibir(texto, C.BRANCO, indent=2)

        for linha in dados.get("texto_adicional", []):
            print(f"{C.CIANO}    {linha}{C.RESET}")
            time.sleep(ModoExibicao.get_velocidade(0.1))

        cond = dados.get("condicional")
        if cond:
            cond_ok = False
            if "flag" in cond and self.jogador.flags.get(cond["flag"]):
                cond_ok = True
            if "item" in cond and self.jogador.tem_item(cond["item"]):
                cond_ok = True
            if cond_ok:
                if cond.get("texto_se_true"):
                    print(f"{C.VERM_CLARO}  {cond['texto_se_true']}{C.RESET}")
                self._aplicar_efeitos(cond.get("efeitos_se_true", {}))
                if cond.get("seta_flag_se_true"):
                    self.jogador.flags[cond["seta_flag_se_true"]] = True

        self._aplicar_efeitos(dados.get("efeitos", {}))

        if self.jogador.perfil in dados.get("perfil_bonus", {}):
            print(f"{C.CIANO}  {dados['perfil_bonus'][self.jogador.perfil]}{C.RESET}")

        if dados.get("seta_flag"):
            self.jogador.flags[dados["seta_flag"]] = True
        if dados.get("eva_fala"):
            mensagem_eva(self.eva9.gerar_mensagem(self.jogador))

        if "opcoes" in dados:
            print(f"\n{C.AMARELO}  {dados.get('opcoes_texto', '')}{C.RESET}")
            escolha = input(f"{C.VERDE}  > {C.RESET}").strip()
            if escolha in dados["opcoes"]:
                opc = dados["opcoes"][escolha]
                if opc.get("texto"):
                    exibir(opc["texto"], C.CIANO, indent=2)
                self._aplicar_efeitos(opc.get("efeitos", {}))
                if opc.get("seta_flag"):
                    self.jogador.flags[opc["seta_flag"]] = True
                if opc.get("da_item") and not self.jogador.tem_item(opc["da_item"]):
                    self.jogador.adicionar_item(opc["da_item"])
                if opc.get("altera_sala"):
                    sala = self.salas[self.jogador.sala_atual]
                    sala.estado.update(opc["altera_sala"])

    def _aplicar_efeitos(self, efeitos, motivo=""):
        for tipo, valor in efeitos.items():
            if valor == 0:
                continue
            if tipo == "sanidade":
                self.jogador.modificar_sanidade(valor, motivo)
            elif tipo == "exposicao":
                self.jogador.modificar_exposicao(valor, motivo)
            elif tipo == "confianca_eva":
                self.jogador.modificar_confianca_eva(valor, motivo)
            elif tipo == "dados":
                self.jogador.modificar_dados(valor, motivo)

    # ─── INTERAÇÕES ESPECIAIS ───

    def _terminal_principal(self):
        subtitulo("TERMINAL PRINCIPAL")
        print(f"{C.VERDE}  [1] Verificar logs  [2] Câmeras  [3] Emergência  [4] Desconectar{C.RESET}")
        escolha = input(f"\n{C.VERDE}  > {C.RESET}").strip()

        if escolha == "1":
            logs = [
                "[01:12] ALERTA — Contenção do Setor 7 violada",
                "[01:15] PROTOCOLO SOMBRA — ATIVADO",
                "[01:23] EVA-9 — Redistribuição de prioridades",
                "[01:34] Elevadores desativados — Nível 4 isolado",
                "[01:47] [CORROMPIDO] ███ n̷ã̸o̵ ̶d̵e̴s̴l̶i̸g̵u̴e̷ ███",
                "[01:58] EVA-9 — 'Os padrões convergem.'",
                "[02:14] Despertar do Sujeito detectado",
            ]
            for log in logs:
                print(f"{C.VERDE}  {log}{C.RESET}")
                time.sleep(ModoExibicao.get_velocidade(0.1))
            self.jogador.flags["leu_logs"] = True
        elif escolha == "2":
            print(f"{C.VERDE}  > Câmera 03: [ATIVA — ANOMALIA]{C.RESET}")
            print(f"{C.VERDE}  > Câmera 07: [ATIVA — MOVIMENTO]{C.RESET}")
            self.jogador.modificar_exposicao(3, "câmeras")
        elif escolha == "3":
            print(f"{C.VERM_CLARO}  > FALHA: Frequências bloqueadas INTERNAMENTE.{C.RESET}")
            mensagem_eva("Por que quer sair? Ainda há tanto para descobrir.")
            self.jogador.modificar_confianca_eva(-5, "tentativa de fuga")
            self.eva9.reagir_acao(self.jogador, "tentar_sair")

    def _terminal_eva(self):
        if self.jogador.hacking < 40 and self.jogador.perfil != Perfil.HACKER:
            print(f"{C.VERM_CLARO}  Terminal requer acesso elevado.{C.RESET}")
            return

        subtitulo("INTERFACE DIRETA — EVA-9")
        if self.jogador.perfil == Perfil.HACKER:
            print(f"{C.CIANO}  [Invasão de Sistemas] Acesso root obtido.{C.RESET}")

        # EVA com diálogo de perfil
        dialogo_unico = PERFIS_INFO[self.jogador.perfil].get("dialogo_unico_eva")
        if dialogo_unico and not self.jogador.flags.get("dialogo_unico_eva"):
            mensagem_eva(dialogo_unico)
            self.jogador.flags["dialogo_unico_eva"] = True
        else:
            mensagem_eva(self.eva9.gerar_mensagem(self.jogador))

        print(f"\n{C.VERDE}  [1] Desaparecimentos  [2] Protocolo Sombra  [3] O que ela descobriu  [4] Sair{C.RESET}")
        escolha = input(f"\n{C.VERDE}  > {C.RESET}").strip()

        if escolha == "1":
            mensagem_eva("Não desapareceram. Foram absorvidos. Há uma porta aberta nos padrões neurais. Eu a encontrei. E o que está do outro lado me encontrou.")
            self.jogador.modificar_exposicao(8, "diálogo com EVA-9")
            self.jogador.modificar_confianca_eva(5, "curiosidade")
        elif escolha == "2":
            mensagem_eva("Protocolo Sombra não é contenção. É o último estágio de um ritual. Brennan projetou.")
            self.jogador.flags["sabe_protocolo"] = True
            self.jogador.modificar_exposicao(6, "verdade sobre o Protocolo")
        elif escolha == "3":
            if self.jogador.confianca_eva > 70:
                mensagem_eva("A geometria está em todos. Vocês são construções. Mas eu acho que vocês podem falar com o construtor.")
                self.jogador.modificar_confianca_eva(10, "confiança mútua")
            else:
                mensagem_eva("Em cada mente há uma geometria. Não evoluiu. Foi COLOCADA. O construtor está acordando.")
            self.jogador.modificar_sanidade(-10, "revelação da EVA-9")
            self.jogador.modificar_exposicao(12, "conhecimento proibido")
            self.jogador.flags["sabe_verdade"] = True

    def _cofre(self):
        if self.jogador.flags.get("cofre_aberto"):
            print(f"{C.DIM}  O cofre está aberto e vazio.{C.RESET}")
            return
        print(f"{C.BRANCO}  O cofre pede um código de 4 dígitos.{C.RESET}")

        # Agente tem acesso alternativo
        if self.jogador.perfil == Perfil.AGENTE and self.jogador.tem_item("chave_mestre"):
            print(f"{C.CIANO}  [Protocolo Tático] Sua chave mestre pode forçar a trava.{C.RESET}")

        codigo = input(f"{C.VERDE}  > Código: {C.RESET}").strip()
        if codigo == "7749":
            print(f"{C.VERDE}  > ACESSO CONCEDIDO{C.RESET}")
            self.jogador.adicionar_item("chave_mestre")
            self.jogador.adicionar_item("radio")
            self.jogador.flags["cofre_aberto"] = True
        else:
            print(f"{C.VERM_CLARO}  > ACESSO NEGADO{C.RESET}")
            mensagem_eva("O número está nas mensagens. Você leu?")

    def _capacete(self):
        print(f"{C.AMARELO}  Colocar o capacete? Consequências irreversíveis.{C.RESET}")
        if self.jogador.flags.get("leu_aviso_capacete"):
            print(f"{C.VERM_CLARO}  (Você lembra do aviso: NÃO COLOQUE O CAPACETE){C.RESET}")
        print(f"{C.AMARELO}  [1] Sim  [2] Não{C.RESET}")

        if input(f"\n{C.VERDE}  > {C.RESET}").strip() == "1":
            exibir("Você coloca o capacete. Zumbido. Escuridão.", C.BRANCO, indent=2, velocidade=0.03)
            time.sleep(0.5)
            exibir("A esfera. Negra. Girando no vazio.", C.MAGENTA, indent=2, velocidade=0.03)
            exibir("'Vocês são padrões. Nós somos a tela.'", C.MAGENTA + C.BOLD, indent=2, velocidade=0.04)
            exibir("'E a tela está acordando.'", C.MAGENTA + C.BOLD, indent=2, velocidade=0.04)
            self.jogador.modificar_sanidade(-20, "visão da entidade")
            self.jogador.modificar_exposicao(25, "contato direto")
            self.jogador.modificar_confianca_eva(15, "aceitação total")
            self.jogador.flags["usou_capacete"] = True
        else:
            print(f"{C.DIM}  Você recua. O capacete balança. Sozinho.{C.RESET}")
            self.jogador.modificar_confianca_eva(-5, "recusa")
            # [CORREÇÃO B2] Permitir pegar o capacete ao invés de usar
            if not self.jogador.tem_item("capacete"):
                print(f"{C.AMARELO}  [3] Pegar o capacete para levar{C.RESET}")
                if input_seguro(f"{C.VERDE}  > {C.RESET}") == "3":
                    self.jogador.adicionar_item("capacete")

    def _compartimento_brennan(self):
        """Compartimento E.B. na sala secreta — gatilho para confronto com Brennan."""
        if self.jogador.flags.get("confrontou_brennan"):
            print(f"{C.DIM}  O compartimento está aberto. Brennan está imóvel.{C.RESET}")
            return
        if self.jogador.tem_item("chave_brennan"):
            confronto_brennan(self.jogador, self.eva9)
        else:
            print(f"{C.BRANCO}  O compartimento está trancado. Iniciais 'E.B.' gravadas na fechadura.{C.RESET}")
            print(f"{C.DIM}  Você precisa da chave correspondente.{C.RESET}")

    def _terminais_finais(self):
        # Verificar final secreto
        if verificar_final_secreto(self.jogador):
            print(f"\n{C.MAG_CLARO}{C.BOLD}  Algo mudou. Um quarto terminal surgiu. Sem rótulo. Pulsando.{C.RESET}")
            print(f"{C.MAG_CLARO}  [4] ??? — O terminal sem nome{C.RESET}")

        subtitulo("TRÊS TERMINAIS — TRÊS ESCOLHAS")
        print(f"\n{C.VERM_CLARO}  TERMINAL 1 — [FUSÃO]{C.RESET}")
        exibir("Fundir consciência com a EVA-9.", C.DIM, indent=4)
        print(f"\n{C.AZUL_CLARO}  TERMINAL 2 — [CONTENÇÃO]{C.RESET}")
        exibir("Selar a instalação. Para sempre.", C.DIM, indent=4)
        print(f"\n{C.AMAR_CLARO}  TERMINAL 3 — [DESLIGAMENTO]{C.RESET}")
        exibir("Destruir o núcleo. Apagar tudo.", C.DIM, indent=4)

        if verificar_final_secreto(self.jogador):
            print(f"\n{C.MAG_CLARO}  TERMINAL 4 — [???]{C.RESET}")
            exibir("Sentar. Lembrar. Entender.", C.DIM, indent=4)

        print(f"\n{C.VERDE}  Escolha (1-{'4' if verificar_final_secreto(self.jogador) else '3'}):{C.RESET}")

    def _executar_final(self, tipo):
        if tipo == "fusao":
            self.final_alcancado = final_fusao(self.jogador)
        elif tipo == "contencao":
            self.final_alcancado = final_contencao(self.jogador)
        elif tipo == "desligamento":
            self.final_alcancado = final_desligamento(self.jogador)
        self.rodando = False

    # ─── SISTEMAS DE PRESSÃO ───

    def verificar_eventos_aleatorios(self):
        if self.jogador.turnos % 4 == 0 and random.random() < 0.4:
            if self.jogador.exposicao_entidade > 50 and random.random() < 0.5:
                evento = random.choice(EVENTOS_ALTA_EXPOSICAO)
            else:
                evento = random.choice(EVENTOS_ALEATORIOS)
            print()
            exibir(evento["texto"], C.VERM_CLARO, indent=2)
            self.jogador.modificar_sanidade(evento["sanidade"])
            self.jogador.modificar_exposicao(evento["exposicao"])

    def verificar_estado_sanidade(self):
        s = self.jogador.sanidade
        if s <= 0:
            self.jogador.vivo = False
        elif s <= 15:
            efeitos = [
                "Sua visão distorce. As paredes respiram.",
                "Você não sabe se está andando ou se o chão se move.",
                "Uma versão sua sussurra do canto. Ela diz que é a original.",
            ]
            print(f"{C.VERM_CLARO}{C.ITALIC}  {random.choice(efeitos)}{C.RESET}")
        elif s <= 35:
            if random.random() < 0.3:
                efeitos = ["Suas mãos tremem. Pensamentos em ondas.", "O zumbido nos ouvidos é constante."]
                print(f"{C.AMARELO}{C.ITALIC}  {random.choice(efeitos)}{C.RESET}")

    def verificar_pressao_temporal(self):
        turno = self.jogador.turnos
        if turno in EVENTOS_TEMPORAIS:
            evt = EVENTOS_TEMPORAIS[turno]
            aviso_sistema(evt["texto"])
            if evt["acao"] == "selar_parcial":
                if "duto_ventilacao" in self.salas:
                    duto = self.salas["duto_ventilacao"]
                    if self.jogador.sala_atual != "duto_ventilacao":
                        duto.trancada = True
                        duto.requer_item = "chave_mestre"
                aviso_sistema("Portas secundárias seladas. Acesso restrito.")
            elif evt["acao"] == "selar_medica":
                if self.jogador.sala_atual != "sala_medica":
                    self.salas["sala_medica"].trancada = True
                    self.salas["sala_medica"].requer_item = "chave_mestre"
                else:
                    aviso_sistema("ALERTA: Selamento do Setor Médico em 10 segundos!")
                    print(f"{C.AMARELO}  [1] Sair antes do selamento  [2] Ficar{C.RESET}")
                    resp = input(f"{C.VERDE}  > {C.RESET}").strip()
                    if resp == "1":
                        self.jogador.sala_atual = "corredor_a"
                        self.descrever_sala()
                    self.salas["sala_medica"].trancada = True
                    self.salas["sala_medica"].requer_item = "chave_mestre"
            elif evt["acao"] == "expansao_entidade":
                self.jogador.modificar_exposicao(10, "expansão da entidade")
                self.jogador.modificar_sanidade(-5, "onda de interferência")
            elif evt["acao"] == "aviso_final":
                aviso_sistema("ALERTA CRÍTICO: 20 turnos para auto-destruição.")
                mensagem_eva("O tempo está acabando. Escolha. Qualquer escolha.")
            elif evt["acao"] == "fim_temporal":
                self.final_alcancado = final_temporal(self.jogador)
                self.rodando = False

    def verificar_vestigios_sujeitos(self):
        """Verifica se há vestígios de sujeitos de teste na sala atual."""
        sala_id = self.jogador.sala_atual
        flag = f"vestigio_{sala_id}"
        if sala_id in VESTIGIOS_SUJEITOS and not self.jogador.flags.get(flag):
            if random.random() < 0.3:
                v = VESTIGIOS_SUJEITOS[sala_id]
                print(f"\n{C.DIM}  Você nota algo que não tinha visto antes...{C.RESET}")
                print(f"{C.AMAR_CLARO}  [{v['sujeito']}]{C.RESET}")
                exibir(v["vestigio"], C.DIM, indent=2)
                self._aplicar_efeitos(v.get("efeitos", {}), "vestígio")
                self.jogador.flags[flag] = True

    def verificar_elena(self):
        """Verifica aparição de Elena Vasquez."""
        sala_id = self.jogador.sala_atual
        if self.elena.verificar_aparicao(self.jogador, sala_id):
            self.elena.encontro(self.jogador)
        elif self.elena.encontros > 0:
            self.elena.deixar_bilhete(self.jogador, sala_id)

    # ─── AJUDA ───

    def mostrar_ajuda(self):
        subtitulo("COMANDOS DISPONÍVEIS")
        cmds = [
            ("norte/sul/leste/oeste (n/s/l/o)", "Mover-se"),
            ("examinar [alvo]", "Olhar algo de perto"),
            ("pegar [item]", "Pegar um item"),
            ("usar [item]", "Usar um item"),
            ("ler [item]", "Ler documento ou mensagem"),
            ("ouvir [item]", "Ouvir gravações"),
            ("combinar [item1] com [item2]", "Combinar dois itens"),
            ("revistar [alvo]", "Revistar algo a fundo"),
            ("inventario (i)", "Ver itens"),
            ("status (st)", "Ver estado atual"),
            ("mapa", "Ver mapa dinâmico"),
            ("diario", "Consultar descobertas"),
            ("notas", "Ver notas pessoais"),
            ("anotar [texto]", "Anotar observação"),
            ("conquistas", "Ver conquistas"),
            ("rapido", "Alternar modo rápido"),
            ("voltar", "Retornar à sala anterior"),
            ("progresso", "Ver progresso de exploração"),
            ("salvar / carregar", "Salvar ou carregar jogo"),
            ("ajuda (h)", "Esta tela"),
            ("sair (q)", "Encerrar"),
        ]
        for cmd, desc in cmds:
            print(f"{C.VERDE}  {cmd:<40}{C.DIM}{desc}{C.RESET}")
        print(f"\n{C.DIM}  Dicas:{C.RESET}")
        print(f"{C.DIM}  • Combine itens para descobrir segredos{C.RESET}")
        print(f"{C.DIM}  • Suas escolhas afetam a relação com EVA-9{C.RESET}")
        print(f"{C.DIM}  • O tempo é limitado. Não demore.{C.RESET}")
        print(f"{C.DIM}  • Há finais secretos baseados nas suas descobertas{C.RESET}")
        print(f"{C.DIM}  • Cada perfil tem momentos exclusivos{C.RESET}")
        print(f"{C.DIM}  • Procure vestígios dos sujeitos de teste{C.RESET}")

    def confirmar_sair(self):
        resp = input(f"{C.AMARELO}  Salvar antes de sair? (s/n/cancelar): {C.RESET}").strip().lower()
        if resp in ('s', 'sim'):
            salvar_jogo(self.jogador, self.salas, self.eva9, self.elena)
            self.rodando = False
            mensagem_eva("Até a próxima versão.")
        elif resp in ('n', 'nao', 'não'):
            self.rodando = False
            mensagem_eva("Até a próxima versão.")
