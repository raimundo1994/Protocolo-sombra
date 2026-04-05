# PROTOCOLO SOMBRA v3.0 — COMPLETE EDITION

## Como Executar

```bash
python3 jogar.py
```

Ou como módulo:
```bash
python3 -m protocolo_sombra_v3
```

Rodar testes:
```bash
python3 -m protocolo_sombra_v3.tests.test_mecanicas
```

---

## Changelog v2.0 → v3.0

### ARQUITETURA
- **Código modularizado** em 22 arquivos, 7 subpacotes (era 1 arquivo monolítico de 1900 linhas, agora são 5028 linhas organizadas)
- **Estrutura de pacotes**: `engine/`, `entities/`, `world/`, `narrative/`, `ui/`, `data/`, `tests/`
- **MotorJogo refatorado**: responsabilidades separadas em Parser, SaveSystem, HUD
- **EVA-9 instanciável**: não mais estática — possui estado, memória de interações, humor acumulado
- **Combinações com `frozenset`**: eliminada duplicação de ordem — `("a","b")` e `("b","a")` são automaticamente a mesma chave
- **Sistema de logging** integrado via `logging` module

### PARSER DE COMANDOS (NOVO)
- **Fuzzy matching** com `difflib.get_close_matches` — "gravdor" encontra "gravador"
- **Remoção de stopwords** — "pegar o gravador digital rachado" funciona
- **Aliases expandidos** — 60+ aliases incluindo "vasculhar", "inspecionar", "caminhar", etc.
- **Distorção por sanidade** — com sanidade ≤15, 30% de chance do comando ser interpretado errado (direções trocadas, ações invertidas)
- **Auto-detecção de interações** — se o verbo não é reconhecido, tenta como interação da sala

### MECÂNICAS DO JOGADOR
- **Sanidade com efeitos mecânicos reais**:
  - ≤50: textos das salas começam a ter glitches visuais
  - ≤30: inventário pode mostrar itens "corrompidos" (???)
  - ≤15: parser distorce comandos, alucinações textuais
  - Perfil Psicólogo reduz 40% das perdas de sanidade
- **Perfis com impacto mecânico real**: cada perfil tem motivação pessoal, diálogo único com EVA-9, 4 momentos exclusivos de gameplay
- **Sistema de notas pessoais** — `anotar [texto]` para registrar observações
- **Conquistas** — 12 conquistas desbloqueáveis com tracking visual

### NPC: ELENA VASQUEZ (NOVO)
- **Sobrevivente fantasma** que aparece e desaparece em certas salas
- **5 encontros progressivos** com diálogos únicos e evolução da personagem
- **Sistema de confiança** independente da EVA-9
- **Bilhetes** deixados em salas após primeiro encontro
- **Opção de questionar se ela é real** (encontro 3+)
- **Conexão narrativa** com Brennan (mesma caligrafia — combinação bilhete+diário revela)

### EVA-9 EXPANDIDA
- **5 humores**: hostil, neutra, curiosa, aliada, desesperada (era 3 níveis estáticos)
- **Memória de interações**: lembra ações do jogador, evita repetir frases
- **Momentos de vulnerabilidade**: quando confiança alta + verdade revelada, EVA demonstra medo real
- **Frases por perfil**: cada classe recebe comentários personalizados
- **Reações a ações**: EVA comenta em tempo real sobre pegar itens, entrar em salas perigosas, usar seringa
- **Frequência variável**: intervém mais frequentemente quando desesperada ou quando exposição alta

### NARRATIVA
- **Confronto direto com Dra. Brennan**: interação completa na câmara de testes, com diálogo de múltipla escolha e reações por perfil
- **Motivações pessoais por perfil**: cada classe tem razão única para estar em KHEIRON-4
- **Sujeitos de teste com identidade**: Marina Sousa, Kaito Tanaka, Petra Lindgren, James Wright, Dmitri Volkov — cada um com vestígios encontráveis em salas específicas
- **Bilhetes de Elena** em salas com dicas contextuais
- **Ecos de runs anteriores** (meta-progressão)

### FINAIS
- **Final Secreto** — "A Verdade Completa": acessível com 10+ segredos, confronto com Brennan, capacete usado, confiança EVA >70. Revela que a realidade é autogerada.
- **Variantes expandidas**: finais agora referenciam Elena, Brennan, e ações específicas do jogador
- **Tela de estatísticas expandida**: mostra conquistas, run number, dicas para final secreto

### META-PROGRESSÃO (NOVO)
- **Persistência entre runs**: ações marcantes são salvas em `meta_protocolo_sombra.json`
- **Ecos narrativos**: na segunda run, encontra bilhetes e mensagens deixadas pela versão anterior de si mesmo
- **Contador de iterações**: o jogo sabe quantas vezes você jogou e quais finais alcançou

### QUALIDADE DE VIDA
- **Mapa dinâmico** — comando `mapa` mostra posição atual, salas visitadas, portas trancadas
- **Diário automático** — comando `diario` compila todas as descobertas em texto narrativo
- **Modo rápido** — comando `rapido` pula todas as animações (toggle)
- **Autosave** a cada 10 turnos
- **Save/Load com validação** de schema, ranges e tipos
- **13 testes automatizados** cobrindo parser, mecânicas, combinações, perfis, finais

### NOVOS ITENS E COMBINAÇÕES
- 5 novos itens: bilhete de Elena, fragmento de memória, chave de Brennan, amostra neural, decodificador
- 4 novas combinações: rádio+decodificador, seringa+amostra, bilhete+diário, fragmento+capacete
- Interações expandidas: 35 interações data-driven (era ~25)

---

## Estrutura de Arquivos

```
protocolo_sombra_v3/
├── __init__.py          # Versão e metadata
├── __main__.py          # Entry point
├── engine/
│   ├── motor.py         # Loop principal e delegação (~750 linhas)
│   ├── parser.py        # Parser fuzzy com distorção (~200 linhas)
│   └── save_system.py   # Save/Load + meta-progressão (~250 linhas)
├── entities/
│   ├── jogador.py       # Jogador com mecânicas expandidas (~350 linhas)
│   ├── eva9.py          # EVA-9 instanciável com estado (~300 linhas)
│   └── elena.py         # NPC Elena Vasquez (~250 linhas)
├── world/
│   ├── salas.py         # 9 salas com descrições variáveis (~350 linhas)
│   └── interacoes.py    # 35 interações + 9 combinações (~550 linhas)
├── narrative/
│   ├── eventos.py       # Eventos, pressão temporal, Brennan (~400 linhas)
│   └── finais.py        # 7 finais com variantes (~400 linhas)
├── ui/
│   ├── terminal.py      # Cores, formatação, mapa dinâmico (~250 linhas)
│   └── hud.py           # Status, conquistas, diário (~250 linhas)
├── tests/
│   └── test_mecanicas.py # 13 testes automatizados (~250 linhas)
└── data/                # Preparado para JSON externo (futuro)
```
