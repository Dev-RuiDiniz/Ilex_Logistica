DB TECNOLOGIA
Arquitetura, automação e inteligência operacional
ESCOPO PROJETO
ILEX LOGÍSTICA
Rastreio automatizado, atrasos, exceções e relatório diário
Documento profissional para apresentação ao cliente, guia técnico e base de execução da equipe.
| PRAZO   | NÍVEL        | SPRINTS  | FOCO                  |
| ------- | ------------ | -------- | --------------------- |
| 60 dias | MVP Avançado | 4 ciclos | Logística inteligente |
Gerado em 30/05/2026 | Branding: #050505, #B91C1C, #FFFFFF, #D1D5DB

ESCOPO PROJETO ILEX LOGISTICA
Sumário Executivo
O Ilex Logística é o segundo projeto modular da plataforma Ilex. Seu objetivo é automatizar o rastreio de
entregas, consolidar dados de transportadoras, identificar atrasos e exceções operacionais e gerar um relatório
diário de atenção para a equipe de logística.
O projeto será executado em 45 dias com foco em MVP avançado: base web segura, cadastros, importação de
dados, camada preparada para APIs/bots de transportadoras, painel de exceções, alertas e relatório diário. A
arquitetura será modular para permitir evolução posterior com crédito, financeiro, chatbot e integrações mais
profundas.
Problema resolvido Fluxo central
Reduz consultas manuais em portais de Coleta de dados > arquivamento > identificação de
transportadoras, centraliza status de entrega e atraso > painel de exceções > relatório diário
prioriza casos que exigem intervenção humana. matinal.
Entrega inicial Estratégia técnica
MVP web com dashboard logístico, importações, Começar com importação/API/bots de forma
regras de prazo, alertas, logs, histórico e relatórios. flexível, evitando dependência de uma única
transportadora e reduzindo risco de bloqueios por
scraping.
1. Visão Geral do Projeto
Item Definição
Nome do projeto Ilex Logística
Título comercial Rastreio automatizado, atrasos, exceções e relatório diário
Empresa DB Tecnologia
Tipo de sistema Plataforma web operacional / SaaS modular interno
Prazo estimado 45 dias
Nível MVP Avançado
Objetivo Centralizar o acompanhamento logístico e automatizar a identificação de entregas críticas.
Descrição executiva
O Ilex Logística será uma plataforma web voltada para inteligência operacional da área logística. O sistema irá
centralizar dados de entregas, capturar informações de transportadoras, armazenar históricos, identificar
mercadorias atrasadas e gerar um resumo diário com os pontos que demandam ação imediata.
Resumo visual
Indicador Quantidade/Descrição
Número de telas 18 telas web/admin previstas
Número de módulos 9 módulos funcionais
Número de perfis 4 perfis principais
DB Tecnologia | Documento técnico e executivo Página 2 de 13

ESCOPO PROJETO ILEX LOGISTICA
| Indicador |     | Quantidade/Descrição |     |     |
| --------- | --- | -------------------- | --- | --- |
| Prazo     |     | 45 dias              |     |     |
Modelo de entrega 4 sprints de aproximadamente 11 dias úteis ou ciclos quinzenais ajustados ao
calendário
Integrações iniciais Transportadoras via API, scraping controlado ou importação manual de planilhas
2. Perfis de Usuário
| Perfil | Tipo | Descrição | Permissões/Responsabilidades |     |
| ------ | ---- | --------- | ---------------------------- | --- |
Administrador Interno Usuário responsável pelas Gerenciar usuários, transportadoras, regras de
|     |     | configurações globais do | prazo, integrações, parâmetros e logs. |     |
| --- | --- | ------------------------ | -------------------------------------- | --- |
sistema.
Equipe de Operacional Usuário que acompanha Importar relatórios, consultar entregas, atualizar
Logística entregas e trata exceções. tratativas, visualizar painel de exceções e gerar
relatórios.
Gestor Logístico Gerencial Usuário responsável por Visualizar dashboard, indicadores, relatórios
|     |     | indicadores e priorização. | diários, gargalos e performance por |     |
| --- | --- | -------------------------- | ----------------------------------- | --- |
transportadora.
Auditoria/Backoff Controle Usuário de conferência e Consultar histórico, logs, alterações, falhas de
| ice |     | rastreabilidade. | coleta e evidências de tratativas. |     |
| --- | --- | ---------------- | ---------------------------------- | --- |
3. Mapeamento de Telas
App Mobile
O aplicativo mobile não faz parte do MVP de 45 dias. O projeto será entregue como plataforma web responsiva.
Uma futura versão mobile poderá permitir notificações e conferência em campo.
| Código | Nome | Descrição |     | Objetivo |
| ------ | ---- | --------- | --- | -------- |
M01 Não incluído no MVP Aplicativo mobile será evolução futura. Evitar aumento de escopo e
concentrar a entrega no fluxo web
operacional.
Web/Admin
| Código | Tela | Descrição |     | Objetivo |
| ------ | ---- | --------- | --- | -------- |
W01 Login Tela de autenticação segura. Permitir acesso protegido ao sistema.
W02 Dashboard Logístico Indicadores principais de entregas, atrasos e Dar visão executiva e operacional em
|     |     | exceções. |     | tempo real. |
| --- | --- | --------- | --- | ----------- |
W03 Transportadoras Cadastro e configuração de transportadoras. Manter dados de integração e regras
por parceiro.
W04 Importação de Upload de planilhas ou arquivos exportados. Recolher dados quando API/bot não
|     | Entregas |     |     | estiver disponível. |
| --- | -------- | --- | --- | ------------------- |
W05 Validação da Conferência de colunas, duplicidades e Evitar entrada de dados inválidos.
|     | Importação | inconsistências. |     |     |
| --- | ---------- | ---------------- | --- | --- |
W06 Entregas Lista geral de mercadorias rastreadas. Acompanhar status e histórico de
|     | Monitoradas |     |     | entrega. |
| --- | ----------- | --- | --- | -------- |
DB Tecnologia | Documento técnico e executivo Página 3 de 13

