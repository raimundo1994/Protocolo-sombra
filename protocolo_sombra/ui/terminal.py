#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Terminal — Cores, formatação e utilidades de exibição.
Centraliza toda interação visual com o terminal.
"""

import os
import sys
import time
import random
import textwrap
import threading


# ═══════════════════════════════════════════════════════════
# CORES ANSI
# ═══════════════════════════════════════════════════════════

class Cores:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    ITALIC     = "\033[3m"
    UNDERLINE  = "\033[4m"
    BLINK      = "\033[5m"
    REVERSE    = "\033[7m"
    STRIKE     = "\033[9m"

    PRETO      = "\033[30m"
    VERMELHO   = "\033[31m"
    VERDE      = "\033[32m"
    AMARELO    = "\033[33m"
    AZUL       = "\033[34m"
    MAGENTA    = "\033[35m"
    CIANO      = "\033[36m"
    BRANCO     = "\033[37m"

    BG_PRETO   = "\033[40m"
    BG_VERMELHO= "\033[41m"
    BG_VERDE   = "\033[42m"
    BG_AMARELO = "\033[43m"
    BG_AZUL    = "\033[44m"
    BG_MAGENTA = "\033[45m"

    VERM_CLARO = "\033[91m"
    VERDE_CLARO= "\033[92m"
    AMAR_CLARO = "\033[93m"
    AZUL_CLARO = "\033[94m"
    MAG_CLARO  = "\033[95m"
    CIANO_CLARO= "\033[96m"

C = Cores

LARGURA = 72

# ═══════════════════════════════════════════════════════════
# MODO RÁPIDO (skippable animations)
# ═══════════════════════════════════════════════════════════

class ModoExibicao:
    """Controla velocidade de animações — permite skip com qualquer tecla."""
    rapido = False
    velocidade_mult = 1.0

    @classmethod
    def set_rapido(cls, valor=True):
        cls.rapido = valor
        cls.velocidade_mult = 0.0 if valor else 1.0

    @classmethod
    def get_velocidade(cls, base):
        if cls.rapido:
            return 0
        return base * cls.velocidade_mult


# ═══════════════════════════════════════════════════════════
# [MELHORIA ROB1] INPUT SEGURO
# ═══════════════════════════════════════════════════════════

def input_seguro(prompt="", default=""):
    """Wrapper seguro para input que captura EOFError e KeyboardInterrupt."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default


# ═══════════════════════════════════════════════════════════
# FUNÇÕES DE EXIBIÇÃO
# ═══════════════════════════════════════════════════════════

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')


def digitando(texto, velocidade=0.02, cor=""):
    """Efeito de digitação com velocidade ajustável."""
    vel = ModoExibicao.get_velocidade(velocidade)
    if vel == 0:
        print(f"{cor}{texto}{C.RESET}")
        return

    for char in texto:
        sys.stdout.write(f"{cor}{char}{C.RESET}")
        sys.stdout.flush()
        if char in '.!?':
            time.sleep(vel * 6)
        elif char == ',':
            time.sleep(vel * 3)
        elif char == '\n':
            time.sleep(vel * 2)
        else:
            time.sleep(vel)
    print()


def exibir(texto, cor="", indent=0, velocidade=None):
    """Exibe texto com word-wrap e indentação opcional."""
    prefixo = " " * indent
    linhas = textwrap.fill(texto, width=LARGURA - indent).split('\n')
    for linha in linhas:
        if velocidade:
            digitando(f"{prefixo}{linha}", velocidade, cor)
        else:
            print(f"{cor}{prefixo}{linha}{C.RESET}")


def separador(char="═", cor=C.DIM):
    print(f"{cor}{char * LARGURA}{C.RESET}")


def separador_fino(char="─", cor=C.DIM):
    print(f"{cor}{char * LARGURA}{C.RESET}")


def titulo(texto, cor=C.VERM_CLARO):
    separador("═", cor)
    espacos = (LARGURA - len(texto)) // 2
    print(f"{cor}{' ' * espacos}{C.BOLD}{texto}{C.RESET}")
    separador("═", cor)


def subtitulo(texto, cor=C.AMARELO):
    print(f"\n{cor}{C.BOLD}  ▸ {texto}{C.RESET}")
    separador_fino("─", C.DIM)


def aviso_sistema(texto, cor=C.VERM_CLARO):
    print(f"\n{cor}{C.BOLD}  [SISTEMA] {texto}{C.RESET}")


def mensagem_eva(texto):
    print(f"\n{C.MAGENTA}{C.ITALIC}  EVA-9: \"{texto}\"{C.RESET}")


def mensagem_terminal(texto):
    print(f"{C.VERDE}  > {texto}{C.RESET}")


