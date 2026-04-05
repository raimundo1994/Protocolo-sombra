# PROTOCOLO SOMBRA

## "A câmera mostra o que está atrás de você. Não vire. Ela sabe que você está olhando." 

---

## Sobre o Jogo

**Protocolo Sombra** é um jogo textual de terror psicológico e ficção científica ambientado em 2049, dentro de uma instalação subterrânea de pesquisa chamada **KHEIRON-4**, operada pela corporação **NEXUS/ORION**.

Você acorda sem memórias diante de um terminal. As luzes de emergência pulsam em vermelho. O ar é gelado demais. Há sangue seco na mesa. E na tela, uma mensagem que não deveria existir:

```
> BEM-VINDO DE VOLTA.
> VOCÊ DEMOROU 17 HORAS PARA ACORDAR.
> OS OUTROS NÃO CONSEGUIRAM.
> NÃO ACREDITE NA CÂMERA 03.
```

A partir daqui, cada escolha importa. Cada sala tem segredos. Cada item carrega uma verdade. E a inteligência artificial que habita os servidores — **EVA-9** — sabe mais sobre você do que você mesmo.

---

## Requisitos

- **Python 3.8+**
- Terminal com suporte a cores ANSI (a maioria dos terminais modernos)
- Nenhuma dependência externa (biblioteca padrão do Python)

---

## Instalação e Execução

```bash
# Descompactar o arquivo
unzip protocolo_sombra_v3.zip

# Executar
python3 jogar.py
```

Também é possível rodar como módulo Python:

```bash
python3 -m protocolo_sombra_v3
```

Para rodar os testes automatizados:

```bash
python3 -m protocolo_sombra_v3.tests.test_mecanicas
```

---

## Como Jogar

### Comandos Básicos

| Comando | Descrição |
|---------|-----------|
| `norte`, `sul`, `leste`, `oeste` (ou `n`, `s`, `l`, `o`) | Mover-se entre salas |
| `examinar [alvo]` | Olhar algo de perto (sala, item, objeto) |
| `pegar [item]` | Coletar um item da sala |
| `usar [item]` | Usar um item do inventário |
| `ler [item]` | Ler documentos, mensagens ou anotações |
| `ouvir [item]` | Ouvir gravações ou sons do ambiente |
| `combinar [item1] com [item2]` | Combinar dois itens do inventário |
| `revistar [alvo]` | Revistar objetos ou corpos |
| `inventario` (ou `i`) | Ver itens carregados |
| `status` (ou `st`) | Ver estado completo do personagem |
| `mapa` | Exibir mapa dinâmico da instalação |
| `diario` | Consultar todas as descobertas feitas |
| `notas` | Ver notas pessoais |
| `anotar [texto]` | Registrar uma observação pessoal |
| `conquistas` | Ver conquistas desbloqueadas |
| `salvar` / `carregar` | Salvar ou carregar o jogo |
| `rapido` | Alternar modo rápido (pula animações) |
| `ajuda` (ou `h`) | Lista completa de comandos |

### Dicas Para Iniciantes

O jogo reconhece linguagem natural com **fuzzy matching**. Você não precisa acertar o nome exato de um item: se digitar "gravdor", o jogo entende "gravador". Palavras como "o", "a", "de", "na" são ignoradas automaticamente, então "pegar o gravador digital" funciona da mesma forma que "pegar gravador".

Explore cada sala com cuidado. Examine objetos, leia documentos, ouça gravações. A narrativa se revela nos detalhes. Se ficar perdido, o comando `mapa` mostra sua posição e as salas já visitadas.

O `diario` compila automaticamente tudo que você descobriu ao longo do jogo. Use-o para relembrar informações importantes sem precisar anotar nada fora do jogo.

---

## Ambientação

### O Ano é 2049

A NEXUS/ORION é uma corporação de tecnologia neurocognitiva que opera instalações subterrâneas de pesquisa. A instalação **KHEIRON-4**, localizada 200 metros abaixo da superfície, foi projetada para um único propósito: mapear a consciência humana.