ESCOPO PROJETO ILEX LOGISTICA
Código Tela Descrição Objetivo
W07 Detalhe da Entrega Histórico, eventos, datas, ocorrência e Permitir análise individual.
tratativas.
W08 Painel de Exceções Fila priorizada de atrasos e ocorrências. Focar no que exige intervenção
imediata.
W09 Regras de Prazo Parâmetros por transportadora, região e tipo Definir critérios de atraso.
de entrega.
W10 Relatório Diário Resumo matinal com pontos críticos. Orientar rotina da equipe logística.
W11 Tratativas Registro de ações feitas pela equipe. Documentar acompanhamento
humano.
W12 Logs de Coleta Histórico das automações e falhas. Auditar execução de bots, APIs e
importações.
W13 Alertas Configuração e acompanhamento de alertas. Notificar atrasos e falhas críticas.
W14 Relatórios Exportações e relatórios gerenciais. Apoiar reuniões e acompanhamento.
W15 Usuários e Gestão de usuários. Controlar acesso por perfil.
Permissões
W16 Configurações Parâmetros gerais do sistema. Configurar ambiente, horários e
notificações.
W17 Integrações Credenciais e status de APIs/bots. Controlar conexões externas.
W18 Auditoria Histórico de eventos e alterações. Garantir rastreabilidade.
4. Módulos Funcionais
Autenticação e Permissões Transportadoras
Login seguro, sessão, perfis, proteção de rotas e Cadastro de parceiros logísticos, tipo de integração,
controle de acesso. credenciais, regras e status.
Coleta de Dados Arquivamento Histórico
Importação de planilhas, APIs e bots/scraping Banco centralizado com dados de entrega, eventos,
controlado para coleta de status de entrega. ocorrências e atualizações.
Monitoramento de Atrasos Painel de Exceções
Cálculo de prazo, SLA, atraso e criticidade por Fila priorizada com entregas fora do prazo, sem
mercadoria. atualização ou com ocorrência negativa.
Relatório Diário Alertas e Notificações
Resumo matinal automático com entregas críticas, Alertas por e-mail, dashboard e, futuramente,
atrasos e falhas de coleta. WhatsApp/Teams/Slack.
Logs e Auditoria
Registro de importações, coletas, falhas, alterações
e tratativas humanas.
DB Tecnologia | Documento técnico e executivo Página 4 de 13

ESCOPO PROJETO ILEX LOGISTICA
Funcionalidades essenciais do MVP
(cid:127) Cadastro de transportadoras e parâmetros de integração.
(cid:127) Importação de relatórios de entrega em Excel/CSV.
(cid:127) Validação de colunas obrigatórias, duplicidades e formatos.
(cid:127) Armazenamento de entregas e eventos em banco de dados central.
(cid:127) Identificação automática de atrasos com base em data prevista e regras de SLA.
(cid:127) Classificação de criticidade: normal, atenção, crítico e resolvido.
(cid:127) Painel de exceções para mercadorias que exigem ação humana.
(cid:127) Registro de tratativas por entrega.
(cid:127) Geração de relatório diário de atenção.
(cid:127) Logs detalhados de coletas, falhas e alterações.
5. Fluxos do Sistema
Onboarding
(cid:127) Cadastro dos usuários internos e definição de perfis.
(cid:127) Cadastro das transportadoras prioritárias.
(cid:127) Configuração de regras de prazo por transportadora, região ou tipo de frete.
(cid:127) Upload da primeira base de entregas ou conexão inicial com fonte externa.
(cid:127) Validação dos dados importados e homologação do painel de exceções.
Login
(cid:127) Usuário acessa a plataforma web.
(cid:127) Sistema valida credenciais e perfil.
(cid:127) Usuário é direcionado ao dashboard conforme permissões.
(cid:127) Ações sensíveis ficam registradas em auditoria.
Fluxo core - Rastreio e exceções
Etapa Descrição Resultado
1. Coleta Sistema importa ou consulta dados de entrega nas fontes Dados brutos coletados e versionados.
configuradas.
2. Validação Sistema valida campos obrigatórios, datas, códigos e Base confiável para processamento.
duplicidades.
3. Arquivamento Registros são salvos no banco com histórico e origem. Histórico consultável e auditável.
4. Análise Motor de regras calcula atraso, criticidade e status. Classificação operacional da entrega.
5. Exceções Sistema exibe apenas casos críticos ou em atenção. Equipe atua no que importa.
6. Relatório Resumo diário é gerado automaticamente. Gestão recebe visão matinal dos
riscos.
Processos internos
(cid:127) Rotina agendada de coleta por transportadora.
(cid:127) Rotina de recálculo de atrasos e criticidade.
DB Tecnologia | Documento técnico e executivo Página 5 de 13

