# Backlog A - Produto/API (11/05/2026 a 21/05/2026)

Objetivo: Estruturar o backend fundacional para autenticação, perfis, cadastro de transportadoras e base de persistência.

## Tarefas (10)

### A-01
- ID da tarefa: `A-01`
- Título objetivo: Estruturar projeto FastAPI em camadas
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: API / arquitetura base
- Função/Módulo: `core`, `modules`, bootstrap da aplicação
- Descrição da entrega: Criar esqueleto FastAPI modular com versionamento de rotas e padrão de erro.
- Dependências: LOG-001; alinhamento de estrutura com Docs.
- Story points: `5`
- Definition of Done (DoD): Aplicação sobe localmente com `/health` e organização modular validada.
- Critérios de aceite testáveis: `GET /health` responde 200; estrutura de pastas segue padrão documentado.

### A-02
- ID da tarefa: `A-02`
- Título objetivo: Configurar conexão PostgreSQL e sessão SQLAlchemy
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Persistência
- Função/Módulo: `database/session`
- Descrição da entrega: Implementar conexão por variáveis de ambiente e gerenciamento de sessão/transação.
- Dependências: A-01; ambiente local provido por Infra.
- Story points: `3`
- Definition of Done (DoD): Sessão de banco disponível para módulos da API.
- Critérios de aceite testáveis: API conecta no banco local; erro de credencial retorna falha tratável e logada.

### A-03
- ID da tarefa: `A-03`
- Título objetivo: Criar migrations iniciais de usuários e perfis
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Banco de dados
- Função/Módulo: `migrations`, `models/users`
- Descrição da entrega: Definir modelos e migração inicial para usuários, perfis e relacionamentos mínimos.
- Dependências: A-02.
- Story points: `5`
- Definition of Done (DoD): `upgrade` e `downgrade` funcionam sem inconsistências.
- Critérios de aceite testáveis: Tabelas de usuários/perfis criadas com constraints básicas válidas.

### A-04
- ID da tarefa: `A-04`
- Título objetivo: Implementar autenticação JWT
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Segurança
- Função/Módulo: `modules/auth`
- Descrição da entrega: Criar login com emissão de token JWT e validação segura de credenciais.
- Dependências: A-03.
- Story points: `5`
- Definition of Done (DoD): Endpoints de auth operacionais e cobertos por casos de sucesso/erro.
- Critérios de aceite testáveis: Login válido retorna token; inválido retorna 401; token expirado é recusado.

### A-05
- ID da tarefa: `A-05`
- Título objetivo: Aplicar autorização por perfil nas rotas protegidas
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Autorização
- Função/Módulo: dependências/middlewares RBAC
- Descrição da entrega: Restringir rotas por perfil (admin, logística, gestor, auditoria).
- Dependências: A-04; matriz de permissões no Docs.
- Story points: `5`
- Definition of Done (DoD): Rotas sensíveis bloqueiam acessos indevidos por perfil.
- Critérios de aceite testáveis: Usuário sem perfil recebe 403; perfil auditoria mantém leitura sem edição.

### A-06
- ID da tarefa: `A-06`
- Título objetivo: Criar CRUD de transportadoras
- Prioridade: `P0`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Cadastro de transportadoras
- Função/Módulo: `modules/carriers`
- Descrição da entrega: Implementar create/list/update/inativar de transportadoras com metadados essenciais.
- Dependências: A-05.
- Story points: `5`
- Definition of Done (DoD): CRUD funcional com validações mínimas e inativação lógica.
- Critérios de aceite testáveis: Criação e edição persistem; inativação remove da listagem padrão.

### A-07
- ID da tarefa: `A-07`
- Título objetivo: Padronizar validação e respostas de erro
- Prioridade: `P1`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Qualidade de API
- Função/Módulo: `schemas`, `exception handlers`
- Descrição da entrega: Aplicar contratos de entrada/saída e mensagens de erro consistentes para auth e carriers.
- Dependências: A-04 e A-06.
- Story points: `3`
- Definition of Done (DoD): Endpoints principais seguem schema e padrões de erro definidos.
- Critérios de aceite testáveis: Payload inválido retorna 422 padronizado; respostas válidas seguem schema.

### A-08
- ID da tarefa: `A-08`
- Título objetivo: Criar testes automatizados mínimos de fundação
- Prioridade: `P1`
- Repositório responsável: `Api`
- Página/Tela/Área impactada: Testes backend
- Função/Módulo: `tests/auth`, `tests/carriers`
- Descrição da entrega: Cobrir login, autorização e CRUD básico de transportadoras.
- Dependências: A-06 e A-07.
- Story points: `3`
- Definition of Done (DoD): Suite essencial executa com resultado verde no ambiente local.
- Critérios de aceite testáveis: Casos críticos de auth e carriers passam sem falha.

### A-09
- ID da tarefa: `A-09`
- Título objetivo: Publicar contrato técnico dos endpoints fundacionais
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Documentação de integração API/Web
- Função/Módulo: Contratos de API
- Descrição da entrega: Documentar endpoints de auth e carriers para consumo do frontend.
- Dependências: A-04 a A-07.
- Story points: `2`
- Definition of Done (DoD): Documento publicado e referenciado no README da API.
- Critérios de aceite testáveis: Inclui exemplos de request/response e regras de autorização por perfil.

### A-10
- ID da tarefa: `A-10`
- Título objetivo: Consolidar checklist de prontidão backend da Sprint 1
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Governança de entrega
- Função/Módulo: Checklist de aceite
- Descrição da entrega: Consolidar critérios de fechamento técnico para LOG-001..005 no eixo backend.
- Dependências: A-01 a A-09.
- Story points: `2`
- Definition of Done (DoD): Checklist revisado na review técnica e aprovado.
- Critérios de aceite testáveis: Todos os critérios P0 mapeados com status, responsável e evidência.
