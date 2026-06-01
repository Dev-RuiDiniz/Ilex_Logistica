# Backlog C - Infra/QA/Governança (11/05/2026 a 21/05/2026)

Objetivo: Garantir ambiente reproduzível, CI mínimo, observabilidade inicial e governança Scrum da Sprint 1.

## Tarefas (10)

### C-01
- ID da tarefa: `C-01`
- Título objetivo: Criar docker-compose base para API + PostgreSQL
- Prioridade: `P0`
- Repositório responsável: `Infra`
- Página/Tela/Área impactada: Ambiente local
- Função/Módulo: `docker-compose`
- Descrição da entrega: Definir serviços mínimos para API e banco com rede e volume persistente.
- Dependências: A-01 e A-02.
- Story points: `5`
- Definition of Done (DoD): Stack sobe com comando único em ambiente local.
- Critérios de aceite testáveis: `docker compose up` inicia serviços; API responde healthcheck.

### C-02
- ID da tarefa: `C-02`
- Título objetivo: Padronizar variáveis de ambiente
- Prioridade: `P0`
- Repositório responsável: `Infra`
- Página/Tela/Área impactada: Configuração
- Função/Módulo: `env templates`
- Descrição da entrega: Criar `.env.example` e instruções de preenchimento para API e Web.
- Dependências: C-01.
- Story points: `3`
- Definition of Done (DoD): Templates publicados e consistentes com os serviços.
- Critérios de aceite testáveis: Novo integrante sobe ambiente seguindo apenas documentação.

### C-03
- ID da tarefa: `C-03`
- Título objetivo: Configurar CI inicial da API
- Prioridade: `P0`
- Repositório responsável: `Infra`
- Página/Tela/Área impactada: Pipeline backend
- Função/Módulo: Workflow GitHub Actions da API
- Descrição da entrega: Executar lint e testes básicos da API no fluxo de integração.
- Dependências: A-08 e C-02.
- Story points: `3`
- Definition of Done (DoD): Pipeline valida API e sinaliza falhas automaticamente.
- Critérios de aceite testáveis: Workflow passa com branch saudável e falha ao quebrar teste.

### C-04
- ID da tarefa: `C-04`
- Título objetivo: Configurar CI inicial do Web
- Prioridade: `P0`
- Repositório responsável: `Infra`
- Página/Tela/Área impactada: Pipeline frontend
- Função/Módulo: Workflow GitHub Actions do Web
- Descrição da entrega: Executar lint/build do frontend com cache de dependências.
- Dependências: B-01 e C-02.
- Story points: `3`
- Definition of Done (DoD): Pipeline do Web valida build e bloqueia regressões básicas.
- Critérios de aceite testáveis: Workflow falha em erro de build/lint e passa em estado saudável.

### C-05
- ID da tarefa: `C-05`
- Título objetivo: Implementar healthchecks e logs básicos
- Prioridade: `P1`
- Repositório responsável: `Infra`
- Página/Tela/Área impactada: Observabilidade inicial
- Função/Módulo: Healthcheck Docker e logging
- Descrição da entrega: Configurar sinais de saúde e padrão mínimo de logs para troubleshooting.
- Dependências: C-01.
- Story points: `3`
- Definition of Done (DoD): Serviços com estado de saúde observável e logs acessíveis.
- Critérios de aceite testáveis: Falha simulada no DB reflete estado unhealthy com causa nos logs.

### C-06
- ID da tarefa: `C-06`
- Título objetivo: Criar templates de Issue e PR
- Prioridade: `P1`
- Repositório responsável: `.github`
- Página/Tela/Área impactada: Governança GitHub
- Função/Módulo: Templates de trabalho Scrum
- Descrição da entrega: Padronizar issue e PR com campos de DoD, critérios e validação.
- Dependências: Definição de rito no Docs.
- Story points: `2`
- Definition of Done (DoD): Novas issues/PRs seguem formato rastreável.
- Critérios de aceite testáveis: Template exige ID, testes e evidências antes da submissão.

### C-07
- ID da tarefa: `C-07`
- Título objetivo: Publicar ADR-001 de arquitetura fundacional
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Arquitetura
- Função/Módulo: ADR
- Descrição da entrega: Registrar decisões de stack, limites por repositório e consequências técnicas.
- Dependências: A-01, B-01 e C-01.
- Story points: `3`
- Definition of Done (DoD): ADR aprovado em revisão técnica.
- Critérios de aceite testáveis: Documento contém contexto, decisão, alternativas e consequências.

### C-08
- ID da tarefa: `C-08`
- Título objetivo: Publicar matriz de riscos da Sprint 1
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Gestão de riscos
- Função/Módulo: Matriz de risco
- Descrição da entrega: Mapear riscos com probabilidade, impacto, gatilhos e mitigação.
- Dependências: C-05 e C-07.
- Story points: `2`
- Definition of Done (DoD): Matriz revisada no planning e acompanhada nas dailies.
- Critérios de aceite testáveis: Todo risco P0/P1 possui dono e ação de mitigação definida.

### C-09
- ID da tarefa: `C-09`
- Título objetivo: Definir plano de QA mínimo para LOG-001..005
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: QA
- Função/Módulo: Plano de teste da Sprint 1
- Descrição da entrega: Definir estratégia de validação funcional/técnica para critérios de aceite.
- Dependências: A-08, B-10, C-03 e C-04.
- Story points: `5`
- Definition of Done (DoD): Plano executável com casos e critérios de saída da sprint.
- Critérios de aceite testáveis: Cada critério de aceite da sprint tem ao menos um teste associado.

### C-10
- ID da tarefa: `C-10`
- Título objetivo: Estruturar pacote de cerimônias Scrum da semana
- Prioridade: `P2`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Ritual de equipe
- Função/Módulo: Atas e roteiros Scrum
- Descrição da entrega: Criar templates para Planning, Daily, Review e Retro com foco em execução.
- Dependências: C-08 e C-09.
- Story points: `5`
- Definition of Done (DoD): Cerimônias executadas com registros de decisão e ação.
- Critérios de aceite testáveis: Atas registram impedimentos, decisões e responsáveis com prazo.
