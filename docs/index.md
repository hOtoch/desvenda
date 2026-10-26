# Documentação do Desvenda

Este é o mapa da documentação. Se você acabou de chegar, ele diz o que ler, em que ordem e onde fica cada assunto.

**Situação em 26/10/2026:** o projeto ainda não tem código de aplicação. Por isso, os documentos de hoje descrevem o processo de desenvolvimento e as ferramentas que já estão no repositório. Os documentos sobre banco, painel administrativo e módulos do sistema nascem junto com o código (veja a última tabela).

## Ordem de leitura sugerida

1. [README.md](../README.md): o que é o projeto e como rodar o que existe.
2. [architecture.md](architecture.md): o que existe hoje, o que está decidido e como as peças se ligam.
3. [workflow.md](workflow.md): como uma issue vira código, passo a passo.
4. [Constituição](../.specify/memory/constitution.md): as regras que valem acima de tudo.
5. [apps/speckit.md](apps/speckit.md): por dentro das ferramentas de especificação.

## Documentos gerais

| Documento | Assunto |
|---|---|
| [architecture.md](architecture.md) | Visão geral, mapa dos módulos, arquitetura decidida, integrações, configuração e pegadinhas |
| [workflow.md](workflow.md) | Fluxo de desenvolvimento: issue, spec, plano, tarefas, TDD, PR e portões de qualidade |
| [../.specify/memory/constitution.md](../.specify/memory/constitution.md) | Constituição do projeto (fonte das regras; não é gerada a partir do código) |

## Documentação por módulo

| Módulo | Documento | Onde fica o código |
|---|---|---|
| Ferramentas de SDD (spec-kit) | [apps/speckit.md](apps/speckit.md) | `.specify/` e `.claude/skills/` |

## Documentos que nascem com o código

Estes documentos ainda não existem porque o que eles descrevem ainda não existe. Criá-los antes seria inventar.

| Documento | Nasce quando | Previsto para |
|---|---|---|
| `docs/database.md` | O primeiro modelo do Django for criado | Milestone M0 (usuário customizado) |
| `docs/admin.md` | O painel administrativo do Django for configurado | M0 |
| `docs/apps/<app>.md` | Cada app do Django ou módulo do frontend nascer | A partir do M0 |

## Convenções da documentação

Estas regras valem para todo documento em `docs/` (Princípio VIII da constituição).

1. **Do leigo ao técnico.** Todo documento começa com uma visão geral sem jargão, com analogias, dizendo o que é, para que serve e como se usa. Só depois vêm os detalhes: campos, índices, fluxos, decisões, integrações e casos de borda.
2. **Só o que está no código.** Nada é inventado. O que é decisão ainda não implementada aparece marcado como tal, com a fonte. Na dúvida, abra o arquivo.
3. **Caminhos reais.** Os caminhos são relativos à raiz e, quando apontam para código, levam a linha (ex.: `.specify/scripts/bash/common.sh:163`). Use os nomes reais de funções e classes.
4. **Tabelas** para campos, rotas, variáveis de ambiente, arquivos e responsabilidades.
5. **Diagramas Mermaid** (`graph`, `sequenceDiagram`, `erDiagram`) sempre que houver hierarquia, fluxo ou relacionamento. O GitHub os desenha sozinho.
6. **Pegadinhas e dívidas técnicas** têm seção própria em cada documento: bugs latentes, TODOs, acoplamentos, segredos versionados e divergências entre o que se diz e o que o código faz.
7. **Português do Brasil.**
8. **Completo em vez de curto.** Na dúvida, prefira o detalhe.
9. **Blocos fechados.** Toda cerca de código ou de diagrama é fechada.

### Quando atualizar

- Um módulo novo ganha `docs/apps/<módulo>.md` e uma linha na tabela "Documentação por módulo".
- Modelo novo ou alterado: atualize `docs/database.md`, incluindo o diagrama ER.
- Rota, variável de ambiente, tarefa assíncrona ou peça de infraestrutura nova: atualize o documento do módulo e `docs/architecture.md`.
- A atualização vai no mesmo PR da mudança, e o revisor confere.

### Modelo de documento de módulo

```text
# <Módulo>
## Visão geral            (linguagem leiga, com analogia)
## Responsabilidades
## Estrutura de arquivos  (tabela: arquivo → papel)
## Modelos                (resumo + link para database.md)
## Rotas                  (tabela: rota → handler → nome → o que faz)
## Fluxos principais      (com diagramas)
## Integração com outros módulos (diagrama)
## Pegadinhas e dívidas técnicas
```
