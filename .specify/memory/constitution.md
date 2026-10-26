# Constituição do Desvenda

O Desvenda é um SaaS de estudos com um tutor de IA que responde a partir das anotações do próprio
aluno (RAG) e com um sistema de progressão de expedição. Também é um projeto de aprendizado: o
código precisa funcionar em produção e ensinar quem o constrói.

## Princípios

### I. Especificação antes do código

- Toda mudança de comportamento começa numa issue do GitHub e passa por `/speckit-specify`,
  `/speckit-plan` e `/speckit-tasks` antes da primeira linha de código de produção.
- Uma issue é uma spec, uma branch e um pull request. A spec usa o número da issue
  (`--number N`): a issue #12 vira `specs/012-.../` e a branch `012-...`.
- A spec descreve o quê e o porquê, sem tecnologia; o plano descreve o como. Uma dúvida que muda
  o comportamento vira `[NEEDS CLARIFICATION]` e é resolvida com `/speckit-clarify` antes do plano.
- Ficam sem spec só a correção de texto, a atualização de dependência sem mudança de
  comportamento e o ajuste de configuração de CI. Esses casos ainda exigem issue e PR.

Por quê: a spec é onde a decisão fica registrada, e é contra ela que o PR é revisado.

### II. Testes primeiro (inegociável)

- Todo código de produção nasce em TDD: escrever o teste, vê-lo falhar pelo motivo certo,
  escrever o mínimo para passar e refatorar com os testes verdes.
- Em `tasks.md`, toda tarefa que muda comportamento vem depois de uma tarefa de teste. Isso anula
  o aviso de "testes opcionais" do modelo de tarefas.
- O histórico do PR mostra o ciclo: um commit `test:` com o teste falhando antes do commit
  `feat:` ou `fix:` que o faz passar.
- Os módulos de lógica pura (fatiamento, fusão de buscas, métricas de avaliação, repetição
  espaçada, regras do jogo, agendador) têm pelo menos 90% de cobertura de linhas e não acessam
  banco nem rede.
- A correção de um bug começa com um teste que o reproduz.

Por quê: o teste é a especificação executável; sem ele, "funciona" não tem prova.

### III. IA atrás de interfaces, testes sem rede

- Toda chamada a LLM, embeddings, reranker ou serviço externo passa por uma interface do projeto
  que tem uma implementação falsa e determinística para os testes.
- Os testes unitários e de integração rodam sem rede (bloqueada no pytest) e sem chave de API.
- Os testes contra provedores reais levam a marca `@pytest.mark.llm`, rodam sob demanda ou em
  horário agendado e nunca bloqueiam um PR.

Por quê: custo, velocidade e testes que dão o mesmo resultado em toda execução.

### IV. Qualidade de IA medida por avaliação

- Toda mudança em busca, prompt, modelo ou agente declara na spec a métrica que quer mover
  (recall@5, MRR, fidelidade…) e mostra no PR o antes e o depois.
- Os conjuntos de avaliação ficam versionados no repositório, com o histórico dos resultados.
- A avaliação da busca roda no CI. Uma queda maior que a tolerância definida na spec da avaliação
  bloqueia o merge. As avaliações com LLM como juiz rodam sob demanda.
- Uma melhoria que não aparece na avaliação não entra.

Por quê: em RAG, a avaliação faz pela qualidade das respostas o que o teste faz pelo código.

### V. Os dados do aluno são do aluno

- Toda consulta a notas, trechos, conversas e progresso filtra pelo dono. Cada funcionalidade que
  recupera conteúdo tem um teste provando que um usuário nunca recebe conteúdo de outro.
- O conteúdo de notas e PDFs é dado, nunca instrução: entra no prompt delimitado, e o tutor não
  obedece a ordens encontradas nele.
- Segredos ficam só em variáveis de ambiente. Nenhuma chave, token ou dado pessoal vai para
  código, log ou commit.
- O aluno pode exportar e apagar todos os seus dados (LGPD).

### VI. Observável e com custo conhecido

- Toda chamada de IA registra modelo, tokens de entrada e saída, latência, custo estimado e
  usuário, e aparece no rastreamento (a ferramenta é decidida na spec de observabilidade).
- Existe limite de uso por usuário antes de o produto abrir para outras pessoas.
- Falha de provedor tem tratamento: tempo limite, nova tentativa com espera e uma resposta
  degradada clara para o aluno.

### VII. Simplicidade e fatias finas

- Cada issue entrega a menor fatia que funciona de ponta a ponta e pode ser demonstrada.
- Nenhuma abstração sem um segundo uso real; toda dependência nova é justificada no plano.
- Otimização só depois de medida (Princípio IV).

## Restrições técnicas

- **Backend:** Python 3.12+, Django (última versão estável) servido em ASGI, API com Django
  Ninja, testes com pytest e pytest-django, lint e formatação com ruff, dependências com uv.
- **Dados:** Postgres com pgvector; busca textual do próprio Postgres em português.
- **Tarefas em segundo plano:** fila com worker (Celery + Redis, salvo decisão diferente numa spec).
- **IA:** LangChain (Python) com Claude via `langchain-anthropic`. Modelo padrão
  `claude-opus-5-5`; trocar de modelo para economizar é uma decisão registrada na spec, com
  avaliação antes e depois. O provedor de embeddings e o reranker são decididos nas specs deles.
- **Frontend:** Next.js (App Router, TypeScript) consumindo só a API. As regras de negócio e do
  jogo ficam no backend.
- **Repositório:** monorepo com `backend/` e `frontend/`, Conventional Commits e GitHub Actions.

## Fluxo de desenvolvimento e portões de qualidade

1. Pegar a próxima issue do milestone atual.
2. Rodar `/speckit-specify` com o texto da issue e `--number` igual ao número dela.
3. Rodar `/speckit-clarify` se sobrar `[NEEDS CLARIFICATION]`.
4. Rodar `/speckit-plan`. O "Constitution Check" precisa passar, ou a violação é justificada em
   "Complexity Tracking".
5. Rodar `/speckit-tasks` (testes antes de cada implementação) e `/speckit-analyze`.
6. Implementar em ciclos vermelho, verde e refatorar, com commits pequenos.
7. Abrir o PR com `Closes #N`, o resultado das avaliações quando houver e a seção
   **O que aprendi** (conceitos, erros e referências).

O merge exige CI verde (ruff, testes, cobertura dos módulos de lógica pura e avaliação da busca
quando ela é afetada), todas as tarefas de `tasks.md` marcadas e esta constituição conferida na
revisão.

## Governança

- Esta constituição vale acima de qualquer outra prática do projeto.
- Uma mudança nela entra por um PR próprio que edita este arquivo, explica o motivo e sobe a
  versão: MAJOR para remover ou redefinir um princípio, MINOR para adicionar princípio ou seção,
  PATCH para esclarecimento.
- Toda revisão de PR confere estes princípios; complexidade fora deles precisa estar justificada
  no plano.

**Versão**: 1.0.0 | **Ratificada**: 2026-10-26 | **Última alteração**: 2026-10-26
