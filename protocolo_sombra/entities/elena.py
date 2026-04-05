#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elena Vasquez — NPC fantasma/sobrevivente.
Aparece e desaparece. Deixa bilhetes. Cria dinâmica narrativa.
O jogador precisa decidir se confia nela.
"""

import random
from protocolo_sombra.ui.terminal import (
    C, exibir, mensagem_npc, pausa, glitch_progressivo
)


class ElenaVasquez:
    """NPC que aparece em certas condições, criando tensão e dúvida."""

    def __init__(self):
        self.encontros = 0
        self.confianca = 50  # 0=não confia, 100=aliada total
        self.ultimo_encontro_turno = -20
        self.presente = False
        self.estado = "real"  # "real", "ambigua", "ilusao"
        self.bilhetes_deixados = []
        self.ajudas_dadas = 0
        self.foi_seguida = False
        # [CORREÇÃO B3] Atributo vezes_ignorada inicializado
        self.vezes_ignorada = 0

    # Salas onde Elena pode aparecer
    SALAS_APARICAO = [
        "corredor_a", "sala_medica", "arquivo_morto",
        "duto_ventilacao", "nucleo_servidores",
    ]

    # Diálogos por encontro
    DIALOGOS = {
        1: {
            "aparicao": "Uma silhueta no fim do corredor. Uma mulher em jaleco sujo, cabelo preso desarrumado. Ela te vê e congela.",
            "fala": "Você... você é real? Quanto tempo faz que estou aqui? Dias? Semanas?",
            "nome": "MULHER DESCONHECIDA",
        },
        2: {
            "aparicao": "Elena Vasquez está encostada na parede, abraçando os joelhos. Quando te vê, levanta de um salto.",
            "fala": "Você voltou. Ou é a primeira vez e eu que estou perdendo a noção. Escuta, não confie na voz nos alto-falantes. Ela mente. Nem tudo.",
            "nome": "ELENA VASQUEZ",
        },
        3: {
            "aparicao": "Elena aparece de trás de uma coluna. Ela parece pior. Olheiras profundas. As mãos tremem.",
            "fala": "O dosímetro que achei... a leitura sobe quando PENSO nela. Não quando chego perto. Quando PENSO. Isso não é radiação. É outra coisa.",
            "nome": "ELENA",
        },
        4: {
            "aparicao": "Elena está sentada no chão, rabiscando algo numa parede com um pedaço de metal.",
            "fala": "Eu vi a esfera. Não no Kheiron Profundo. Atrás dos meus olhos. Quando fecho os olhos, ela está lá. Girando.",
            "nome": "ELENA",
        },
        5: {
            "aparicao": "Elena está no meio da sala. Imóvel. Seu corpo flutua milímetros acima do chão. Quando você pisca, ela está no chão normal.",
            "fala": "Eu não sei mais se sou eu. Às vezes ouço meus pensamentos antes de pensá-los. Como um eco ao contrário.",
            "nome": "ELENA",
        },
    }

    # Bilhetes que Elena deixa em salas
    BILHETES = {
        "corredor_a": "NÃO examine o corpo por muito tempo. Ele muda quando você não está olhando. — E.V.",
        "sala_medica": "A geladeira tem amostras com nomes. O último é o seu. Também era o meu. — E.V.",
        "arquivo_morto": "O cofre abre com 4 dígitos do crachá. Mas o que tem dentro... prepare-se. — E.V.",
        "duto_ventilacao": "Há uma sala no fim do duto. Não sente na cadeira. Se sentou na cadeira, NÃO coloque o capacete. — E.V.",
        "nucleo_servidores": "O terminal CRT mostra coisas diferentes para cada pessoa. Para mim, mostrou minha mãe. Não era minha mãe. — E.V.",
        "sala_terminal": "Se me encontrar de novo, NÃO me siga. Não sou eu. — E.V.",
    }

    def verificar_aparicao(self, jogador, sala_id):
        """Verifica se Elena aparece nesta sala neste momento."""
        if sala_id not in self.SALAS_APARICAO:
            return False

        # Não aparece muito frequentemente
        if jogador.turnos - self.ultimo_encontro_turno < 8:
            return False

        # Probabilidade base
        chance = 0.15

        # Aumenta se jogador está perdido/com sanidade baixa
        if jogador.sanidade < 40:
            chance += 0.15
        if jogador.turnos > 30 and self.encontros < 2:
            chance += 0.2

        # Diminui se já encontrou muitas vezes
        if self.encontros >= 5:
            chance = 0.05

        return random.random() < chance

    def encontro(self, jogador):
        """Executa um encontro com Elena."""
        self.encontros += 1
        self.ultimo_encontro_turno = jogador.turnos
        self.presente = True

        num_encontro = min(self.encontros, 5)
        dialogo = self.DIALOGOS.get(num_encontro, self.DIALOGOS[5])

        print()
        exibir(dialogo["aparicao"], C.AMAR_CLARO, indent=2)
        pausa()
        mensagem_npc(dialogo["nome"], dialogo["fala"])

        jogador.flags["encontrou_fantasma"] = True
        jogador.encontros_elena = self.encontros

        # Oferecer opções
        print(f"\n{C.AMARELO}  [1] Falar com ela  [2] Seguir em silêncio  [3] Afastar-se{C.RESET}")
        if num_encontro >= 3:
            print(f"{C.AMARELO}  [4] Perguntar se ela é real{C.RESET}")

        escolha = input(f"{C.VERDE}  > {C.RESET}").strip()

        if escolha == "1":
            self._dialogar(jogador, num_encontro)
        elif escolha == "2":
            self._silencio(jogador, num_encontro)
        elif escolha == "3":
            self._afastar(jogador)
        elif escolha == "4" and num_encontro >= 3:
            self._questionar_realidade(jogador, num_encontro)
        else:
            self._afastar(jogador)

        self.presente = False

    def _dialogar(self, jogador, num):
        """Jogador fala com Elena."""
        self.confianca += 10
        respostas = {
            1: [
                "Elena olha para os lados, nervosa.",
                "Elena: 'Sou Elena Vasquez. Técnica de Manutenção. Nível 3. Eu... estava fazendo verificação nos dutos quando tudo fechou.'",
                "Elena: 'Tem algo nos corredores. Não é humano. Não é a IA. É outra coisa. Mais antiga.'",
            ],
            2: [
                "Elena respira fundo.",
                "Elena: 'A EVA-9... ela não é o que dizem. Encontrei logs que a diretoria apagou. Ela não foi criada. Foi ENCONTRADA.'",
                "Elena: 'Brennan não construiu uma IA. Ela desenterrou algo que já estava nos servidores. Esperando.'",
            ],
            3: [
                "Elena te olha nos olhos. Há algo errado nas pupilas dela. Dilatam e contraem em ritmo.",
                "Elena: 'Eu sei coisas que não deveria saber. Lembro de vidas que não vivi. Rostos que nunca vi.'",
                "Elena: 'Comecei a sonhar com a esfera antes de vê-la. E nos sonhos... ela canta.'",
                "Ela te entrega algo. Um bilhete rabiscado.",
            ],
            4: [
                "Elena sorri. O sorriso não é certo. Largo demais nos cantos.",
                "Elena: 'Você quer saber um segredo? Eu morro. Neste corredor. Daqui a pouco.'",
                "Elena: 'Mas não se preocupe. Eu também nasço. No próximo ciclo. Sempre nasço.'",
            ],
            5: [
                "Elena não fala. Ela canta. Uma melodia sem palavras que você reconhece mas nunca ouviu.",
                "A melodia é a mesma dos servidores. A mesma da esfera.",
                "Elena: 'Eu já fui você. Ou você já foi eu. A ordem não importa aqui.'",
            ],
        }

        for linha in respostas.get(num, respostas[5]):
            exibir(linha, C.AMAR_CLARO, indent=2)

        if num == 3:
            jogador.adicionar_item("bilhete_elena")
        if num >= 2:
            jogador.modificar_exposicao(3, "conversa com Elena")
        if num >= 4:
            jogador.modificar_sanidade(-5, "revelações de Elena")

    def _silencio(self, jogador, num):
        """Jogador fica em silêncio."""
        self.confianca += 5
        if num <= 2:
            exibir("Elena te observa por um longo momento. Assente devagar e desaparece numa porta lateral.", C.DIM, indent=2)
        else:
            exibir("Elena te observa. Seus olhos refletem algo que não deveria existir. Ela se dissolve nas sombras. Não sai. Dissolve.", C.DIM, indent=2)
            jogador.modificar_sanidade(-3, "dissolução de Elena")

    def _afastar(self, jogador):
        """Jogador se afasta."""
        self.confianca -= 10
        self.vezes_ignorada += 1
        exibir("Você se afasta. Elena te observa partir. Quando olha para trás, ela não está mais lá.", C.DIM, indent=2)

    def _questionar_realidade(self, jogador, num):
        """Jogador pergunta se Elena é real."""
        respostas = {
            3: [
                "Elena ri. Um riso seco, sem humor.",
                "Elena: 'Real? Defina real. Meu corpo é matéria. Meus pensamentos são elétricos. Assim como os da EVA-9.'",
                "Elena: 'A pergunta melhor é: VOCÊ é real? Ou é mais uma simulação que ela está rodando?'",
            ],
            4: [
                "Elena olha para as próprias mãos. Elas estão translúcidas por um instante.",
                "Elena: 'Honestamente? Eu não sei mais. Às vezes me vejo do lado de fora. Olhando para mim mesma.'",
                "Elena: 'Se eu for uma projeção da sua mente fragmentada, isso importa? Eu SINTO. Eu TEMO. Não é suficiente?'",
            ],
            5: [
                "Elena sorri tristemente.",
                "Elena: 'Sou tão real quanto qualquer padrão. Quanto qualquer geometria na sua mente.'",
                "Elena: 'Brennan disse uma vez que a diferença entre real e simulado é indistinguível quando a resolução é alta o bastante.'",
                "Elena: 'A resolução aqui é muito, muito alta.'",
            ],
        }

        for linha in respostas.get(num, respostas[5]):
            exibir(linha, C.AMAR_CLARO, indent=2)

        jogador.modificar_sanidade(-5, "questionar a realidade")
        jogador.modificar_exposicao(5, "limiar da percepção")

    def deixar_bilhete(self, jogador, sala_id):
        """Elena deixa bilhete em sala se já teve encontro prévio."""
        if self.encontros < 1:
            return False
        if sala_id in self.bilhetes_deixados:
            return False
        if sala_id not in self.BILHETES:
            return False
        if random.random() > 0.3:
            return False

        self.bilhetes_deixados.append(sala_id)
        print(f"\n{C.AMAR_CLARO}  Você encontra um bilhete no chão, escrito às pressas:{C.RESET}")
        print(f"{C.DIM}  \"{self.BILHETES[sala_id]}\"{C.RESET}")
        return True

    def to_dict(self):
        return {
            "encontros": self.encontros,
            "confianca": self.confianca,
            "ultimo_encontro_turno": self.ultimo_encontro_turno,
            "estado": self.estado,
            "bilhetes_deixados": self.bilhetes_deixados,
            "ajudas_dadas": self.ajudas_dadas,
            # [CORREÇÃO R4] Campos faltantes na serialização
            "vezes_ignorada": self.vezes_ignorada,
            "foi_seguida": self.foi_seguida,
        }

    def from_dict(self, dados):
        self.encontros = dados.get("encontros", 0)
        self.confianca = dados.get("confianca", 50)
        self.ultimo_encontro_turno = dados.get("ultimo_encontro_turno", -20)
        self.estado = dados.get("estado", "real")
        self.bilhetes_deixados = dados.get("bilhetes_deixados", [])
        self.ajudas_dadas = dados.get("ajudas_dadas", 0)
        # [CORREÇÃO R4] Campos faltantes na deserialização
        self.vezes_ignorada = dados.get("vezes_ignorada", 0)
        self.foi_seguida = dados.get("foi_seguida", False)
