# Desvenda

App de estudos com um tutor de IA (a arara) que responde a partir das anotações do próprio aluno (RAG) e com uma progressão de expedição. A documentação completa está em [docs/index.md](docs/index.md).

- Leia `.specify/memory/constitution.md` antes de começar: SDD, TDD e documentação viva são obrigatórios.
- Uma issue do GitHub é uma spec, uma branch e um PR, todos com o número da issue em três dígitos. Crie a branch com `git switch -c NNN-<nome>` e rode `/speckit-specify` com `SPECIFY_FEATURE_DIRECTORY=specs/NNN-<nome>`. O `/speckit-specify` não aceita `--number` nem cria branch (ver [docs/apps/speckit.md](docs/apps/speckit.md)).
- Todo PR que muda módulo, modelo, rota, variável de ambiente, tarefa assíncrona ou infraestrutura atualiza `docs/` seguindo as convenções de [docs/index.md](docs/index.md#convenções-da-documentação).
- O usuário acompanha a implementação para aprender: trabalhe em passos pequenos, explique cada um e pare nos pontos de decisão.
- Backend em `backend/` (Django, Django Ninja, pgvector, LangChain); frontend em `frontend/` (Next.js). Os scripts do spec-kit são bash: no Windows, rode-os pelo Git Bash.

## ⚠ OBRIGATÓRIO: Sincronização de documentação

**Ao finalizar QUALQUER alteração de código neste repositório, é OBRIGATÓRIO executar, como última etapa, o agente `doc-sync-onboarding` para atualizar a documentação (`CLAUDE.md` e arquivos em `docs/`) refletindo as mudanças feitas.**

Isso vale para toda e qualquer modificação: novos modelos/campos, migrations, views, rotas, tasks assíncronas, signals, middlewares, integrações, variáveis de ambiente, scripts de infraestrutura, etc. Nenhuma tarefa de código é considerada concluída antes de a documentação ter sido sincronizada por esse agente.