ESCOPO PROJETO ILEX LOGISTICA
(cid:127) Rotina de geração do relatório diário.
(cid:127) Registro de falhas de integração e tentativas.
(cid:127) Registro de tratativas humanas e status de resolução.
6. Stack Tecnológico
Camada Tecnologias recomendadas Finalidade
Backend Python, FastAPI, SQLAlchemy, Pydantic, API principal, regras de atraso, jobs de coleta e
Celery/RQ relatórios.
Frontend Next.js, TypeScript, Tailwind CSS, shadcn/ui, Dashboard, tabelas, filtros, formulários e experiência
Recharts web.
Mobile Não incluído no MVP. Futuro: React Native ou Notificações e acompanhamento em campo em fase
Flutter. posterior.
Banco de Dados PostgreSQL Histórico de entregas, eventos, transportadoras, logs
e usuários.
Infraestrutura Docker, Nginx, GitHub Actions, Deploy, CI/CD, ambientes e operação.
VPS/AWS/Render/Railway
Integrações APIs de transportadoras, scraping Coleta de dados, alertas e armazenamento de
controlado, SMTP, storage relatórios.
7. Integrações
Integração Finalidade Observação para o MVP
APIs de transportadoras Consultar status, eventos e comprovantes de Usar quando houver API oficial disponível.
entrega.
Portais de transportadoras / Acessar relatórios quando não existir API. Implementar com cautela por risco de
bots captcha, bloqueio ou mudança de layout.
Importação Excel/CSV Entrada manual controlada de relatórios. Estratégia principal para reduzir risco no
primeiro ciclo.
SMTP / provedor de e-mail Enviar relatório diário para equipe. Pode usar SMTP corporativo, SendGrid,
Brevo ou SES.
Storage de arquivos Guardar relatórios originais e anexos. Pode ser local no MVP ou S3/compatível
em produção.
ERP/Sistema atual Buscar notas, pedidos ou clientes. Fora do núcleo do MVP, preparado para
fase futura.
Módulo de Crédito Ilex Cruzamento futuro entre logística e crédito. Não faz parte do Projeto 2, mas a
arquitetura ficará preparada.
Observação técnica: a esteira de crédito citada no escopo macro do Ilex permanece como projeto separado.
Neste documento, ela aparece apenas como integração futura e dependência arquitetural, não como entrega do
Projeto 2.
8. Segurança
DB Tecnologia | Documento técnico e executivo Página 6 de 13

ESCOPO PROJETO ILEX LOGISTICA
LGPD
Minimização de dados pessoais, controle de acesso, registro de tratamento e mascaramento de informações
sensíveis quando necessário.
Autenticação
Login seguro, tokens JWT, expiração de sessão e rotas protegidas por perfil.
Criptografia
Credenciais de transportadoras e tokens de integração devem ser criptografados em repouso e nunca expostos
no frontend.
Logs
Logs de coleta, importação, alteração, falha, tratativa e geração de relatórios devem ser persistidos para
auditoria.
Controle de acesso
Perfis separados para administrador, logística, gestor e auditoria, com restrição por ação e tela.
Auditoria operacional
Toda alteração de status, regra de prazo e tratativa deve registrar usuário, data, origem e justificativa quando
aplicável.
9. Design System
Cores oficiais do documento e interface
Elemento Cor Uso
Preto profundo #050505 Base principal, cabeçalhos, menus e contraste premium.
Vermelho premium #B91C1C Destaques, alertas críticos, botões primários e identidade visual.
Branco puro #FFFFFF Fundo de leitura, cards e áreas de conteúdo.
Cinza neutro #D1D5DB Bordas, divisórias, elementos de apoio e estados neutros.
Cinza escuro #1F2937 Textos principais e subtítulos.
Fundo claro #F8FAFC Áreas internas e agrupamento de cards.
Tipografia
(cid:127) Família recomendada: Inter, Noto Sans ou equivalente sem serifa.
(cid:127) Títulos com peso 700 e alto contraste.
(cid:127) Textos operacionais com peso 400/500 para leitura prolongada.
(cid:127) Tabelas densas com hierarquia por status e etiquetas.
Componentes
(cid:127) Cards de KPI: total de entregas, atrasos, críticos, sem atualização e resolvidos.
(cid:127) Tabelas filtráveis por transportadora, status, prazo, cidade, UF e criticidade.
(cid:127) Badges de status: No prazo, Atenção, Atrasado, Crítico, Resolvido, Sem atualização.
(cid:127) Timeline da entrega no detalhe individual.
(cid:127) Alertas visuais para exceções e falhas de coleta.
DB Tecnologia | Documento técnico e executivo Página 7 de 13

