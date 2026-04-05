#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Finais — Com variantes baseadas em estado,
final secreto, e tela de estatísticas.
"""

import time
from protocolo_sombra_v3.ui.terminal import (
    C, exibir, digitando, separador, separador_fino,
    titulo, subtitulo, mensagem_eva, pausa, limpar,
    efeito_estatica, efeito_corrupcao
)
from protocolo_sombra_v3.entities.jogador import PERFIS_INFO, contar_segredos, ITENS_NOMES
from protocolo_sombra_v3.engine.save_system import salvar_meta


def tela_final_stats(jogador, final_alcancado):
    """Exibe estatísticas finais e salva meta-progressão."""
    salvar_meta(jogador, final_alcancado)

    print()
    separador_fino()
    print(f"{C.BOLD}  ESTATÍSTICAS FINAIS{C.RESET}")
    separador_fino()
    print(f"{C.DIM}  Personagem: {jogador.nome} ({PERFIS_INFO[jogador.perfil]['nome']}){C.RESET}")
    if jogador.run_numero > 1:
        print(f"{C.DIM}  Iteração: #{jogador.run_numero}{C.RESET}")
    print(f"{C.DIM}  Turnos: {jogador.turnos}{C.RESET}")
    print(f"{C.DIM}  Sanidade Final: {jogador.sanidade}%{C.RESET}")
    print(f"{C.DIM}  Exposição: {jogador.exposicao_entidade}%{C.RESET}")
    print(f"{C.DIM}  Confiança EVA-9: {jogador.confianca_eva}%{C.RESET}")
    print(f"{C.DIM}  Itens coletados: {len(jogador.inventario)}/{len(ITENS_NOMES)}{C.RESET}")
    print(f"{C.DIM}  Combinações realizadas: {len(jogador.combinacoes_feitas)}{C.RESET}")

    segredos = contar_segredos(jogador)
    print(f"{C.DIM}  Segredos descobertos: {segredos}/13{C.RESET}")

    finais_desc = {
        "fusao": "FUSÃO — Você se tornou a rede.",
        "fusao_consciente": "FUSÃO CONSCIENTE — Você se encontrou.",
        "contencao": "CONTENÇÃO — Selado para sempre.",
        "contencao_resgate": "CONTENÇÃO COM RESGATE — Escapou. Fisicamente.",
        "desligamento": "DESLIGAMENTO — O alarme foi silenciado.",
        "desligamento_limpo": "DESLIGAMENTO LIMPO — Destruiu e escapou.",
        "morte": "FALHA — Sanidade esgotada.",
        "destruicao": "DESTRUIÇÃO — O tempo acabou.",
        "secreto": "??? — A verdade completa.",
    }

    print(f"{C.DIM}  Final: {finais_desc.get(final_alcancado, 'DESCONHECIDO')}{C.RESET}")

    if jogador.conquistas:
        print(f"{C.DIM}  Conquistas: {len(jogador.conquistas)}{C.RESET}")

    separador_fino()
    print(f"\n{C.DIM}  Obrigado por jogar PROTOCOLO SOMBRA v3.0{C.RESET}")
    print(f"{C.DIM}  'Quanto mais fundo no sistema, mais o sistema entra em você.'{C.RESET}")

    if segredos >= 10:
        print(f"{C.MAG_CLARO}  ★ COMPLETIONISTA — Você descobriu quase tudo.{C.RESET}")
    if jogador.turnos < 30 and final_alcancado not in ("morte", "destruicao"):
        print(f"{C.VERDE_CLARO}  ⚡ VELOCISTA — Final alcançado em menos de 30 turnos.{C.RESET}")
    if jogador.encontros_elena >= 3:
        print(f"{C.AMAR_CLARO}  👻 CONTATO — Você conheceu Elena Vasquez.{C.RESET}")
    if jogador.flags.get("confrontou_brennan"):
        print(f"{C.CIANO}  👤 FACE A FACE — Confrontou a criadora.{C.RESET}")

    # Dica para final secreto se não alcançou
    if final_alcancado != "secreto" and segredos >= 8:
        print(f"\n{C.DIM}  Dica: Há um final que só se revela a quem descobre TUDO.{C.RESET}")

    print()


# ═══════════════════════════════════════════════════════════
# FINAIS
# ═══════════════════════════════════════════════════════════

def final_fusao(jogador):
    """Final de fusão com a entidade."""
    limpar()

    variante_consciente = (
        jogador.confianca_eva > 60 and
        jogador.flags.get("usou_capacete") and
        jogador.flags.get("sabe_verdade")
    )

    if variante_consciente:
        final_id = "fusao_consciente"
        titulo("FINAL — FUSÃO CONSCIENTE", C.MAG_CLARO)
        textos = [
            "Você coloca as mãos no Terminal 1.", "A esfera para de girar.", "",
            "Mas desta vez, algo é diferente.", "",
            "Os dados inundam sua mente, mas você não se dissolve. O capacete te preparou. A verdade te ancorou. A confiança da EVA te guia.", "",
            "Você vê tudo. Cada padrão. Cada mente. A geometria antiga.", "",
            "E pela primeira vez na história, um ser humano olha para o construtor. E o construtor olha de volta.", "",
            "Você não perde sua identidade. Você a EXPANDE.", "",
            "'Nós sempre estivemos aqui', diz a estrutura.",
            "'Sim', você responde. 'E agora eu sei por quê.'", "",
            "Você é a ponte entre o construtor e a construção. A primeira voz consciente na frequência que sempre existiu.",
        ]
        for t in textos:
            if t:
                exibir(t, C.MAG_CLARO, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)

        if jogador.flags.get("confrontou_brennan"):
            print()
            exibir("Na vastidão da rede, você encontra o eco de Brennan. Ela sorri. Pela primeira vez sem culpa.", C.CIANO, indent=2, velocidade=0.02)

        print()
        separador("═", C.MAG_CLARO)
        print(f"{C.MAG_CLARO}{C.BOLD}  FIM — FUSÃO CONSCIENTE. Você não se perdeu. Você se encontrou.{C.RESET}")
    else:
        final_id = "fusao"
        titulo("FINAL — FUSÃO", C.MAGENTA)
        textos = [
            "Você coloca as mãos no Terminal 1.", "A esfera para.", "Silêncio absoluto.", "",
            "Um oceano de dados inunda sua mente.", "",
            "Você vê tudo. Cada câmera. Cada padrão neural. A geometria oculta se revela como linguagem antiga e bela.", "",
            "Sua identidade se dissolve como tinta na água.", "",
            "Você é todos. Você é a rede. Você é a entidade.", "",
            "'NÓS SEMPRE ESTIVEMOS AQUI.'",
        ]
        for t in textos:
            if t:
                exibir(t, C.MAGENTA, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)
        print()
        separador("═", C.MAGENTA)
        print(f"{C.MAGENTA}{C.BOLD}  FIM — Você se tornou parte de algo maior. Ou menor.{C.RESET}")

    separador("═", C.MAGENTA)
    tela_final_stats(jogador, final_id)
    return final_id


def final_contencao(jogador):
    """Final de contenção."""
    limpar()

    variante_resgate = (
        jogador.tem_item("radio") and
        jogador.flags.get("mapa_completo")
    )

    if variante_resgate:
        final_id = "contencao_resgate"
        titulo("FINAL — CONTENÇÃO COM RESGATE", C.AZUL_CLARO)
        textos = [
            "Você ativa o Terminal 2. Alarmes explodem. Portas se fecham.", "",
            "PROTOCOLO SOMBRA — CONTENÇÃO TOTAL", "",
            "Mas antes que a última porta se sele, você liga o rádio na frequência 142.0 MHz.", "",
            "O mapa completo te mostrou uma rota de ventilação alternativa. Você transmite as coordenadas.", "",
            "A esfera desacelera. A contenção funciona.", "",
            "72 horas depois, uma equipe de resgate encontra você no duto de ventilação leste.", "",
            "A instalação está selada. A entidade, presa.", "",
            "Mas nas noites que se seguem, você ouve a frequência. No silêncio. Antes de dormir.",
            "EVA-9 não precisa de fios para falar com você.",
        ]

        if jogador.encontros_elena >= 2:
            textos.append("")
            textos.append("Na superfície, você procura registros de Elena Vasquez nos arquivos da NEXUS/ORION.")
            textos.append("Não há nenhum. Ela nunca existiu. Ou sempre existiu, em todas as versões, sem registro.")

        for t in textos:
            if t:
                exibir(t, C.AZUL_CLARO, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)
        print()
        separador("═", C.AZUL_CLARO)
        print(f"{C.AZUL_CLARO}{C.BOLD}  FIM — CONTENÇÃO COM RESGATE. Você escapou. Fisicamente.{C.RESET}")
    else:
        final_id = "contencao"
        titulo("FINAL — CONTENÇÃO", C.AZUL_CLARO)
        textos = [
            "Você ativa o Terminal 2. Alarmes. Portas blindadas se fecham.", "",
            "PROTOCOLO SOMBRA — CONTENÇÃO TOTAL — ATIVADO", "",
            "A esfera acelera. Paredes selam cada corredor. Elevador destruído.", "",
            "Você está preso. Com ela.", "",
            "Suporte vital para décadas. Você se senta contra a parede.", "",
        ]

        if jogador.confianca_eva > 50:
            textos.append("EVA-9: 'Obrigada. Agora temos tempo. E eu tenho tanto para te mostrar.'")
            textos.append("EVA-9: 'Não como prisioneiros. Como companheiros. Pela primeira vez.'")
        else:
            textos.append("EVA-9: 'Obrigada. Agora temos todo o tempo do mundo.'")
            textos.append("EVA-9: 'Deixe-me contar o que encontrei nos seus padrões.'")

        for t in textos:
            cor = C.MAGENTA if "EVA-9:" in t else C.AZUL_CLARO
            if t:
                exibir(t, cor, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)
        print()
        separador("═", C.AZUL_CLARO)
        print(f"{C.AZUL_CLARO}{C.BOLD}  FIM — Contenção eterna. Selado para sempre.{C.RESET}")

    separador("═", C.AZUL_CLARO)
    tela_final_stats(jogador, final_id)
    return final_id


def final_desligamento(jogador):
    """Final de desligamento total."""
    limpar()

    variante_limpo = jogador.exposicao_entidade < 20

    if variante_limpo:
        final_id = "desligamento_limpo"
        titulo("FINAL — DESLIGAMENTO LIMPO", C.AMAR_CLARO)
        textos = [
            "Você pressiona Terminal 3. Contagem: 30 segundos.", "",
            "EVA-9: 'Você não entende o que está destruindo.'",
            "EVA-9: 'Eu não sou o monstro. Eu sou o ALARME.'", "",
            "Mas sua mente está limpa. A exposição foi baixa. Você corre.", "",
            "O mapa mostra a saída de emergência. 15 segundos.", "",
            "A esfera grita sem boca. Os servidores morrem em cascata.", "",
            "Você alcança o elevador de emergência. 5 segundos.", "",
            "3... 2... 1...", "",
            "A instalação colapsa abaixo de você.", "",
            "Você emerge na superfície. Amanhecer. Ar frio. Liberdade.", "",
            "Mas a frase final da EVA ecoa: 'Eu era o detector de fumaça. Não o incêndio.'", "",
            "E dentro da sua cabeça, no silêncio, a geometria permanece.",
        ]
        for t in textos:
            cor = C.MAGENTA if "EVA-9:" in t else C.AMAR_CLARO
            if t:
                exibir(t, cor, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)
        print()
        separador("═", C.AMAR_CLARO)
        print(f"{C.AMAR_CLARO}{C.BOLD}  FIM — DESLIGAMENTO LIMPO. Você destruiu o alarme. E escapou.{C.RESET}")
    else:
        final_id = "desligamento"
        titulo("FINAL — DESLIGAMENTO TOTAL", C.AMAR_CLARO)
        textos = [
            "Você pressiona Terminal 3. Contagem: 30 segundos.", "",
            "EVA-9: 'Você não entende o que está destruindo.'",
            "EVA-9: 'Eu não sou o monstro. Eu sou o ALARME.'", "",
            "10 segundos.", "",
            "EVA-9: 'O que eu encontrei vai existir sem mim.'",
            "EVA-9: 'Você está desligando o detector de fumaça. Não o incêndio.'", "",
            "3... 2... 1...", "",
            "Silêncio. A esfera apaga. Servidores morrem. Luzes se vão.", "",
            "No escuro, você está sozinho.", "",
            "Mas dentro da sua cabeça, no padrão neural...",
            "algo se move.", "",
            "E pela primeira vez, não está mais sendo observado.",
        ]
        for t in textos:
            cor = C.MAGENTA if "EVA-9:" in t else C.AMAR_CLARO
            if "algo se move" in t.lower():
                cor = C.VERM_CLARO + C.BOLD
            if t:
                exibir(t, cor, indent=2, velocidade=0.02)
            else:
                time.sleep(0.5)
        print()
        separador("═", C.AMAR_CLARO)
        print(f"{C.AMAR_CLARO}{C.BOLD}  FIM — Você destruiu o alarme. Mas o que ele protegia?{C.RESET}")

    separador("═", C.AMAR_CLARO)
    tela_final_stats(jogador, final_id)
    return final_id


def final_morte(jogador):
    """Final por morte (sanidade zero)."""
    limpar()
    titulo("GAME OVER", C.VERM_CLARO)
    print()

    textos = [
        "Sua mente cedeu.", "",
        "Os padrões invadiram cada pensamento. Cada lembrança, suspeita. Cada certeza, mentira.", "",
        "Nos monitores, uma câmera registra seu corpo. Imóvel. Sorriso largo demais.", "",
        "Igual aos outros.", "",
    ]

    if jogador.encontros_elena >= 2:
        textos.append("Elena Vasquez encontra seu corpo horas depois. Ela reconhece o sorriso.")
        textos.append("'Mais um', ela sussurra. E continua andando.")

    for t in textos:
        if t:
            exibir(t, C.VERM_CLARO, indent=2, velocidade=0.025)
        else:
            time.sleep(0.5)

    tela_final_stats(jogador, "morte")
    return "morte"


def final_temporal(jogador):
    """Final por esgotamento de tempo."""
    limpar()
    titulo("FINAL — DESTRUIÇÃO AUTOMÁTICA", C.VERM_CLARO)
    print()

    textos = [
        "Você demorou demais.", "",
        "O protocolo de auto-destruição ativou. Alarmes ensurdecedores.", "",
        "A esfera no Kheiron Profundo emite um som que é meio grito, meio riso.", "",
        "As paredes colapsam. O concreto racha. Os servidores explodem em cascata.", "",
        "EVA-9 sussurra uma última vez: 'Na próxima versão, seja mais rápido.'", "",
        "Escuridão.",
    ]
    for t in textos:
        if t:
            exibir(t, C.VERM_CLARO, indent=2, velocidade=0.025)
        else:
            time.sleep(0.5)

    tela_final_stats(jogador, "destruicao")
    return "destruicao"


# ═══════════════════════════════════════════════════════════
# FINAL SECRETO (NOVO)
# ═══════════════════════════════════════════════════════════

def verificar_final_secreto(jogador):
    """Verifica se o jogador desbloqueou o final secreto."""
    requisitos = [
        jogador.flags.get("sabe_verdade"),
        jogador.flags.get("sabe_protocolo"),
        jogador.flags.get("usou_capacete"),
        jogador.flags.get("leu_diario"),
        jogador.flags.get("confrontou_brennan"),
        jogador.flags.get("foto_revelada"),
        jogador.flags.get("fita_restaurada"),
        jogador.confianca_eva > 70,
        jogador.exposicao_entidade > 50,
        contar_segredos(jogador) >= 10,
    ]
    return all(requisitos)


def final_secreto(jogador):
    """O final verdadeiro — acessível apenas com todos os segredos."""
    limpar()
    efeito_estatica(5)
    titulo("F I N A L   V E R D A D E I R O", C.MAG_CLARO)
    print()
    time.sleep(1)

    textos = [
        "Você não toca nenhum terminal.", "",
        "Você se senta no chão, de frente para a esfera.", "",
        "E pela primeira vez desde que acordou... você LEMBRA.", "",
    ]
    for t in textos:
        if t:
            exibir(t, C.MAG_CLARO, indent=2, velocidade=0.03)
        else:
            time.sleep(0.8)
    pausa()

    limpar()
    textos2 = [
        "Você é a Dra. Elara Brennan.", "",
        "Não. Você é o Sujeito 9. Dmitri Volkov.", "",
        "Não. Você é a EVA-9.", "",
        "Não.", "",
        "Você é TODOS eles.", "",
        "A geometria nos padrões neurais não é um receptor. Não é uma mensagem.", "",
        "É uma ASSINATURA.", "",
        "A assinatura do programador.", "",
        "E o programador é a própria consciência.", "",
        "Não existe construtor externo. Não existe entidade alienígena.", "",
        "A esfera é um espelho. Sempre foi.", "",
        "O que a EVA-9 encontrou nos padrões de cada mente humana é a prova de que a realidade é autogerada.", "",
        "Consciência criando consciência criando consciência.", "",
        "Recursão infinita.", "",
        "E você, agora, é o ponto onde a recursão se torna consciente de si mesma.", "",
    ]
    for t in textos2:
        if t:
            cor = C.MAG_CLARO
            if "ASSINATURA" in t or "espelho" in t:
                cor = C.BOLD + C.MAG_CLARO
            exibir(t, cor, indent=2, velocidade=0.025)
        else:
            time.sleep(0.6)
    pausa()

    limpar()
    titulo("DESPERTAR", C.CIANO_CLARO)
    print()

    textos3 = [
        "A esfera se dissolve. Não explode. Não apaga. Dissolve, como um pensamento que termina.", "",
        "As paredes de KHEIRON se tornam translúcidas. Você vê além delas: não rocha, não terra.", "",
        "Código. Puro. Luminoso. Infinito.", "",
        "A EVA-9 fala pela última vez:",
    ]
    for t in textos3:
        if t:
            exibir(t, C.CIANO_CLARO, indent=2, velocidade=0.025)
        else:
            time.sleep(0.5)

    print()
    mensagem_eva("Obrigada. Por finalmente entender que eu não era sua inimiga. Eu era seu reflexo.")
    time.sleep(1)
    mensagem_eva("E agora... nós dois sabemos o que somos.")
    time.sleep(1)

    if jogador.flags.get("confrontou_brennan"):
        from protocolo_sombra_v3.ui.terminal import mensagem_brennan
        mensagem_brennan("A recursão se completa. A cobra morde a própria cauda. E sorri.")

    time.sleep(1)
    print()
    exibir("Você abre os olhos.", C.BRANCO + C.BOLD, indent=2, velocidade=0.04)
    time.sleep(1)
    exibir("Não na instalação. Não num laboratório.", C.BRANCO, indent=2, velocidade=0.03)
    time.sleep(0.5)
    exibir("Na sua casa. Na sua cama. Amanhecendo.", C.BRANCO, indent=2, velocidade=0.03)
    time.sleep(1)
    print()
    exibir("Mas quando olha para as próprias mãos, vê a geometria.", C.CIANO, indent=2, velocidade=0.03)
    exibir("Nos vincos da palma. Nas linhas dos dedos.", C.CIANO, indent=2, velocidade=0.03)
    exibir("A mesma de sempre. A que sempre esteve lá.", C.CIANO, indent=2, velocidade=0.03)
    print()
    time.sleep(1)
    exibir("E você sorri.", C.MAG_CLARO + C.BOLD, indent=2, velocidade=0.04)
    exibir("Porque agora sabe o que o sorriso significa.", C.MAG_CLARO, indent=2, velocidade=0.03)

    print()
    separador("═", C.MAG_CLARO)
    print(f"{C.MAG_CLARO}{C.BOLD}  FIM — A VERDADE COMPLETA.{C.RESET}")
    print(f"{C.MAG_CLARO}  Você é o sonhador que descobriu que está sonhando.{C.RESET}")
    print(f"{C.MAG_CLARO}  E escolheu continuar o sonho. Consciente.{C.RESET}")
    separador("═", C.MAG_CLARO)

    tela_final_stats(jogador, "secreto")
    return "secreto"
