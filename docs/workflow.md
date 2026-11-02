# Fluxo de desenvolvimento

## Visão geral

Pense numa cozinha de restaurante que não improvisa. Cada pedido (a **issue**) primeiro vira uma ficha dizendo o que o cliente quer e por quê (a **spec**). Depois o chef decide como vai preparar (o **plano**) e quebra o preparo em passos (as **tarefas**). Antes de cozinhar cada passo, ele escreve como vai provar que ficou certo (o **teste**), e só então cozinha. No fim, o prato vai para a mesa com a ficha anexada (o **pull request**).

No Desvenda, toda mudança passa por esse caminho. Isso deixa cada decisão registrada, cada comportamento provado por um teste e cada passo pequeno o bastante para ser acompanhado. As regras vêm da [constituição](../.specify/memory/constitution.md): Princípios I (SDD), II (TDD) e VIII (documentação viva), e a seção "Fluxo de desenvolvimento e portões de qualidade".

## O ciclo de uma issue

```mermaid
graph TD
    I["Issue #N no GitHub"] --> B["Branch NNN-nome"]
    B --> S["/speckit-specify: spec.md"]
    S --> C{"Sobrou NEEDS CLARIFICATION?"}
    C -->|sim| CL["/speckit-clarify"]
    CL --> P
    C -->|não| P["/speckit-plan: plan.md e anexos"]
    P --> T["/speckit-tasks: tasks.md, testes antes"]
    T --> A["/speckit-analyze: consistência"]
    A --> TDD["Ciclos vermelho, verde e refatorar"]
    TDD --> D["Agente doc-sync-onboarding: atualizar docs/"]
    D --> PR["PR com Closes #N e O que aprendi"]
    PR --> G{"Portões de qualidade"}
    G -->|ok| M["Merge na main"]
    G -->|falhou| TDD
```

## Passo a passo

O exemplo usa a issue #1, "Monorepo e ferramentas do backend". NNN é o número da issue com três dígitos.

| # | Passo | Comando ou ação | Resultado |
|---|---|---|---|
| 1 | Pegar a próxima issue do milestone atual | GitHub | Número e texto da issue |
| 2 | Criar a branch | `git switch -c 001-monorepo-ferramentas` | Branch com o número da issue |
| 3 | Especificar | `/speckit-specify <texto da issue> SPECIFY_FEATURE_DIRECTORY=specs/001-monorepo-ferramentas` | `specs/001-monorepo-ferramentas/spec.md`, `checklists/requirements.md` e `.specify/feature.json` |
| 4 | Esclarecer, se preciso | `/speckit-clarify` | Respostas gravadas na spec |
| 5 | Planejar | `/speckit-plan` | `plan.md` e, quando fizer sentido, `research.md`, `data-model.md`, `contracts/` e `quickstart.md` |
| 6 | Quebrar em tarefas | `/speckit-tasks` | `tasks.md`, com uma tarefa de teste antes de cada tarefa que muda comportamento |
| 7 | Conferir | `/speckit-analyze` | Relatório de inconsistências entre spec, plano e tarefas (não altera arquivos) |
| 8 | Implementar | TDD, tarefa por tarefa | Commits `test:`, `feat:`/`fix:` e `refactor:` |
| 9 | Documentar | Rodar o agente `doc-sync-onboarding` e revisar o que ele mudou | `CLAUDE.md`, `README.md` e `docs/` atualizados no mesmo PR |
| 10 | Abrir o PR | GitHub | PR com `Closes #1` |

### Por que a branch e a pasta da spec são passos separados

O `/speckit-specify` não cria branch nem aceita `--number`. Sem `SPECIFY_FEATURE_DIRECTORY`, ele escolhe o próximo número livre em `specs/` (`.claude/skills/speckit-specify/SKILL.md:89-92`), que só coincide com o número da issue se as issues forem feitas exatamente em ordem. A criação de branch existe apenas como gancho da extensão `git` do spec-kit (`.claude/skills/speckit-specify/SKILL.md:281`), que não está instalada. Por isso a branch é criada à mão e a pasta é passada explicitamente.

## Artefatos de cada feature

