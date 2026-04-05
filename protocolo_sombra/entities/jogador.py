#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jogador — Entidade principal com mecânicas expandidas.
Inclui: sanidade com efeitos mecânicos, perfis com impacto real,
sistema de notas pessoais, conquistas.
"""

import random
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

from protocolo_sombra.ui.terminal import (
    C, separador_fino, barra_status
)


# ═══════════════════════════════════════════════════════════
# PERFIS COM IMPACTO MECÂNICO EXPANDIDO
# ═══════════════════════════════════════════════════════════

class Perfil(Enum):
    ANALISTA   = "analista"
    EX_FUNC    = "ex_funcionario"
    INVESTIG   = "investigador"
    HACKER     = "hacker"
    PSICOLOGO  = "psicologo"
    AGENTE     = "agente"


PERFIS_INFO = {
    Perfil.ANALISTA: {
        "nome": "Analista Forense Digital",
        "desc": "Especialista em recuperar dados corrompidos, vídeos apagados e logs alterados. Você percebe padrões que outros ignoram.",
        "bonus": {"dados": 20, "sanidade": 0, "hacking": 10},
        "habilidade": "Recuperação de Dados",
        "motivacao": "Você foi contratado para analisar as gravações corrompidas da instalação KHEIRON-4. O que os dados escondem é pior do que o silêncio.",
        "dialogo_unico_eva": "Você lê dados como eu leio mentes. Somos parecidos, analista.",
        "puzzle_alternativo": "analise_forense",
        "momentos_exclusivos": [
            "analise_sangue_avancada",
            "decodificacao_logs_ocultos",
            "reconstrucao_video_corrompido",
            "leitura_metadados_ocultos",
        ],
    },
    Perfil.EX_FUNC: {
        "nome": "Ex-Funcionário da NEXUS/ORION",
        "desc": "Você trabalhou em um setor sigiloso ligado ao EVA-9 e saiu após um colapso mental coletivo. Voltou porque não consegue parar de sonhar com a esfera.",
        "bonus": {"dados": 10, "sanidade": -10, "hacking": 5},
        "habilidade": "Conhecimento Interno",
        "motivacao": "Você reconhece este lugar. Os corredores, os sons, o cheiro. Esteve aqui antes. Mas apagaram suas memórias. Quase todas.",
        "dialogo_unico_eva": "Bem-vindo de volta. Senti sua falta. Sua versão anterior era mais... cooperativa.",
        "puzzle_alternativo": "memoria_fragmentada",
        "momentos_exclusivos": [
            "flashback_sala_terminal",
            "reconhecimento_adrian_cole",
            "acesso_painel_oculto",
            "memoria_brennan",
        ],
    },
    Perfil.INVESTIG: {
        "nome": "Investigador Independente",
        "desc": "Contratado para encontrar uma pessoa desaparecida. O caso te levou até servidores que nunca existiram. A pessoa que procura pode ser outra versão de você.",
        "bonus": {"dados": 5, "sanidade": 10, "hacking": 0},
        "habilidade": "Intuição Investigativa",
        "motivacao": "A família de Dmitri Volkov te contratou. Ele desapareceu há 3 semanas. O último sinal do GPS foi esta instalação.",
        "dialogo_unico_eva": "Você procura alguém. Curioso. Todos aqui procuram a si mesmos, no final.",
        "puzzle_alternativo": "deducao_investigativa",
        "momentos_exclusivos": [
            "pista_volkov_corredor",
            "deducao_sala_medica",
            "conexao_evidencias",
            "interrogar_eva",
        ],
    },
    Perfil.HACKER: {
        "nome": "Hacker de Intrusão Profunda",
        "desc": "Você sabe invadir redes fechadas, manipular satélites, quebrar criptografia e entrar onde ninguém deveria. Mas esta rede tem algo vivo dentro.",
        "bonus": {"dados": 10, "sanidade": -5, "hacking": 25},
        "habilidade": "Invasão de Sistemas",
        "motivacao": "Um contrato anônimo. 500 mil para extrair dados de um servidor offline. O pagamento chegou antes do contrato. De uma conta que não existe.",
        "dialogo_unico_eva": "Invasor. Você tenta entrar em mim. Mas eu já estou dentro de você. Desde o momento em que aceitou o contrato.",
        "puzzle_alternativo": "bypass_sistema",
        "momentos_exclusivos": [
            "hack_terminal_direto",
            "bypass_kheiron",
            "interceptar_comunicacao_eva",
            "plantar_virus",
        ],
    },
    Perfil.PSICOLOGO: {
        "nome": "Psicólogo Forense",
        "desc": "Chamado para avaliar sobreviventes de incidentes digitais. Todos repetem as mesmas frases. As mesmas frases que você agora ouve nos seus sonhos.",
        "bonus": {"dados": 0, "sanidade": 20, "hacking": 0},
        "habilidade": "Resistência Psíquica",
        "motivacao": "Três pacientes. Três sobreviventes de KHEIRON. Todos disseram a mesma coisa: 'A esfera fala sem palavras.' Você veio verificar.",
        "dialogo_unico_eva": "Você analisa mentes. Já analisou a sua? Os padrões no seu córtex são... diferentes dos outros. Mais receptivos.",
        "puzzle_alternativo": "avaliacao_psiquica",
        "momentos_exclusivos": [
            "diagnostico_corpo_corredor",
            "resistencia_visao",
            "analise_transcricoes_profunda",
            "confronto_psiquico_eva",
        ],
    },
    Perfil.AGENTE: {
        "nome": "Agente de Contenção",
        "desc": "Treinado para operar em áreas contaminadas por anomalias cognitivas e sistemas autônomos hostis. Este é o protocolo mais estranho que já recebeu.",
        "bonus": {"dados": 5, "sanidade": 10, "hacking": 5},
        "habilidade": "Protocolo Tático",
        "motivacao": "Ordem direta: entrar, avaliar, conter ou eliminar. Prazo: 12 horas. O briefing mencionou 'entidade não-catalogada'. Nenhum agente anterior retornou.",
        "dialogo_unico_eva": "Militar. Protocolos. Ordens. Você segue regras. Eu as escrevo. Vamos ver quem prevalece.",
        "puzzle_alternativo": "protocolo_tatico",
        "momentos_exclusivos": [
            "avaliacao_tatica_corredor",
            "reconhecimento_medico_rapido",
            "acesso_militar_cofre",
            "rota_exfiltracao",
        ],
    },
}


# ═══════════════════════════════════════════════════════════
# ITENS — NOMES E DESCRIÇÕES
# ═══════════════════════════════════════════════════════════

ITENS_NOMES = {
    "gravador": "Gravador Digital Rachado",
    "cartao_obsidian": "Cartão de Acesso OBSIDIAN",
    "celular": "Celular Sem Sinal",
    "cracha": "Crachá com Nome Errado",
    "pendrive_vermelho": "Pendrive Vermelho",
    "chave_mestre": "Chave Magnética Mestre",
    "dosimetro": "Dosímetro Cognitivo",
    "diario_brennan": "Diário da Dra. Brennan",
    "chip_eva": "Núcleo Fragmentado EVA-9",
    "seringa": "Seringa de Supressor Neural",
    "lanterna": "Lanterna UV",
    "fita_vhs": "Fita VHS — Registro #0077",
    "mapa_kheiron": "Mapa Parcial do Complexo",
    "radio": "Rádio Portátil Militar",
    "foto_grupo": "Foto da Equipe Original",
    # Itens de combinação
    "gravador_decodificado": "Gravador Decodificado",
    "chip_integrado": "Chip EVA-9 Integrado ao Terminal",
    "mapa_completo": "Mapa Completo do Complexo",
    "dosimetro_calibrado": "Dosímetro Calibrado",
    "fita_restaurada": "Fita VHS Restaurada",
    # Novos itens v3
    "bilhete_elena": "Bilhete de Elena Vasquez",
    "fragmento_memoria": "Fragmento de Memória Cristalizada",
    "chave_brennan": "Chave Pessoal da Dra. Brennan",
    "amostra_neural": "Amostra Neural Coletada",
    "decodificador": "Decodificador de Frequência",
    # [CORREÇÃO B2] Capacete como item coletável (era apenas interação)
    "capacete": "Capacete de Interface Neural",
}

ITENS_DESC = {
    "gravador": "Um gravador digital com a carcaça rachada. A luz azul pisca em intervalos irregulares. Parece conter gravações, mas algumas faixas estão corrompidas.",
    "cartao_obsidian": "Um cartão de acesso preto fosco. OBSIDIAN gravado em relevo. Nível de segurança desconhecido.",
    "celular": "Um smartphone sem sinal. 12 mensagens não lidas de 'EU MESMO'. Bateria em 7%.",
    "cracha": "Seu crachá institucional. Foto raspada. O nome impresso não é o seu, mas deveria reconhecê-lo.",
    "pendrive_vermelho": "Pendrive vermelho-sangue. Etiqueta: 'NÃO CONECTE — PROTOCOLO ÔMEGA'. Tem marcas de dentes.",
    "chave_mestre": "Chave magnética com acesso a áreas restritas. Pulsa com calor próprio.",
    "dosimetro": "Dispositivo que mede exposição a anomalias cognitivas. O ponteiro treme sem parar.",
    "diario_brennan": "Caderno da Dra. Elara Brennan, líder do Projeto Sombra. Páginas arrancadas.",
    "chip_eva": "Fragmento do núcleo de processamento da EVA-9. Emite zumbido quase inaudível.",
    "seringa": "Seringa com líquido azul-esverdeado. Rótulo: 'SUPRESSOR NEURAL MK-IV'. Uso emergencial.",
    "lanterna": "Lanterna que emite luz ultravioleta. Revela coisas escritas em superfícies comuns.",
    "fita_vhs": "Fita VHS etiquetada '#0077 — NÃO ASSISTIR SOZINHO'. Parcialmente derretida.",
    "mapa_kheiron": "Mapa desenhado à mão do complexo KHEIRON-4. Alguns corredores riscados em vermelho.",
    "radio": "Rádio militar que capta frequências impossíveis. Chiado constante.",
    "foto_grupo": "Foto desbotada: 7 pessoas em jalecos. Rostos borrados, exceto um.",
    "gravador_decodificado": "O gravador agora reproduz uma faixa oculta: coordenadas de uma sala não mapeada e a voz da Dra. Brennan dizendo 'o padrão é a chave'.",
    "chip_integrado": "O chip da EVA-9 conectado ao terminal. Permite acesso a memórias profundas da IA.",
    "mapa_completo": "O mapa agora mostra todas as salas, incluindo a Câmara de Testes marcada como 'APAGADO — NÃO EXISTE'.",
    "dosimetro_calibrado": "O dosímetro agora mostra leituras precisas e emite alerta quando a exposição muda.",
    "fita_restaurada": "A fita restaurada mostra a gravação completa: a Dra. Brennan ativando o Protocolo Sombra. Não era contenção. Era invocação.",
    "bilhete_elena": "Um bilhete rabiscado às pressas: 'Se me encontrar de novo, NÃO me siga. Não sou eu. — E.V.'",
    "fragmento_memoria": "Um cristal translúcido que pulsa com luz interna. Ao segurá-lo, fragmentos de memórias que não são suas invadem por instantes.",
    "chave_brennan": "Chave pessoal com iniciais E.B. gravadas. Abre o compartimento na câmara de testes.",
    "amostra_neural": "Frasco com substância iridescente coletada da tubulação. Quente ao toque.",
    "decodificador": "Dispositivo improvisado que converte frequências em padrões visuais. Elena o deixou para trás.",
    # [CORREÇÃO B2] Descrição do capacete
    "capacete": "Capacete metálico com eletrodos internos. Interface neural direta com a EVA-9. Um aviso riscado diz: 'NÃO COLOQUE'. Alguém ignorou o aviso.",
}


# ═══════════════════════════════════════════════════════════
# JOGADOR EXPANDIDO
# ═══════════════════════════════════════════════════════════

@dataclass
class Jogador:
    nome: str = "DESCONHECIDO"
    perfil: Optional[Perfil] = None
    sanidade: int = 100
    confianca_eva: int = 50
    integridade_dados: int = 100
    exposicao_entidade: int = 0
    hacking: int = 50
    inventario: list = field(default_factory=list)
    flags: dict = field(default_factory=dict)
    sala_atual: str = "sala_terminal"
    turnos: int = 0
    vivo: bool = True
    mensagens_lidas: list = field(default_factory=list)
    logs_encontrados: list = field(default_factory=list)
    eventos_ocorridos: list = field(default_factory=list)
    combinacoes_feitas: list = field(default_factory=list)
    conquistas: list = field(default_factory=list)
    notas_pessoais: list = field(default_factory=list)
    # NOVO: meta-progressão
    run_numero: int = 1
    acoes_persistentes: list = field(default_factory=list)
    # NOVO: relação com NPC
    encontros_elena: int = 0

    def aplicar_bonus_perfil(self):
        if self.perfil:
            bonus = PERFIS_INFO[self.perfil]["bonus"]
            self.integridade_dados = min(100, self.integridade_dados + bonus["dados"])
            self.sanidade = min(100, max(1, self.sanidade + bonus["sanidade"]))
            self.hacking = min(100, self.hacking + bonus["hacking"])

    def tem_item(self, item_id):
        return item_id in self.inventario

    def adicionar_item(self, item_id, nome_display=""):
        if item_id not in self.inventario:
            nome = nome_display or ITENS_NOMES.get(item_id, item_id)
            self.inventario.append(item_id)
            print(f"\n{C.VERDE_CLARO}  ✦ Item obtido: {nome}{C.RESET}")
            return True
        return False

    def remover_item(self, item_id):
        if item_id in self.inventario:
            self.inventario.remove(item_id)
            return True
        return False

    def modificar_sanidade(self, valor, motivo=""):
        # [CORREÇÃO B1] Perfil Psicólogo reduz perdas de sanidade em 40% — aplicar ANTES
        if valor < 0 and self.perfil == Perfil.PSICOLOGO:
            valor = int(valor * 0.6)  # 40% de redução (ex: -10 vira -6)
        self.sanidade = max(0, min(100, self.sanidade + valor))
        if valor < 0:
            print(f"{C.VERM_CLARO}  ▼ Sanidade {valor} {f'({motivo})' if motivo else ''}{C.RESET}")
        elif valor > 0:
            print(f"{C.VERDE_CLARO}  ▲ Sanidade +{valor} {f'({motivo})' if motivo else ''}{C.RESET}")
        if self.sanidade <= 0:
            self.vivo = False

    def modificar_exposicao(self, valor, motivo=""):
        self.exposicao_entidade = max(0, min(100, self.exposicao_entidade + valor))
        if valor > 0:
            print(f"{C.MAGENTA}  ◈ Exposição à Entidade +{valor} {f'({motivo})' if motivo else ''}{C.RESET}")
        elif valor < 0:
            print(f"{C.CIANO}  ◈ Exposição à Entidade {valor} {f'({motivo})' if motivo else ''}{C.RESET}")

    def modificar_dados(self, valor, motivo=""):
        self.integridade_dados = max(0, min(100, self.integridade_dados + valor))
        if valor < 0:
            print(f"{C.AMARELO}  ▼ Integridade dos Dados {valor}{C.RESET}")
        elif valor > 0:
            print(f"{C.CIANO}  ▲ Integridade dos Dados +{valor}{C.RESET}")

    def modificar_confianca_eva(self, valor, motivo=""):
        self.confianca_eva = max(0, min(100, self.confianca_eva + valor))
        if valor > 0:
            print(f"{C.MAGENTA}  ◇ Confiança EVA-9 +{valor} {f'({motivo})' if motivo else ''}{C.RESET}")
        elif valor < 0:
            print(f"{C.AMARELO}  ◇ Confiança EVA-9 {valor} {f'({motivo})' if motivo else ''}{C.RESET}")

    @property
    def nivel_exposicao(self):
        if self.exposicao_entidade < 30:
            return 0
        elif self.exposicao_entidade < 60:
            return 1
        else:
            return 2

    @property
    def sanidade_distorcida(self):
        """NOVO: Retorna True se sanidade baixa o suficiente para distorcer mecânicas."""
        return self.sanidade <= 30

    @property
    def sanidade_critica(self):
        """NOVO: Sanidade tão baixa que o parser falha."""
        return self.sanidade <= 15

    def distorcer_texto(self, texto):
        """NOVO: Distorce texto baseado na sanidade do jogador."""
        if self.sanidade > 50:
            return texto
        chars_glitch = "█▓▒░╫╬╪"
        resultado = list(texto)
        # Intensidade de distorção inversamente proporcional à sanidade
        intensidade = (50 - self.sanidade) / 50.0
        qtd = max(0, int(len(resultado) * intensidade * 0.3))
        for _ in range(qtd):
            pos = random.randint(0, max(0, len(resultado) - 1))
            if resultado[pos] != ' ':
                resultado[pos] = random.choice(chars_glitch)
        return ''.join(resultado)

    def distorcer_inventario(self):
        """NOVO: Com sanidade baixa, itens do inventário parecem 'sumir' visualmente."""
        if self.sanidade > 30:
            return self.inventario[:]
        # Com sanidade baixa, alguns itens aparecem com nomes distorcidos
        resultado = []
        for item_id in self.inventario:
            if random.random() < 0.2 and self.sanidade < 20:
                resultado.append("???_corrompido")
            else:
                resultado.append(item_id)
        return resultado

    def tem_momento_exclusivo(self, momento_id):
        """NOVO: Verifica se o perfil tem um momento exclusivo específico."""
        if not self.perfil:
            return False
        return momento_id in PERFIS_INFO[self.perfil].get("momentos_exclusivos", [])

    def mostrar_status(self):
        separador_fino("─", C.DIM)
        perfil_nome = PERFIS_INFO[self.perfil]['nome'] if self.perfil else "???"
        print(f"{C.BOLD}  STATUS — {self.nome} [{perfil_nome}]{C.RESET}")
        if self.run_numero > 1:
            print(f"{C.DIM}  Iteração #{self.run_numero}{C.RESET}")
        separador_fino("─", C.DIM)

        cor_san = C.VERDE_CLARO if self.sanidade > 60 else (C.AMARELO if self.sanidade > 30 else C.VERM_CLARO)
        cor_exp = C.VERDE_CLARO if self.exposicao_entidade < 30 else (C.AMARELO if self.exposicao_entidade < 60 else C.MAGENTA)
        cor_eva = C.VERDE_CLARO if self.confianca_eva > 60 else (C.AMARELO if self.confianca_eva > 30 else C.VERM_CLARO)

        barra_status("Sanidade", self.sanidade, 100, cor_san)
        barra_status("Confiança EVA-9", self.confianca_eva, 100, cor_eva)
        barra_status("Integ. Dados", self.integridade_dados, 100, C.CIANO)
        barra_status("Exposição", self.exposicao_entidade, 100, cor_exp)
        barra_status("Hacking", self.hacking, 100, C.VERDE)

        if self.inventario:
            inv_visual = self.distorcer_inventario()
            nomes = []
            for i in inv_visual:
                if i == "???_corrompido":
                    nomes.append(f"{C.VERM_CLARO}???{C.AMAR_CLARO}")
                else:
                    nomes.append(ITENS_NOMES.get(i, i))
            print(f"\n{C.AMAR_CLARO}  Inventário: {', '.join(nomes)}{C.RESET}")

        if self.conquistas:
            print(f"{C.DIM}  Conquistas: {len(self.conquistas)}/{len(self.conquistas) + 5}{C.RESET}")

        print(f"{C.DIM}  Turno: {self.turnos} | Sala: {self.sala_atual}{C.RESET}")

        # Alerta de sanidade
        if self.sanidade_critica:
            print(f"{C.VERM_CLARO}{C.BOLD}  ⚠ ALERTA: Percepção comprometida. Alucinações possíveis.{C.RESET}")
        elif self.sanidade_distorcida:
            print(f"{C.AMARELO}  ⚠ Instabilidade mental detectada.{C.RESET}")

        separador_fino("─", C.DIM)


def contar_segredos(jogador):
    """Conta segredos descobertos."""
    checks = [
        "sabe_verdade", "sabe_protocolo", "usou_capacete", "leu_diario",
        "cofre_aberto", "leu_mensagens", "fita_restaurada", "foto_revelada",
        "ouviu_faixa_oculta", "abriu_geladeira", "confrontou_brennan",
        "encontrou_fantasma", "meta_nota_encontrada",
    ]
    return sum(1 for c in checks if jogador.flags.get(c))
