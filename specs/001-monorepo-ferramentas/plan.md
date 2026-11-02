# Implementation Plan: Monorepo e ferramentas do backend

**Branch**: `001-monorepo-ferramentas` | **Date**: 2026-11-02 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-monorepo-ferramentas/spec.md`

## Summary

Criar `backend/` como um projeto uv autocontido, com o Python 3.12 e as ferramentas de desenvolvimento travadas em `backend/uv.lock`: ruff para padrão e formatação, pytest com pytest-cov para testes e cobertura, pytest-socket para bloquear a rede nos testes (liberando só a própria máquina) e pre-commit para rodar o ruff antes de cada commit. O pre-commit usa ganchos locais que chamam o mesmo ruff travado. `frontend/` fica reservado, com um README. As decisões e as alternativas estão em [research.md](research.md). Os comandos e o roteiro de validação vão para o `README.md`, que o Princípio VIII já obriga a atualizar; por isso esta feature não tem `contracts/` nem `quickstart.md`.

## Technical Context

**Language/Version**: Python 3.12 (`requires-python = ">=3.12"`, `backend/.python-version`)

**Primary Dependencies**: só ferramentas de desenvolvimento, no grupo `dev`: ruff, pytest, pytest-cov, pytest-socket, pre-commit. Versões fixadas pelo `uv.lock`. O pytest-django fica para a #2 (research D8).

**Storage**: N/A

**Testing**: pytest + pytest-cov + pytest-socket, configurados em `backend/pyproject.toml`

**Target Platform**: máquina de desenvolvimento Windows (Git Bash e PowerShell) e Linux (o CI da #4)

**Project Type**: monorepo com aplicação web (backend Django a partir da #2, frontend Next.js a partir da #26); nesta feature, só a fundação de ferramentas

**Performance Goals**: suíte desta feature em menos de 10 s (SC-006); conexão externa bloqueada em menos de 1 s (SC-004)

**Constraints**: testes sem rede externa; mesmos comandos no Windows e no Linux; o gancho e os comandos manuais com a mesma versão do ruff

**Scale/Scope**: 1 projeto Python, 2 a 4 testes, 3 arquivos de configuração

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio | Como esta feature atende | Situação |
|---|---|---|
| I. Especificação antes do código | Issue #1 → `spec.md` aprovada → este plano → `tasks.md` | ✅ |
| II. Testes primeiro | Os testes do bloqueio de rede são escritos e vistos falhando antes de instalar e configurar o pytest-socket; commit `test:` antes do `feat:`. Não há módulo de lógica pura, então o mínimo de 90% ainda não se aplica | ✅ |
| III. IA atrás de interfaces, testes sem rede | Esta feature implementa o bloqueio de rede que o princípio exige. A marca `@pytest.mark.llm` chega com o primeiro teste contra provedor real (#9) | ✅ |
| IV. Qualidade de IA medida por avaliação | Nada de busca, prompt ou modelo | N/A |
| V. Os dados do aluno são do aluno | Nenhum dado; nenhum segredo (não há `.env` nesta feature) | N/A |
| VI. Observável e com custo conhecido | Nenhuma chamada de IA | N/A |
| VII. Simplicidade e fatias finas | Cinco ferramentas, todas exigidas pela spec ou pela constituição e justificadas em research.md; pytest-django adiado por não ter uso; nenhum script ou `Makefile` próprio | ✅ |
| VIII. Documentação viva | `README.md` (passos de setup saem de "O que ainda não existe"; inclui como ver o `uv sync --locked` falhar e o gancho barrar um commit), `docs/architecture.md` (o que existe, arquivos de configuração, pegadinhas) e `docs/workflow.md` (comandos de teste e verificação) no mesmo PR, sincronizados pelo agente `doc-sync-onboarding` | ✅ |
| Restrições técnicas | Python 3.12+, pytest, ruff e uv, como a constituição manda; monorepo com `backend/` e `frontend/` | ✅ |

**Reavaliação depois do design (Fase 1)**: sem mudança. A Fase 1 não gerou artefatos: não há dados (`data-model.md`), e os comandos ficam no `README.md`.

## Project Structure

### Documentation (this feature)

```text
specs/001-monorepo-ferramentas/
├── plan.md              # Este arquivo
├── research.md          # Decisões D1 a D10
├── checklists/
│   └── requirements.md  # Checklist da spec
└── tasks.md             # Criado pelo /speckit-tasks
```

Sem `data-model.md` (não há dados), `contracts/` nem `quickstart.md` (os comandos e o roteiro de validação ficam no `README.md`).

### Source Code (repository root)

```text
.pre-commit-config.yaml      # Ganchos locais do ruff (check --fix e format) para backend/**/*.py
backend/
├── .python-version          # 3.12
├── pyproject.toml           # Projeto uv (package = false), grupo dev, [tool.ruff], [tool.pytest.ini_options], [tool.coverage.run]
├── uv.lock                  # Versões travadas
└── tests/
    ├── __init__.py
    └── test_bloqueio_de_rede.py   # Conexão externa bloqueada (por IP e por nome) e conexão local permitida
frontend/
└── README.md                # Reservado para o Next.js (M4, #26)
```

**Structure Decision**: monorepo com `backend/` e `frontend/`, como a constituição define. O `backend/` é o único projeto Python e é autocontido (research D1); o `.pre-commit-config.yaml` fica na raiz porque o gancho é do repositório inteiro. O código da aplicação (o projeto Django) entra em `backend/` na #2.

## Complexity Tracking

Nenhuma violação a justificar.