Tudo fica em `specs/NNN-nome/`. Os caminhos são montados por `get_feature_paths` (`.specify/scripts/bash/common.sh:163`).

| Arquivo | Criado por | Conteúdo |
|---|---|---|
| `spec.md` | `/speckit-specify` | O quê e o porquê, sem tecnologia: histórias de usuário com prioridade, requisitos e critérios de sucesso |
| `checklists/requirements.md` | `/speckit-specify` | Checklist de qualidade da própria spec |
| `plan.md` | `/speckit-plan` (o modelo é copiado por `setup-plan.sh`) | Contexto técnico, Constitution Check, estrutura de pastas e Complexity Tracking |
| `research.md` | `/speckit-plan`, quando necessário | Pesquisa e decisões técnicas |
| `data-model.md` | `/speckit-plan`, quando necessário | Entidades e campos |
| `contracts/` | `/speckit-plan`, quando necessário | Contratos de API |
| `quickstart.md` | `/speckit-plan`, quando necessário | Como validar a feature à mão |
| `tasks.md` | `/speckit-tasks` | Tarefas numeradas (`T001`…), com as fases Setup, Foundational, uma por história e Polish |

## TDD na prática

1. Escolha a próxima tarefa de teste em `tasks.md`.
2. Escreva o teste em `backend/tests/` e rode-o com `uv run pytest`, dentro de `backend/`: ele precisa **falhar pelo motivo certo** (a funcionalidade não existe, não um erro de digitação). Para rodar um arquivo só: `uv run pytest tests/test_x.py`.
3. Commit `test: ...` com o teste falhando.
4. Escreva o mínimo de código para o teste passar. Commit `feat: ...` ou `fix: ...`.
5. Melhore o código com os testes verdes. Commit `refactor: ...`, se houver.
6. Marque a tarefa em `tasks.md` e siga para a próxima.

Regras complementares da constituição:

