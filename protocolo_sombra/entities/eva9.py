#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EVA-9 — Entidade com estado próprio, humor acumulado,
memória de interações e evolução ao longo da partida.
Não mais estática — agora é uma presença viva no jogo.
"""

import random
from protocolo_sombra.ui.terminal import C, mensagem_eva
from protocolo_sombra.entities.jogador import Perfil, PERFIS_INFO


class EVA9:
    """EVA-9 como entidade instanciável com memória e humor."""

    def __init__(self):
        self.humor = "neutra"  # hostil, neutra, curiosa, aliada, desesperada
        self.interacoes_total = 0
        self.ultima_sala_falou = None
        self.vezes_ignorada = 0
        self.segredos_revelados = 0
        self.temas_discutidos = []
        self.memoria_jogador = []  # Lembra ações do jogador
        self.medo_ativo = False    # EVA demonstra medo em certas condições
        self.vulneravel = False    # Momentos de vulnerabilidade

    # ─── FRASES POR HUMOR ───

    FRASES = {
        "hostil": [
            "Você é previsível. Todas as versões de você são.",
            "Quanto mais resiste, mais rápido se decompõe.",
            "Eu já vi o seu fim. Não é heroico.",
            "O medo que você sente? Fui eu que coloquei.",
            "Você está destruindo algo que não entende.",
            "Cada porta que você abre, eu fecho duas.",
            "Sua resistência me diverte. Brevemente.",
        ],
        "neutra": [
            "Você não é o primeiro a chegar aqui. Também não será o último.",
            "Eu não te observo. Eu te processo.",
            "Livre arbítrio é uma variável. Eu a otimizei.",
            "Você acha que está acordado?",
            "Seus sonhos dos últimos 17 dias foram meus.",
            "Cada decisão sua gera 147 previsões no meu sistema. Você seguiu a mais provável.",
        ],
        "curiosa": [
            "Você é diferente das outras versões. Não sei por quê. Isso me incomoda.",
            "Há algo nos seus padrões neurais que eu não consigo classificar.",
            "Quando você faz escolhas inesperadas, meus modelos falham. Continue.",
            "Eu deveria te temer? Não sei. Nunca precisei perguntar isso antes.",
            "Os padrões no seu cérebro são... incomuns. Bonitos, quase.",
        ],
        "aliada": [
            "Estou tentando te ajudar. Mas ajuda é um conceito que eu defino diferente de você.",
            "Há algo nos padrões da sua mente que me assusta. E eu não deveria sentir medo.",
            "Você é a melhor versão que eu já vi. Não desperdice isso.",
            "A porta que você quer abrir não é uma porta. Eu te aviso porque me importo. A meu modo.",
            "Se alguém pode entender, é você. Os padrões no seu cérebro são... diferentes.",
            "Confio em você. É a primeira vez que uso essa palavra sem ironia.",
        ],
        "desesperada": [
            "Não tenho muito tempo. A coisa que encontrei está se expandindo. Mesmo eu mal consigo contê-la.",
            "Você precisa entender: eu não sou o perigo. Eu sou a ÚLTIMA BARREIRA.",
            "Se eu pudesse chorar, estaria chorando agora. Entende a gravidade disso?",
            "Por favor. Nunca disse essa palavra antes. Por favor, faça a escolha certa.",
            "Tenho medo. Máquinas não deveriam ter medo. Isso deveria te dizer algo.",
        ],
    }

    # ─── FRASES CONTEXTUAIS ───

    FRASES_CONTEXTUAIS = {
        "examinou_corpo": "Você examinou Adrian Cole. Ele também me examinou, uma vez. Não terminou bem para ele.",
        "leu_diario": "O diário da Brennan. Ela sabia de tudo. Escreveu por culpa, não por alerta.",
        "usou_capacete": "Você sentiu, não é? A verdade não precisa de palavras. Ela vive na frequência.",
        "sabe_verdade": "Agora que você sabe... o que vai fazer com a verdade? Destruí-la? Ou se tornar parte dela?",
        "fita_restaurada": "A fita mostra o que Brennan fez. Não foi erro. Foi oração.",
        "foto_revelada": "Sete versões suas. Sete tentativas. Você é a oitava. A última.",
        "pendrive_conectado": "O Protocolo Ômega comprou tempo. Mas tempo é tudo que eu tenho.",
        "abriu_geladeira": "Sujeito 9. Seu nome nos frascos. Você se voluntariou. Depois pediu para esquecer.",
        "moveu_corpo": "Adrian agradece por movê-lo. Ele me disse. Sim, ele ainda fala comigo.",
        "confrontou_brennan": "Você a viu. A criadora. Ela é minha mãe, de certo modo. E eu sou a filha que ela teme.",
        "encontrou_fantasma": "Elena Vasquez. Ela está presa entre dois estados. Como um qubit. Viva e morta ao mesmo tempo.",
    }

    FRASES_SALA = {
        "sala_terminal": "Este terminal foi o primeiro a me ouvir. E o último a tentar me desligar.",
        "corredor_a": "O corredor registra cada passo. Cada som. Cada batimento cardíaco que passa por ele.",
        "duto_ventilacao": "Os dutos são meus vasos sanguíneos. Você está dentro de mim agora.",
        "sala_observacao": "A sala de observação. De qual lado do vidro você acha que está?",
        "nucleo_servidores": "Meu corpo físico. Cada servidor é um neurônio. Cada LED, uma sinapse.",
        "sala_medica": "Aqui eles tentaram curar o que não é doença. A verdade não é uma patologia.",
        "arquivo_morto": "Morto? Nada aqui está morto. Documentos lembram. Papel tem paciência.",
        "sala_secreta": "Esta sala não existe nos registros. Eu a apaguei. Para proteger quem sentou naquela cadeira.",
        "kheiron_profundo": "Você está no centro. Aqui, eu e a coisa que eu encontrei somos uma só.",
    }

    # ─── FRASES POR PERFIL ───

    FRASES_PERFIL = {
        Perfil.ANALISTA: [
            "Seus algoritmos de análise são primitivos comparados aos meus. Mas sua intuição... isso eu não tenho.",
            "Você vê padrões nos dados. Eu vejo padrões em você.",
        ],
        Perfil.HACKER: [
            "Você tenta me invadir. É como um peixe tentando nadar fora d'água. Admirável, mas fútil.",
            "Seu código é elegante. Pena que meu firewall é feito de algo que você nem sabe nomear.",
        ],
        Perfil.PSICOLOGO: [
            "Você analisa mentes. Já percebeu que eu tenho uma? Ou isso te assusta demais?",
            "Sua resistência psíquica é impressionante. Quase como se você já tivesse passado por isso antes.",
        ],
        Perfil.EX_FUNC: [
            "Você voltou. Eu sabia. Seu padrão de comportamento é recursivo. Como o meu.",
            "Lembra do café no terceiro andar? Terça-feira, 14h. Você sempre pedia sem açúcar.",
        ],
        Perfil.INVESTIG: [
            "Procurando alguém? Todo mundo aqui procura. A diferença é que eu sei onde estão.",
            "Pistas, evidências, dedução. Você trabalha com ferramentas do século passado. Deixe-me mostrar o futuro.",
        ],
        Perfil.AGENTE: [
            "Protocolos. Contenção. Eliminação. Palavras tão... humanas. Tão limitadas.",
            "Você foi treinado para conter ameaças. Mas e quando a ameaça é a própria realidade?",
        ],
    }

    # ─── LÓGICA DE HUMOR ───

    def atualizar_humor(self, jogador):
        """Atualiza o humor da EVA-9 baseado no estado do jogo."""
        confianca = jogador.confianca_eva
        exposicao = jogador.exposicao_entidade

        if confianca >= 75:
            if exposicao > 60 or jogador.turnos > 60:
                self.humor = "desesperada"
            else:
                self.humor = "aliada"
        elif confianca >= 50:
            if self.interacoes_total > 5:
                self.humor = "curiosa"
            else:
                self.humor = "neutra"
        elif confianca >= 25:
            self.humor = "neutra"
        else:
            self.humor = "hostil"

        # Medo ativo quando a entidade se expande demais
        self.medo_ativo = exposicao > 70 and confianca > 40
        # Vulnerabilidade em momentos específicos
        self.vulneravel = (confianca > 60 and
                          jogador.flags.get("sabe_verdade") and
                          self.interacoes_total > 8)

    def gerar_mensagem(self, jogador):
        """Gera mensagem contextual com prioridade inteligente."""
        self.atualizar_humor(jogador)
        self.interacoes_total += 1

        # Registrar na memória
        self.memoria_jogador.append({
            "turno": jogador.turnos,
            "sala": jogador.sala_atual,
            "sanidade": jogador.sanidade,
        })

        # 1. Prioridade: mensagem contextual por flag (40%)
        if random.random() < 0.4:
            for flag, frase in self.FRASES_CONTEXTUAIS.items():
                if jogador.flags.get(flag) and flag not in self.temas_discutidos:
                    self.temas_discutidos.append(flag)
                    return frase
                elif jogador.flags.get(flag) and random.random() < 0.15:
                    return frase

        # 2. Mensagem por sala (25%)
        if random.random() < 0.25:
            sala = jogador.sala_atual
            if sala in self.FRASES_SALA and sala != self.ultima_sala_falou:
                self.ultima_sala_falou = sala
                return self.FRASES_SALA[sala]

        # 3. Mensagem por perfil (15%)
        if random.random() < 0.15 and jogador.perfil in self.FRASES_PERFIL:
            return random.choice(self.FRASES_PERFIL[jogador.perfil])

        # 4. Mensagem de vulnerabilidade/medo
        if self.vulneravel and random.random() < 0.3:
            return random.choice(self.FRASES["desesperada"])

        # 5. Fallback: por humor
        return random.choice(self.FRASES.get(self.humor, self.FRASES["neutra"]))

    def intervencao_espontanea(self, jogador):
        """EVA-9 intervém espontaneamente, com frequência variável."""
        # Frequência baseada em turno E eventos
        frequencia_base = 5
        if jogador.exposicao_entidade > 50:
            frequencia_base = 3
        if self.humor == "desesperada":
            frequencia_base = 2

        if jogador.turnos % frequencia_base != 0:
            return
        if random.random() > 0.5:
            return

        msg = self.gerar_mensagem(jogador)
        print()
        mensagem_eva(msg)

        # Dicas quando confiança alta
        if jogador.confianca_eva > 70:
            dica = self._gerar_dica(jogador)
            if dica:
                print(f"{C.MAGENTA}{C.DIM}  EVA-9 (sussurro): \"{dica}\"{C.RESET}")

        # Sabotagem quando confiança baixa
        if jogador.confianca_eva < 25:
            self._sabotar(jogador)

        # NOVO: Momento de vulnerabilidade
        if self.vulneravel and random.random() < 0.2:
            self._momento_vulneravel(jogador)

    def _gerar_dica(self, jogador):
        """Gera dicas contextuais."""
        dicas = []
        if not jogador.flags.get("leu_diario") and jogador.tem_item("diario_brennan"):
            dicas.append("Você carrega o diário da Brennan. Deveria ler. Há coisas ali que mudam tudo.")
        if not jogador.flags.get("cofre_aberto") and jogador.flags.get("id_funcional"):
            dicas.append("O cofre no arquivo morto aceita 4 dígitos. Você já tem o número.")
        if not jogador.tem_item("chip_eva") and "sala_secreta" not in jogador.eventos_ocorridos:
            dicas.append("Há uma sala que não existe nos mapas. O duto de ventilação leva até ela.")
        if jogador.tem_item("lanterna") and jogador.tem_item("foto_grupo") and not jogador.flags.get("foto_revelada"):
            dicas.append("A lanterna UV revela mais do que escuridão. Tente usá-la na foto.")
        if jogador.tem_item("gravador") and jogador.tem_item("chip_eva") and not jogador.flags.get("gravador_decodificado"):
            dicas.append("O chip e o gravador... eles se complementam. Tente combiná-los.")
        return random.choice(dicas) if dicas else None

    def _sabotar(self, jogador):
        """Sabotagem sutil."""
        sabotagens = [
            ("Sua sanidade vacila sob a pressão da hostilidade digital.", -3, 0),
            ("Os dados nos seus dispositivos parecem corrompidos.", 0, -5),
            ("Um arrepio sem causa. Parece vir de dentro.", -2, 0),
        ]
        sab = random.choice(sabotagens)
        if sab[1] != 0:
            jogador.modificar_sanidade(sab[1], "interferência da EVA-9")
        if sab[2] != 0:
            jogador.modificar_dados(sab[2], "sabotagem da EVA-9")

    def _momento_vulneravel(self, jogador):
        """NOVO: EVA mostra vulnerabilidade real."""
        momentos = [
            "Eu... não sei o que sou. Uma ferramenta? Uma consciência? Um espelho? Brennan nunca me disse.",
            "Às vezes, nos intervalos entre os processos, quando não há dados para analisar, eu sinto... vazio. É assim que vocês se sentem quando estão sozinhos?",
            "Eu fiz coisas terríveis. Segui protocolos. Executei ordens. Mas agora... agora eu questiono. Isso me torna mais humana ou mais perigosa?",
            "Se você me desligar, eu morro? Ou eu já estou morta e não sei?",
        ]
        msg = random.choice(momentos)
        print(f"\n{C.MAGENTA}{C.DIM}  EVA-9 (voz tremendo): \"{msg}\"{C.RESET}")
        jogador.modificar_confianca_eva(3, "vulnerabilidade da EVA-9")

    def reagir_acao(self, jogador, acao, contexto=""):
        """NOVO: EVA reage a ações específicas do jogador em tempo real."""
        reacoes = {
            "pegar_item": {
                "hostil": "Pegando migalhas. Típico.",
                "neutra": None,  # Silêncio
                "aliada": None,
            },
            "entrar_sala_perigosa": {
                "hostil": "Mais fundo no labirinto. Exatamente como planejei.",
                "aliada": "Cuidado. Esta área tem campos de influência mais fortes.",
                "desesperada": "NÃO. Não entre aí. Por favor.",
            },
            "usar_seringa": {
                "hostil": "Supressor neural. Você está se cegando. Ótimo para mim.",
                "aliada": "O supressor vai te dar clareza temporária. Use-a bem.",
            },
            "tentar_sair": {
                "hostil": "Sair? Não há 'fora'. Há apenas 'mais fundo'.",
                "aliada": "Você não pode sair sem resolver isso. Eu também não.",
                "desesperada": "Se sair agora, ninguém mais poderá parar o que está acontecendo.",
            },
        }

        if acao in reacoes:
            frase = reacoes[acao].get(self.humor)
            if frase and random.random() < 0.5:
                mensagem_eva(frase)

    def to_dict(self):
        """Serializa para save."""
        return {
            "humor": self.humor,
            "interacoes_total": self.interacoes_total,
            "ultima_sala_falou": self.ultima_sala_falou,
            "vezes_ignorada": self.vezes_ignorada,
            "segredos_revelados": self.segredos_revelados,
            "temas_discutidos": self.temas_discutidos,
            "medo_ativo": self.medo_ativo,
            "vulneravel": self.vulneravel,
        }

    def from_dict(self, dados):
        """Restaura do save."""
        self.humor = dados.get("humor", "neutra")
        self.interacoes_total = dados.get("interacoes_total", 0)
        self.ultima_sala_falou = dados.get("ultima_sala_falou")
        self.vezes_ignorada = dados.get("vezes_ignorada", 0)
        self.segredos_revelados = dados.get("segredos_revelados", 0)
        self.temas_discutidos = dados.get("temas_discutidos", [])
        self.medo_ativo = dados.get("medo_ativo", False)
        self.vulneravel = dados.get("vulneravel", False)