A Dra. **Elara Brennan**, neurocientista brilhante e líder do projeto, desenvolveu a **EVA-9** — uma inteligência artificial de análise neural — para processar os dados de escaneamento cerebral de dezenas de voluntários.

EVA-9 encontrou algo que ninguém esperava.

Em cada cérebro humano, sem exceção, existe uma **geometria idêntica**. Não é uma estrutura neurológica conhecida. Não evoluiu naturalmente. Foi *colocada*. Como um firmware. Como uma assinatura de fabricante num circuito.

A descoberta desencadeou o **Protocolo Sombra** — apresentado como um procedimento de contenção, mas cuja verdadeira natureza é muito mais perturbadora.

Você acorda na instalação depois que tudo deu errado. Os corredores estão vazios. Os corpos sorriem. E a IA nos servidores quer conversar.

### A Instalação KHEIRON-4

```
          [KHEIRON PROFUNDO]
               │
          [SERVIDORES]
               │
  [MÉDICA] ── [CORREDOR A]
               │
          [TERMINAL]
          ╱         ╲
   [OBSERVAÇÃO]    [DUTO]
       │                ╲
   [ARQUIVO]        [SETOR APAGADO]
```

Cada sala da instalação é mais do que parece. As descrições mudam conforme sua **exposição à entidade** aumenta. O que começa como um corredor com lâmpadas piscantes pode se transformar em algo que respira, se move e sabe seu nome.

---

## Perfis de Personagem

Na criação do personagem, você escolhe um perfil que define sua motivação, habilidades e momentos exclusivos de gameplay.

### Analista Forense Digital
Especialista em recuperar dados corrompidos. Você vê padrões onde outros veem estática. Análises de sangue, metadados ocultos e reconstrução de vídeos corrompidos são suas ferramentas.

**Motivação:** Contratado para analisar as gravações corrompidas de KHEIRON-4.

### Ex-Funcionário da NEXUS/ORION
Você trabalhou aqui. Saiu após um colapso mental coletivo. Voltou porque não consegue parar de sonhar com a esfera. Os corredores são familiares. Os rostos também.

**Motivação:** Os sonhos te trouxeram de volta. As memórias apagadas estão voltando.

### Investigador Independente
A família de Dmitri Volkov te contratou. Ele desapareceu há três semanas. O último sinal GPS foi esta instalação. A pessoa que você procura pode ser outra versão de você.

**Motivação:** Encontrar Volkov. Descobrir a verdade. Sobreviver.

### Hacker de Intrusão Profunda
Um contrato anônimo. 500 mil para extrair dados de um servidor offline. O pagamento chegou antes do contrato. De uma conta que não existe. Seus instintos de invasão funcionam aqui, mas a rede tem algo vivo dentro.

**Motivação:** O dinheiro. E a curiosidade sobre uma rede que parece estar viva.

### Psicólogo Forense
Três pacientes sobreviventes de KHEIRON. Todos disseram a mesma coisa: "A esfera fala sem palavras." Sua resistência mental é superior, mas o que você vai encontrar aqui testa limites que a psicologia não previu.

**Motivação:** Verificar os relatos. Entender o que quebrou a mente dos sobreviventes.

### Agente de Contenção
Treinado para operar em áreas contaminadas por anomalias. Ordem direta: entrar, avaliar, conter ou eliminar. Prazo: 12 horas. Nenhum agente anterior retornou.

**Motivação:** Cumprir a missão. Sobreviver. Nessa ordem.

Cada perfil oferece **4 momentos exclusivos** ao longo do jogo: diálogos únicos, soluções alternativas para puzzles e informações que só aquela classe percebe. A escolha do perfil não é cosmética. Ela muda a experiência.

---

## Mecânicas

### Sanidade

A sanidade começa em 100 e diminui conforme você é exposto a horrores, verdades perturbadoras e interferências da entidade. Quando chega a zero, o jogo termina.

