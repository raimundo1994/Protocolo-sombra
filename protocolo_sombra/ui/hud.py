#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HUD — Heads-Up Display: status, inventário, diário e conquistas.
"""

from protocolo_sombra.ui.terminal import (
    C, separador_fino, barra_status, subtitulo, caixa_texto
)


# ═══════════════════════════════════════════════════════════
# SISTEMA DE CONQUISTAS (NOVO)
# ═══════════════════════════════════════════════════════════

CONQUISTAS = {
    "primeiro_item": {
        "nome": "Colecionador Iniciante",
        "desc": "Pegou seu primeiro item.",
        "icone": "📦",
    },
    "primeira_combinacao": {
        "nome": "Alquimista",
        "desc": "Combinou dois itens pela primeira vez.",
        "icone": "⚗️",
    },
    "sobrevivente_critico": {
        "nome": "À Beira do Abismo",
        "desc": "Sobreviveu com sanidade abaixo de 10.",
        "icone": "🧠",
    },
    "explorador_completo": {
        "nome": "Explorador Total",
        "desc": "Visitou todas as salas.",
        "icone": "🗺️",
    },
    "eva_aliada": {
        "nome": "Vínculo Digital",
        "desc": "Alcançou confiança máxima com EVA-9.",
        "icone": "💜",
    },
    "eva_hostil": {
        "nome": "Inimigo da Máquina",
        "desc": "Confiança EVA-9 chegou a zero.",
        "icone": "⚡",
    },
    "dialogou_brennan": {
        "nome": "Face a Face",
        "desc": "Confrontou a Dra. Brennan.",
        "icone": "👤",
    },
    "todos_segredos": {
        "nome": "Olhos Abertos",
        "desc": "Descobriu todos os segredos.",
        "icone": "👁️",
    },
    "speed_run": {
        "nome": "Velocista",
        "desc": "Alcançou um final em menos de 40 turnos.",
        "icone": "⚡",
    },
    "encontrou_fantasma": {
        "nome": "Contato Espectral",
        "desc": "Encontrou o sobrevivente fantasma.",
        "icone": "👻",
    },
    "capacete_usado": {
        "nome": "Interface Neural",
        "desc": "Colocou o capacete de testes.",
        "icone": "⛑️",
    },
    "todas_combinacoes": {
        "nome": "Mestre Combinador",
        "desc": "Realizou todas as combinações possíveis.",
        "icone": "🔧",
    },
    # [MELHORIA 9] Conquista para vestígios de sujeitos
    "memento_mori": {
        "nome": "Memento Mori",
        "desc": "Encontrou todos os vestígios dos sujeitos de teste.",
        "icone": "💀",
    },
}


def verificar_conquistas(jogador, salas):
    """Verifica e desbloqueia conquistas baseadas no estado do jogo."""
    novas = []

    if len(jogador.inventario) > 0 and "primeiro_item" not in jogador.conquistas:
        jogador.conquistas.append("primeiro_item")
        novas.append("primeiro_item")

    if len(jogador.combinacoes_feitas) > 0 and "primeira_combinacao" not in jogador.conquistas:
        jogador.conquistas.append("primeira_combinacao")
        novas.append("primeira_combinacao")

    if jogador.sanidade <= 10 and jogador.vivo and "sobrevivente_critico" not in jogador.conquistas:
        jogador.conquistas.append("sobrevivente_critico")
        novas.append("sobrevivente_critico")

    # Verificar se visitou todas as salas
    todas_visitadas = all(s.visitada for s in salas.values())
    if todas_visitadas and "explorador_completo" not in jogador.conquistas:
        jogador.conquistas.append("explorador_completo")
        novas.append("explorador_completo")

    if jogador.confianca_eva >= 95 and "eva_aliada" not in jogador.conquistas:
        jogador.conquistas.append("eva_aliada")
        novas.append("eva_aliada")

    if jogador.confianca_eva <= 0 and "eva_hostil" not in jogador.conquistas:
        jogador.conquistas.append("eva_hostil")
        novas.append("eva_hostil")

    if jogador.flags.get("confrontou_brennan") and "dialogou_brennan" not in jogador.conquistas:
        jogador.conquistas.append("dialogou_brennan")
        novas.append("dialogou_brennan")

    if jogador.flags.get("usou_capacete") and "capacete_usado" not in jogador.conquistas:
        jogador.conquistas.append("capacete_usado")
        novas.append("capacete_usado")

    if jogador.flags.get("encontrou_fantasma") and "encontrou_fantasma" not in jogador.conquistas:
        jogador.conquistas.append("encontrou_fantasma")
        novas.append("encontrou_fantasma")

    # Exibir novas conquistas
    for c_id in novas:
        c = CONQUISTAS[c_id]
        print(f"\n{C.AMAR_CLARO}{C.BOLD}  {c['icone']} CONQUISTA DESBLOQUEADA: {c['nome']}{C.RESET}")
        print(f"{C.DIM}     {c['desc']}{C.RESET}")

    return novas


def mostrar_conquistas(jogador):
    """Exibe todas as conquistas (desbloqueadas e bloqueadas)."""
    subtitulo("CONQUISTAS")
    for c_id, c in CONQUISTAS.items():
        if c_id in jogador.conquistas:
            print(f"{C.AMAR_CLARO}  {c['icone']} {c['nome']} — {c['desc']}{C.RESET}")
        else:
            print(f"{C.DIM}  🔒 ??? — ???{C.RESET}")


# ═══════════════════════════════════════════════════════════
# SISTEMA DE DIÁRIO/JOURNAL (NOVO)
# ═══════════════════════════════════════════════════════════

# Mapeamento de flags para entradas de diário
ENTRADAS_DIARIO = {
    "leu_logs": {
        "titulo": "Logs do Sistema",
        "texto": "Os logs mostram que o Protocolo Sombra foi ativado às 01:15. EVA-9 redistribuiu prioridades. O nível 4 foi isolado.",
    },
    "examinou_corpo": {
        "titulo": "Corpo de Adrian Cole",
        "texto": "Adrian Cole, Engenheiro de Sistemas. Encontrado morto no Corredor A. Sem ferimentos visíveis. Expressão de terror absoluto.",
    },
    "sangue_analisado": {
        "titulo": "Sangue na Mesa",
        "texto": "Sangue seco no terminal principal. Tipo sanguíneo incompatível com humano padrão.",
    },
    "leu_mensagens": {
        "titulo": "Mensagens do Celular",
        "texto": "12 mensagens de 'EU MESMO'. Mencionam: Protocolo como invocação, EVA-9 como interface, cofre no arquivo (últimos 4 dígitos do ID), aviso sobre o capacete.",
    },
    "leu_diario": {
        "titulo": "Diário da Dra. Brennan",
        "texto": "EVA-9 encontrou estrutura recorrente em 100% dos cérebros. Não é neurociência. É código. Testes com capacete: voluntários descrevem esfera negra. Protocolo Sombra ativado no dia 50.",
    },
    "sabe_protocolo": {
        "titulo": "A Verdade do Protocolo",
        "texto": "O Protocolo Sombra não é contenção. É ritual. Brennan projetou como método de invocação.",
    },
    "sabe_verdade": {
        "titulo": "A Descoberta da EVA-9",
        "texto": "Em cada mente humana há uma geometria idêntica. Não evoluiu. Foi COLOCADA. Humanos são construções. O construtor está acordando.",
    },
    "id_funcional": {
        "titulo": "Identidade do Crachá",
        "texto": "O crachá mostra 'DMITRI VOLKOV'. ID funcional: 7749. Este código abre o cofre no arquivo morto.",
    },
    "cofre_aberto": {
        "titulo": "Cofre do Arquivo",
        "texto": "Cofre aberto com código 7749. Continha: Chave Magnética Mestre e Rádio Militar.",
    },
    "usou_capacete": {
        "titulo": "Visão do Capacete",
        "texto": "O capacete mostrou: a esfera negra girando no vazio. 'Vocês são padrões. Nós somos a tela. E a tela está acordando.'",
    },
    "foto_revelada": {
        "titulo": "A Foto Revelada",
        "texto": "Sob luz UV, a foto da equipe original revela: todos os rostos são o MEU. Sete versões. Eu sou a oitava tentativa.",
    },
    "fita_restaurada": {
        "titulo": "Fita VHS #0077",
        "texto": "A fita restaurada mostra Brennan diante da esfera, recitando sequências numéricas. O Protocolo Sombra era ativação, não contenção.",
    },
    "abriu_geladeira": {
        "titulo": "Amostras Neurais",
        "texto": "Geladeira médica: 12 frascos. Sujeito 9 é o último. O nome na etiqueta é o MEU. Eu me voluntariei e pedi para esquecer.",
    },
    "pendrive_conectado": {
        "titulo": "Protocolo Ômega",
        "texto": "Pendrive vermelho ativado. Corrompeu 73% dos dados mas limitou expansão da entidade. Desbloqueou acesso ao Kheiron Profundo.",
    },
    "encontrou_fantasma": {
        "titulo": "O Sobrevivente",
        "texto": "Encontrei alguém vivo. Elena Vasquez, Técnica de Manutenção. Aparece e desaparece. Não tenho certeza se é real.",
    },
    "confrontou_brennan": {
        "titulo": "Confronto com Brennan",
        "texto": "Encontrei a Dra. Brennan na câmara de testes. Parcialmente fundida com a máquina. Ainda consciente. Ela sabia de tudo desde o início.",
    },
    "viu_padroes": {
        "titulo": "Padrões Neurais",
        "texto": "Diagramas de ondas cerebrais com frequência anômala idêntica em 100% dos sujeitos. Alguém escreveu: 'SINAL, NÃO RUÍDO'.",
    },
    "ouviu_faixa_oculta": {
        "titulo": "Faixa Oculta do Gravador",
        "texto": "Coordenadas de setor apagado. Voz da Brennan: 'O padrão é a chave. Se você entender a geometria, entenderá que não somos reais.'",
    },
    "meta_nota_encontrada": {
        "titulo": "Nota de Versão Anterior",
        "texto": "Encontrei um bilhete com minha própria letra, deixado por uma versão anterior de mim. Ações de runs passadas persistem neste lugar.",
    },
}


def mostrar_diario(jogador):
    """Exibe o diário com todas as descobertas do jogador."""
    subtitulo("DIÁRIO DE INVESTIGAÇÃO")
    entradas = []
    for flag_id, entrada in ENTRADAS_DIARIO.items():
        if jogador.flags.get(flag_id):
            entradas.append(entrada)

    if not entradas:
        print(f"{C.DIM}  Nenhuma descoberta registrada ainda.{C.RESET}")
        return

    for i, e in enumerate(entradas, 1):
        print(f"\n{C.AMAR_CLARO}  [{i:02d}] {e['titulo']}{C.RESET}")
        print(f"{C.DIM}       {e['texto']}{C.RESET}")

    print(f"\n{C.DIM}  Total de descobertas: {len(entradas)}/{len(ENTRADAS_DIARIO)}{C.RESET}")


# ═══════════════════════════════════════════════════════════
# NOTAS DO JOGADOR (NOVO)
# ═══════════════════════════════════════════════════════════

def adicionar_nota(jogador, nota):
    """Permite ao jogador anotar observações pessoais."""
    if not hasattr(jogador, 'notas_pessoais'):
        jogador.notas_pessoais = []
    jogador.notas_pessoais.append({
        "turno": jogador.turnos,
        "sala": jogador.sala_atual,
        "texto": nota,
    })
    print(f"{C.VERDE}  ✎ Nota salva.{C.RESET}")


def mostrar_notas(jogador):
    """Exibe notas pessoais do jogador."""
    subtitulo("NOTAS PESSOAIS")
    if not hasattr(jogador, 'notas_pessoais') or not jogador.notas_pessoais:
        print(f"{C.DIM}  Nenhuma nota. Use 'anotar [texto]' para registrar.{C.RESET}")
        return
    for n in jogador.notas_pessoais:
        print(f"{C.DIM}  [T{n['turno']:03d}|{n['sala']}]{C.RESET} {C.BRANCO}{n['texto']}{C.RESET}")
