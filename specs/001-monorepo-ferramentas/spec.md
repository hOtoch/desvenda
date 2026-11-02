# Feature Specification: Monorepo e ferramentas do backend

**Feature Branch**: `001-monorepo-ferramentas`

**Created**: 2026-11-02

**Status**: Draft

**Input**: User description: "Issue #1 — Criar a estrutura `backend/` e `frontend/` (vazio por enquanto) e as ferramentas Python: uv, ruff, pytest, pytest-django, pytest-cov, pre-commit e o bloqueio de rede nos testes. Critérios: `uv sync` instala tudo com versões travadas em `uv.lock`; `ruff check` e `ruff format --check` passam; `pytest` roda e um teste que tenta abrir uma conexão de rede falha; o pre-commit roda o ruff antes de cada commit. Fora do escopo: Django (#2)."

## User Scenarios & Testing *(mandatory)*

Os usuários desta feature são quem desenvolve o Desvenda (pessoas e agentes de IA), não os alunos. Ela não entrega nada visível no produto: entrega a base que torna todo o código seguinte reproduzível, testável sem rede e uniforme.

### User Story 1 - Preparar o ambiente do backend com versões travadas (Priority: P1)

Quem acabou de clonar o repositório entra na área do backend, roda um comando de instalação e recebe exatamente as mesmas versões de todas as ferramentas de desenvolvimento que qualquer outra cópia do projeto, porque essas versões ficam travadas num arquivo versionado junto com o código.

**Why this priority**: sem um ambiente reproduzível, nenhum teste ou verificação das outras histórias é confiável ("funciona na minha máquina"). Todo o resto do backlog apoia aqui.

**Independent Test**: num clone limpo, rodar a instalação e comparar as versões instaladas com o arquivo de travamento; rodar a instalação de novo não muda nada.

**Acceptance Scenarios**:

1. **Given** um clone limpo do repositório e a ferramenta de instalação disponível na máquina, **When** o desenvolvedor roda o comando de instalação na área do backend, **Then** todas as ferramentas de desenvolvimento ficam disponíveis, nas versões registradas no arquivo de travamento.
2. **Given** um ambiente já preparado, **When** o comando de instalação roda de novo, **Then** nada é instalado ou removido e o arquivo de travamento não muda.
3. **Given** que a lista de dependências foi alterada sem atualizar o arquivo de travamento, **When** o modo de instalação verificada roda, **Then** ele falha e diz que os dois arquivos divergem.
4. **Given** o repositório, **When** o desenvolvedor olha a raiz, **Then** encontra a área do backend e a área reservada ao frontend, e esta traz um texto dizendo o que vai entrar nela e em que milestone.

---

### User Story 2 - Testes que nunca usam a rede (Priority: P1)

O desenvolvedor roda a suíte de testes com um comando e vê o resultado de cada teste e a cobertura de linhas do código. Qualquer teste que tente falar com um servidor fora da máquina falha na hora, com uma mensagem dizendo que a rede está bloqueada nos testes. Assim a suíte dá sempre o mesmo resultado, é rápida e nunca gasta dinheiro chamando um provedor de IA por engano (Princípio III da constituição).