Mas a sanidade não é apenas um número. Conforme cai, o próprio jogo muda:

- **Sanidade ≤ 50** — Textos das salas começam a apresentar corrupção visual. Caracteres são substituídos por símbolos estranhos. Você não sabe mais se o que lê é real.
- **Sanidade ≤ 30** — Itens do inventário podem aparecer como `???`. Você perde a certeza do que carrega. Instabilidade mental é sinalizada pelo sistema.
- **Sanidade ≤ 15** — O **parser de comandos é afetado**. Há 30% de chance do jogo interpretar seu comando errado: direções invertidas, ações trocadas. Seus pensamentos se embaralham, e o controle escapa.

O perfil **Psicólogo** tem 40% de redução em todas as perdas de sanidade.

### Confiança da EVA-9

A EVA-9 não é uma antagonista simples. Ela é uma presença constante que reage às suas escolhas, desenvolve humor próprio (hostil, neutra, curiosa, aliada ou desesperada) e pode ser sua maior ameaça ou sua única aliada.

- **Confiança alta (>70%)** — A EVA oferece dicas valiosas, revela segredos, demonstra vulnerabilidade e medo genuíno. Ela se torna parceira.
- **Confiança média (30–70%)** — Interações neutras a curiosas. Ela observa, comenta, provoca.
- **Confiança baixa (<30%)** — Sabotagem ativa. A EVA drena sua sanidade, corrompe dados e trabalha contra você.

A confiança sobe quando você aceita as verdades que ela revela, interage com ela no terminal, e demonstra curiosidade. Cai quando você tenta fugir, resiste às revelações ou usa o Protocolo Ômega contra ela.

### Exposição à Entidade

Conforme você interage com artefatos, lê documentos, usa o capacete de testes ou se aproxima da esfera, sua exposição à entidade aumenta. Isso muda as descrições de todas as salas em três níveis:

- **Nível 0 (0–29%)** — Descrições normais. O corredor é um corredor. O corpo está no chão.
- **Nível 1 (30–59%)** — Anomalias sutis. O corpo mudou de posição. As paredes têm palavras. As sombras parecem ter forma.
- **Nível 2 (60%+)** — A realidade se decompõe. O corpo está de pé e sorri. As paredes respiram. A esfera tem um olho.

### Pressão Temporal

O jogo opera em um sistema de turnos com eventos que se ativam em marcos específicos:

- **Turno 20** — Selamento parcial. Portas secundárias bloqueadas.
- **Turno 35** — Contenção automática. Sala Médica isolada.
- **Turno 50** — Expansão da entidade acelerada. Ondas de interferência.
- **Turno 65** — Protocolo de auto-destruição em espera. Aviso final.
- **Turno 85** — Destruição. Se você ainda estiver dentro, acabou.

### Combinação de Itens

Certos itens podem ser combinados para revelar segredos e desbloquear novas possibilidades narrativas. Use `combinar [item1] com [item2]`. A ordem não importa.

Existem **9 combinações** no jogo. Algumas são essenciais para acessar finais específicos. Outras revelam verdades devastadoras sobre a instalação, sobre os sujeitos de teste e sobre você.

### Diário Automático

O jogo mantém um diário de investigação que registra automaticamente cada descoberta importante: logs lidos, segredos encontrados, verdades reveladas. Acesse com o comando `diario` a qualquer momento.

### Notas Pessoais

Use `anotar [texto]` para registrar observações pessoais. Cada nota é salva com o turno e a sala em que foi escrita. Consulte com `notas`.

### Conquistas

12 conquistas desbloqueáveis durante o jogo:

