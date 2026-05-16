# Checklist UAT - Importação e Listagem de Shipments

## Sprint 2 Trilha B - Frontend Admin

## Pré-requisitos

- [ ] Backend API rodando em `http://127.0.0.1:8000`
- [ ] Frontend Web rodando em `http://localhost:3000`
- [ ] Usuário autenticado com perfil admin, logistica ou gestor
- [ ] Arquivo CSV de teste válido disponível
- [ ] Arquivo CSV de teste com erros disponível

## Testes de Autenticação e RBAC

### Permissões de Edição (canEditShipments)

**Perfil: admin, logistica, gestor**
- [ ] Acessar `/shipments/import` - deve exibir tela de importação
- [ ] Input de arquivo deve estar habilitado
- [ ] Botão "Fazer Upload" deve estar habilitado
- [ ] Botão "Confirmar Importação" deve estar habilitado quando validado

**Perfil: auditoria**
- [ ] Acessar `/shipments/import` - deve exibir mensagem "Perfil com permissão somente leitura"
- [ ] Input de arquivo deve estar desabilitado
- [ ] Botões de ação devem estar desabilitados

### Permissões de Visualização (canViewShipments)

**Perfil: admin, logistica, gestor, auditoria**
- [ ] Acessar `/shipments` - deve exibir tabela de listagem
- [ ] Dados devem ser carregados da API

**Perfil sem permissão**
- [ ] Acessar `/shipments` - deve exibir mensagem "Perfil sem permissão para visualizar envios"
- [ ] Tabela não deve carregar dados

## Fluxo de Importação de Shipments

### 1. Upload CSV

**Cenário: Upload de arquivo válido**
- [ ] Navegar para `/shipments/import`
- [ ] Selecionar arquivo CSV válido (MIME type text/csv ou extensão .csv)
- [ ] Nome do arquivo deve ser exibido
- [ ] Clicar em "Fazer Upload"
- [ ] Spinner deve aparecer: "Fazendo upload do arquivo..."
- [ ] Estado deve mudar para `validated` ou `failed`
- [ ] Resumo de validação deve ser exibido

**Cenário: Upload de arquivo inválido**
- [ ] Selecionar arquivo não CSV (ex: .txt, .pdf)
- [ ] Mensagem de erro deve aparecer: "Por favor, selecione um arquivo CSV válido (.csv)."
- [ ] Nome do arquivo não deve ser exibido
- [ ] Botão "Fazer Upload" deve estar desabilitado

**Cenário: Cancelar upload**
- [ ] Selecionar arquivo CSV
- [ ] Clicar em "Limpar"
- [ ] Input deve ser limpo
- [ ] Nome do arquivo deve desaparecer
- [ ] Estado deve voltar para `idle`

**Cenário: Erro de API no upload**
- [ ] Simular erro de API
- [ ] Mensagem de erro deve aparecer com Error.message
- [ ] Estado deve mudar para `failed`
- [ ] Botão "Tentar Novamente" deve estar disponível

### 2. Validação e Exibição de Erros

**Cenário: Validação bem-sucedida**
- [ ] Upload de CSV válido
- [ ] Resumo deve mostrar: total_rows, valid_rows, invalid_rows
- [ ] valid_rows deve ser maior que 0
- [ ] invalid_rows deve ser 0 ou maior
- [ ] Tabela de erros não deve aparecer (se invalid_rows = 0)

**Cenário: Validação com erros**
- [ ] Upload de CSV com erros
- [ ] Resumo deve mostrar: total_rows, valid_rows, invalid_rows
- [ ] invalid_rows deve ser maior que 0
- [ ] Tabela de erros deve aparecer
- [ ] Tabela deve ter colunas: Linha, Campo, Mensagem, Valor
- [ ] Tabela deve ter scroll vertical (max-height: 256px)
- [ ] Header deve ser sticky
- [ ] Cada erro deve mostrar row_number, field, message, value

**Cenário: Validação falhou completamente**
- [ ] Upload de CSV totalmente inválido
- [ ] Mensagem deve aparecer: "Validação falhou. Verifique os erros abaixo."
- [ ] Botão "Confirmar Importação" deve estar desabilitado
- [ ] Botão "Tentar Novamente" deve estar disponível

