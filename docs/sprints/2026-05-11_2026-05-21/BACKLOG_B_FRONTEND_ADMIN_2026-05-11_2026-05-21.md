# Backlog B - Frontend/Admin (11/05/2026 a 21/05/2026)

Objetivo: Entregar base web com autenticação integrada, layout inicial e fluxo principal de transportadoras.

## Tarefas (10)

### B-01
- ID da tarefa: `B-01`
- Título objetivo: Scaffold da aplicação Next.js com TypeScript
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Fundação frontend
- Função/Módulo: `src/app`, configs base
- Descrição da entrega: Estruturar projeto com app router, lint e organização inicial por features.
- Dependências: LOG-001; estrutura base definida.
- Story points: `3`
- Definition of Done (DoD): App inicia localmente com rota raiz funcional.
- Critérios de aceite testáveis: `npm run dev` sobe sem erro e rota inicial renderiza.

### B-02
- ID da tarefa: `B-02`
- Título objetivo: Implementar layout base autenticado
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Shell da aplicação
- Função/Módulo: `layout`, navegação principal
- Descrição da entrega: Criar shell com menu, cabeçalho e área de conteúdo para rotas privadas.
- Dependências: B-01.
- Story points: `5`
- Definition of Done (DoD): Shell aplicável às páginas protegidas e responsivo.
- Critérios de aceite testáveis: Usuário autenticado vê menu e conteúdo em desktop/tablet sem quebra.

### B-03
- ID da tarefa: `B-03`
- Título objetivo: Construir tela de login integrada à API
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Login
- Função/Módulo: `features/auth/login`
- Descrição da entrega: Implementar formulário de login com consumo do endpoint JWT.
- Dependências: A-04 (contrato de auth API).
- Story points: `5`
- Definition of Done (DoD): Login funcional com feedback de erro/sucesso e redirecionamento.
- Critérios de aceite testáveis: Credencial válida autentica; inválida exibe erro claro sem quebrar UI.

### B-04
- ID da tarefa: `B-04`
- Título objetivo: Proteger rotas por autenticação
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Rotas privadas
- Função/Módulo: Guardas/middleware de rota
- Descrição da entrega: Impedir acesso sem sessão e redirecionar para login.
- Dependências: B-03.
- Story points: `3`
- Definition of Done (DoD): Navegação protegida consistente para usuários não autenticados.
- Critérios de aceite testáveis: Acesso anônimo a rota privada redireciona para login.

### B-05
- ID da tarefa: `B-05`
- Título objetivo: Aplicar visibilidade por perfil na interface
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Menu e ações sensíveis
- Função/Módulo: Controle de permissões frontend
- Descrição da entrega: Exibir/esconder áreas e ações conforme perfil do usuário.
- Dependências: A-05 e B-04.
- Story points: `5`
- Definition of Done (DoD): Interface respeita matriz de perfis definida.
- Critérios de aceite testáveis: Perfil auditoria sem ações de edição; admin com acesso completo.

### B-06
- ID da tarefa: `B-06`
- Título objetivo: Criar listagem de transportadoras com filtros básicos
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Tela de transportadoras
- Função/Módulo: Listagem (`carriers/list`)
- Descrição da entrega: Exibir tabela de transportadoras com busca por nome e status.
- Dependências: A-06 e B-02.
- Story points: `3`
- Definition of Done (DoD): Listagem integra com API e trata loading/erro.
- Critérios de aceite testáveis: Filtro por nome funciona; status ativo/inativo é exibido corretamente.

### B-07
- ID da tarefa: `B-07`
- Título objetivo: Implementar formulário de cadastro/edição de transportadora
- Prioridade: `P0`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Formulário de transportadoras
- Função/Módulo: `carriers/form`
- Descrição da entrega: Criar formulário com validação mínima para create/update.
- Dependências: B-06 e A-06.
- Story points: `5`
- Definition of Done (DoD): Fluxo de create/update com retorno visual de sucesso/erro.
- Critérios de aceite testáveis: Criar e editar reflete na tabela; validação bloqueia envio inválido.

### B-08
- ID da tarefa: `B-08`
- Título objetivo: Implementar inativação com confirmação
- Prioridade: `P1`
- Repositório responsável: `Web`
- Página/Tela/Área impactada: Ações da listagem
- Função/Módulo: `carriers/actions`
- Descrição da entrega: Adicionar modal de confirmação para inativação e atualização imediata da tabela.
- Dependências: B-07 e A-06.
- Story points: `2`
- Definition of Done (DoD): Inativação protegida e sincronizada com API.
- Critérios de aceite testáveis: Após confirmação, item some da visão padrão sem recarregar página.

### B-09
- ID da tarefa: `B-09`
- Título objetivo: Documentar fluxo de navegação e permissões
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: Guia de produto
- Função/Módulo: Navegação Sprint 1
- Descrição da entrega: Registrar fluxo login -> áreas privadas -> transportadoras, com regras por perfil.
- Dependências: B-05 a B-08.
- Story points: `2`
- Definition of Done (DoD): Documento revisado por frontend e backend.
- Critérios de aceite testáveis: Fluxo completo descrito com critérios de acesso por perfil.

### B-10
- ID da tarefa: `B-10`
- Título objetivo: Criar checklist UAT básico da trilha Web
- Prioridade: `P1`
- Repositório responsável: `Docs`
- Página/Tela/Área impactada: QA funcional
- Função/Módulo: Roteiro de validação Sprint 1
- Descrição da entrega: Definir roteiro manual de validação para login, guardas e CRUD de transportadoras.
- Dependências: B-03 a B-08.
- Story points: `3`
- Definition of Done (DoD): Roteiro executável com evidências esperadas por caso.
- Critérios de aceite testáveis: Casos felizes e de erro principais documentados com resultado esperado.
