#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser de Comandos — Fuzzy matching, remoção de stopwords,
distorção por sanidade baixa.
"""

import random
from difflib import get_close_matches
from protocolo_sombra_v3.ui.terminal import C


# Stopwords em português para limpar comandos
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "no", "na", "nos", "nas",
    "em", "ao", "à", "aos", "às", "por", "pelo", "pela",
    "com", "para", "pra", "pro", "que", "este", "esta",
    "esse", "essa", "aquele", "aquela", "meu", "minha",
    "seu", "sua", "este", "neste", "nesta", "deste", "desta",
    "é", "e", "ou", "mas", "se", "me", "te", "lhe",
}

# Aliases de comandos expandidos
ALIASES = {
    # Direções
    "n": "norte", "s": "sul", "l": "leste", "o": "oeste",
    "cima": "norte", "baixo": "sul", "direita": "leste", "esquerda": "oeste",
    "frente": "norte",

    # Ações básicas
    "i": "inventario", "inv": "inventario",
    "st": "status", "stat": "status",
    "h": "ajuda", "help": "ajuda", "?": "ajuda",
    "olhar": "examinar", "ver": "examinar", "look": "examinar",
    "inspecionar": "examinar", "observar": "examinar", "checar": "examinar",
    "ir": "mover", "andar": "mover", "caminhar": "mover",
    "pegar": "pegar", "get": "pegar", "take": "pegar",
    "apanhar": "pegar", "coletar": "pegar",
    "usar": "usar", "use": "usar", "utilizar": "usar", "aplicar": "usar",
    "ler": "ler", "read": "ler", "abrir": "ler",
    "ouvir": "ouvir", "escutar": "ouvir", "listen": "ouvir",
    "sair": "sair", "quit": "sair", "q": "sair", "exit": "sair",
    "salvar": "salvar", "save": "salvar",
    "carregar": "carregar", "load": "carregar",
    "combinar": "combinar", "combine": "combinar", "juntar": "combinar",
    "misturar": "combinar", "unir": "combinar",
    "revistar": "revistar", "search": "revistar", "vasculhar": "revistar",
    "procurar": "revistar",

    # Novos comandos v3
    "mapa": "mapa", "map": "mapa",
    "diario": "diario", "journal": "diario",
    "notas": "notas", "notes": "notas",
    "anotar": "anotar", "note": "anotar", "escrever": "anotar",
    "conquistas": "conquistas", "achievements": "conquistas",
    "falar": "interagir", "conversar": "interagir",
    "tocar": "interagir", "empurrar": "interagir",
    "puxar": "interagir", "quebrar": "interagir",
    "cheirar": "interagir", "sentir": "interagir",
    "rapido": "rapido", "fast": "rapido",
}

# Todos os verbos reconhecidos
VERBOS_VALIDOS = {
    "norte", "sul", "leste", "oeste", "mover",
    "examinar", "pegar", "inventario", "status",
    "usar", "ler", "ouvir", "interagir", "combinar",
    "revistar", "ajuda", "sair", "salvar", "carregar",
    "mapa", "diario", "notas", "anotar", "conquistas",
    "rapido",
}


class ComandoParseado:
    """Resultado do parsing de um comando."""
    def __init__(self, verbo="", args="", original="", distorcido=False):
        self.verbo = verbo
        self.args = args
        self.original = original
        self.distorcido = distorcido  # True se sanidade baixa alterou o comando

    def __repr__(self):
        return f"Comando({self.verbo}, '{self.args}')"


def limpar_stopwords(texto):
    """Remove stopwords do texto."""
    palavras = texto.split()
    return ' '.join(p for p in palavras if p.lower() not in STOPWORDS)


def encontrar_item_fuzzy(nome_parcial, itens_dict, limiar=0.5):
    """Encontra item por nome parcial com fuzzy matching."""
    nome_lower = nome_parcial.lower()

    # Match exato primeiro
    for item_id, nome_completo in itens_dict.items():
        if nome_lower == item_id.lower() or nome_lower == nome_completo.lower():
            return item_id

    # Match parcial (substring)
    for item_id, nome_completo in itens_dict.items():
        if nome_lower in item_id.lower() or nome_lower in nome_completo.lower():
            return item_id

    # Fuzzy matching como último recurso
    todos_nomes = {}
    for item_id, nome_completo in itens_dict.items():
        todos_nomes[item_id.lower()] = item_id
        todos_nomes[nome_completo.lower()] = item_id

    matches = get_close_matches(nome_lower, todos_nomes.keys(), n=1, cutoff=limiar)
    if matches:
        return todos_nomes[matches[0]]

    return None


def encontrar_interacao_fuzzy(nome_parcial, interacoes_dict, limiar=0.5):
    """Encontra interação por nome parcial com fuzzy matching."""
    nome_lower = nome_parcial.lower()

    # Match exato
    if nome_lower in interacoes_dict:
        return nome_lower

    # Match parcial
    for chave in interacoes_dict:
        if nome_lower in chave or chave in nome_lower:
            return chave

    # Fuzzy
    matches = get_close_matches(nome_lower, list(interacoes_dict.keys()), n=1, cutoff=limiar)
    if matches:
        return matches[0]

    return None


def distorcer_comando(comando, sanidade):
    """NOVO: Distorce o comando quando a sanidade está muito baixa."""
    if sanidade > 15:
        return comando, False

    # 30% de chance de distorcer
    if random.random() > 0.3:
        return comando, False

    distorcoes = [
        # Troca direção
        lambda c: c.replace("norte", "sul").replace("leste", "oeste") if any(d in c for d in ["norte", "sul", "leste", "oeste"]) else c,
        # Inverte ação
        lambda c: c.replace("pegar", "soltar") if "pegar" in c else c,
        # Alucina nome de item
        lambda c: c + " de vidro" if "examinar" in c else c,
        # Perde parte do comando
        lambda c: ' '.join(c.split()[:1]),
    ]

    distorcao = random.choice(distorcoes)
    resultado = distorcao(comando)
    if resultado != comando:
        return resultado, True
    return comando, False


def parsear(entrada, sanidade=100, sala_interacoes=None):
    """
    Parseia entrada do jogador em verbo + argumentos.

    Args:
        entrada: string do jogador
        sanidade: nível de sanidade (afeta parsing)
        sala_interacoes: dict de interações da sala atual

    Returns:
        ComandoParseado
    """
    original = entrada.strip()
    if not original:
        return ComandoParseado()

    entrada_limpa = original.lower()
    distorcido = False

    # Distorção por sanidade
    if sanidade <= 15:
        entrada_limpa, distorcido = distorcer_comando(entrada_limpa, sanidade)
        if distorcido:
            print(f"{C.VERM_CLARO}{C.DIM}  [Seus pensamentos se embaralham...]{C.RESET}")

    # Separar em partes
    partes = entrada_limpa.split(None, 1)
    verbo_raw = partes[0] if partes else ""
    args_raw = partes[1] if len(partes) > 1 else ""

    # Resolver alias
    verbo = ALIASES.get(verbo_raw, verbo_raw)

    # Se o verbo é uma direção, retorna direto
    if verbo in ("norte", "sul", "leste", "oeste"):
        return ComandoParseado(verbo, "", original, distorcido)

    # Limpar stopwords dos argumentos
    args = limpar_stopwords(args_raw) if args_raw else ""

    # Se verbo não reconhecido, tentar como interação da sala
    if verbo not in VERBOS_VALIDOS:
        # Tentar o texto inteiro como interação
        if sala_interacoes:
            # Tentar verbo sozinho
            match = encontrar_interacao_fuzzy(verbo_raw, sala_interacoes)
            if match:
                return ComandoParseado("interagir", match, original, distorcido)
            # Tentar texto inteiro
            match = encontrar_interacao_fuzzy(entrada_limpa, sala_interacoes)
            if match:
                return ComandoParseado("interagir", match, original, distorcido)

        # Fuzzy match no verbo
        verbos_e_aliases = list(VERBOS_VALIDOS) + list(ALIASES.keys())
        matches = get_close_matches(verbo_raw, verbos_e_aliases, n=1, cutoff=0.6)
        if matches:
            sugestao = ALIASES.get(matches[0], matches[0])
            print(f"{C.DIM}  (Interpretando como '{sugestao}'...){C.RESET}")
            return ComandoParseado(sugestao, args, original, distorcido)

        # Desconhecido
        return ComandoParseado(verbo, args, original, distorcido)

    # Verbo de ação que precisa de args para interação
    if verbo == "interagir" and args and sala_interacoes:
        match = encontrar_interacao_fuzzy(args, sala_interacoes)
        if match:
            args = match

    return ComandoParseado(verbo, args, original, distorcido)