### 3. Confirmação de Importação

**Cenário: Confirmar importação válida**
- [ ] Upload de CSV válido
- [ ] Estado deve ser `validated`
- [ ] valid_rows deve ser maior que 0
- [ ] Clicar em "Confirmar Importação"
- [ ] Spinner deve aparecer: "Processando importação..."
- [ ] Estado deve mudar para `importing`
- [ ] Estado deve mudar para `completed` ou `failed`

**Cenário: Importação bem-sucedida**
- [ ] Após confirmação, estado deve ser `completed`
- [ ] Resumo deve mostrar: total_rows, imported_count, rejected_count
- [ ] imported_count deve ser maior que 0
- [ ] Mensagem "Importação Concluída" deve aparecer (verde)
- [ ] Botão "Nova Importação" deve estar disponível

**Cenário: Importação com rejeições**
- [ ] Após confirmação, estado deve ser `completed`
- [ ] Resumo deve mostrar: imported_count, rejected_count
- [ ] rejected_count pode ser maior que 0
- [ ] Tabela de erros pode aparecer se houver erros na importação

**Cenário: Importação falhou**
- [ ] Após confirmação, estado deve ser `failed`
- [ ] Mensagem deve aparecer: "Importação falhou. Verifique os erros abaixo."
- [ ] Tabela de erros deve aparecer se houver erros
- [ ] Botão "Tentar Novamente" deve estar disponível

**Cenário: Cancelar importação**
- [ ] Após validação, clicar em "Cancelar"
- [ ] Estado deve voltar para `idle`
- [ ] Arquivo deve ser limpo
- [ ] Resumo deve desaparecer

**Cenário: Erro de API na confirmação**
- [ ] Simular erro de API ao confirmar
- [ ] Mensagem de erro deve aparecer com Error.message
- [ ] Estado deve mudar para `failed`
- [ ] Botão "Tentar Novamente" deve estar disponível

### 4. Tela de Conclusão

**Cenário: Nova importação após conclusão**
- [ ] Após importação concluída, clicar em "Nova Importação"
- [ ] Estado deve voltar para `idle`
- [ ] Todos os campos devem ser limpos
- [ ] Input de arquivo deve estar pronto para novo upload

## Fluxo de Listagem de Shipments

### 1. Listagem Básica

**Cenário: Carregar listagem**
- [ ] Navegar para `/shipments`
- [ ] Tabela deve ser exibida
- [ ] Colunas devem ser: Tracking, Carrier ID, Status, Entrega Estimada, Nota Fiscal, Doc. Fiscal, Valor, Vencimento, Atraso (dias), Criticidade
- [ ] Dados devem ser carregados da API
- [ ] Paginação deve ser exibida se houver mais de 20 itens

**Cenário: Empty state**
- [ ] Filtrar para não retornar resultados
- [ ] Mensagem deve aparecer: "Nenhum envio encontrado."

**Cenário: Loading state**
- [ ] Carregar listagem
- [ ] Texto deve aparecer: "Carregando..."
- [ ] Botões devem estar desabilitados

**Cenário: Error state**
- [ ] Simular erro de API
- [ ] Mensagem de erro deve aparecer: "Não foi possível carregar envios."
- [ ] Tabela não deve mostrar dados

**Cenário: Formatação de dados**
- [ ] Verificar formato de moeda: R$ 1.234,56
- [ ] Verificar formato de data: 16/05/2026
- [ ] Verificar valores nulos: devem exibir "-"

**Cenário: Badges de criticidade**
- [ ] Verificar badge Normal: verde
- [ ] Verificar badge Baixa: amarelo
- [ ] Verificar badge Média: laranja
- [ ] Verificar badge Alta: vermelho

### 2. Busca Global

**Cenário: Busca por código de rastreio**
- [ ] Seletor de tipo: "Código de rastreio"
- [ ] Placeholder deve ser: "Código de rastreio"
- [ ] Digitar código de rastreio
- [ ] Clicar em "Buscar"
- [ ] Resultados devem filtrar por tracking_code
- [ ] Página deve resetar para 1

