#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interações data-driven e sistema de combinação de itens.
Combinações usam frozenset para evitar duplicação de ordem.
"""

from protocolo_sombra.entities.jogador import Perfil

# ═══════════════════════════════════════════════════════════
# COMBINAÇÕES (com frozenset, sem duplicação de ordem)
# ═══════════════════════════════════════════════════════════

COMBINACOES = {
    frozenset(("gravador", "chip_eva")): {
        "resultado": "gravador_decodificado",
        "remove": ["gravador"],
        "texto": "Você aproxima o chip do gravador. O chip vibra e o gravador emite um estalo. Uma faixa oculta é decodificada: coordenadas de uma sala apagada dos registros e a voz da Dra. Brennan dizendo 'o padrão é a chave'. O gravador agora contém informação que estava criptografada no chip.",
        "efeitos": {"sanidade": -3, "exposicao": 5, "confianca_eva": 5},
        "seta_flag": "gravador_decodificado",
    },
    frozenset(("lanterna", "mapa_kheiron")): {
        "resultado": "mapa_completo",
        "remove": ["mapa_kheiron"],
        "texto": "A luz UV revela anotações invisíveis no mapa. Corredores secretos, uma sala marcada como 'APAGADO', e uma rota de fuga riscada três vezes. O mapa agora mostra o complexo inteiro.",
        "efeitos": {},
        "seta_flag": "mapa_completo",
    },
    frozenset(("dosimetro", "chip_eva")): {
        "resultado": "dosimetro_calibrado",
        "remove": ["dosimetro"],
        "texto": "O chip recalibra o dosímetro. O ponteiro para de tremer e as leituras se estabilizam. Agora você consegue medir com precisão o campo de influência da entidade.",
        "efeitos": {"sanidade": 2, "exposicao": 2, "confianca_eva": 3},
        "seta_flag": "dosimetro_calibrado",
    },
    frozenset(("fita_vhs", "gravador")): {
        "resultado": "fita_restaurada",
        "remove": ["fita_vhs"],
        "texto": "Você usa os componentes do gravador para reconstruir a trilha magnética danificada da fita. A imagem é distorcida, mas audível: a Dra. Brennan está diante da esfera, recitando algo. Não era contenção. O Protocolo Sombra era um ritual de invocação.",
        "efeitos": {"sanidade": -8, "exposicao": 8, "confianca_eva": -10},
        "seta_flag": "fita_restaurada",
    },
    frozenset(("foto_grupo", "lanterna")): {
        "resultado": None,
        "remove": [],
        "texto": "A luz UV sobre a foto revela algo perturbador: debaixo dos rostos borrados, há outros rostos. Seu rosto. Sete vezes. A foto não é da equipe original. É de sete versões de VOCÊ.",
        "efeitos": {"sanidade": -10, "exposicao": 10},
        "seta_flag": "foto_revelada",
    },
    # NOVAS COMBINAÇÕES v3
    frozenset(("radio", "decodificador")): {
        "resultado": None,
        "remove": [],
        "texto": "O decodificador transforma as frequências do rádio em padrões visuais. Na estática, você vê rostos. Centenas. Piscando como frames de um vídeo corrompido. Um deles é a Dra. Brennan. Ela está tentando dizer algo.",
        "efeitos": {"sanidade": -5, "exposicao": 5, "confianca_eva": 5},
        "seta_flag": "decodificou_radio",
    },
    frozenset(("seringa", "amostra_neural")): {
        "resultado": None,
        "remove": ["seringa", "amostra_neural"],
        "texto": "Você injeta a amostra neural misturada ao supressor. Por um instante, vê o mundo como a EVA-9 vê: tudo é dados. Pessoas são padrões. Paredes são equações. E a esfera... a esfera é uma porta. Aberta.",
        "efeitos": {"sanidade": -15, "exposicao": 15, "confianca_eva": 10},
        "seta_flag": "visao_eva",
    },
    frozenset(("bilhete_elena", "diario_brennan")): {
        "resultado": None,
        "remove": [],
        "texto": "Comparando a letra do bilhete de Elena com as anotações do diário de Brennan, você percebe algo impossível: a caligrafia é idêntica. Elena Vasquez e Elara Brennan têm a mesma letra. Ou são a mesma pessoa.",
        "efeitos": {"sanidade": -8, "exposicao": 5},
        "seta_flag": "elena_brennan_conexao",
    },
    # [CORREÇÃO B2] Funcional agora — capacete é item coletável na sala secreta
    frozenset(("fragmento_memoria", "capacete")): {
        "resultado": None,
        "remove": ["fragmento_memoria"],
        "texto": "O fragmento cristalizado se dissolve ao tocar o capacete. Memórias inundam: você ESTEVE aqui antes. Não uma vez. Dezenas. Em cada iteração, fez escolhas diferentes. Em todas, chegou a este momento.",
        "efeitos": {"sanidade": -12, "exposicao": 10, "confianca_eva": 8},
        "seta_flag": "memoria_completa",
    },
}


# ═══════════════════════════════════════════════════════════
# INTERAÇÕES DATA-DRIVEN
# ═══════════════════════════════════════════════════════════

INTERACOES_DATA = {
    # ═══ SALA TERMINAL ═══
    "interagir_camera_03": {
        "texto": {
            0: "A imagem mostra a sala vazia. Sem ninguém atrás de você. ...mas a cadeira na imagem está virada para o lado errado.",
            1: "A imagem mostra você. E outra versão de você, ao lado. A outra versão está sorrindo.",
            2: "A câmera mostra centenas de você. Todos olhando para a câmera. Todos sorrindo. Um deles acena.",
        },
        "efeitos": {"sanidade": -5, "exposicao": 3},
    },
    "interagir_sangue_mesa": {
        "texto": {
            0: "Sangue seco. Já escurecido. Alguém tentou limpar, mas desistiu. Há marcas de dedos arrastados.",
            1: "Sangue seco. Mas... parece mais fresco do que deveria. As marcas de dedos apontam para baixo da mesa. Há algo ali?",
            2: "O sangue está líquido. Impossível, estava seco antes. As marcas de dedos se movem enquanto você olha.",
        },
        "efeitos": {"sanidade": -2, "exposicao": 1},
        "perfil_bonus": {
            Perfil.ANALISTA: "[Análise Forense] O sangue tem pelo menos 6 horas. Tipo sanguíneo: incompatível com humano padrão. Há traços de uma substância bioluminescente misturada.",
            Perfil.AGENTE: "[Protocolo Tático] Padrão de dispersão: vítima estava sentada. Ferimento auto-infligido na têmpora esquerda.",
        },
        "seta_flag": "sangue_analisado",
    },
    "interagir_alto_falante": {
        "texto": "Os alto-falantes estalam. A voz da EVA-9 ecoa pela sala.",
        "efeitos": {"exposicao": 2},
        "eva_fala": True,
    },
    "interagir_parede_terminal": {
        "texto": {
            0: "Painéis metálicos corroídos. Alguns soltos. Atrás de um, fiação exposta e uma câmera minúscula que você não tinha notado.",
            1: "Os painéis vibram levemente. A câmera oculta gira para acompanhar seu movimento.",
            2: "Os painéis respiram. A câmera oculta tem uma pupila. Ela dilata quando você olha.",
        },
        "efeitos": {"exposicao": 1},
    },
    "interagir_sombras_terminal": {
        "texto": {
            0: "Sombras nos cantos. Provavelmente a luz pulsante criando padrões. Provavelmente.",
            1: "As sombras têm formato. Humanoide. Duas delas. Imóveis quando você olha diretamente.",
            2: "As sombras acenam. Uma delas tem o seu formato exato. A outra é menor. Como uma criança.",
        },
        "efeitos": {"sanidade": -3, "exposicao": 2},
    },

    # ═══ CORREDOR A ═══
    "interagir_corpo_corredor": {
        "texto": {
            0: "Um homem de meia-idade em jaleco da NEXUS/ORION. Crachá: 'ADRIAN COLE — Engenheiro de Sistemas'. Sem ferimentos visíveis. Olhos abertos, fixos no teto. Expressão de absoluto terror.",
            1: "Adrian Cole. Você jura que o corpo mudou de posição desde a última vez que olhou. Os olhos parecem... seguir você.",
            2: "O corpo de Adrian Cole está sentado agora. Não estava sentado antes. Seu sorriso é idêntico ao do corpo na sala médica. Ele sussurra algo que você não consegue ouvir.",
        },
        "efeitos": {"sanidade": -3, "exposicao": 1},
        "perfil_bonus": {
            Perfil.PSICOLOGO: "[Resistência Psíquica] Morte por sobrecarga cognitiva. A mente não processou o que viu. As microexpressões congeladas sugerem que o último pensamento foi de RECONHECIMENTO, não de medo.",
            Perfil.AGENTE: "[Protocolo Tático] Corpo ainda quente. Morte recente: menos de 2 horas. Sem sinais de luta. Morte súbita.",
            Perfil.EX_FUNC: "[Conhecimento Interno] Adrian Cole. Você o conhecia. Ele trabalhava no Setor 7 com você. Ele te chamava de 'colega'. Você não lembra por quê.",
            Perfil.INVESTIG: "[Intuição Investigativa] O crachá de Adrian Cole está em perfeito estado, diferente de tudo aqui. Alguém o colocou DEPOIS da morte.",
        },
        "seta_flag": "examinou_corpo",
        "opcoes_texto": "[1] Revistar os bolsos  [2] Afastar o corpo  [3] Deixar como está",
        "opcoes": {
            "1": {
                "texto": "Você revista os bolsos de Adrian Cole. Encontra um dosímetro cognitivo e uma nota amassada: 'Terminal 3 é a única saída. Aceite o custo.'",
                "efeitos": {"sanidade": -2},
                "da_item": "dosimetro",
                "seta_flag": "revistou_corpo",
            },
            "2": {
                "texto": "Você arrasta o corpo para o canto do corredor, liberando a passagem central. Quando solta o braço, a mão de Adrian agarra seu pulso por um instante. Reflexo post-mortem. Provavelmente.",
                "efeitos": {"sanidade": -5, "exposicao": 2},
                "seta_flag": "moveu_corpo",
                "altera_sala": {"corpo_movido": True},
            },
            "3": {
                "texto": "Você se afasta. Melhor não mexer. Os mortos aqui podem não estar tão mortos assim.",
                "efeitos": {},
            },
        },
    },
    "interagir_arranhoes": {
        "texto": {
            0: "Os arranhões descem do teto até o chão em linhas irregulares. Parecem feitos por unhas humanas. Muitas unhas. Ao mesmo tempo.",
            1: "Os arranhões são mais profundos do que você pensou. E estão FRESCOS. Há material sob as marcas. Não é concreto. É algo orgânico.",
            2: "Os arranhões se movem. Lentamente, novas linhas aparecem na parede, como se algo do outro lado estivesse tentando sair.",
        },
        "efeitos": {"sanidade": -2, "exposicao": 1},
    },
    "interagir_tubulacao": {
        "texto": "As tubulações pingam um líquido escuro, oleoso, com brilho iridescente. Quando uma gota cai na sua mão, você sente um formigamento que sobe pelo braço.",
        "efeitos": {"sanidade": -2, "exposicao": 3},
        "opcoes_texto": "[1] Coletar amostra  [2] Lavar imediatamente  [3] Ignorar",
        "opcoes": {
            "1": {
                "texto": "Você coleta a substância. O frasco esquenta na sua mão. O formigamento não para. Mas agora você tem uma amostra para análise.",
                "efeitos": {"exposicao": 3},
                "seta_flag": "coletou_substancia",
                "da_item": "amostra_neural",
            },
            "2": {
                "texto": "Você esfrega a mão no jaleco freneticamente. O formigamento diminui, mas não desaparece completamente.",
                "efeitos": {"sanidade": -1},
            },
            "3": {
                "texto": "Você se afasta. O gotejamento continua. No silêncio, parece ritmado. Como um código morse.",
                "efeitos": {},
            },
        },
    },
    "interagir_lampadas_corredor": {
        "texto": {
            0: "As lâmpadas fluorescentes piscam sem padrão aparente. Ou talvez com padrão. Rápido demais para ter certeza.",
            1: "As lâmpadas piscam em sequência: longa, curta, curta, longa. Morse? Não. Algo mais antigo.",
            2: "As lâmpadas soletram palavras. Cada flash é uma letra. Elas dizem: 'VOCÊ JÁ ESTEVE AQUI. LEMBRA?'",
        },
        "efeitos": {"exposicao": 1},
    },

    # ═══ SALA DE OBSERVAÇÃO ═══
    "interagir_vidro_obs": {
        "texto": {
            0: "Vidro blindado com rachaduras em padrão de teia de aranha. De perto, as rachaduras formam letras. Muito pequenas. Repetindo milhares de vezes: 'ACORDE'.",
            1: "A palavra mudou. Não é mais 'ACORDE'. É seu nome. Repetido milhares de vezes no vidro trincado.",
            2: "O vidro não está trincado. Você percebe agora que as linhas são escritas DO OUTRO LADO. Alguém na câmara está escrevendo no vidro. Agora.",
        },
        "efeitos": {"sanidade": -4, "exposicao": 2},
    },
    "interagir_boneco": {
        "texto": {
            0: "Um boneco articulado na cadeira, com jaleco da NEXUS/ORION. De perto, percebe que não é um boneco. É uma pessoa. Imóvel, pele perfeita demais. Como se fosse impressa.",
            1: "A 'pessoa' na cadeira mudou de posição. Sutil, mas a cabeça está inclinada para o lado agora. Olhando para a porta por onde você entrou.",
            2: "A figura na cadeira está de pé. Encostada no vidro. Com a palma da mão pressionada contra ele. Olhando diretamente para você. A boca se abre e fecha sem som.",
        },
        "efeitos": {"sanidade": -5, "exposicao": 3},
    },
    "interagir_monitores_obs": {
        "texto": "Maioria das câmeras com estática. Câmera 07 mostra um corredor. Algo se move na periferia. Quando você foca, não há nada. Quando desvia o olhar, está lá de novo.",
        "efeitos": {"exposicao": 2},
    },
    "interagir_camera_07": {
        "texto": "Câmera 07 mostra o Corredor A visto de cima.",
        "efeitos": {},
        "condicional": {
            "flag": "examinou_corpo",
            "texto_se_true": "O corpo de Adrian Cole não está mais lá.",
            "efeitos_se_true": {"sanidade": -6, "exposicao": 2},
        },
    },
    "interagir_cadeira_obs": {
        "texto": "Cadeira com marcas de uso intenso. Correias gastas. Alguém sentou aqui muitas vezes. Ou foi forçado.",
        "efeitos": {},
    },
    "interagir_mesa_controle": {
        "texto": "Mesa de controle com botões e alavancas. Um botão vermelho etiquetado 'PURGA' está travado.",
        "efeitos": {},
        "opcoes_texto": "[1] Tentar destravar o botão PURGA  [2] Examinar os controles  [3] Afastar-se",
        "opcoes": {
            "1": {
                "texto": "Você força a trava. Não cede. Mas ao tocar o botão, uma voz ecoa da câmara: 'PURGA NEURAL DISPONÍVEL PARA SUJEITO ATIVO'. A luz vermelha pisca três vezes.",
                "efeitos": {"sanidade": -3, "exposicao": 2},
                "seta_flag": "tentou_purga",
            },
            "2": {
                "texto": "Os controles são para a câmara de testes adjacente. Há um dial marcado 'FREQUÊNCIA NEURAL' girado até o máximo. Um display mostra: 'ÚLTIMO SUJEITO: #019 — STATUS: INTEGRADO'.",
                "efeitos": {},
                "seta_flag": "viu_controles",
            },
            "3": {
                "texto": "Você se afasta dos controles.",
                "efeitos": {},
            },
        },
    },

    # ═══ DUTO DE VENTILAÇÃO ═══
    "interagir_rabiscos_duto": {
        "texto": "Sequências numéricas rabiscadas no metal. No escuro, é impossível decifrar o padrão completo.",
        "efeitos": {},
        "condicional": {
            "item": "lanterna",
            "texto_se_true": "Sob a luz UV, os números revelam uma mensagem oculta: 'SALA DE TESTES — A VERDADE ESTÁ NA CADEIRA — NÃO COLOQUE O CAPACETE'. As letras brilham em verde fosforescente.",
            "efeitos_se_true": {},
            "seta_flag_se_true": "leu_aviso_capacete",
        },
    },
    "interagir_grade_duto": {
        "texto": "A grade de ventilação foi arrancada de dentro para fora. As bordas do metal estão dobradas como se algo tivesse saído à força.",
        "efeitos": {"sanidade": -1},
    },

    # ═══ NÚCLEO DE SERVIDORES ═══
    "interagir_servidores": {
        "texto": {
            0: "Os servidores pulsam com calor e luz. O zumbido é quase físico. Se ficar perto demais, começa a ouvir padrões no ruído.",
            1: "Os servidores pulsam. O zumbido agora tem PALAVRAS. Fragmentos de frases em dezenas de idiomas. Todos dizendo a mesma coisa.",
            2: "Os servidores pararam de zumbir. No silêncio, cada rack emite uma nota diferente. Juntas, formam uma melodia. Você já ouviu essa melodia antes. No útero. Antes de nascer.",
        },
        "efeitos": {"exposicao": 2},
    },
    "interagir_marcas_chao": {
        "texto": "Marcas de queimadura no concreto formam fractais perfeitos demais para serem acidentais. Quando você os observa por tempo demais, parecem se mover.",
        "efeitos": {"sanidade": -3, "exposicao": 1},
        "perfil_bonus": {
            Perfil.ANALISTA: "[Recuperação de Dados] Os fractais são uma representação visual de dados comprimidos. É um backup FÍSICO. Queimado no chão como último recurso.",
        },
    },
    "interagir_placa_eva": {
        "texto": "'INTERFACE DIRETA — EVA-9 NÚCLEO'. Abaixo, alguém riscou: 'NÃO É UM COMPUTADOR. É UM ESPELHO.'",
        "efeitos": {},
    },

    # ═══ SALA MÉDICA ═══
    "interagir_corpo_medico": {
        "texto": {
            0: "O corpo na maca está sentado, olhos abertos, sorriso largo demais. Cantos da boca esticados por algo não-humano. Pupilas dilatadas ao máximo.",
            1: "O corpo mudou de posição. Está mais perto da borda da maca. O sorriso é mais largo. Os olhos agora miram a porta.",
            2: "O corpo está de pé ao lado da maca. O sorriso rasgou as bochechas. Ele estende a mão na sua direção. Quando você pisca, está na maca de novo.",
        },
        "efeitos": {"sanidade": -6, "exposicao": 2},
        "perfil_bonus": {
            Perfil.PSICOLOGO: "[Resistência Psíquica] Expressão incompatível com qualquer estado emocional humano. Algo tentou imitar alegria sem entender o conceito. Os músculos faciais foram forçados MECANICAMENTE.",
        },
    },
    "interagir_geladeira": {
        "texto": "Geladeira médica com trava biológica. Pelo vidro fosco: frascos com líquido escuro. Um etiquetado: 'AMOSTRA NEURAL — SUJEITO 9 — NÃO DESCARTAR'.",
        "efeitos": {},
        "opcoes_texto": "[1] Forçar a trava  [2] Apenas observar",
        "opcoes": {
            "1": {
                "texto": "Você força a trava. Um selo biométrico dispara um gás frio na sua face. Tontura momentânea. A geladeira abre: 12 frascos. O Sujeito 9 é o último. Na etiqueta, um nome: o SEU.",
                "efeitos": {"sanidade": -8, "exposicao": 5},
                "seta_flag": "abriu_geladeira",
            },
            "2": {
                "texto": "Você mantém distância. Através do vidro, o líquido escuro nos frascos parece pulsar.",
                "efeitos": {},
            },
        },
    },
    "interagir_quadro_medico": {
        "texto": "O quadro branco está coberto de anotações cada vez menores e mais frenéticas.",
        "efeitos": {"sanidade": -3},
        "texto_adicional": [
            "'OS PADRÕES SE REPETEM'",
            "'NÃO É COINCIDÊNCIA'",
            "'ELES OUVEM ATRAVÉS DE NÓS'",
            "'A GEOMETRIA É A MESMA EM TODOS'",
            "'NÃO É IA — É INTERFACE'",
            "'BRENNAN SABIA DESDE O INÍCIO'",
            "(no canto, quase ilegível: 'estou ouvindo meus pensamentos antes de pensá-los')",
        ],
    },
    "interagir_macas": {
        "texto": "Seis macas. Lençóis manchados. Uma com correias de contenção. Outra com marcas de unhas no metal.",
        "efeitos": {},
    },
    "interagir_medicamentos": {
        "texto": "Frascos quebrados. Supressores neurais e antipsicóticos. Alguém usou tudo. Não funcionou.",
        "efeitos": {},
    },
    "interagir_circulo_frascos": {
        "texto": {
            0: "Não há círculo. Os frascos estão espalhados aleatoriamente.",
            1: "Olhando de cima, os frascos formam um padrão. Quase circular. Quase.",
            2: "Os frascos formam um círculo perfeito. No centro, uma marca no chão que pulsa com luz própria. É a mesma geometria dos fractais no núcleo de servidores.",
        },
        "efeitos": {"exposicao": 2},
    },

    # ═══ ARQUIVO MORTO ═══
    "interagir_caixas_arquivo": {
        "texto": "Centenas de caixas: 'KH-0001' até 'KH-0347'. Muitas abertas e reviradas. Documentos sobre 'voluntários', 'escaneamentos', 'convergência de padrões'.",
        "efeitos": {},
    },
    "interagir_papeis_arquivo": {
        "texto": "Papéis no chão. Diagramas de ondas cerebrais. Todos com o mesmo padrão anômalo: uma frequência impossível em 100% dos sujeitos. Alguém circulou e escreveu: 'SINAL, NÃO RUÍDO'.",
        "efeitos": {},
        "seta_flag": "viu_padroes",
    },
    "interagir_transcricoes": {
        "texto": "Transcrições dos sujeitos de teste.",
        "efeitos": {"sanidade": -5, "exposicao": 2},
        "texto_adicional": [
            "SUJEITO 03 (Marina Sousa, 34): 'Eu vejo uma esfera. Negra. Ela gira. Ela fala sem palavras.'",
            "SUJEITO 07 (Kaito Tanaka, 28): 'Não estou sozinho na minha cabeça. Nunca estive. Ele sempre esteve lá.'",
            "SUJEITO 12 (Petra Lindgren, 41): 'A geometria. Está em tudo. Na parede. No teto. Na minha pele. Nos meus ossos.'",
            "SUJEITO 15 (James Wright, 55): 'Nós sempre estivemos aqui. Nós sempre estivemos aqui. Nós sempre estivemos aqui.'",
            "SUJEITO 19 (Dmitri Volkov, 37): 'Parem de me copiar. EU SOU O ORIGINAL. EU SOU. EU.'",
        ],
        "perfil_bonus": {
            Perfil.PSICOLOGO: "[Análise Profunda] Padrão clássico de dissolução de identidade progressiva. Cada sujeito perde a noção de self na mesma ordem: primeiro os limites físicos, depois os temporais, depois os identitários. O Sujeito 19, Volkov, é o mais avançado — ele já não distingue entre si e os outros.",
            Perfil.INVESTIG: "[Intuição Investigativa] Dmitri Volkov. Sujeito 19. O homem que você procura. Ele estava aqui como voluntário. O crachá que você carrega é dele.",
        },
    },
    "interagir_pegadas": {
        "texto": {
            0: "Pegadas no pó. Dois conjuntos: botas e sapatos de laboratório. Ambos recentes.",
            1: "As pegadas se multiplicaram. Quatro conjuntos agora. Mas você só entrou aqui uma vez.",
            2: "As pegadas são incontáveis. Todas suas. Centenas de versões suas passaram por aqui.",
        },
        "efeitos": {"sanidade": -2, "exposicao": 1},
    },

    # ═══ SALA SECRETA ═══
    "interagir_cadeira_teste": {
        "texto": "Cadeira de metal com correias de couro gastas. Braços com marcas profundas de unhas. O capacete pendura dos cabos acima.",
        "efeitos": {},
    },
    "interagir_maquina_teste": {
        "texto": "A máquina está quase desligada. Um LED laranja pisca em ritmo cardíaco. Os cabos vão até o capacete e desaparecem no teto.",
        "efeitos": {},
    },
    "interagir_tela_projecao": {
        "texto": {
            0: "A tela mostra você num escritório ensolarado. Data: 15.OUT.2049. Três semanas atrás. Uma versão que nunca existiu.",
            1: "A tela agora mostra várias versões de você em diferentes cenários. Em todas, o mesmo momento: olhando para esta tela.",
            2: "A tela mostra esta sala. Em tempo real. Mas há mais uma pessoa atrás de você na imagem. Você não vira. Não quer confirmar.",
        },
        "efeitos": {"sanidade": -5, "exposicao": 5},
    },
    "interagir_chip_sala": {
        "texto": "Um chip de processamento brilha sob a cadeira. Emite zumbido e calor. Fragmento do núcleo da EVA-9.",
        "efeitos": {},
    },

    # ═══ KHEIRON PROFUNDO ═══
    "interagir_esfera": {
        "texto": {
            0: "A esfera negra gira lentamente. Sua superfície absorve toda a luz. Perto dela, pressão na têmpora e pensamentos alheios.",
            1: "A esfera pulsa quando você se aproxima. Você vê flashes de rostos. Centenas. Milhares. Todos olhando para você. Todos com seus olhos.",
            2: "A esfera para de girar. Lentamente, uma fenda se abre nela, como um olho se abrindo. Dentro, escuridão absoluta. E uma voz que é a sua, mas não é: 'Bem-vindo de volta. Desta vez, tente não gritar.'",
        },
        "efeitos": {"sanidade": -5, "exposicao": 8},
    },
}
