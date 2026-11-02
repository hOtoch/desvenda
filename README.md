# Desvenda

> **Documentação completa: [docs/index.md](docs/index.md).** Comece por lá se você acabou de chegar.

Desvende o que você ainda não sabe. Um app de estudos com um tutor de IA que responde a partir das suas próprias anotações, e um mapa que se revela conforme você estuda.

## O que é, em poucas palavras

Pense num caderno que responde. Você escreve as suas anotações como sempre. Quando bate uma dúvida, pergunta a uma arara-guia, e ela responde **usando o que você mesmo escreveu**, mostrando de qual nota e de qual trecho tirou a resposta. Em volta disso existe um jogo: cada objetivo de estudo é uma expedição num mapa coberto de névoa, que se revela conforme você estuda e revisa.

O projeto também é um projeto de aprendizado: serve para dominar agentes de IA e RAG (busca nas notas + geração de resposta) com qualidade de produção.

## Estado atual

**Ainda não existe código de aplicação.** O repositório tem só a base do processo de desenvolvimento:

| O que existe | Para que serve |
|---|---|
| [.specify/memory/constitution.md](.specify/memory/constitution.md) | As regras do projeto: especificação antes do código (SDD), testes primeiro (TDD), documentação viva e as decisões de tecnologia |
| [.specify/](.specify/) | O [spec-kit](https://github.com/github/spec-kit) 1.1.1: modelos e scripts que criam as specs, os planos e as tarefas de cada issue |
| [.claude/skills/](.claude/skills/) | Os comandos `/speckit-*` usados no Claude Code |
| [.claude/agents/](.claude/agents/) | O agente `doc-sync-onboarding`, que atualiza a documentação no fim de cada alteração de código |
| [docs/](docs/index.md) | Esta documentação |
| `CLAUDE.md`, `.gitignore`, `.gitattributes` | Instruções para o agente, arquivos ignorados e finais de linha LF |

Os detalhes estão em [docs/architecture.md](docs/architecture.md).

## Como rodar o projeto

### O que dá para rodar hoje

O único código executável são os scripts bash do spec-kit. Para usá-los:

1. **Pré-requisitos**
   - Git.
   - Bash. No Windows, use o **Git Bash**: os scripts são `.sh` e não rodam no PowerShell.
   - [Claude Code](https://docs.anthropic.com/en/docs/claude-code/setup), para os comandos `/speckit-*`.
   - Opcional: `jq`. Sem ele, os scripts usam Python ou `grep`/`sed` para ler JSON.
   - Opcional: a CLI `specify`, só para atualizar o spec-kit. Ela não é dependência do projeto.
2. **Clonar**

   ```bash
   git clone https://github.com/hOtoch/desvenda.git
   ```

3. **Conferir os scripts** com uma simulação que não cria nada:

   ```bash
   bash .specify/scripts/bash/create-new-feature.sh --dry-run --number 1 --short-name monorepo-ferramentas "Monorepo e ferramentas do backend"
   ```

   Saída esperada:

   ```text
   BRANCH_NAME: 001-monorepo-ferramentas
   SPEC_FILE: <raiz>/specs/001-monorepo-ferramentas/spec.md
   FEATURE_NUM: 001
   ```

4. **Trabalhar numa issue**: siga o passo a passo de [docs/workflow.md](docs/workflow.md).

### O que ainda não existe

Estes passos de setup só vão existir quando o código chegar. Cada um será documentado aqui no mesmo PR que o criar (Princípio VIII da constituição).

| Passo de setup | Situação hoje | Previsto para |
|---|---|---|
| Dependências da aplicação (uv, Node) | Não existe | Milestone M0 (fundação) |
| Variáveis de ambiente (`.env`) | Não existe | M0 |
| Banco de dados (Postgres + pgvector) e Redis | Não existe | M0 |
| Migrações | Não existe | M0 |
| Usuário admin | Não existe | M0 |
| Servidor (uvicorn) | Não existe | M0 |
| Serviços auxiliares (worker Celery) | Não existe | M1 |
| Frontend (Next.js) | Não existe | M4 |

## Arquitetura e infraestrutura

- **Hoje:** só a camada de processo. Não há servidor, banco, fila nem deploy.
- **Decidido, ainda não implementado** (constituição, seção "Restrições técnicas"): backend em Django com Django Ninja servido em ASGI; Postgres com pgvector; fila com Celery + Redis; IA com LangChain e Claude; frontend em Next.js; monorepo com `backend/` e `frontend/`; CI no GitHub Actions.
- **Repositório remoto:** `https://github.com/hOtoch/desvenda.git`, **público**. A `main` foi enviada em 02/11/2026, e o plano de trabalho (issues #1 a #39, milestones M0 a M15) está nas [issues do GitHub](https://github.com/hOtoch/desvenda/issues).

O mapa completo, com diagramas, está em [docs/architecture.md](docs/architecture.md).