ESCOPO PROJETO ILEX LOGISTICA
(cid:127) Modais de confirmação para alteração de regras e encerramento de tratativas.
UX
(cid:127) Priorizar o painel de exceções como centro operacional.
(cid:127) Reduzir ruído: mostrar primeiro o que exige ação humana.
(cid:127) Permitir filtros rápidos por criticidade e transportadora.
(cid:127) Evitar excesso de cliques para registrar tratativas.
(cid:127) Exibir mensagens claras para falhas de importação e integração.
10. Divisão de Repositórios - GitHub Organization
Repositório Camada Tecnologias Responsabilidade
ilex-logistics-api Backend FastAPI, PostgreSQL, API principal, regras de prazo, coletas,
SQLAlchemy, Celery/RQ entregas, alertas e relatórios.
ilex-logistics-web Frontend Web Next.js, TypeScript, Tailwind, Interface, dashboard, painéis, filtros e
shadcn/ui gestão operacional.
ilex-logistics-mobile Mobile futuro React Native ou Flutter Reservado para fase futura; não
implementado no MVP.
ilex-logistics-infra Infraestrutura Docker, Nginx, GitHub Actions Deploy, CI/CD, ambientes, variáveis e
observabilidade.
ilex-logistics-integratio Integrações Python workers, clients de API, Conectores de transportadoras, bots e
ns Playwright adaptadores externos.
ilex-logistics-docs Documentação Markdown, PDFs, modelos Escopo, regras de negócio, manuais,
templates e atas.
Estrutura sugerida - API
ilex-logistics-api/app/modules/auth, users, carriers, shipments, imports, tracking, exceptions, reports, alerts,
audit; app/core; app/database; app/jobs; app/main.py; migrations; tests; Dockerfile; README.md.
Estrutura sugerida - Web
ilex-logistics-web/src/app, components, features/auth, dashboard, carriers, imports, shipments, exceptions,
reports, settings, audit; lib; services; public; package.json; README.md.
Estrutura sugerida - Integrations
ilex-logistics-integrations/connectors/api_clients, bots, parsers, mappers, tests, docs, examples. Cada
transportadora deve ter adaptador isolado para reduzir impacto de mudanças externas.
11. Organização Scrum - Sprints
O prazo total será de 45 dias, organizado em 4 sprints curtas. Essa estrutura permite checkpoints frequentes,
validação progressiva com o cliente e redução de riscos em integrações externas.
Sprint Período Objetivo
Sprint 1 - Fundação Dias 1 a 11 Setup, infra, banco, autenticação, perfis, layout base e cadastro de
transportadoras.
DB Tecnologia | Documento técnico e executivo Página 8 de 13

ESCOPO PROJETO ILEX LOGISTICA
Sprint Período Objetivo
Sprint 2 - Core Logístico Dias 12 a 22 Importação de entregas, validação de dados, armazenamento
histórico e listagem de entregas.
Sprint 3 - Exceções e Dias 23 a 34 Cálculo de atraso, painel de exceções, tratativas, alertas e relatório
Relatório diário.
Sprint 4 - Integrações, QA e Dias 35 a 45 Camada de integrações, logs avançados, testes, ajustes,
Deploy documentação e deploy.
Sprint 1 - Fundação
(cid:127) Criar repositórios e estrutura base.
(cid:127) Configurar PostgreSQL, migrations e ambiente Docker.
(cid:127) Criar autenticação e perfis.
(cid:127) Criar layout base do dashboard.
(cid:127) Criar cadastro de transportadoras.
(cid:127) Criar logs básicos.
Sprint 2 - Core
(cid:127) Criar importador Excel/CSV.
(cid:127) Validar colunas obrigatórias.
(cid:127) Salvar entregas e eventos.
(cid:127) Criar listagem com filtros.
(cid:127) Criar detalhe da entrega.
(cid:127) Criar histórico de importações.
Sprint 3 - Expansão
(cid:127) Criar regras de prazo e SLA.
(cid:127) Calcular atraso e criticidade.
(cid:127) Criar painel de exceções.
(cid:127) Criar tratativas por entrega.
(cid:127) Criar relatório diário matinal.
(cid:127) Criar alertas por e-mail/dashboard.
Sprint 4 - Finalização
(cid:127) Preparar conectores de API/bots.
(cid:127) Criar logs avançados de coleta.
(cid:127) Executar testes integrados.
(cid:127) Ajustar performance e UX.
(cid:127) Realizar deploy de homologação.
(cid:127) Criar documentação técnica e manual de uso.
12. Backlog Detalhado
DB Tecnologia | Documento técnico e executivo Página 9 de 13