**Why this priority**: o bloqueio precisa existir antes do primeiro código que chama um serviço externo (embeddings na #9, LLM na #17). Colocá-lo depois deixaria uma janela para testes dependentes de rede entrarem sem ninguém perceber.

**Independent Test**: com o ambiente preparado e a máquina desconectada da internet, a suíte passa; o teste-sentinela que tenta uma conexão externa prova que o bloqueio está ligado.

**Acceptance Scenarios**:

1. **Given** o ambiente preparado, **When** o desenvolvedor roda o comando de testes, **Then** a suíte roda, mostra o resultado de cada teste e um relatório de cobertura de linhas.
2. **Given** um teste que tenta abrir uma conexão com um destino fora da máquina, seja por nome ou por endereço numérico, **When** a suíte roda, **Then** a tentativa falha imediatamente, sem esperar tempo limite, com um erro que identifica o bloqueio de rede.
3. **Given** um teste que se conecta a um serviço na própria máquina, **When** a suíte roda, **Then** a conexão é permitida.
4. **Given** uma mudança de configuração que desligue o bloqueio, **When** a suíte roda, **Then** o teste-sentinela falha e denuncia a mudança.

---

### User Story 3 - Padrão de código verificado antes de cada commit (Priority: P2)

Um comando aponta erros comuns no código do backend e outro aponta diferenças de formatação. Depois que o desenvolvedor instala o gancho uma vez na sua cópia do repositório, essas verificações rodam sozinhas antes de cada commit: o que é seguro corrigir é corrigido automaticamente, e o commit é barrado para o desenvolvedor revisar a correção ou resolver o que não tem correção automática.

**Why this priority**: mantém o código uniforme e pega erros antes da revisão, mas depende do ambiente da US1 e não bloqueia o desenvolvimento se faltar por um tempo.

**Independent Test**: criar um arquivo do backend com problema de formatação e tentar o commit: ele é barrado e o arquivo sai corrigido; adicionar a correção e repetir: o commit passa.

**Acceptance Scenarios**:

1. **Given** o repositório recém-preparado, **When** o desenvolvedor roda as verificações de padrão e de formatação, **Then** nenhuma aponta problema.
2. **Given** o gancho instalado e um arquivo do backend com problema de formatação, **When** o desenvolvedor tenta o commit, **Then** o commit é barrado, o arquivo é corrigido no disco e a mensagem diz qual verificação mudou o arquivo.
3. **Given** o gancho instalado e um problema sem correção automática (por exemplo, um nome usado sem ter sido definido), **When** o desenvolvedor tenta o commit, **Then** o commit é barrado e a mensagem aponta o arquivo, a linha e o problema.
4. **Given** um arquivo que passa nas verificações manuais, **When** o desenvolvedor faz o commit com o gancho instalado, **Then** o gancho também o aceita, porque usa as mesmas regras e as mesmas versões.
5. **Given** um commit que só muda documentação, **When** o desenvolvedor faz o commit, **Then** o gancho não barra nem altera nada.

---

### Edge Cases

- **Ferramenta de instalação ausente na máquina:** o guia de entrada explica como instalá-la; sem ela, o primeiro comando falha com a mensagem do próprio sistema.
- **Versão da linguagem ausente ou antiga:** a instalação obtém a versão exigida pelo projeto ou falha dizendo qual versão falta, nunca prossegue com uma versão diferente.
- **Conexão externa por nome ou por endereço numérico:** as duas formas são bloqueadas, inclusive a consulta de nome que vem antes da conexão.
- **Serviço na própria máquina:** permitido, porque os testes de banco de dados (#3) e de fila dependem disso.
- **Gancho não instalado num clone novo ou commit feito pulando o gancho:** nada é verificado no commit. A rede de segurança é o CI (#4), que roda as mesmas verificações em todo PR; até ele existir, a revisão do PR confere.
- **Arquivo de travamento desatualizado:** a instalação comum atualiza o arquivo, e a instalação verificada falha; é a verificada que o CI vai usar.
- **Sistema operacional:** o desenvolvimento acontece no Windows e o CI vai rodar no Linux; os mesmos comandos precisam funcionar nos dois.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O repositório MUST ter uma área para o backend e uma área reservada para o frontend. A do frontend MUST conter só um texto que explica o que vai entrar nela e em que milestone.
- **FR-002**: Todas as ferramentas de desenvolvimento do backend MUST estar declaradas num único arquivo de dependências e travadas, com versões exatas, num arquivo de travamento versionado.
- **FR-003**: Um único comando, rodado na área do backend, MUST instalar todas as ferramentas nas versões travadas. Rodá-lo de novo MUST NOT mudar nada.
- **FR-004**: MUST existir um modo de instalação verificada que falha quando o arquivo de dependências e o de travamento divergem.
- **FR-005**: MUST existir um comando que roda toda a suíte de testes do backend e mostra um relatório de cobertura de linhas.
- **FR-006**: Durante os testes, toda tentativa de conexão com um destino fora da máquina MUST falhar imediatamente, com uma mensagem que identifica o bloqueio de rede.
- **FR-007**: Durante os testes, conexões com serviços na própria máquina MUST continuar permitidas.
- **FR-008**: A suíte MUST conter testes permanentes que provam o bloqueio (FR-006) e a liberação local (FR-007), de modo que uma mudança que desligue o bloqueio quebre a suíte.
- **FR-009**: MUST existir comandos que verificam, sem alterar arquivos, o padrão de código (erros comuns) e a formatação do backend.
- **FR-010**: Depois de instalado uma vez por cópia do repositório, um gancho MUST rodar as verificações de padrão e de formatação antes de cada commit, corrigir automaticamente o que for seguro e barrar o commit enquanto houver correção a revisar ou problema sem correção automática.
- **FR-011**: O gancho de commit e os comandos manuais MUST usar as mesmas regras e as mesmas versões das ferramentas.
- **FR-012**: Os comandos de instalação, testes e verificações MUST funcionar no Windows e no Linux.
- **FR-013**: O guia de entrada do repositório MUST trazer o passo a passo de instalação, testes, verificações e instalação do gancho, e a documentação do projeto MUST refletir a nova estrutura (Princípio VIII).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Seguindo só o guia de entrada, um desenvolvedor vai de um clone limpo a uma suíte de testes verde com no máximo 4 comandos e em até 5 minutos numa conexão doméstica comum.
- **SC-002**: Duas cópias preparadas em máquinas ou momentos diferentes têm 100% das ferramentas de desenvolvimento nas mesmas versões.
- **SC-003**: Com o ambiente já preparado e a máquina desconectada da internet, 100% da suíte passa.
- **SC-004**: 100% das tentativas de conexão externa feitas pelos testes falham em menos de 1 segundo, sem esperar tempo limite.
- **SC-005**: Com o gancho instalado, 100% dos commits com problema de padrão ou de formatação no backend são barrados, e os commits sem problema passam sem nenhum passo extra.
- **SC-006**: A suíte de testes desta feature roda em menos de 10 segundos.

## Assumptions

- As ferramentas concretas (gerenciador de dependências, verificador e formatador de código, executor de testes, gancho de commit) já estão fixadas na constituição, seção "Restrições técnicas", e na issue #1; o plano detalha versões e configuração.
- Tudo o que é do backend fica dentro da área do backend e é preparado a partir dela. O gancho de commit vale para o repositório inteiro, mas só verifica código do backend.
- A área do frontend só fica reservada nesta feature; nenhuma ferramenta de frontend é instalada. O frontend chega no milestone M4 (#26).
- O relatório de cobertura aparece, mas sem mínimo obrigatório: ainda não existe módulo de lógica pura. O mínimo de 90% do Princípio II passa a valer com o primeiro desses módulos (#8), e os portões automáticos chegam com o CI (#4).
- O gancho de commit é instalado uma vez em cada cópia do repositório; esse passo fica no guia de entrada.
- O gancho corrige automaticamente só o que é seguro (formatação e correções seguras de padrão) e sempre barra o commit quando mexe num arquivo, para que nenhuma mudança entre sem o desenvolvedor ver.
- Fora do escopo:
  - o framework web e tudo o que depende dele (#2);
  - banco de dados, fila e serviços em contêiner (#3);
  - o CI (#4);
  - o jeito de rodar sob demanda os testes contra provedores reais de IA, que chega com o primeiro teste desse tipo (#9).
