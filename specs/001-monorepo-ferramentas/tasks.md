---

description: "Tarefas da issue #1: monorepo e ferramentas do backend"
---

# Tasks: Monorepo e ferramentas do backend

**Input**: `specs/001-monorepo-ferramentas/` (spec.md, plan.md, research.md)

**Tests**: obrigatórios pela constituição (Princípio II). O comportamento novo desta feature (o bloqueio de rede) nasce em TDD: teste escrito e visto falhando antes da configuração. As histórias de configuração pura (US1 e US3) não têm código de produção; nelas, a tarefa de verificação roda os cenários de aceite da spec.

**Organization**: uma fase por história da spec, na ordem de prioridade.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependência)
- **[Story]**: história da spec (US1, US2, US3)
- Todos os comandos `uv` rodam dentro de `backend/`, salvo indicação

---

## Phase 1: Setup

**Purpose**: o projeto uv vazio que todas as histórias usam (research D1, D2, D3)

- [x] T001 Criar `backend/pyproject.toml` (`name = "desvenda-backend"`, `version = "0.1.0"`, `requires-python = ">=3.12"`, `[tool.uv] package = false`) e `backend/.python-version` com `3.12`
- [x] T002 Rodar `uv add --dev pytest` em `backend/` (cria `backend/uv.lock` e `backend/.venv/`) e criar `backend/tests/__init__.py` vazio

**Checkpoint**: `uv run pytest` roda em `backend/` e diz que não há testes.

---

## Phase 2: User Story 1 - Ambiente com versões travadas (Priority: P1) 🎯 MVP

**Goal**: qualquer cópia do repositório instala as mesmas versões com um comando; `frontend/` reservado.

**Independent Test**: em `backend/`, `uv sync --locked` passa sem mudar `uv.lock`, e falha quando `pyproject.toml` e `uv.lock` divergem.

- [x] T003 [P] [US1] Criar `frontend/README.md` dizendo que a pasta recebe o Next.js (App Router, TypeScript) no milestone M4, issue #26, e que até lá não há nada para instalar (research D9)
- [x] T004 [US1] Verificar os cenários 1 a 3 da US1 em `backend/`: `uv sync --locked` passa e `git status` não mostra mudança em `backend/uv.lock`; rodar de novo não instala nada; acrescentar uma dependência em `backend/pyproject.toml` sem `uv lock` faz `uv sync --locked` falhar (desfazer em seguida)
- [x] T005 [US1] Commit `chore:` com `backend/pyproject.toml`, `backend/.python-version`, `backend/uv.lock`, `backend/tests/__init__.py` e `frontend/README.md`

**Checkpoint**: US1 entregue.

---

## Phase 3: User Story 2 - Testes que nunca usam a rede (Priority: P1)

**Goal**: conexões externas falham na hora durante os testes; a própria máquina continua liberada; a cobertura aparece (research D5, D6).

**Independent Test**: `uv run pytest` passa, e os testes-sentinela provam o bloqueio e a liberação local.

### Tests for User Story 2 ⚠️

> Escrever primeiro e ver falhar pelo motivo certo: sem bloqueio, a conexão é tentada de verdade.

- [x] T006 [US2] Escrever `backend/tests/test_bloqueio_de_rede.py` com quatro testes:
  - conexão por endereço numérico externo (`192.0.2.1:80`, faixa reservada para documentação, com tempo limite de 2 s no socket) levanta um erro cujo tipo se chama `SocketConnectBlockedError`, em menos de 1 s;
  - `socket.create_connection(("example.com", 80), timeout=2)` levanta esse mesmo erro;
  - `socket.getaddrinfo("example.com", 80)` levanta erro de bloqueio, sem consultar o DNS;
  - um servidor aberto pelo próprio teste em `127.0.0.1` (porta 0, numa thread) aceita a conexão.
- [x] T007 [US2] Rodar `uv run pytest` e confirmar que os três testes de bloqueio falham porque a conexão foi tentada (tempo limite ou sucesso) e que o teste local passa; commit `test:` com os testes falhando

### Implementation for User Story 2

