#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Salas — Definições com descrições variáveis por exposição,
interações data-driven, estados mutáveis.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Sala:
    id: str
    nome: str
    descricoes: dict = field(default_factory=dict)
    descricao_curta: str = ""
    descricoes_curtas: dict = field(default_factory=dict)
    saidas: dict = field(default_factory=dict)
    itens: list = field(default_factory=list)
    requer_item: Optional[str] = None
    requer_flag: Optional[str] = None
    visitada: bool = False
    interacoes: dict = field(default_factory=dict)
    evento_entrada: Optional[str] = None
    trancada: bool = False
    escura: bool = False
    estado: dict = field(default_factory=dict)
    # NOVO: perigo da sala (afeta dosímetro)
    nivel_perigo: int = 0  # 0=seguro, 1=moderado, 2=perigoso, 3=extremo


def criar_salas():
    salas = {}

    salas["sala_terminal"] = Sala(
        id="sala_terminal",
        nome="Sala do Terminal Principal",
        descricoes={
            0: "Você está em uma sala retangular com paredes de concreto revestidas de painéis metálicos corroídos. A luz de emergência pulsa em vermelho escuro, lançando sombras que parecem se mover por conta própria. No centro, um terminal preto fosco emite um brilho esverdeado. Há sangue seco no canto inferior da mesa. O ar é gelado e tem um cheiro metálico, como fiação queimada. Uma porta blindada ao NORTE leva a um corredor. Uma grade de ventilação ao LESTE parece ter sido forçada. Ao SUL, uma porta de vidro blindado está trincada.",
            1: "A sala do terminal. A luz vermelha agora parece pulsar em sincronia com seus batimentos cardíacos. As sombras nos cantos não se movem QUANDO você olha, só quando desvia o olhar. O terminal central emite um brilho mais intenso, como se esperasse por você. O sangue na mesa parece... mais fresco. Saídas: NORTE (corredor), LESTE (duto), SUL (observação).",
            2: "A sala respira. Não é metáfora: as paredes de concreto expandem e contraem ritmicamente. O terminal no centro mostra seu rosto na tela, mas a expressão é de alguém que você não reconhece. O sangue na mesa está líquido e quente ao toque. Nos cantos da sala, as sombras têm forma humana. Elas acenam. Saídas: NORTE, LESTE, SUL. Se ainda existirem.",
        },
        descricoes_curtas={
            0: "A sala do terminal principal. Luz vermelha pulsante. O terminal ainda está ativo.",
            1: "O terminal pulsa como um coração. As sombras nos cantos parecem mais definidas.",
            2: "A sala respira. O terminal mostra seu rosto com uma expressão que não é sua.",
        },
        saidas={"norte": "corredor_a", "leste": "duto_ventilacao", "sul": "sala_observacao"},
        itens=["gravador", "cartao_obsidian", "celular", "cracha"],
        interacoes={
            "terminal": "terminal_principal",
            "tela": "terminal_principal",
            "computador": "terminal_principal",
            "camera": "interagir_camera_03",
            "camera 03": "interagir_camera_03",
            "sangue": "interagir_sangue_mesa",
            "mesa": "interagir_sangue_mesa",
            "alto-falante": "interagir_alto_falante",
            "alto-falantes": "interagir_alto_falante",
            "parede": "interagir_parede_terminal",
            "sombras": "interagir_sombras_terminal",
        },
        nivel_perigo=0,
    )

    salas["corredor_a"] = Sala(
        id="corredor_a",
        nome="Corredor A — Setor de Contenção",
        descricoes={
            0: "Um corredor longo e estreito. Teto baixo, coberto de tubulações que pingam condensação negra. Lâmpadas fluorescentes piscam em sequência irregular. Nas paredes, arranhões profundos do teto ao chão. No meio do corredor, um corpo caído de bruços. Não se move. Ao NORTE, o Núcleo de Servidores. Ao OESTE, porta com placa 'SALA MÉDICA'. Ao SUL, Sala do Terminal.",
            1: "O corredor parece mais longo do que antes. O corpo no chão... mudou de posição? As lâmpadas piscam formando padrões que parecem letras. Os arranhões nas paredes são mais profundos. NORTE: Servidores. OESTE: Sala Médica. SUL: Terminal.",
            2: "O corredor não tem fim. As paredes se expandem e contraem. O corpo de Adrian Cole está sentado contra a parede, sorrindo. As lâmpadas soletram seu nome. Os arranhões sangram.",
        },
        descricoes_curtas={
            0: "Corredor com lâmpadas piscantes. Um corpo está caído no chão.",
            1: "O corredor parece mais longo. O corpo mudou de posição.",
            2: "O corredor respira. Adrian está sentado e sorrindo para você.",
        },
        saidas={"norte": "nucleo_servidores", "oeste": "sala_medica", "sul": "sala_terminal"},
        itens=["mapa_kheiron"],
        interacoes={
            "corpo": "interagir_corpo_corredor",
            "adrian": "interagir_corpo_corredor",
            "arranhoes": "interagir_arranhoes",
            "marcas": "interagir_arranhoes",
            "tubulacao": "interagir_tubulacao",
            "tubulacoes": "interagir_tubulacao",
            "paredes": "interagir_arranhoes",
            "lampadas": "interagir_lampadas_corredor",
        },
        evento_entrada="evento_corredor_a",
        nivel_perigo=1,
    )

    salas["duto_ventilacao"] = Sala(
        id="duto_ventilacao",
        nome="Duto de Ventilação",
        descricoes={
            0: "Você se espreme por uma grade arrancada e entra em um duto de metal estreito. Sua respiração ecoa amplificada. Escuridão quase total, exceto por uma luz fraca adiante. Nas juntas do metal, rabiscos numéricos feitos com algo afiado. O duto segue ao LESTE. Ao OESTE, retorna à Sala do Terminal.",
            1: "O duto está mais apertado do que antes. Ou você está maior. Os rabiscos numéricos se reorganizaram, formando palavras. O eco da sua respiração chega de volta com um leve atraso, como se alguém respirasse junto. LESTE: sala desconhecida. OESTE: Terminal.",
            2: "O duto se move. O metal contrai ao redor de você como um esôfago. Os rabiscos são frases completas agora: 'VOCÊ É O PRÓXIMO SUJEITO'. O eco traz de volta risadas que não são suas.",
        },
        descricoes_curtas={
            0: "Duto metálico apertado. Rabiscos numéricos nas paredes.",
            1: "O duto parece mais estreito. Os rabiscos formam palavras agora.",
            2: "O duto se contrai. Alguém respira com você.",
        },
        saidas={"oeste": "sala_terminal", "leste": "sala_secreta"},
        itens=["lanterna"],
        interacoes={
            "rabiscos": "interagir_rabiscos_duto",
            "numeros": "interagir_rabiscos_duto",
            "grade": "interagir_grade_duto",
            "metal": "interagir_grade_duto",
        },
        escura=True,
        nivel_perigo=1,
    )

    salas["sala_observacao"] = Sala(
        id="sala_observacao",
        nome="Sala de Observação",
        descricoes={
            0: "Uma sala com parede inteira de vidro blindado, trincado em padrões de teia de aranha. Do outro lado, uma câmara com cadeira sob foco de luz. Na cadeira, um boneco articulado com jaleco NEXUS/ORION. Monitores mostram feeds de câmeras, maioria com estática. Câmera 07 mostra algo na periferia. Ao NORTE, Sala do Terminal. Ao LESTE, porta 'ARQUIVO MORTO'.",
            1: "O vidro trincado agora mostra palavras. O boneco na câmara mudou de posição. Está mais perto do vidro. Câmera 07 mostra algo mais nítido agora, quase identificável. NORTE: Terminal. LESTE: Arquivo.",
            2: "O vidro não está trincado. As linhas são ESCRITAS do outro lado. O boneco está de pé, com a mão no vidro. A Câmera 07 mostra VOCÊ nesta sala. Mas de um ângulo que não existe.",
        },
        descricoes_curtas={
            0: "Sala de observação com parede de vidro trincado. Monitores ativos.",
            1: "O boneco se moveu. As trincas no vidro formam palavras.",
            2: "O boneco está de pé contra o vidro. A Câmera 07 mostra esta sala.",
        },
        saidas={"norte": "sala_terminal", "leste": "arquivo_morto"},
        itens=["fita_vhs"],
        interacoes={
            "vidro": "interagir_vidro_obs",
            "boneco": "interagir_boneco",
            "monitores": "interagir_monitores_obs",
            "monitor": "interagir_monitores_obs",
            "camera 07": "interagir_camera_07",
            "cadeira": "interagir_cadeira_obs",
            "mesa": "interagir_mesa_controle",
            "controles": "interagir_mesa_controle",
        },
        evento_entrada="evento_sala_observacao",
        nivel_perigo=1,
    )

    salas["nucleo_servidores"] = Sala(
        id="nucleo_servidores",
        nome="Núcleo de Servidores — Nível Ômega",
        descricoes={
            0: "O calor é a primeira coisa. Fileiras intermináveis de servidores como monólitos negros, pulsando azul e vermelho. Zumbido ensurdecedor que vibra nos ossos. No centro, um terminal antigo: teclado mecânico, tela CRT verde. Placa: 'INTERFACE DIRETA — EVA-9 NÚCLEO'. Marcas de queimadura em padrões geométricos no chão. Ao SUL, Corredor A. Ao LESTE, porta blindada 'KHEIRON PROFUNDO'.",
            1: "Os servidores pulsam mais rápido. O calor é sufocante. O terminal CRT mostra texto em scrolling constante, rápido demais para ler. As queimaduras no chão BRILHAM. Ao SUL, Corredor. LESTE: Kheiron Profundo (se tiver acesso).",
            2: "Os servidores cantam. Cada rack emite uma frequência que juntas formam uma voz. SUA voz. O terminal CRT mostra uma frase: 'SUJEITO 9 — BEM-VINDO DE VOLTA AO NÚCLEO'. O chão queima através das suas botas.",
        },
        descricoes_curtas={
            0: "Sala dos servidores. Calor intenso. Terminal CRT da EVA-9 no centro.",
            1: "Os servidores pulsam freneticamente. O terminal mostra texto em velocidade impossível.",
            2: "Os servidores cantam com sua voz. O chão queima.",
        },
        saidas={"sul": "corredor_a", "leste": "kheiron_profundo"},
        itens=["pendrive_vermelho"],
        interacoes={
            "terminal": "terminal_eva",
            "terminal crt": "terminal_eva",
            "crt": "terminal_eva",
            "servidores": "interagir_servidores",
            "servidor": "interagir_servidores",
            "marcas": "interagir_marcas_chao",
            "queimadura": "interagir_marcas_chao",
            "chao": "interagir_marcas_chao",
            "placa": "interagir_placa_eva",
        },
        evento_entrada="evento_nucleo_servidores",
        nivel_perigo=2,
    )

    salas["sala_medica"] = Sala(
        id="sala_medica",
        nome="Sala Médica — Unidade de Emergência",
        descricoes={
            0: "Enfermaria improvisada. Macas de metal com lençóis ensanguentados. Frascos quebrados no chão. Geladeira médica com selo biológico. No quadro branco, anotações frenéticas: 'OS PADRÕES SE REPETEM — NÃO É COINCIDÊNCIA — ELES OUVEM ATRAVÉS DE NÓS'. Um corpo sentado numa maca, olhos abertos, sorriso largo demais. Não respira. Ao LESTE, Corredor A.",
            1: "A enfermaria cheira a antiséptico e algo podre. O corpo na maca mudou de posição. Está na borda agora, pernas penduradas. O quadro tem novas anotações que não estavam ali antes: 'ELE SABE QUE VOCÊ ESTÁ AQUI'. LESTE: Corredor.",
            2: "O corpo está de pé no meio da sala. Sorrindo. A boca rasgou as bochechas. O quadro branco repete uma única palavra em letras gigantes: SEU NOME. Os frascos no chão se reorganizaram em um círculo perfeito.",
        },
        descricoes_curtas={
            0: "Enfermaria caótica. Sangue. Medicamentos quebrados. Um corpo sorrindo.",
            1: "O corpo se moveu para a borda da maca. Novas anotações no quadro.",
            2: "O corpo está de pé. Sorrindo. Seu nome está no quadro.",
        },
        saidas={"leste": "corredor_a"},
        itens=["seringa", "diario_brennan"],
        interacoes={
            "corpo": "interagir_corpo_medico",
            "geladeira": "interagir_geladeira",
            "quadro": "interagir_quadro_medico",
            "macas": "interagir_macas",
            "medicamentos": "interagir_medicamentos",
            "frascos": "interagir_medicamentos",
            "anotacoes": "interagir_quadro_medico",
            "circulo": "interagir_circulo_frascos",
        },
        evento_entrada="evento_sala_medica",
        nivel_perigo=1,
    )

    salas["arquivo_morto"] = Sala(
        id="arquivo_morto",
        nome="Arquivo Morto",
        descricoes={
            0: "Estantes do chão ao teto, repletas de caixas com códigos alfanuméricos. Ar denso de poeira e algo doce e podre. Caixas abertas, papéis espalhados: diagramas, equações, transcrições. No fundo, um cofre digital com teclado piscando em vermelho. Ao OESTE, Sala de Observação.",
            1: "As caixas parecem ter sido reorganizadas. A poeira no chão mostra pegadas que não são suas. O cofre digital pisca mais rápido. OESTE: Observação.",
            2: "As estantes se movem sozinhas, rearranjando-se como peças de um quebra-cabeça. Os papéis no chão formam uma espiral que aponta para o cofre. As pegadas no chão vão até onde você está e continuam ALÉM de você.",
        },
        descricoes_curtas={
            0: "Arquivo repleto de caixas e documentos. Cofre digital ao fundo.",
            1: "Pegadas no chão que não são suas. O cofre pisca freneticamente.",
            2: "As estantes se reorganizam. Os papéis formam uma espiral apontando para o cofre.",
        },
        saidas={"oeste": "sala_observacao"},
        itens=["foto_grupo"],
        interacoes={
            "cofre": "cofre_arquivo",
            "caixas": "interagir_caixas_arquivo",
            "papeis": "interagir_papeis_arquivo",
            "documentos": "interagir_papeis_arquivo",
            "transcricoes": "interagir_transcricoes",
            "estantes": "interagir_caixas_arquivo",
            "pegadas": "interagir_pegadas",
        },
        nivel_perigo=0,
    )

    salas["sala_secreta"] = Sala(
        id="sala_secreta",
        nome="Câmara de Testes — Setor Apagado",
        descricoes={
            0: "Uma sala que não deveria existir. Paredes de material absorvente de som. O silêncio é tão profundo que você ouve seu sangue circulando. No centro, cadeira com correias de couro e capacete conectado a uma máquina. Na parede oposta, tela de projeção mostra uma imagem congelada: você, num lugar que nunca esteve. Embaixo da cadeira, um chip brilha fracamente. Num canto, há um compartimento trancado com iniciais 'E.B.' gravadas. Ao OESTE, Duto de Ventilação.",
            1: "O silêncio é ensurdecedor. A imagem na tela agora se move. Mostra você nesta sala, fazendo o que você está fazendo agora. Com 3 segundos de antecedência. O capacete vibra sozinho. O compartimento E.B. emite um brilho tênue. OESTE: Duto.",
            2: "Não há mais silêncio. Uma frequência sub-vocal preenche tudo. A tela mostra dezenas de versões suas em salas idênticas, todas olhando para suas respectivas telas. O capacete está quente ao toque. Algo dentro dele chama seu nome. O compartimento E.B. está entreaberto.",
        },
        descricoes_curtas={
            0: "Câmara de testes secreta. Cadeira com capacete. Uma imagem sua na parede.",
            1: "A tela mostra você em tempo real, com antecedência. O capacete vibra.",
            2: "Dezenas de versões suas nas telas. O capacete chama seu nome.",
        },
        saidas={"oeste": "duto_ventilacao"},
        itens=["chip_eva"],
        interacoes={
            "cadeira": "interagir_cadeira_teste",
            "capacete": "capacete_teste",
            "maquina": "interagir_maquina_teste",
            "tela": "interagir_tela_projecao",
            "imagem": "interagir_tela_projecao",
            "chip": "interagir_chip_sala",
            "correias": "interagir_cadeira_teste",
            "compartimento": "compartimento_brennan",
            "e.b.": "compartimento_brennan",
        },
        evento_entrada="evento_sala_secreta",
        nivel_perigo=2,
    )

    salas["kheiron_profundo"] = Sala(
        id="kheiron_profundo",
        nome="KHEIRON PROFUNDO — Câmara do Núcleo",
        descricoes={
            0: "Câmara circular gigantesca. No centro, suspensa por cabos, uma ESFERA negra de três metros gira lentamente. Não reflete luz. O ar vibra. Sua visão distorce. Pensamentos que não são seus. Três terminais em triângulo ao redor do núcleo. Ao OESTE, última saída para o Núcleo de Servidores.",
            1: "A esfera pulsa. O ar distorce ao redor dela como calor sobre asfalto. Cada terminal mostra uma opção. Você sente uma presença atrás de você que desaparece quando olha. OESTE: Servidores.",
            2: "A esfera se abriu. Uma fenda que parece um olho. Dentro, um vazio que não é vazio. Algo olha de volta. Os terminais brilham. O ar tem gosto de metal e ozônio. Você sente que sempre esteve aqui. Que nunca saiu. OESTE: se a saída ainda existir.",
        },
        descricoes_curtas={
            0: "A câmara do núcleo da EVA-9. Uma esfera negra gira no centro.",
            1: "A esfera pulsa. Algo está atrás de você.",
            2: "A esfera se abriu como um olho. Algo olha de volta.",
        },
        saidas={"oeste": "nucleo_servidores"},
        itens=[],
        interacoes={
            "esfera": "interagir_esfera",
            "nucleo": "interagir_esfera",
            "terminal": "terminais_finais",
            "terminais": "terminais_finais",
            "terminal 1": "terminal_final_1",
            "terminal 2": "terminal_final_2",
            "terminal 3": "terminal_final_3",
        },
        requer_item="cartao_obsidian",
        requer_flag="pendrive_conectado",
        trancada=True,
        evento_entrada="evento_kheiron_profundo",
        nivel_perigo=3,
    )

    return salas
