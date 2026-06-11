# BETA Assisted Homologation Checklist

## Importação de Dados Sintéticos

- [ ] Preparar arquivo CSV sintético no formato Braspress
- [ ] Upload de arquivo via UploadFile
- [ ] Preview de importação gerado
- [ ] Validação de linhas válidas/inválidas
- [ ] Detecção de duplicatas
- [ ] Confirmação de importação
- [ ] Persistência de shipments no banco

## Validação de Registros

- [ ] Campos obrigatórios preenchidos
- [ ] Formato de datas brasileiro validado
- [ ] Formato monetário brasileiro validado
- [ ] Validação de schema
- [ ] Tratamento de erros de validação
- [ ] Logs de importação registrados

## Persistência de Shipments

- [ ] Shipments persistidos no banco
- [ ] Campos fiscais/financeiros persistidos
- [ ] Transportadora reconhecida
- [ ] Tracking codes únicos
- [ ] Invoice numbers únicos
- [ ] Dados de cliente persistidos

## SLA

- [ ] Regras de SLA configuradas
- [ ] Cálculo de dias de trânsito
- [ ] Cálculo de atraso
- [ ] Classificação de criticidade
- [ ] Detecção de shipments late
- [ ] Detecção de shipments critical
- [ ] SLA badges exibidos corretamente

## Exceções

- [ ] Regras de exceção configuradas
- [ ] Detecção de exceções
- [ ] Classificação de severidade
- [ ] Painel de exceções exibe dados
- [ ] Filtros de exceção funcionam
- [ ] Tratativas associadas

## Tratativas

- [ ] Criação de tratativas
- [ ] Associação com shipment
- [ ] Status de tratativa
- [ ] Timeline de tratativas
- [ ] Histórico de tratativas
- [ ] Audit logs de tratativas

## Alertas

- [ ] Geração de alertas automáticos
- [ ] Alertas de SLA critical
- [ ] Alertas de SLA late
- [ ] Alertas de exceções
- [ ] Painel de alertas exibe dados
- [ ] Filtros de alerta funcionam
- [ ] Marcar como lido funciona
- [ ] Marcar como resolvido funciona

## Relatório Diário

- [ ] Geração de relatório diário
- [ ] Consolidação de KPIs
- [ ] Inclusão de alertas ativos
- [ ] Inclusão de eficiência por transportadora
- [ ] Inclusão de falhas de importação
- [ ] Relatório exibe dados corretamente
- [ ] Filtros de relatório funcionam
- [ ] Exportação de relatório

## Auditoria

- [ ] Registro de audit logs
- [ ] Logs de importação
- [ ] Logs de relatório
- [ ] Logs de alerta
- [ ] Logs de SLA
- [ ] Logs de tratativas
- [ ] Filtros de auditoria funcionam
- [ ] Resumo estatístico exibido
- [ ] Detalhe de log exibido

## RBAC

- [ ] Papéis configurados (admin, logistica, gestor, auditoria, manager, operator, viewer)
- [ ] Permissões configuradas por papel
- [ ] Endpoints protegidos por permissão
- [ ] 401 para não autenticado
- [ ] 403 para sem permissão
- [ ] Admin pode acessar tudo
- [ ] Viewer pode ler mas não escrever
- [ ] Operator pode escrever endpoints operacionais
- [ ] Manager pode acessar relatórios e alertas
- [ ] Auditoria pode acessar audit logs

## Frontend

- [ ] Dashboard renderiza dados sintéticos
- [ ] Importações não quebram
- [ ] Shipments listam dados sintéticos
- [ ] Exceções aparecem corretamente
- [ ] Alertas são exibidos
- [ ] Relatório diário mostra dados
- [ ] Auditoria lista eventos
- [ ] Users/RBAC funcionam
- [ ] Navegação por permissão
- [ ] Sidebar condicional

## 401/403

- [ ] 401 renderiza tela de login
- [ ] 403 renderiza AccessDenied
- [ ] AccessDenied tem botão de voltar
- [ ] AccessDenied tem mensagem clara
- [ ] Redirecionamento após login funciona
- [ ] Refresh token funciona

## Build

- [ ] Lint 0 errors
- [ ] Testes 100% passing
- [ ] Build OK
- [ ] TypeScript compila
- [ ] Assets gerados
- [ ] Rotas estáticas geradas

## Gates

- [ ] check_secrets verdes (1 falso positivo documentado)
- [ ] check_secrets --self-test OK
- [ ] validate_migrations OK
- [ ] validate_docs OK
- [ ] beta_validate OK

## Limitações

- [ ] Importação via service_v2 (API não testada diretamente, UploadFile validado)
- [ ] Relatório diário via service (API não testada diretamente, contrato validado)
- [ ] Audit logs via service (API não testada diretamente, contrato validado)
- [ ] Dados sintéticos podem não cobrir todos os edge cases
- [ ] GitHub CLI não autenticado

## Aceite Técnico

- [ ] Todos os critérios obrigatórios atendidos
- [ ] Limitações conhecidas documentadas
- [ ] Riscos mitigados
- [ ] Evidências registradas
- [ ] Runbook validado
- [ ] Matriz go/no-go preenchida

## Rejeição Técnica

- [ ] Critérios obrigatórios não atendidos
- [ ] Limitações críticas não mitigadas
- [ ] Riscos severos não mitigados
- [ ] Evidências insuficientes
- [ ] Runbook incompleto
- [ ] Matriz go/no-go incompleta

## Rollback

- [ ] Migrations revertidas
- [ ] Código revertido
- [ ] Frontend revertido
- [ ] Build revertido
- [ ] Validação pós-rollback
- [ ] Evidências de rollback registradas

## Notas

Este checklist é operacional para o agente/equipe técnica quando houver ambiente de homologação. Não requer ação manual do usuário.