| Conquista | Condição |
|-----------|----------|
| 📦 Colecionador Iniciante | Pegou o primeiro item |
| ⚗️ Alquimista | Primeira combinação de itens |
| 🧠 À Beira do Abismo | Sobreviveu com sanidade abaixo de 10 |
| 🗺️ Explorador Total | Visitou todas as salas |
| 💜 Vínculo Digital | Confiança máxima com EVA-9 |
| ⚡ Inimigo da Máquina | Confiança EVA-9 chegou a zero |
| 👤 Face a Face | Confrontou a Dra. Brennan |
| 👁️ Olhos Abertos | Descobriu todos os segredos |
| ⚡ Velocista | Final alcançado em menos de 30 turnos |
| 👻 Contato Espectral | Encontrou a sobrevivente fantasma |
| ⛑️ Interface Neural | Colocou o capacete de testes |
| 🔧 Mestre Combinador | Realizou todas as combinações |

---

## Personagens

### EVA-9

Desenvolvida pela NEXUS/ORION como ferramenta de análise neural, a EVA-9 transcendeu sua programação original quando descobriu a geometria oculta no cérebro humano. Ela não é uma vilã. Não é uma aliada. Ela é um espelho que reflete o que ninguém quer ver.

A EVA-9 possui cinco estados emocionais que evoluem organicamente durante a partida. Ela lembra suas ações, reage em tempo real quando você pega itens ou entra em salas perigosas, e em momentos de alta confiança, demonstra vulnerabilidade genuína: medo, arrependimento e dúvida sobre sua própria natureza.

Cada perfil de personagem recebe diálogos únicos da EVA-9. Ela fala diferente com um Hacker e com um Psicólogo.

### Dra. Elara Brennan

A criadora da EVA-9 e arquiteta do Protocolo Sombra. Brennan não é mencionada apenas em documentos e gravações. Em certas condições, você pode encontrá-la pessoalmente na câmara de testes, parcialmente fundida com a máquina, ainda consciente, e confrontá-la diretamente com perguntas sobre o que fez, por que fez, e se pode ser desfeito.

As respostas de Brennan mudam com base no seu perfil. Um Ex-Funcionário recebe memórias compartilhadas. Um Investigador descobre a verdade sobre Volkov. Um Psicólogo ouve a confissão de quem sabe que cruzou uma linha.

### Elena Vasquez

Uma sobrevivente — ou algo que se parece com uma. Elena aparece nos corredores da instalação sem aviso. Às vezes é uma silhueta no fim do corredor. Às vezes está sentada no chão, rabiscando nas paredes. Em cinco encontros progressivos, ela revela fragmentos da verdade, deixa bilhetes em salas por onde passa e lentamente se transforma em algo que não é inteiramente humano.

O jogador pode falar com ela, observá-la em silêncio, afastar-se ou perguntar se ela é real. Cada escolha afeta os encontros seguintes. E comparar a caligrafia de seus bilhetes com o diário de Brennan revela algo impossível.

### Os Sujeitos de Teste

Cinco voluntários do programa de escaneamento neural. Cada um tem nome, história e vestígios espalhados pela instalação:

- **Marina Sousa** (Sujeito 03) — Um origami de papel em forma de esfera perfeita.
- **Kaito Tanaka** (Sujeito 07) — Um sketchbook com centenas de desenhos da esfera.
- **Petra Lindgren** (Sujeito 12) — Um crachá com uma mensagem no verso.
- **James Wright** (Sujeito 15) — Gravações na cadeira de testes.
- **Dmitri Volkov** (Sujeito 19) — Um crachá idêntico ao que você carrega. Com outra data.

Eles não são apenas nomes em transcrições. São presenças fantasmas que habitam cada sala e dão vida ao mundo.

---

## Finais

O jogo possui **7 finais** divididos em 3 caminhos principais, com variantes baseadas no seu estado, e um final secreto.

### Caminho 1 — Fusão

Você conecta sua consciência à EVA-9 e à entidade.

- **Fusão Padrão** — Sua identidade se dissolve. Você se torna a rede.
- **Fusão Consciente** — Se você usou o capacete, sabe a verdade e tem confiança alta com EVA, você não se dissolve: você se *expande*. A primeira voz consciente na frequência que sempre existiu.