**Cenário: Busca por nota fiscal**
- [ ] Seletor de tipo: "Nota fiscal"
- [ ] Placeholder deve ser: "Número da nota fiscal"
- [ ] Digitar número da nota fiscal
- [ ] Clicar em "Buscar"
- [ ] Resultados devem filtrar por invoice_number
- [ ] Página deve resetar para 1

**Cenário: Busca automática (heurística)**
- [ ] Seletor de tipo: "Automático (heurística)"
- [ ] Placeholder deve ser: "Código de rastreio ou nota fiscal"
- [ ] Digitar valor numérico (ex: 12345)
- [ ] Clicar em "Buscar"
- [ ] Resultados devem filtrar por invoice_number
- [ ] Digitar valor não numérico (ex: ABC123)
- [ ] Clicar em "Buscar"
- [ ] Resultados devem filtrar por tracking_code

**Cenário: Busca vazia**
- [ ] Deixar campo de busca vazio
- [ ] Clicar em "Buscar"
- [ ] Todos os registros devem ser exibidos
- [ ] Filtros de busca não devem ser aplicados

### 3. Filtros Avançados

**Cenário: Filtro por status**
- [ ] Selecionar status: "Pendente"
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por status = pending
- [ ] Página deve resetar para 1

**Cenário: Filtro por carrier_id**
- [ ] Digitar ID da transportadora
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por carrier_id
- [ ] Página deve resetar para 1

**Cenário: Filtro por criticality**
- [ ] Selecionar criticidade: "Alta"
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por criticality = alta
- [ ] Página deve resetar para 1

**Cenário: Filtro por entrega estimada (de/até)**
- [ ] Selecionar data de: 2026-05-01
- [ ] Selecionar data até: 2026-05-31
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por estimated_delivery no intervalo
- [ ] Página deve resetar para 1

**Cenário: Filtro por vencimento (de/até)**
- [ ] Selecionar data de: 2026-05-01
- [ ] Selecionar data até: 2026-05-31
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por due_date no intervalo
- [ ] Página deve resetar para 1

### 4. Filtro Temporal por Mês/Ano

**Cenário: Ativar filtro temporal**
- [ ] Marcar checkbox "Filtro por mês/ano"
- [ ] Seletor de target deve aparecer
- [ ] Select de mês deve aparecer
- [ ] Select de ano deve aparecer

**Cenário: Filtro temporal por entrega estimada**
- [ ] Checkbox marcado
- [ ] Seletor de target: "Entrega estimada"
- [ ] Selecionar mês: "Maio"
- [ ] Selecionar ano: "2026"
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por estimated_delivery em 01/05/2026 a 31/05/2026
- [ ] Inputs manuais de entrega estimada devem estar desabilitados

**Cenário: Filtro temporal por vencimento**
- [ ] Checkbox marcado
- [ ] Seletor de target: "Vencimento"
- [ ] Selecionar mês: "Maio"
- [ ] Selecionar ano: "2026"
- [ ] Clicar em "Aplicar Filtros"
- [ ] Resultados devem filtrar por due_date em 01/05/2026 a 31/05/2026
- [ ] Inputs manuais de vencimento devem estar desabilitados

**Cenário: Desativar filtro temporal**
- [ ] Desmarcar checkbox "Filtro por mês/ano"
- [ ] Seletor de target deve desaparecer
- [ ] Select de mês deve desaparecer
- [ ] Select de ano deve desaparecer
- [ ] Inputs manuais de data devem ser reabilitados

**Cenário: Ano bissexto**
- [ ] Checkbox marcado
- [ ] Selecionar mês: "Fevereiro"
- [ ] Selecionar ano: "2024"
- [ ] Clicar em "Aplicar Filtros"
- [ ] Intervalo deve ser 01/02/2024 a 29/02/2024 (29 dias)

### 5. Ordenação

**Cenário: Ordenar por data de criação**
- [ ] Seletor de ordenação: "Data de criação"
- [ ] Ordem deve ser "Descendente" (padrão)
- [ ] Resultados devem ser ordenados por created_at desc
- [ ] Clicar em botão de ordem
- [ ] Ordem deve mudar para "Ascendente"
- [ ] Resultados devem ser ordenados por created_at asc