def mensagem_brennan(texto):
    """Nova: mensagens da Dra. Brennan (holográficas/gravadas)."""
    print(f"\n{C.CIANO}{C.ITALIC}  DRA. BRENNAN: \"{texto}\"{C.RESET}")


def mensagem_npc(nome, texto, cor=C.AMAR_CLARO):
    """Nova: mensagens de NPCs genéricos."""
    print(f"\n{cor}{C.ITALIC}  {nome}: \"{texto}\"{C.RESET}")


def glitch(texto):
    """Efeito de corrupção de texto."""
    chars_glitch = "█▓▒░╫╬╪┼╳"
    resultado = list(texto)
    qtd = max(1, len(texto) // 5)
    for _ in range(qtd):
        pos = random.randint(0, len(resultado) - 1)
        resultado[pos] = random.choice(chars_glitch)
    print(f"{C.VERM_CLARO}{''.join(resultado)}{C.RESET}")


def glitch_progressivo(texto, intensidade=0.2):
    """Nova: glitch com intensidade variável (0.0 a 1.0)."""
    chars_glitch = "█▓▒░╫╬╪┼╳◈◊"
    resultado = list(texto)
    qtd = max(1, int(len(texto) * intensidade))
    for _ in range(qtd):
        pos = random.randint(0, len(resultado) - 1)
        resultado[pos] = random.choice(chars_glitch)
    print(f"{C.VERM_CLARO}{''.join(resultado)}{C.RESET}")


def pausa(msg=""):
    if msg:
        print(f"\n{C.DIM}  {msg}{C.RESET}")
    input_seguro(f"{C.DIM}  [Pressione ENTER para continuar...]{C.RESET}")


def barra_status(nome, valor, maximo, cor_cheia, cor_vazia=C.DIM):
    total = 20
    cheio = int((valor / maximo) * total)
    vazio = total - cheio
    barra = f"{'█' * cheio}{'░' * vazio}"
    print(f"  {cor_cheia}{nome:<22} [{barra}] {valor}/{maximo}{C.RESET}")


def caixa_texto(texto, cor=C.CIANO, largura=60):
    """Nova: exibe texto em uma caixa decorada."""
    linhas = textwrap.fill(texto, width=largura - 4).split('\n')
    print(f"{cor}  ┌{'─' * (largura - 2)}┐{C.RESET}")
    for linha in linhas:
        espacos = largura - 2 - len(linha)
        print(f"{cor}  │ {linha}{' ' * espacos}│{C.RESET}")
    print(f"{cor}  └{'─' * (largura - 2)}┘{C.RESET}")


def efeito_estatica(linhas=3):
    """Nova: efeito de estática visual."""
    chars = "█▓▒░┃┆┇╎╏"
    for _ in range(linhas):
        linha = ''.join(random.choice(chars) for _ in range(LARGURA))
        print(f"{C.DIM}{linha}{C.RESET}")
        time.sleep(ModoExibicao.get_velocidade(0.05))


def efeito_corrupcao(texto, frames=5, delay=0.1):
    """Nova: anima texto sendo corrompido e restaurado."""
    vel = ModoExibicao.get_velocidade(delay)
    if vel == 0:
        print(f"{C.VERM_CLARO}  {texto}{C.RESET}")
        return

    chars_glitch = "█▓▒░╫╬╪"
    for i in range(frames):
        resultado = list(texto)
        intensidade = (frames - i) / frames
        qtd = int(len(resultado) * intensidade * 0.5)
        for _ in range(qtd):
            pos = random.randint(0, len(resultado) - 1)
            resultado[pos] = random.choice(chars_glitch)
        sys.stdout.write(f"\r{C.VERM_CLARO}  {''.join(resultado)}{C.RESET}")
        sys.stdout.flush()
        time.sleep(vel)
    print(f"\r{C.BRANCO}  {texto}{C.RESET}")


# ═══════════════════════════════════════════════════════════
# MAPA DINÂMICO (NOVO)
# ═══════════════════════════════════════════════════════════

def exibir_mapa_dinamico(jogador, salas, completo=False):
    """Exibe mapa ASCII que atualiza com salas visitadas e posição atual."""

    def marca_sala(sala_id, nome_curto):
        """Retorna o nome da sala com indicador visual de status."""
        if sala_id == jogador.sala_atual:
            return f"{C.VERDE_CLARO}{C.BOLD}[★ {nome_curto}]{C.RESET}{C.CIANO}"
        elif sala_id in salas and salas[sala_id].visitada:
            return f"{C.BRANCO}[{nome_curto}]{C.RESET}{C.CIANO}"
        else:
            return f"{C.DIM}[???]{C.RESET}{C.CIANO}"

    kp = marca_sala("kheiron_profundo", "KHEIRON")
    ns = marca_sala("nucleo_servidores", "SERVIDORES")
    ca = marca_sala("corredor_a", "CORREDOR A")
    sm = marca_sala("sala_medica", "MÉDICA")
    st = marca_sala("sala_terminal", "TERMINAL")
    so = marca_sala("sala_observacao", "OBSERVAÇÃO")
    dv = marca_sala("duto_ventilacao", "DUTO")
    am = marca_sala("arquivo_morto", "ARQUIVO")

    print(f"\n{C.CIANO}{C.BOLD}  ═══ MAPA KHEIRON-4 ═══{C.RESET}")
    print(f"{C.CIANO}")
    print(f"           {kp}")
    print(f"               │")
    print(f"           {ns}")
    print(f"               │")
    print(f"      {sm} ── {ca}")
    print(f"               │")
    print(f"           {st}")
    print(f"          ╱         ╲")
    print(f"     {so}    {dv}")
    print(f"         │")
    print(f"     {am}")

    if completo or jogador.flags.get("mapa_completo"):
        ss = marca_sala("sala_secreta", "SETOR APAG.")
        print(f"                        {ss}")
        print(f"                  (via duto →)")

    print(f"{C.RESET}")

    # Legenda
    print(f"{C.DIM}  ★ = Sua posição | [NOME] = Visitada | [???] = Não visitada{C.RESET}")

    # Alertas de portas trancadas
    for sala_id, sala in salas.items():
        if sala.trancada and sala.visitada:
            print(f"{C.VERM_CLARO}  🔒 {sala.nome} está trancada{C.RESET}")


# ═══════════════════════════════════════════════════════════
# [MELHORIA 2] BARRA DE PROGRESSO DE EXPLORAÇÃO
# ═══════════════════════════════════════════════════════════

def barra_progresso(jogador, salas, total_segredos=12, total_combinacoes=9):
    """Exibe indicador percentual de progresso de exploração."""
    from protocolo_sombra_v3.entities.jogador import contar_segredos
    salas_visitadas = sum(1 for s in salas.values() if s.visitada)
    total_salas = len(salas)
    segredos = contar_segredos(jogador)
    combos = len(jogador.combinacoes_feitas)

    print(f"{C.DIM}  ─── Progresso ───{C.RESET}")
    print(f"{C.DIM}  Salas: {salas_visitadas}/{total_salas} | "
          f"Segredos: {segredos}/{total_segredos} | "
          f"Combinações: {combos}/{total_combinacoes}{C.RESET}")


# ═══════════════════════════════════════════════════════════
# [MELHORIA 7] SONS AMBIENTAIS POR SALA
# ═══════════════════════════════════════════════════════════

SONS_AMBIENTE = {
    "sala_terminal": [
        "Zumbido elétrico baixo e constante.",
        "O ventilador de teto tossiu e parou.",
        "Cliques espaçados do terminal, como se digitasse sozinho.",
    ],
    "corredor_a": [
        "Gotejamento ritmado ao longe.",
        "Metal rangendo em algum lugar acima.",
        "Um sussurro que some quando você presta atenção.",
    ],
    "duto_ventilacao": [
        "Sua respiração ecoa amplificada.",
        "Algo se arrasta nas juntas do metal. Longe.",
        "O ar vibra com uma frequência grave demais para ouvir.",
    ],
    "sala_observacao": [
        "Estática nos monitores. Ritmada.",
        "O vidro trincado emite um estalido térmico.",
        "Zumbido dos equipamentos ligados sem operador.",
    ],
    "nucleo_servidores": [
        "O zumbido dos servidores tem cadência cardíaca.",
        "LEDs piscam em padrão que parece morse.",
        "Calor. O ar ondula visivelmente.",
    ],
    "sala_medica": [
        "A geladeira médica treme periodicamente.",
        "Gotejamento de soro caindo num frasco vazio.",
        "Algo se move sob uma das macas. Provavelmente.",
    ],
    "arquivo_morto": [
        "Papel se deslocando sozinho numa das caixas.",
        "Poeira dançando em espiral impossível.",
        "O cofre emite um beep suave, repetidamente.",
    ],
    "sala_secreta": [
        "Silêncio absoluto. Você ouve seu sangue circulando.",
        "Um tom agudo, no limite da percepção.",
        "O ar tem textura. Espesso. Quente.",
    ],
    "kheiron_profundo": [
        "A esfera gira com um sussurro que não é som.",
        "Os terminais pulsam luz como velas ao vento.",
        "Algo respira. Não é você.",
    ],
}


def som_ambiente(sala_id):
    """Exibe um som ambiente aleatório baseado na sala atual."""
    if sala_id in SONS_AMBIENTE and random.random() < 0.25:
        som = random.choice(SONS_AMBIENTE[sala_id])
        print(f"{C.DIM}{C.ITALIC}  [{som}]{C.RESET}")