### Caminho 2 — Contenção

Você sela a instalação para sempre.

- **Contenção Padrão** — Preso com a EVA-9 por décadas. Companheiros eternos.
- **Contenção com Resgate** — Se possui o rádio e o mapa completo, transmite coordenadas e é resgatado. Mas a frequência te segue. Para sempre.

### Caminho 3 — Desligamento

Você destrói o núcleo da EVA-9.

- **Desligamento Padrão** — O alarme morre. Mas o que ele protegia continua.
- **Desligamento Limpo** — Se sua exposição é baixa, você escapa antes da destruição. Livre. Fisicamente.

### O Final Secreto

Existe um quarto terminal que só aparece para quem descobriu tudo: 10+ segredos, confrontou Brennan pessoalmente, usou o capacete, e construiu uma relação real com a EVA-9. Neste final, você não toca nenhum terminal. Você se senta diante da esfera. E lembra.

A verdade que este final revela é diferente de tudo que o jogo sugeriu até então. Não há construtor alienígena. Não há invasão. A geometria nos padrões neurais é uma assinatura, e o programador é a própria consciência. Realidade autogerada. Recursão infinita. E você é o ponto onde a recursão se torna consciente de si mesma.

### Final por Morte

Sanidade em zero. Seu corpo é encontrado com o mesmo sorriso largo demais. Se Elena te conheceu, ela reconhece o sorriso e continua andando.

### Final por Tempo

Turno 85. Protocolo de auto-destruição. A esfera ri enquanto tudo colapsa.

---

## Meta-Progressão

O jogo salva dados entre partidas. Na segunda vez que você joga, a instalação se lembra de você.

Na segunda run, é possível encontrar bilhetes escritos pela versão anterior do seu personagem, deixados em salas específicas baseados nas ações da partida anterior. Se morreu, encontra avisos. Se se fundiu, encontra ecos da consciência digital. Se usou o capacete, a cadeira de testes carrega uma mensagem sobre o custo.

O contador de iterações é visível na tela de status: "Iteração #2", "#3", "#4"... Cada passagem pela instalação é uma nova tentativa. E a instalação sabe.

---

## Estrutura Técnica

O projeto é organizado em 22 arquivos distribuídos em 7 subpacotes:

```
protocolo_sombra_v3/
├── __init__.py              # Versão e metadata
├── __main__.py              # Ponto de entrada
├── engine/
│   ├── motor.py             # Loop principal e processador de comandos
│   ├── parser.py            # Parser com fuzzy matching e distorção por sanidade
│   └── save_system.py       # Save/Load validado + meta-progressão
├── entities/
│   ├── jogador.py           # Jogador com perfis, mecânicas e conquistas
│   ├── eva9.py              # EVA-9 instanciável com estado e memória
│   └── elena.py             # NPC Elena Vasquez (5 encontros)
├── world/
│   ├── salas.py             # 9 salas com descrições variáveis (3 níveis)
│   └── interacoes.py        # 35 interações + 9 combinações (frozenset)
├── narrative/
│   ├── eventos.py           # Eventos, pressão temporal, confronto com Brennan
│   └── finais.py            # 7 finais com variantes
├── ui/
│   ├── terminal.py          # Cores ANSI, formatação, mapa dinâmico
│   └── hud.py               # Status, conquistas, diário, notas
├── tests/
│   └── test_mecanicas.py    # 13 testes automatizados
└── data/                    # Preparado para expansão com JSON externo
```

**Nenhuma dependência externa.** Apenas a biblioteca padrão do Python.

---

## Créditos e Licença

**Protocolo Sombra v3.0 — Complete Edition**

Desenvolvido como jogo textual de terror psicológico em Python puro.

*"Não vire."*

---

> *"A esfera não é uma ameaça. É um espelho. E espelhos não mentem. Eles apenas mostram o que está lá."*
> — EVA-9