**Cenário: Ordenar por entrega estimada**
- [ ] Seletor de ordenação: "Entrega estimada"
- [ ] Clicar em botão de ordem
- [ ] Resultados devem ser ordenados por estimated_delivery

**Cenário: Ordenar por vencimento**
- [ ] Seletor de ordenação: "Vencimento"
- [ ] Clicar em botão de ordem
- [ ] Resultados devem ser ordenados por due_date

**Cenário: Ordenar por valor**
- [ ] Seletor de ordenação: "Valor"
- [ ] Clicar em botão de ordem
- [ ] Resultados devem ser ordenados por amount

**Cenário: Ordenar por criticidade**
- [ ] Seletor de ordenação: "Criticidade"
- [ ] Clicar em botão de ordem
- [ ] Resultados devem ser ordenados por criticality

**Cenário: Reload automático**
- [ ] Mudar ordenação
- [ ] Resultados devem recarregar automaticamente
- [ ] Não precisa clicar em "Aplicar Filtros"

### 6. Controles de Ação

**Cenário: Limpar filtros**
- [ ] Aplicar vários filtros
- [ ] Clicar em "Limpar Filtros"
- [ ] Todos os filtros devem ser resetados
- [ ] Ordenação deve voltar para padrão (created_at desc)
- [ ] Página deve voltar para 1
- [ ] Todos os registros devem ser exibidos

**Cenário: Paginação**
- [ ] Navegar para página 2
- [ ] Botão "Anterior" deve estar habilitado
- [ ] Clicar em "Anterior"
- [ ] Página deve voltar para 1
- [ ] Botão "Anterior" deve estar desabilitado
- [ ] Clicar em "Próxima"
- [ ] Página deve avançar
- [ ] Botão "Próxima" deve estar desabilitado na última página

**Cenário: Disabled states durante loading**
- [ ] Carregar listagem
- [ ] Todos os botões devem estar desabilitados
- [ ] Inputs devem estar desabilitados

### 7. Limitações Conhecidas

**Cenário: Carrier ID exibido**
- [ ] Verificar que tabela exibe carrier_id (número)
- [ ] Verificar que nome da transportadora não é exibido
- [ ] Banner informativo deve mencionar esta limitação

**Cenário: Filtros de cliente/UF não disponíveis**
- [ ] Verificar que não há filtros de cliente/UF
- [ ] Banner informativo deve mencionar esta limitação

**Cenário: Rota de detalhe não disponível**
- [ ] Verificar que não há botão "Ver Envios" após conclusão da importação
- [ ] Verificar que não há link para detalhe na tabela

**Cenário: Ações de CRUD não disponíveis**
- [ ] Verificar que não há botões de editar/excluir na tabela
- [ ] Verificar que não há formulário de edição

## Testes de Responsividade

**Desktop**
- [ ] Filtros devem aparecer em grid de 3 colunas
- [ ] Busca deve aparecer em linha única

**Mobile**
- [ ] Filtros devem aparecer em grid de 1 coluna
- [ ] Busca deve aparecer em coluna única
- [ ] Tabela deve ter scroll horizontal se necessário

## Testes de Navegação

**Sidebar**
- [ ] Link "Envios" deve estar presente
- [ ] Link deve estar destacado quando em `/shipments`
- [ ] Link "Importar Envios" deve estar presente
- [ ] Link deve estar destacado quando em `/shipments/import`

## Testes de Performance

**Carregamento**
- [ ] Listagem deve carregar em < 3 segundos
- [ ] Upload deve completar em < 5 segundos
- [ ] Importação deve completar em < 10 segundos

**Interação**
- [ ] Filtros devem aplicar instantaneamente
- [ ] Paginação deve ser responsiva

## Testes de Acessibilidade

**Contraste**
- [ ] Texto deve ter contraste suficiente
- [ ] Badges de criticidade devem ser legíveis

**Foco**
- [ ] Inputs devem receber foco corretamente
- [ ] Botões devem ser acessíveis por teclado

**Labels**
- [ ] Todos os inputs devem ter labels associados

## Testes de Compatibilidade

**Browsers**
- [ ] Testar no Chrome
- [ ] Testar no Firefox
- [ ] Testar no Edge

**API**
- [ ] Endpoints devem responder corretamente
- [ ] Erros de API devem ser tratados adequadamente
