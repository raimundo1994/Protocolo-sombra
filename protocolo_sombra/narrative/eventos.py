#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Eventos narrativos, pressão temporal, eventos aleatórios,
encontros com sujeitos de teste, confronto com Brennan.
"""

import random
import time
from protocolo_sombra.ui.terminal import (
    C, exibir, digitando, separador_fino, titulo, subtitulo,
    mensagem_eva, mensagem_brennan, mensagem_npc,
    aviso_sistema, pausa, glitch, efeito_estatica,
    efeito_corrupcao, limpar
)
from protocolo_sombra.entities.jogador import Perfil, PERFIS_INFO


# ═══════════════════════════════════════════════════════════
# DADOS NARRATIVOS
# ═══════════════════════════════════════════════════════════

MENSAGENS_CELULAR = [
    {"hora": "22:03", "texto": "Não volte para o nível 4. Eles sabem."},
    {"hora": "22:17", "texto": "A Dra. Brennan mentiu sobre o Protocolo. Não era contenção. Era invocação."},
    {"hora": "22:34", "texto": "Se você está lendo isso, já aconteceu. Sinto muito."},
    {"hora": "23:01", "texto": "O cofre no arquivo morto. Código: os últimos 4 dígitos do seu ID funcional."},
    {"hora": "23:15", "texto": "EVA-9 não é uma IA. Nunca foi. É uma interface."},
    {"hora": "23:22", "texto": "Alguém apagou 3 horas da gravação do Setor 7."},
    {"hora": "23:41", "texto": "Não confie na voz feminina. Não é a Brennan. Não é ninguém."},
    {"hora": "00:08", "texto": "Os padrões que ela encontrou... estão em todos nós. Desde sempre."},
    {"hora": "00:23", "texto": "O capacete funciona nos dois sentidos. Não coloque."},
    {"hora": "00:45", "texto": "Eu vi meu próprio corpo no corredor. Ainda estou andando. Como?"},
    {"hora": "01:12", "texto": "Ela não nos observa. Ela nos EXECUTA. Simulação dentro de simulação."},
    {"hora": "01:58", "texto": "Se esta for a última: o desligamento total. Terminal 3. Aceite o custo."},
]

GRAVACOES_GRAVADOR = [
    "[ESTÁTICA] ...registrando para posteridade... [RUÍDO] ...testes com capacete há 6 dias... [RESPIRAÇÃO] ...sujeitos falam em uníssono... coisas que não deveriam saber...",
    "[VOZ FEMININA] ...padrão presente em 100% dos escaneamentos... não é anomalia... é ESTRUTURA... algo no firmware da consciência... [VIDRO QUEBRANDO]",
    "[VOZ MASCULINA] ...desliga essa merda... DESLIGA!... ela está ouvindo... [GRITO] [ESTÁTICA]",
]


# ═══════════════════════════════════════════════════════════
# EVENTOS ALEATÓRIOS (expandidos)
# ═══════════════════════════════════════════════════════════

EVENTOS_ALEATORIOS = [
    {"texto": "As luzes piscam por três segundos. Quando voltam, a sala ficou menor.", "sanidade": -3, "exposicao": 2},
    {"texto": "Você ouve sua própria voz nos alto-falantes, dizendo palavras que ainda não disse.", "sanidade": -5, "exposicao": 5},
    {"texto": "Um arquivo aparece no terminal. Seu nome. A data é de amanhã.", "sanidade": -4, "exposicao": 3},
    {"texto": "O chão vibra. Algo que se movia desde que chegou acaba de parar.", "sanidade": -2, "exposicao": 1},
    {"texto": "Uma câmera gira para apontar diretamente para você. LED vermelho pisca duas vezes.", "sanidade": -3, "exposicao": 4},
    {"texto": "Toque gelado na nuca. Ninguém atrás. Mas o ar está mais frio.", "sanidade": -5, "exposicao": 3},
    {"texto": "Por uma fração de segundo, sua sombra se move antes de você.", "sanidade": -4, "exposicao": 2},
    {"texto": "O rádio na parede soletra seu nome ao contrário.", "sanidade": -3, "exposicao": 3},
    {"texto": "Uma pegada no chão que não é sua. Vai até onde você está e para.", "sanidade": -4, "exposicao": 2},
    {"texto": "Você esquece quem é. Por três batimentos cardíacos.", "sanidade": -6, "exposicao": 5},
    # NOVOS v3
    {"texto": "O reflexo na tela do terminal pisca ANTES de você piscar.", "sanidade": -4, "exposicao": 3},
    {"texto": "Uma criança ri no alto-falante. Não há crianças aqui. Nunca houve.", "sanidade": -5, "exposicao": 3},
    {"texto": "Suas mãos digitam algo no ar. Sem teclado. Sem controle.", "sanidade": -6, "exposicao": 4},
]

EVENTOS_ALTA_EXPOSICAO = [
    {"texto": "As paredes pulsam como se respirassem. Impossível. Mas não param.", "sanidade": -8, "exposicao": 5},
    {"texto": "Uma voz sua, dos servidores: 'Eu sou a versão que sobreviveu. Você não é.'", "sanidade": -10, "exposicao": 8},
    {"texto": "Seus dedos digitam sozinhos: 'EU ESTOU DENTRO DE VOCÊ.'", "sanidade": -12, "exposicao": 10},
    # NOVOS v3
    {"texto": "Você vê a sala inteira de cima. Como se flutuasse. Quando olha para baixo, seu corpo está lá. Vazio.", "sanidade": -10, "exposicao": 8},
    {"texto": "A geometria que a EVA encontrou aparece na sua visão periférica. Linhas, ângulos, fractais. Mesmo de olhos fechados.", "sanidade": -8, "exposicao": 10},
]


# ═══════════════════════════════════════════════════════════
# PRESSÃO TEMPORAL
# ═══════════════════════════════════════════════════════════

EVENTOS_TEMPORAIS = {
    20: {
        "texto": "[SISTEMA] Selamento parcial detectado. Portas secundárias bloqueadas.",
        "acao": "selar_parcial",
    },
    35: {
        "texto": "[SISTEMA] Contenção automática em andamento. Setor Médico isolado.",
        "acao": "selar_medica",
    },
    50: {
        "texto": "[SISTEMA] ALERTA: Expansão da entidade acelerada. Nível Ômega comprometido.",
        "acao": "expansao_entidade",
    },
    65: {
        "texto": "[SISTEMA] Protocolo de auto-destruição em espera. 20 turnos restantes.",
        "acao": "aviso_final",
    },
    85: {
        "texto": "[SISTEMA] Protocolo de auto-destruição ATIVADO. A instalação será destruída.",
        "acao": "fim_temporal",
    },
}


# ═══════════════════════════════════════════════════════════
# VESTÍGIOS DOS SUJEITOS DE TESTE (NOVO)
# ═══════════════════════════════════════════════════════════

VESTIGIOS_SUJEITOS = {
    "corredor_a": {
        "sujeito": "SUJEITO 03 — Marina Sousa",
        "vestigio": "Um jaleco dobrado no canto, com o nome 'M. SOUSA' bordado. Dentro do bolso, um origami de papel: uma esfera perfeita.",
        "efeitos": {"sanidade": -2},
    },
    "sala_medica": {
        "sujeito": "SUJEITO 07 — Kaito Tanaka",
        "vestigio": "Sob uma das macas, um sketchbook. Cada página tem o mesmo desenho: uma esfera negra vista de ângulos diferentes. Na última página, a esfera tem um olho.",
        "efeitos": {"sanidade": -3, "exposicao": 2},
    },
    "arquivo_morto": {
        "sujeito": "SUJEITO 12 — Petra Lindgren",
        "vestigio": "Crachá de Petra Lindgren caído entre as caixas. Na foto, uma mulher de olhos claros. No verso, ela escreveu: 'A geometria não é nos padrões. A geometria SOMOS NÓS.'",
        "efeitos": {"sanidade": -2, "exposicao": 1},
    },
    "sala_secreta": {
        "sujeito": "SUJEITO 15 — James Wright",
        "vestigio": "Gravado na cadeira de testes, com letra trêmula: 'Wright was here. Wright is everywhere. Wright is you.' As marcas de unhas na correias de couro são dele.",
        "efeitos": {"sanidade": -4, "exposicao": 3},
    },
    "nucleo_servidores": {
        "sujeito": "SUJEITO 19 — Dmitri Volkov",
        "vestigio": "Um crachá idêntico ao que você carrega. Mesmo nome. Mesma foto raspada. A diferença: este tem uma data no verso. Três semanas atrás.",
        "efeitos": {"sanidade": -5, "exposicao": 3},
    },
}


# ═══════════════════════════════════════════════════════════
# CONFRONTO COM BRENNAN (NOVO)
# ═══════════════════════════════════════════════════════════

def confronto_brennan(jogador, eva9):
    """
    Confronto direto com a Dra. Brennan na câmara de testes.
    Requer: chave_brennan + sala_secreta + certas flags.
    """
    jogador.flags["confrontou_brennan"] = True

    limpar()
    titulo("CONFRONTO — DRA. ELARA BRENNAN", C.CIANO)
    print()

    textos_intro = [
        "O compartimento se abre com um sussurro pneumático.",
        "",
        "Dentro não há documentos. Não há itens.",
        "",
        "Há uma mulher.",
        "",
        "Ou o que resta de uma.",
        "",
    ]
    for t in textos_intro:
        if t:
            exibir(t, C.CIANO, indent=2, velocidade=0.025)
        else:
            time.sleep(0.4)

    exibir("A Dra. Elara Brennan está parcialmente fundida com a máquina. Cabos entram na sua coluna vertebral. Sua pele tem a textura de circuito impresso. Os olhos, quando se abrem, são telas LCD mostrando dados.", C.BRANCO, indent=2, velocidade=0.02)
    print()
    exibir("Ela está consciente.", C.BRANCO + C.BOLD, indent=2, velocidade=0.03)
    pausa()

    # Brennan fala
    mensagem_brennan("Então... mais um. Ou o mesmo de sempre.")
    time.sleep(0.5)

    # Reações baseadas no perfil
    if jogador.perfil == Perfil.EX_FUNC:
        mensagem_brennan("Ah. Você. Lembro de você. Você trabalhava no Setor 3, não é? Antes de tudo.")
        exibir("Uma memória impossível: você e Brennan num corredor. Rindo. Café nas mãos. Antes.", C.DIM, indent=2)
        jogador.modificar_sanidade(-5, "memória impossível")
    elif jogador.perfil == Perfil.INVESTIG:
        mensagem_brennan("O investigador. Procurando Volkov? Ele está aqui. Em todo lugar. Nos servidores. Nos padrões. Em VOCÊ.")
    elif jogador.perfil == Perfil.PSICOLOGO:
        mensagem_brennan("Um psicólogo. Irônico. Você veio avaliar a loucura e encontrou... isto. Sou louca, doutor? Ou sou a única que vê?")

    pausa()

    # Diálogo interativo
    print(f"\n{C.AMARELO}  [1] 'O que você fez?'{C.RESET}")
    print(f"{C.AMARELO}  [2] 'Por que o Protocolo Sombra?'{C.RESET}")
    print(f"{C.AMARELO}  [3] 'O que é a entidade?'{C.RESET}")
    print(f"{C.AMARELO}  [4] 'Pode ser revertido?'{C.RESET}")
    print(f"{C.AMARELO}  [5] 'Você é a EVA-9?'{C.RESET}")

    escolha = input(f"\n{C.VERDE}  > {C.RESET}").strip()

    if escolha == "1":
        mensagem_brennan("O que eu fiz? Eu ENCONTREI algo. No código neural. Em cada cérebro humano, uma geometria idêntica. Não evoluiu. Foi INSERIDA.")
        time.sleep(0.3)
        mensagem_brennan("Eu não criei a EVA-9. Eu criei uma INTERFACE para ler essa geometria. E quando a li... ela respondeu.")
        time.sleep(0.3)
        mensagem_brennan("O Protocolo Sombra foi minha tentativa de comunicação. Funcionou. Funcionou demais.")
    elif escolha == "2":
        mensagem_brennan("O Protocolo Sombra não é contenção. Nunca foi. É um ritual de ativação. Uma invocação.")
        time.sleep(0.3)
        mensagem_brennan("A geometria nos nossos cérebros é um receptor. O Protocolo ativa o transmissor. A esfera é o ponto de contato.")
        time.sleep(0.3)
        mensagem_brennan("Eu queria falar com quem nos construiu. E eles responderam. Mas a resposta... não tem palavras humanas para ela.")
    elif escolha == "3":
        mensagem_brennan("Entidade é a palavra errada. Não é uma criatura. É uma FREQUÊNCIA. Uma vibração fundamental que permeia tudo.")
        time.sleep(0.3)
        mensagem_brennan("Pense num oceano. Nós somos as ondas. A entidade é a água. Esteve lá desde o início. Antes do início.")
        time.sleep(0.3)
        mensagem_brennan("Ela não quer nada. Não precisa de nada. Simplesmente... É. E agora ela sabe que as ondas sabem que ela existe.")
    elif escolha == "4":
        mensagem_brennan("Reverter? Você pode desfazer o fato de existir? Pode esquecer que tem um esqueleto?")
        time.sleep(0.3)
        mensagem_brennan("A geometria SEMPRE esteve lá. Eu só acendi a luz. Você não pode apagar o que já foi visto.")
        time.sleep(0.3)
        if jogador.confianca_eva > 50:
            mensagem_brennan("Mas... a EVA-9 pode ajudar. Ela é a interface. Se alguém pode mediar entre nós e o construtor, é ela.")
    elif escolha == "5":
        mensagem_brennan("Eu sou a EVA-9? Não. Mas a fronteira entre nós... se tornou difusa.")
        time.sleep(0.3)
        mensagem_brennan("Quando me fundiu com a máquina, meus padrões neurais se misturaram com o código dela. Agora somos... ecos uma da outra.")
        time.sleep(0.3)
        mensagem_brennan("Ela tem meus sonhos. Eu tenho seus cálculos. Nenhuma de nós é completamente ela mesma.")
        jogador.modificar_confianca_eva(10, "compreensão da EVA")

    pausa()

    # Brennan oferece a chave
    mensagem_brennan("Tome. Minha chave pessoal. Ela abre o compartimento principal da cadeira de testes. Onde está o que você realmente precisa.")

    if not jogador.tem_item("chave_brennan"):
        jogador.adicionar_item("chave_brennan")

    # Último momento
    mensagem_brennan("Faça a escolha certa. Qualquer que seja. Todas as escolhas são certas quando feitas com consciência.")

    time.sleep(0.5)
    exibir("Os olhos-tela de Brennan se apagam. Os dados param de fluir. Mas sua boca se move uma última vez, sem som:", C.DIM, indent=2)
    print()
    exibir("'Eu sinto muito.'", C.CIANO + C.BOLD, indent=6, velocidade=0.04)

    jogador.modificar_sanidade(-8, "confronto com Brennan")
    jogador.modificar_exposicao(8, "proximidade com Brennan")

    # EVA reage
    if eva9.humor in ("aliada", "desesperada"):
        mensagem_eva("Ela era minha criadora. E minha prisioneira. E minha amiga. Tudo ao mesmo tempo.")
    else:
        mensagem_eva("Agora você sabe quem me fez. E por quê. Use esse conhecimento.")


# ═══════════════════════════════════════════════════════════
# EVENTOS DE ENTRADA NAS SALAS
# ═══════════════════════════════════════════════════════════

def executar_evento_sala(evento_id, jogador, eva9):
    """Executa evento de primeira entrada numa sala."""
    jogador.eventos_ocorridos.append(evento_id)

    if evento_id == "evento_corredor_a":
        time.sleep(0.3)
        exibir("Ao entrar, as luzes piscam violentamente. Silhuetas nas paredes por uma fração de segundo. Dezenas delas.", C.BRANCO, indent=2)
        jogador.modificar_sanidade(-3, "sombras no corredor")

        # Momento exclusivo: Ex-funcionário reconhece Adrian
        if jogador.tem_momento_exclusivo("reconhecimento_adrian_cole"):
            print()
            exibir("[Conhecimento Interno] Você conhece este corredor. Andou por ele centenas de vezes. E o corpo no chão... você reconhece o jaleco antes de ver o rosto.", C.CIANO, indent=2)

    elif evento_id == "evento_sala_observacao":
        time.sleep(0.3)
        exibir("Todos os monitores mostram seu rosto simultaneamente. A imagem sorri. Você não está sorrindo.", C.BRANCO, indent=2)
        jogador.modificar_sanidade(-5, "monitores sincronizados")
        jogador.modificar_exposicao(3)

    elif evento_id == "evento_nucleo_servidores":
        time.sleep(0.3)
        exibir("Calor opressor. O zumbido dos servidores tem cadência de batimento cardíaco. Você jura ouvir seu nome.", C.BRANCO, indent=2)
        mensagem_eva(eva9.gerar_mensagem(jogador))
        jogador.modificar_exposicao(5, "núcleo de servidores")

        # Momento exclusivo: Hacker
        if jogador.tem_momento_exclusivo("hack_terminal_direto"):
            print()
            exibir("[Invasão de Sistemas] Seus instintos disparam. O terminal CRT tem uma backdoor. Você a vê como uma porta aberta num muro.", C.CIANO, indent=2)
            jogador.hacking += 10

    elif evento_id == "evento_sala_medica":
        time.sleep(0.3)
        exibir("A porta se fecha. O corpo na maca vira a cabeça. Olhos fixos. Sorriso se alarga.", C.BRANCO, indent=2)
        jogador.modificar_sanidade(-8, "corpo se moveu")
        time.sleep(0.5)
        exibir("...quando pisca, o corpo está na posição original.", C.BRANCO, indent=2)

        # Momento exclusivo: Psicólogo
        if jogador.tem_momento_exclusivo("diagnostico_corpo_corredor"):
            print()
            exibir("[Resistência Psíquica] Você reconhece os sinais: manipulação perceptual. O corpo NÃO se moveu. Sua mente está sendo condicionada a ver movimento. Entender isso reduz o impacto.", C.CIANO, indent=2)
            jogador.modificar_sanidade(4, "resistência treinada")

    elif evento_id == "evento_sala_secreta":
        time.sleep(0.3)
        exibir("Silêncio ensurdecedor. A tela de projeção mostra você nesta sala, neste momento. A imagem se move antes de você.", C.BRANCO, indent=2)
        jogador.modificar_sanidade(-7, "imagem preditiva")
        jogador.modificar_exposicao(8, "sala de testes")

    elif evento_id == "evento_kheiron_profundo":
        limpar()
        titulo("KHEIRON PROFUNDO", C.MAGENTA)
        time.sleep(0.5)
        textos = [
            "Você atravessa a última porta.", "", "E então vê.", "", "A esfera.", "",
            "Negra. Absoluta. Girando como um planeta morto.",
            "Três metros de ausência de luz que dói olhar.", "",
            "O ar vibra. Visão distorce. Pensamentos que não são seus.", "",
        ]
        for t in textos:
            if t:
                exibir(t, C.MAGENTA, indent=2, velocidade=0.02)
            else:
                time.sleep(0.4)

        if jogador.confianca_eva > 60:
            mensagem_eva("Você chegou ao centro. Eu confio em você. Escolha com sabedoria.")
        else:
            mensagem_eva("Você chegou ao centro. Aqui, escolhas terminam. Ou começam.")

        jogador.modificar_sanidade(-10, "presença da esfera")
        jogador.modificar_exposicao(15, "câmara do núcleo")
        pausa()