- [x] T008 [US2] Rodar `uv add --dev pytest-socket pytest-cov` e configurar em `backend/pyproject.toml`: `[tool.pytest.ini_options]` com `testpaths = ["tests"]` e `addopts = "--allow-hosts=127.0.0.1,::1,localhost --cov --cov-report=term-missing --strict-markers"`; `[tool.coverage.run]` com `source = ["."]` e `omit = ["tests/*", ".venv/*"]`
- [x] T009 [US2] Rodar `uv run pytest`. Se só o teste do `getaddrinfo` ainda falhar, criar `backend/conftest.py` (na raiz do backend, para entrar na cobertura, que ignora `tests/`) com uma fixture `autouse` que troca `socket.getaddrinfo` por uma versão que só resolve os destinos do `--allow-hosts` e levanta `SocketConnectBlockedError` para o resto (research D6)
- [x] T010 [US2] Confirmar a suíte verde, a tabela de cobertura no fim e o tempo total abaixo de 10 s (SC-006); commit `feat:`

**Checkpoint**: US1 e US2 entregues.

---

## Phase 4: User Story 3 - Padrão de código antes de cada commit (Priority: P2)

**Goal**: ruff verifica padrão e formatação, e o pre-commit roda o mesmo ruff antes de cada commit (research D4, D7).

**Independent Test**: um arquivo mal formatado barra o commit e sai corrigido; depois de adicionado de novo, o commit passa.

- [x] T011 [US3] Rodar `uv add --dev ruff pre-commit` e configurar `[tool.ruff]` em `backend/pyproject.toml`: `target-version = "py312"`, `line-length = 100`, `[tool.ruff.lint] select = ["E", "F", "W", "I", "UP", "B"]`
- [x] T012 [US3] Rodar `uv run ruff check` e `uv run ruff format --check` em `backend/` e corrigir o que apontarem em `backend/tests/` (cenário 1)
- [x] T013 [US3] Criar `.pre-commit-config.yaml` na raiz com `repo: local` e dois ganchos `language: system`, `files: ^backend/.*\.py$`: `uv run --project backend ruff check --fix` e `uv run --project backend ruff format`
- [x] T014 [US3] Na raiz, rodar `uv run --project backend pre-commit install` e verificar os cenários 2 a 5 da US3 com um `backend/rascunho.py` temporário: `x=1` barra o commit e sai `x = 1`; `print(nome_indefinido)` barra o commit apontando arquivo e linha (`F821`); um commit só de documentação passa. Apagar o rascunho
- [x] T015 [US3] Commit `chore:` com `backend/pyproject.toml`, `backend/uv.lock` e `.pre-commit-config.yaml` (este commit já passa pelo gancho)

**Checkpoint**: as três histórias entregues.

---

## Phase 5: Polish

- [ ] T016 Rodar o agente `doc-sync-onboarding` (obrigatório pelo `CLAUDE.md`) e revisar o que ele mudou: `README.md` (passos de setup saem de "O que ainda não existe"; como ver o `uv sync --locked` falhar e o gancho barrar um commit), `docs/architecture.md` e `docs/workflow.md`; commit `docs:`
- [ ] T017 Validação final em `backend/`: `uv sync --locked`, `uv run pytest`, `uv run ruff check`, `uv run ruff format --check`, todos com código 0; marcar todas as tarefas deste arquivo
- [ ] T018 Enviar a branch e abrir o PR com `Closes #1`, a lista de documentos alterados e a seção **O que aprendi**

---

## Dependencies & Execution Order

- **Setup (T001–T002)** → todas as histórias.
- **US1 (T003–T005)** → depende só do Setup.
- **US2 (T006–T010)** → depende do Setup; independe da US1 além do `uv.lock` já existir.
- **US3 (T011–T015)** → depende do Setup; o T012 olha os testes da US2, então vem depois dela.
- **Polish (T016–T018)** → depois das três histórias.

Paralelismo: só o T003 (um arquivo à parte, no frontend). O resto mexe em `backend/pyproject.toml` e `backend/uv.lock` e precisa ser em sequência.

## Implementation Strategy

Um passo de cada vez, com commit ao fim de cada história: Setup + US1 (MVP: ambiente reproduzível), depois US2 (bloqueio de rede, em TDD), depois US3 (padrão de código) e por fim a documentação e o PR.