- LLM, embeddings, reranker e serviços externos ficam atrás de interfaces, com versões falsas e determinísticas nos testes. Os testes não usam rede (Princípio III): o pytest-socket e a guarda de `backend/conftest.py` fazem qualquer conexão fora da própria máquina falhar com `SocketConnectBlockedError` (detalhes em [architecture.md](architecture.md#ferramentas-do-backend)).
- Testes contra provedores reais levam `@pytest.mark.llm` e nunca bloqueiam um PR.
- Os módulos de lógica pura têm pelo menos 90% de cobertura (Princípio II).
- Mudanças de busca, prompt, modelo ou agente mostram as métricas de avaliação antes e depois (Princípio IV).

## A sincronização da documentação

Pense no responsável pela planta de uma casa em reforma. Toda vez que uma parede muda de lugar, ele confere a obra e corrige a planta, para que quem chegar depois encontre no papel exatamente o que está construído. No Desvenda, esse papel é do agente `doc-sync-onboarding`: no fim de toda alteração de código, ele lê o que mudou e atualiza a documentação.

A regra está no `CLAUDE.md` (seção "OBRIGATÓRIO: Sincronização de documentação"): nenhuma tarefa de código está concluída antes de o agente rodar. Ela põe em prática o Princípio VIII da constituição.

| Item | Como é |
|---|---|
| Arquivo | `.claude/agents/doc-sync-onboarding.md` |
| Quando roda | Como última etapa de toda alteração de código, antes do commit ou do PR |
| Como chamar | Pedir ao Claude Code que rode o agente `doc-sync-onboarding`; o agente principal também o chama sozinho, por causa da regra do `CLAUDE.md` |
| Ferramentas | `Read`, `Grep`, `Glob`, `Bash`, `Edit` e `Write` (campo `tools` do frontmatter) |
| O que lê | O diff da branch contra a `main` (`git diff main...HEAD`), as mudanças sem commit, os arquivos não rastreados e, quando existem, `spec.md` e `plan.md` da feature |
| O que edita | Só arquivos `.md`: `CLAUDE.md`, `README.md` e `docs/` |
| O que não toca | Código, `.specify/memory/constitution.md` e `specs/`; também não faz commit nem push |
| Memória | `memory: project`: as notas do agente ficam em `.claude/agent-memory/doc-sync-onboarding/`, versionadas com o repositório. A pasta nasce na primeira vez que o agente grava algo |
| Resultado | Um resumo dos documentos alterados ou criados e da mudança de código que motivou cada um |

```mermaid
sequenceDiagram
    actor Dev as Desenvolvedor
    participant CC as Claude Code
    participant DS as doc-sync-onboarding
    participant Git as git
    participant Docs as CLAUDE.md, README.md e docs/
    Dev->>CC: pede uma alteração de código
    CC->>CC: implementa em TDD
    CC->>DS: última etapa: sincronizar a documentação
    DS->>Git: git diff main...HEAD, git diff, git status
    DS->>DS: lê o código alterado e os documentos afetados
    DS->>Docs: atualiza só o que a mudança afetou
    DS-->>CC: resumo dos documentos alterados
    CC-->>Dev: mudança pronta para revisão e commit
```

## O pull request

| Seção | O que contém |
|---|---|
| Título | Conventional Commits, por exemplo `feat: monorepo e ferramentas do backend` |
| Descrição | O que mudou e por quê, com link para `specs/NNN-nome/spec.md` |
| `Closes #N` | Fecha a issue no merge |
| Avaliações | Métricas antes e depois, quando a mudança afeta a IA |
| Documentação | Quais arquivos de `docs/` mudaram |
| **O que aprendi** | Conceitos, erros e referências |

## Portões de qualidade

O merge exige:

- CI verde: ruff, testes, cobertura dos módulos de lógica pura e avaliação da busca quando ela é afetada. **O CI ainda não existe** (chega na #4); até lá, o gancho de commit roda o ruff em cada máquina e a revisão confere os testes à mão (`uv run pytest`, `uv run ruff check` e `uv run ruff format --check` em `backend/`);
- todas as tarefas de `tasks.md` marcadas;
- `docs/` atualizada pelo agente `doc-sync-onboarding` e conferida na revisão;
- a constituição conferida na revisão.

## Exceções

Não precisam de spec: correção de texto, atualização de dependência sem mudança de comportamento e ajuste de configuração de CI (Princípio I). Esses casos ainda exigem issue e PR.

Os commits iniciais do repositório (spec-kit, constituição, finais de linha e esta documentação) foram feitos direto na `main`, antes de existirem issues no GitHub.

A issue #40 (o agente `doc-sync-onboarding` e a regra do `CLAUDE.md`) também ficou sem spec: ela muda só ferramenta de desenvolvimento e documentação, sem comportamento do produto nem código de produção.

## Pegadinhas e dívidas técnicas

| # | Problema | Como evitar |
|---|---|---|
| 1 | `/speckit-specify` ignora o número da issue se `SPECIFY_FEATURE_DIRECTORY` não for passado | Sempre passar `SPECIFY_FEATURE_DIRECTORY=specs/NNN-nome` |
| 2 | A branch não é criada por nenhum comando | `git switch -c NNN-nome` antes de especificar |
| 3 | `.specify/feature.json` aponta para a última feature especificada e não acompanha a troca de branch | Depois de trocar de branch, reexportar `SPECIFY_FEATURE_DIRECTORY` antes de `/speckit-plan` ou `/speckit-tasks` |
| 4 | O modelo de tarefas diz que testes são opcionais | A constituição prevalece; conferir em `/speckit-analyze` que há teste antes de cada implementação |
| 5 | A constituição v1.0.0 mandava usar `--number` no `/speckit-specify` | Corrigido na v1.1.0 |
| 6 | O Claude Code carrega os agentes de `.claude/agents/` quando a sessão começa | Depois de criar ou mudar um agente, abrir uma sessão nova |
| 7 | A regra do `CLAUDE.md` fala em "`CLAUDE.md` e arquivos em `docs/`", mas o agente também atualiza o `README.md` | Conferir o resumo do agente, que lista todos os arquivos tocados |
| 8 | O agente é um prompt: pode deixar passar uma mudança ou descrevê-la errado | Revisar o diff da documentação antes do commit, como qualquer outra mudança |

Os detalhes técnicos de cada item estão em [apps/speckit.md](apps/speckit.md).