ESCOPO PROJETO ILEX LOGISTICA
| ID Título | Descrição | Repo | Tipo Prior. | SP Critério de aceite |
| --------- | --------- | ---- | ----------- | --------------------- |
LOG-00 Criar arquitetura Estruturar API, Web, Infra, Todos feat Alta 3 Repositórios criados,
1 inicial dos Integrations e Docs. README inicial e estrutura
repositórios validada.
LOG-00 Configurar banco Criar conexão, migrations e ilex-logistics-api feat Alta 3 Banco sobe localmente e
| 2 PostgreSQL | modelos iniciais. |     |     | migrations executam com |
| ------------ | ----------------- | --- | --- | ----------------------- |
sucesso.
LOG-00 Criar autenticação Implementar login, sessão e api/web feat Alta 5 Usuário loga, acessa rotas
| 3 JWT | proteção de rotas. |     |     | protegidas e faz logout. |
| ----- | ------------------ | --- | --- | ------------------------ |
LOG-00 Criar perfis de Admin, Logística, Gestor e api/web feat Alta 3 Permissões aplicadas em
| 4 acesso | Auditoria. |     |     | telas e endpoints. |
| -------- | ---------- | --- | --- | ------------------ |
LOG-00 Criar cadastro de CRUD de transportadoras e api/web feat Alta 5 Transportadora pode ser
5 transportadoras tipo de integração. criada, editada, listada e
inativada.
LOG-00 Criar importador Upload de arquivos de api/web feat Alta 5 Sistema aceita arquivo
| 6 Excel/CSV | entregas. |     |     | válido e rejeita formato |
| ----------- | --------- | --- | --- | ------------------------ |
inválido.
LOG-00 Validar colunas Checar campos mínimos da api feat Alta 3 Erros são exibidos antes
| 7 obrigatórias | base. |     |     | do processamento. |
| -------------- | ----- | --- | --- | ----------------- |
LOG-00 Criar prévia de Mostrar amostra e web/api feat Média 3 Usuário visualiza dados
| 8 importação | inconsistências. |     |     | antes de confirmar. |
| ------------ | ---------------- | --- | --- | ------------------- |
LOG-00 Persistir entregas Salvar entregas e eventos no api feat Alta 5 Registros importados
| 9   | banco. |     |     | aparecem na listagem. |
| --- | ------ | --- | --- | --------------------- |
LOG-01 Criar histórico de Registrar arquivo, data, api/web feat Média 2 Histórico consultável por
| 0 importações | usuário e status. |     |     | período e status. |
| ------------- | ----------------- | --- | --- | ----------------- |
LOG-01 Criar listagem de Tabela com filtros e web/api feat Alta 5 Usuário filtra por
| 1 entregas | paginação. |     |     | transportadora, status, |
| ---------- | ---------- | --- | --- | ----------------------- |
período e UF.
LOG-01 Criar detalhe da Tela individual com timeline e web/api feat Média 3 Detalhe mostra dados,
| 2 entrega | eventos. |     |     | eventos e origem. |
| --------- | -------- | --- | --- | ----------------- |
LOG-01 Criar regras de Parâmetros por api/web feat Alta 5 Regras podem ser
| 3 prazo/SLA | transportadora/região. |     |     | cadastradas e aplicadas. |
| ----------- | ---------------------- | --- | --- | ------------------------ |
LOG-01 Calcular atraso Comparar data prevista, api feat Alta 5 Entrega fora do prazo
4 automaticamente atualizações e status. recebe status de atraso.
LOG-01 Classificar Normal, Atenção, Crítico e api feat Alta 3 Criticidade calculada
| 5 criticidade | Resolvido. |     |     | conforme regras. |
| ------------- | ---------- | --- | --- | ---------------- |
LOG-01 Criar painel de Fila priorizada de casos web/api feat Alta 5 Painel mostra apenas
| 6 exceções | críticos. |     |     | entregas que exigem |
| ---------- | --------- | --- | --- | ------------------- |
ação.
LOG-01 Criar registro de Usuário registra ação, web/api feat Média 3 Tratativas ficam no
| 7 tratativas | observação e status. |     |     | histórico da entrega. |
| ------------ | -------------------- | --- | --- | --------------------- |
LOG-01 Criar relatório Resumo matinal de atrasos e api/web feat Alta 5 Relatório é gerado e
| 8 diário | exceções. |     |     | visualizado no sistema. |
| -------- | --------- | --- | --- | ----------------------- |
LOG-01 Criar envio do Enviar resumo diário para api feat Média 3 E-mail é disparado e
| 9 relatório por e-mail | responsáveis. |     |     | registrado em log. |
| ---------------------- | ------------- | --- | --- | ------------------ |
LOG-02 Criar logs de coleta Registrar sucesso, falha e api/integrations feat Alta 3 Logs exibem status por
| 0   | tempo de execução. |     |     | fonte/transportadora. |
| --- | ------------------ | --- | --- | --------------------- |
LOG-02 Preparar Criar interface padrão para integrations/api feat Média 5 Conector base
1 conectores de API APIs de transportadoras. documentado e testável.
DB Tecnologia | Documento técnico e executivo Página 10 de 13

ESCOPO PROJETO ILEX LOGISTICA
ID Título Descrição Repo Tipo Prior. SP Critério de aceite
LOG-02 Preparar Criar estrutura isolada para integrations feat Média 5 Bot de exemplo executa
2 bots/scraping portais sem API. em ambiente controlado.
controlado
LOG-02 Criar dashboard KPIs, gráficos e cards web/api feat Alta 5 Dashboard mostra
3 logístico final operacionais. indicadores
reais/importados.
LOG-02 Criar auditoria de Registrar mudanças de regras api feat Média 3 Ações críticas ficam
4 alterações e tratativas. auditáveis.
LOG-02 Testes integrados e Testar importação, cálculo, todos fix Alta 5 Fluxo completo validado
5 QA painel, relatório e envio. em homologação.
LOG-02 Documentação final Manual de uso e docs feat Alta 3 Documentos entregues
6 documentação técnica. para cliente e equipe.
13. Fora do Escopo
(cid:127) Integração com todas as transportadoras do mercado no primeiro ciclo.
(cid:127) Garantia de funcionamento de scraping em portais com captcha, bloqueio ou mudanças frequentes sem manutenção
contínua.
(cid:127) Aplicativo mobile.
(cid:127) Chatbot interno.
(cid:127) Esteira de crédito e integração Serasa.
(cid:127) Módulo financeiro de comissões.
(cid:127) Integração completa com ERP, salvo documentação e API já disponíveis.
(cid:127) WhatsApp automático.
(cid:127) BI avançado com data warehouse.
(cid:127) Machine learning para previsão de atraso.
(cid:127) Roteirização de entregas.
(cid:127) Controle de frota próprio.
(cid:127) Assinatura digital ou comprovantes avançados fora dos arquivos coletados.
14. Diferenciais
(cid:127) Foco operacional em exceções, reduzindo ruído e priorizando ação humana.
(cid:127) Histórico centralizado de entregas e eventos por transportadora.
(cid:127) Arquitetura flexível para API, scraping ou importação manual.
(cid:127) Relatório diário matinal para rotina de acompanhamento.
(cid:127) Rastreabilidade completa com logs e auditoria.
(cid:127) Base preparada para evoluir com chatbot, crédito e financeiro.
(cid:127) Redução de atrasos não percebidos e melhoria de SLA logístico.
(cid:127) Potencial de produto SaaS modular para outros clientes com operação logística semelhante.
15. Design e Branding do Documento
DB Tecnologia | Documento técnico e executivo Página 11 de 13

