# Research: Monorepo e ferramentas do backend

Cada decisão segue o formato Decisão → Motivo → Alternativas. As versões exatas não ficam aqui: quem as fixa é o `backend/uv.lock`, gerado na implementação.

## D1. Onde fica o projeto Python

- **Decisão:** um projeto uv autocontido em `backend/` (`backend/pyproject.toml`, `backend/uv.lock`, `backend/.python-version`), marcado como aplicação e não como pacote (`[tool.uv] package = false`). Os comandos rodam de dentro de `backend/`.
- **Motivo:** a spec pede que tudo do backend fique na área do backend (Assumptions). O frontend vai ter o próprio gerenciador (npm) em `frontend/`, então a raiz não precisa de projeto Python. `package = false` porque o backend é uma aplicação Django (#2), não uma biblioteca a publicar.
- **Alternativas:** `pyproject.toml` na raiz com workspace do uv — mais configuração para um único projeto Python, e misturaria o backend com a raiz do monorepo.

## D2. Versão do Python

- **Decisão:** `requires-python = ">=3.12"` e `backend/.python-version` com `3.12`.
- **Motivo:** a constituição exige 3.12+, e a máquina de desenvolvimento já tem 3.12.3. O `.python-version` faz o uv usar (ou baixar) a mesma versão em toda cópia, o que cobre o caso de borda "versão da linguagem ausente ou antiga".
- **Alternativas:** 3.13 — nada no projeto precisa dela ainda, e o 3.12 já está instalado.

## D3. Como as ferramentas são declaradas e instaladas

- **Decisão:** todas as ferramentas ficam no grupo `dev` de `[dependency-groups]` em `backend/pyproject.toml`. `uv sync` instala o grupo `dev` por padrão. A instalação verificada (FR-004) é `uv sync --locked`, que falha se `pyproject.toml` e `uv.lock` divergirem.
- **Motivo:** é o mecanismo padrão do uv (PEP 735); não exige flag extra no dia a dia, e o `--locked` é o que o CI da #4 vai usar.
- **Alternativas:** `[project.optional-dependencies]` — exigiria `--extra dev` em todo comando; `requirements-dev.txt` com pip-tools — duas ferramentas para o que o uv faz sozinho.

## D4. Verificador e formatador de código

- **Decisão:** ruff, configurado em `backend/pyproject.toml` (`[tool.ruff]`): `target-version = "py312"`, `line-length = 100`, regras `E`, `F`, `W`, `I` (ordem dos imports), `UP` (sintaxe moderna) e `B` (bugs comuns). `ruff check` aponta problemas e `ruff format --check` aponta diferenças de formatação, sem alterar arquivos (FR-009).
- **Motivo:** a constituição fixa o ruff. O conjunto de regras é pequeno de propósito: pega erros reais sem gerar ruído enquanto o código ainda está nascendo; dá para ampliar numa issue futura. Linha de 100 colunas cabe bem no editor e evita quebras artificiais em textos em português.
- **Alternativas:** o conjunto padrão do ruff (`E4`, `E7`, `E9`, `F`) — não ordena imports nem pega padrões propensos a bug; `select = ["ALL"]` — ruído demais para um projeto de aprendizado.

## D5. Executor de testes e cobertura

- **Decisão:** pytest com pytest-cov. Configuração em `[tool.pytest.ini_options]`: `testpaths = ["tests"]`, `addopts` com `--cov --cov-report=term-missing` (FR-005) e `--strict-markers`. Cobertura configurada em `[tool.coverage.run]` com `source = ["."]` e `omit` para `tests/*` e `.venv/*`.
- **Motivo:** a constituição fixa pytest. O relatório aparece em toda execução, sem mínimo obrigatório (Assumptions da spec). `--strict-markers` faz uma marca digitada errada virar erro em vez de ser ignorada.
- **Alternativas:** `--cov-fail-under` já agora — não há código de produção para medir; o mínimo de 90% entra com o primeiro módulo de lógica pura (#8).

## D6. Bloqueio de rede nos testes

- **Decisão:** pytest-socket com `--allow-hosts=127.0.0.1,::1,localhost` em `addopts`. Ele troca o `connect` do socket por uma versão que só aceita esses destinos e levanta `SocketConnectBlockedError` para qualquer outro, sem tentar a conexão (FR-006, FR-007, SC-004).
  - Se os testes mostrarem que a consulta de nome (DNS) ainda escapa do bloqueio — o pytest-socket protege o `connect`, não o `getaddrinfo` —, um `conftest.py` acrescenta uma guarda que recusa a resolução de nomes que não sejam locais. Quem decide é o teste (TDD): primeiro o teste da consulta de nome, depois a guarda, só se ele falhar.
- **Motivo:** o plugin é mantido, pequeno e resolve o caso principal com uma linha de configuração. Liberar `localhost` agora evita mexer no bloqueio quando os testes de banco chegarem (#3). Para liberar a rede num teste específico, o plugin já traz a marca `enable_socket`; o uso organizado disso (marca `llm`, rodar sob demanda) fica para a #9.
- **Alternativas:** `--disable-socket` — bloqueia até a criação do socket, inclusive para `localhost`, o que quebraria os testes de banco da #3; escrever o bloqueio à mão no `conftest.py` — mais código nosso para manter, sem ganho para o caso principal.

## D7. Gancho de commit

- **Decisão:** pre-commit (no grupo `dev`), com `.pre-commit-config.yaml` na raiz do repositório e dois ganchos **locais** (`repo: local`, `language: system`):
  - `ruff check --fix` e `ruff format`, chamados como `uv run --project backend ruff ...`;
  - `files: ^backend/.*\.py$`, para só olhar código do backend (spec, Assumptions).
  Instalação uma vez por cópia: `uv run --project backend pre-commit install`, rodado na raiz.
- **Motivo:** os ganchos locais usam o ruff travado no `uv.lock`, então o gancho e o comando manual têm sempre a mesma versão e as mesmas regras (FR-011). O `--project backend` não muda a pasta atual, então os caminhos que o pre-commit passa (`backend/...`) continuam válidos, e o ruff acha `backend/pyproject.toml` sozinho pela posição do arquivo. Quando um gancho altera um arquivo, o pre-commit barra o commit, que é o comportamento pedido (FR-010).
- **Alternativas:** o repositório oficial `astral-sh/ruff-pre-commit` com `rev` fixo — duplica a versão do ruff em dois lugares e elas podem divergir; um gancho do git escrito à mão — não é portátil entre Windows e Linux e não lida com arquivos parcialmente adicionados.

## D8. pytest-django agora ou na #2

- **Decisão (confirmada pelo usuário em 2026-11-02):** adiar para a #2. A issue #1 lista o pytest-django, mas sem Django instalado nem `DJANGO_SETTINGS_MODULE` não há o que ele faça; ele entra no mesmo PR que cria o projeto Django e o configura.
- **Motivo:** Princípio VII (toda dependência nova é justificada no plano; nada sem uso real). Uma dependência instalada e não usada também não tem teste que prove que funciona.
- **Alternativas:** instalar agora, como diz a issue — cumpre o texto da issue ao pé da letra, mas fica parada até a #2.

## D9. Área do frontend

- **Decisão:** `frontend/README.md` curto, dizendo que a pasta vai receber o Next.js (App Router, TypeScript) no milestone M4, issue #26, e que até lá não há nada para instalar.
- **Motivo:** o git não versiona pasta vazia; o README cumpre FR-001 e explica o motivo para quem chega.
- **Alternativas:** `.gitkeep` — mantém a pasta, mas não explica nada.

## D10. Windows e Linux

- **Decisão:** todos os comandos documentados são do uv, do pytest, do ruff e do pre-commit, que funcionam igual nos dois sistemas; nenhum script de shell novo. A conferência no Linux fica para quando houver um ambiente Linux (contêiner na #3 ou CI na #4).
- **Motivo:** FR-012 sem criar camada própria de scripts.
- **Alternativas:** um `Makefile` ou `justfile` com atalhos — exige ferramenta extra no Windows e é abstração antes do segundo uso.