DB TECNOLOGIA
Arquitetura, automação e inteligência operacional
APÊNDICE 1
SOLICITAÇÕES COMPLEMENTARES
ILEX LOGÍSTICA
Cotação de frete por pedido, campos fiscais, filtros e eficiência por transportadora
BASE TIPO PRAZO FOCO
Escopo Ilex Logística Aditivo técnico A validar Performance logística
Gerado em 13/05/2026 | Branding: #050505, #B91C1C, #FFFFFF, #D1D5DB

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
1. Objetivo do Apêndice
Este apêndice registra e organiza as solicitações complementares apresentadas pelo cliente para evolução
do módulo Ilex Logística. O objetivo é transformar as marcações feitas na interface e as observações
operacionais em requisitos claros, backlog técnico, critérios de aceite e estratégia de implantação.
As  solicitações  ampliam  a  tela  de  logística  atual  com  campos  fiscais,  informações  de  frete,  filtros
avançados, quadro de eficiência por transportadora e uma nova subaba de cotação de frete por pedido.
2. Enquadramento no Escopo Original
O escopo original do Ilex Logística já contempla dashboard logístico, importação Excel/CSV, cadastro de
transportadoras, histórico de entregas, filtros, relatórios, painel de exceções, alertas, logs e arquitetura
preparada para APIs, bots e integrações futuras com ERP. As novas demandas são compatíveis com essa
base,  mas  devem  ser  classificadas  em  duas  frentes:  extensão  direta  do  MVP  e  evolução  funcional
dependente de ERP/transportadoras.
| Frente | Descrição | Classificação |     |
| ------ | --------- | ------------- | --- |
Ajustes da tela atual Novas colunas, filtros, busca ampliada, mês/ano e quadro de eficiência MVP / Sprint atual
por transportadora.
Cotação de frete por pedido Leitura de pedidos do ERP e comparação de valores entre Módulo adicional / Fase
|     | transportadoras. | 2   |     |
| --- | ---------------- | --- | --- |
Braspress Fluxo inicial validado por exportação de relatório e importação de Integração assistida
planilha.
3. Solicitações do Cliente e Tratamento Técnico
| Item Solicitação | Implementação proposta | Impacto | Entrada |
| ---------------- | ---------------------- | ------- | ------- |
1 Adicionar subaba: Cotação de Criar uma nova área dentro do módulo Logística para listar Alta Fase 2 / módulo
Frete por Pedido pedidos novos do ERP, executar cotação de frete por pedido adicional
e comparar os valores por transportadora.
2 Adicionar coluna com número da Incluir o campo número da nota fiscal na base de entregas, Baixa MVP
| nota fiscal | importações, listagem e detalhe da entrega. |     |     |
| ----------- | ------------------------------------------- | --- | --- |
3 Adicionar coluna com data de Incluir data de saída/coleta para permitir análise entre Baixa/Média MVP
| saída da coleta | coleta, previsão, entrega e atraso. |     |     |
| --------------- | ----------------------------------- | --- | --- |
4 Adicionar coluna com valor do Registrar valor de frete por entrega/nota fiscal e exibir na Baixa MVP
| frete | tabela principal. |     |     |
| ----- | ----------------- | --- | --- |
5 Adicionar coluna com % do frete Calcular percentual do frete com base na fórmula: valor do Baixa/Média MVP
frete dividido pelo valor da nota fiscal, multiplicado por 100.
6 Adicionar filtros e busca ampliada Filtros por transportadora, cliente e UF. Busca por nota fiscal, Média MVP
cliente, rastreio e UF.
7 Adicionar quadro de eficiência por Exibir total de notas, entregues no prazo, atrasadas, Média/Alta MVP
| transportadora | extraviadas e percentuais por transportadora. |     |     |
| -------------- | --------------------------------------------- | --- | --- |
8 Filtrar por mês, ano e todo o Filtro temporal global para recalcular a tabela, os KPIs e o Média MVP
| período                                             | quadro de eficiência por transportadora. |     |          |
| --------------------------------------------------- | ---------------------------------------- | --- | -------- |
| Apêndice 1 - Solicitações complementares do cliente |                                          |     | Página 2 |

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
4. Ajustes na Tela Atual de Logística
A tela atual de Logística Inteligente deve permanecer como o painel principal de acompanhamento de
entregas. As alterações propostas ampliam o valor operacional da tabela e transformam a visão atual em
uma análise de rastreio, custo e desempenho logístico.
4.1 Tabela Principal Revisada
Rastreio NF Cliente Transportadora UF Destino Data Previsão Status Valor NF Valor % Frete
Coleta Frete
BR333222111 123456 Construtora ABC Braspress SC Florianópolis 04/05/2026 06/05/2026 Entregue R$ 34.500 R$ 980 2,84%
BR987654321 123457 Atacado Mineiro LogExpress BA Salvador 03/05/2026 07/05/2026 Atrasado R$ 42.300 R$ 1.420 3,36%
4.2 Filtros e Busca
Componente Comportamento esperado
Busca geral Pesquisar por nota fiscal, cliente, rastreio, UF e transportadora.
Filtro de status Todos, em trânsito, entregue, atrasado, extraviado e demais status configurados.
Filtro de transportadora Permitir selecionar uma ou múltiplas transportadoras.
Filtro de cliente Permitir busca por cliente com autocomplete quando houver grande volume.
Filtro de UF Selecionar uma ou múltiplas UFs de destino.
Filtro temporal Mês, ano e opção de todo o período.
4.3 Fórmula do Percentual do Frete
O percentual do frete deve ser calculado automaticamente sempre que houver valor do frete e valor da
nota fiscal preenchidos.
percentual_frete = (valor_frete / valor_nota_fiscal) x 100
Quando algum dos valores estiver ausente ou zerado, o sistema deve exibir campo vazio ou indicador de
dado indisponível, evitando divisão por zero.
5. Quadro de Eficiência por Transportadora
O espaço inferior da tela deve receber um quadro gerencial de eficiência por transportadora. Esse bloco
deve ser recalculado com base nos filtros ativos da página, especialmente período, transportadora, cliente
e UF.
5.1 Exemplo de Estrutura
Transportadora Total NF No Prazo % No Prazo Atrasadas % Extraviad % Frete Total % Frete
Atrasadas as Extraviadas Médio
Braspress 115 98 85,22% 14 12,17% 3 2,61% R$ 64.200 3,12%
Transportadora A 80 70 87,50% 8 10,00% 2 2,50% R$ 42.900 2,94%
5.2 Indicadores Recomendados
(cid:127) Total de notas fiscais no período filtrado.
Apêndice 1 - Solicitações complementares do cliente Página 3

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
(cid:127) Quantidade e percentual de entregas no prazo.
(cid:127) Quantidade e percentual de notas atrasadas.
(cid:127) Quantidade e percentual de notas extraviadas.
(cid:127) Valor total de frete por transportadora.
(cid:127) Percentual médio de frete sobre o valor da nota fiscal.
(cid:127) Ranking visual por eficiência, custo médio e volume operacional.
Apêndice 1 - Solicitações complementares do cliente Página 4

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
6. Nova Subaba: Cotação de Frete por Pedido
A nova subaba deve ser tratada como evolução funcional do módulo Logística. Ela amplia o sistema de
rastreio para apoiar a tomada de decisão antes da expedição, comparando cotações entre transportadoras
por pedido.
6.1 Estrutura da Subaba
Menu sugerido: Logística > Cotação de Frete por Pedido. Como alternativa, a tela de Logística pode usar
abas internas: Entregas Monitoradas, Cotação de Frete por Pedido, Eficiência por Transportadora,
Importações e Relatórios.
6.2 Tabela de Cotação
Nº Pedido Data Cliente UF Valor Transportad Transportad Transportad Transportad Melhor Opção
Destino ora A ora B ora C ora D
10245 13/05/2026 Cliente ABC SP R$ 3.500,00 R$ 180,00 R$ 210,00 R$ 195,00 R$ 220,00 Transportadora A
10246 13/05/2026 Cliente XYZ RJ R$ 8.900,00 R$ 420,00 R$ 385,00 R$ 410,00 R$ 455,00 Transportadora B
6.3 Regras da Cotação
(cid:127) Cada pedido novo do ERP deve gerar uma linha de cotação.
(cid:127) Cada transportadora habilitada deve retornar um valor de frete ou status de indisponibilidade.
(cid:127) O sistema deve destacar a melhor opção por menor preço ou por regra configurável.
(cid:127) A regra futura pode considerar prazo, custo, UF, histórico de eficiência e restrições operacionais.
(cid:127) O histórico da cotação deve ser armazenado para auditoria e comparação posterior.
6.4 Modos de Implantação
Modo Descrição Recomendação
MVP assistido Importação de pedidos por Excel/CSV exportado do ERP e Mais seguro para início.
preenchimento/cálculo de cotações por regras ou planilhas.
Automatizado Leitura de pedidos via API do ERP e consulta de cotação por API das Após validação de APIs.
transportadoras.
Híbrido ERP via planilha ou API e transportadoras via combinação de API, planilha, Cenário provável.
tabela negociada ou portal.
7. Modelo de Dados Complementar
Os campos abaixo devem complementar o modelo de entregas e permitir evolução futura para pedidos e
cotações.
Entidade/Campo Descrição Obrigatório?
shipment.invoice_number Número da nota fiscal vinculada à entrega. Sim, quando
houver NF
shipment.invoice_value Valor da nota fiscal usado para cálculo do percentual de frete. Sim para % frete
shipment.freight_value Valor do frete da entrega. Opcional
shipment.freight_percentage Campo calculado: frete / valor da NF x 100. Calculado
shipment.collection_departure_date Data de saída/coleta da mercadoria. Opcional
Apêndice 1 - Solicitações complementares do cliente Página 5

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
| Entidade/Campo | Descrição | Obrigatório? |
| -------------- | --------- | ------------ |
order.external_order_number Número do pedido vindo do ERP. Sim para
cotação
freight_quote.carrier_id Transportadora consultada na cotação. Sim
freight_quote.quoted_value Valor retornado para o pedido/transportadora. Sim
freight_quote.status Cotado, indisponível, erro, pendente ou vencido. Sim
| Apêndice 1 - Solicitações complementares do cliente |     | Página 6 |
| --------------------------------------------------- | --- | -------- |

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
8. Backlog Técnico Complementar
ID Tarefa Repo Prior. Critério de aceite
LOG-027 Adicionar campos fiscais e financeiros na API/Web Alta Campos NF, valor NF, frete, % frete e data
entrega de coleta disponíveis.
LOG-028 Exibir número da nota fiscal na tabela Web Alta Tabela mostra NF e permite ordenação/filtro
quando aplicável.
LOG-029 Adicionar data de saída/coleta API/Web Alta Data pode ser importada, exibida e usada
em relatórios.
LOG-030 Adicionar valor do frete API/Web Alta Valor do frete aparece na listagem, detalhe
e exportação.
LOG-031 Calcular percentual do frete API/Web Alta Sistema calcula e trata campos ausentes ou
zerados.
LOG-032 Expandir filtros de logística API/Web Alta Filtros por transportadora, cliente, UF, mês,
ano e todo período.
LOG-033 Melhorar busca global API/Web Alta Busca por NF, cliente, rastreio, UF e
transportadora.
LOG-034 Criar eficiência por transportadora API/Web Alta Quadro exibe total, no prazo, atrasos,
extravios e percentuais.
LOG-035 Recalcular indicadores por período API/Web Alta KPIs e eficiência respondem ao filtro de
mês/ano/todo período.
LOG-036 Criar subaba Cotação de Frete por Pedido Web/API Média/Alta Tela criada com estrutura de tabela
comparativa.
LOG-037 Criar importador de pedidos do ERP por API/Web Média Pedidos importados aparecem na tela de
planilha cotação.
LOG-038 Documentar contrato de integração com ERP Docs/API Média Campos mínimos, endpoints e formato de
importação definidos.
LOG-039 Criar motor comparativo de cotação API Alta Sistema compara transportadoras por
pedido.
LOG-040 Criar ranking de melhor frete API/Web Média Melhor opção destacada por regra
configurável.
LOG-041 Documentar fluxo Braspress Docs/Integrations Alta Passo a passo de exportação/importação
documentado sem credenciais sensíveis.
Apêndice 1 - Solicitações complementares do cliente Página 7

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
9. Critérios de Aceite
Os critérios abaixo devem ser usados para homologação das novas solicitações com o cliente.
9.1 Tela de Entregas Monitoradas
(cid:127) A tabela exibe número da nota fiscal, data de saída/coleta, valor do frete e percentual do frete.
(cid:127) A busca localiza registros por nota fiscal, cliente, rastreio, UF e transportadora.
(cid:127) Os filtros por transportadora, cliente, UF, mês, ano e todo o período funcionam em conjunto.
(cid:127) Os KPIs superiores e o quadro inferior são recalculados conforme os filtros aplicados.
(cid:127) O percentual de frete é calculado corretamente e não quebra quando houver valores ausentes ou zerados.
9.2 Eficiência por Transportadora
(cid:127) O quadro apresenta uma linha por transportadora no período filtrado.
(cid:127) Total de notas, entregues no prazo, atrasadas e extraviadas conferem com a base importada.
(cid:127) Percentuais são calculados com base no total de notas da transportadora.
(cid:127) O quadro pode ser utilizado para comparação gerencial entre transportadoras.
9.3 Cotação de Frete por Pedido
(cid:127) A subaba exibe pedidos novos vindos de importação ou integração com ERP.
(cid:127) Cada pedido mostra valores de cotação por transportadora habilitada.
(cid:127) O sistema destaca a melhor opção conforme regra configurada.
(cid:127) Falhas de cotação ficam registradas com status e mensagem operacional.
(cid:127) O histórico da cotação pode ser auditado posteriormente.
10. Integração Braspress e Importação Assistida
Para a Braspress, a abordagem inicial recomendada é importação assistida por relatório exportado. O fluxo
enviado indica pesquisa por período limitado e exportação de dados em planilha. Essa estratégia reduz
risco técnico no MVP, pois não depende de automação em portal, captcha ou API não confirmada.
Fluxo recomendado:
(cid:127) Usuário acessa o portal da transportadora e gera o relatório no período permitido.
(cid:127) Usuário exporta os dados para Excel.
(cid:127) Sistema Ilex importa a planilha.
(cid:127) Sistema valida colunas obrigatórias, duplicidades e formatos.
(cid:127) Entregas, notas, status, datas e valores são atualizados.
(cid:127) Dashboard e eficiência por transportadora são recalculados automaticamente.
Observação de segurança: credenciais, CNPJ, senhas e dados de acesso de transportadoras devem ser
tratados como informação sensível. Esses dados não devem ser expostos no frontend, documentação
pública, prints, repositórios ou commits.
11. Riscos, Dependências e Decisões Pendentes
Ponto Risco/Dependência Ação recomendada
ERP A leitura automática de pedidos depende de API, banco, Solicitar documentação, campos e
exportação ou arquivo padronizado do ERP. ambiente de homologação.
Apêndice 1 - Solicitações complementares do cliente Página 8

ESCOPO PROJETO ILEX LOGISTICA - APENDICE 1 DB Tecnologia | Documento tecnico e executivo
Ponto Risco/Dependência Ação recomendada
Transportadoras Nem todas as transportadoras podem possuir API de cotação ou Começar com importação/planilha e
rastreio. evoluir por conector.
Braspress Portal pode ter restrição de período, layout ou autenticação. Padronizar fluxo de exportação e
importação assistida.
Cálculo de eficiência É necessário definir o que conta como no prazo, atraso e extravio. Validar regras de SLA com a
operação.
Percentual do frete Depende da disponibilidade do valor da nota fiscal e do valor do Validar origem dos dados antes do
frete. cálculo.
Recomendação final
Implementar imediatamente os ajustes da tela atual, filtros e quadro de eficiência por transportadora
dentro do MVP. A subaba de Cotação de Frete por Pedido deve ser planejada como evolução do módulo,
iniciando por importação de pedidos/planilhas e avançando para integração automática com ERP e
transportadoras conforme disponibilidade técnica.
Apêndice 1 - Solicitações complementares do cliente Página 9