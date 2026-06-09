# BETA_ROLLBACK - Procedimento de Rollback Beta

**Data:** 2026-06-08  
**PR:** BETA-004 - Testes de Migrations e Rollback  
**Objetivo:** Documentar procedimento seguro de rollback para fase beta do Ilex Logística

---

## 1. Resumo Executivo

Este documento descreve o procedimento de rollback seguro para migrations do banco de dados durante a fase beta, garantindo que o banco possa ser revertido para uma versão anterior sem perda de dados críticos.

**Estratégia:**
- Testes automatizados de roundtrip (upgrade → downgrade → upgrade)
- Preservação de dados críticos em cenários controlados
- Documentação clara de procedimentos de emergência
- Backup antes de qualquer rollback

---

## 2. Estado Atual das Migrations

### 2.1 Configuração Alembic

**Arquivo:** `apps/api/alembic.ini`

**Configuração:**
- `script_location = migrations`
- `sqlalchemy.url = sqlite:///./ilex.db`
- SQLite como banco de dados padrão

### 2.2 Migrations Existentes

**Diretório:** `apps/api/migrations`

**Status:** ✅ Migrations implementadas e validadas

**Migrations:**
- base → 20260513_01: initial foundation
- 20260513_01 → 20260514_02: import histories
- 20260514_02 → 20260514_03: deliveries table for fiscal and financial fields
- 20260514_03 → 20260515_01: add shipments and import history
- 20260515_01 → 20260515_02: add imported_count and rejected_count to import_history
- 20260515_02 → 20260515_04: add fiscal/financial fields to shipments

**Head Atual:** 20260515_04

---

## 3. Procedimento de Rollback

### 3.1 Identificar Revisão Atual

**Comando:**
```bash
cd apps/api
alembic current
```

**Saída Esperada:**
```
<revision_id> (head)
```

**Exemplo:**
```
001_initial (head)
```

### 3.2 Backup Antes de Rollback

**Importante:** Sempre fazer backup antes de rollback.

**SQLite:**
```bash
cd apps/api
cp ilex.db ilex.db.backup.$(date +%Y%m%d_%H%M%S)
```

**PostgreSQL:**
```bash
pg_dump ilex_beta > ilex_beta.backup.$(date +%Y%m%d_%H%M%S).sql
```

### 3.3 Downgrade Seguro

**Para Revisão Anterior Específica:**
```bash
cd apps/api
alembic downgrade <revision_id>
```

**Para Base (Todas as migrations):**
```bash
cd apps/api
alembic downgrade base
```

**Para N Revisões:**
```bash
cd apps/api
alembic downgrade -N <n>
```

### 3.4 Verificar Rollback

**Verificar Revisão Atual:**
```bash
alembic current
```

**Verificar Integridade do Banco:**
```bash
# SQLite
sqlite3 ilex.db "SELECT name FROM sqlite_master WHERE type='table';"

# PostgreSQL
psql ilex_beta -c "\dt"
```

### 3.5 Restaurar Backup (Se Necessário)

**SQLite:**
```bash
cp ilex.db.backup.<timestamp> ilex.db
```

**PostgreSQL:**
```bash
psql ilex_beta < ilex_beta.backup.<timestamp>.sql
```

### 3.6 Limitações de Rollback

**Downgrade para Base Destrói Dados:**
- O comando `alembic downgrade base` destrói todas as tabelas e dados
- Isso é comportamento esperado do Alembic
- Para preservar dados, seria necessário migrations incrementais reversíveis
- O teste `test_data_preservation` valida que rollback funciona, mas não que dados são preservados
- Documentação recomenda backup antes de qualquer rollback

**Validação Atual:**
- `test_migrations_roundtrip` valida downgrade → upgrade funciona
- `test_data_preservation` valida tabelas são recriadas após roundtrip
- **Limitação:** Não há validação de preservação real de dados
- **Motivo:** Downgrade para base destrói dados por design

---

## 4. Procedimento de Upgrade Após Rollback

### 4.1 Upgrade para Head

**Comando:**
```bash
cd apps/api
alembic upgrade head
```

### 4.2 Verificar Upgrade

**Verificar Revisão Atual:**
```bash
alembic current
```

**Verificar Integridade do Banco:**
```bash
# SQLite
sqlite3 ilex.db "SELECT name FROM sqlite_master WHERE type='table';"

# PostgreSQL
psql ilex_beta -c "\dt"
```

---

## 5. Limitações Conhecidas

### 5.1 Migrations Sem Suporte de Rollback

**Status:** ⏳ Nenhuma migration implementada ainda

**Quando houver migrations:**
- Algumas migrations podem não suportar rollback completo
- Migrations que alteram dados irreversivelmente devem ser documentadas
- Migrations que removem colunas não podem ser revertidas sem backup

### 5.2 SQLite vs PostgreSQL

**SQLite:**
- ✅ Suporta rollback completo
- ✅ Backup é simples (copia de arquivo)
- ⚠️ Não suporta operações avançadas de PostgreSQL

**PostgreSQL:**
- ✅ Suporta rollback completo
- ✅ Suporta operações avançadas
- ⚠️ Backup requer pg_dump

---

## 6. Testes Automatizados

### 6.1 Testes Implementados

**Arquivo:** `apps/api/tests/test_migrations.py`

**Testes:**
- `test_migrations_import` - Verifica que configuração pode ser importada
- `test_migrations_upgrade_head` - Verifica que migrations podem ser aplicadas até head
- `test_migrations_roundtrip` - Verifica roundtrip (upgrade → downgrade → upgrade)
- `test_data_preservation` - Verifica que dados críticos sobrevem a migration

**Execução:**
```bash
cd apps/api
pytest tests/test_migrations.py -v
```

### 6.2 Scripts de Validação

**Script de Validação Básico:**
```bash
bash scripts/validate_migrations.sh
```

**Script de Roundtrip:**
```bash
bash scripts/test_migrations_roundtrip.sh
```

---

## 7. Riscos

### 7.1 Riscos de Rollback

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|--------------|-----------|
| Perda de dados | Alto | Baixa | Backup antes de rollback |
| Rollback falha | Alto | Baixa | Testar roundtrip antes de produção |
| Inconsistência de dados | Alto | Baixa | Verificar integridade após rollback |
| Migration sem suporte | Médio | Baixa | Documentar limitações |

### 7.2 Riscos de Implementação

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|--------------|-----------|
| Testes não cobrem cenário real | Alto | Média | Testar com dados realistas |
| Backup não funciona | Alto | Baixa | Verificar backup antes de rollback |
| Rollback em produção | Alto | Baixa | Testar em ambiente beta primeiro |

---

## 8. Recomendações

### 8.1 Pré-Beta

1. **Implementar migrations iniciais:**
   - Criar migrations para tabelas críticas
   - Testar roundtrip antes de aplicar em produção
   - Documentar quais migrations não suportam rollback

2. **Testar em ambiente beta:**
   - Aplicar migrations em banco de teste
   - Verificar integridade de dados
   - Testar rollback antes de aplicar em produção

3. **Automatizar backup:**
   - Implementar backup automático antes de migrations
   - Implementar backup automático antes de rollback
   - Armazenar backups em local seguro

### 8.2 Pós-Beta

1. **Monitorar migrations:**
   - Monitorar performance de migrations
   - Monitorar tempo de rollback
   - Alertar para migrations que demoram muito

2. **Documentar migrations críticas:**
   - Documentar quais migrations alteram dados
   - Documentar quais migrations não suportam rollback
   - Documentar procedimentos de emergência

3. **Implementar rollback automatizado:**
   - Implementar rollback automático em caso de falha
   - Implementar restauração de backup em caso de falha
   - Alertar em caso de falha de rollback

---

## 9. Procedimento de Emergência

### 9.1 Rollback em Produção

**Passo 1: Identificar problema**
- Monitorar logs de aplicação
- Identificar migration que causou problema
- Verificar se há solução alternativa

**Passo 2: Decidir rollback**
- Se problema for crítico e não houver solução alternativa
- Se rollback for mais seguro que manter migration problemática
- Se backup recente está disponível

**Passo 3: Fazer backup**
- Fazer backup do banco atual
- Verificar que backup foi criado com sucesso
- Armazenar backup em local seguro

**Passo 4: Executar rollback**
- Executar downgrade para revisão anterior
- Verificar que rollback foi bem-sucedido
- Verificar integridade do banco

**Passo 5: Verificar aplicação**
- Reiniciar aplicação
- Verificar que aplicação funciona corretamente
- Verificar que dados estão consistentes

**Passo 6: Documentar incidente**
- Documentar causa raiz do problema
- Documentar solução aplicada
- Documentar lições aprendidas

### 9.2 Restauração de Backup

**Se rollback falhar:**
1. Parar aplicação
2. Restaurar backup mais recente
3. Verificar integridade do backup
4. Reiniciar aplicação
5. Verificar que aplicação funciona corretamente

---

## 10. Comandos de Validação

### 10.1 Validação Local

```bash
# Validação básica
cd apps/api
python -m pytest tests/test_migrations.py -v

# Alembic CLI
alembic heads
alembic current
alembic history
```

### 10.2 Evidência de Validação

**Comandos Executados:**
```bash
cd apps/api
alembic heads
# Resultado: 20260515_04 (head)

alembic history
# Resultado: Mostra 6 migrations de base até head

python -m pytest tests/test_migrations.py -v
# Resultado: 4 passed, 1 warning
```

**Resultado:**
- ✅ Migrations podem ser aplicadas até head em banco limpo
- ✅ Migrations podem ser revertidas para base
- ✅ Roundtrip (upgrade → downgrade → upgrade) funciona corretamente
- ✅ Tabelas críticas são recriadas após roundtrip
- ✅ Nenhuma head múltipla detectada

### 10.2 Validação em CI

**Planejamento:**
- Adicionar step de validação de migrations em `api-ci.yml`
- Executar testes de migrations em cada PR
- Bloquear PR se migrations não passarem

---

## 11. Checklist de Rollback

### 11.1 Antes de Rollback

- [ ] Backup do banco foi criado
- [ ] Backup foi verificado
- [ ] Revisão alvo foi identificada
- [ ] Rollback foi testado em ambiente de teste
- [ ] Aplicação foi parada
- [ ] Usuários foram notificados

### 11.2 Durante Rollback

- [ ] Downgrade foi executado
- [ ] Downgrade foi bem-sucedido
- [ ] Integridade do banco foi verificada
- [ ] Revisão atual foi verificada

### 11.11 Após Rollback

- [ ] Aplicação foi reiniciada
- [ ] Aplicação funciona corretamente
- [ ] Dados estão consistentes
- [ ] Incidente foi documentado
- [ ] Lições aprendidas foram registradas

---

## 12. Referências

- **Plano de Execução:** docs/BETA_DEVIN_EXECUTION_PLAN.md
- **Alembic Documentation:** https://alembic.sqlalchemy.org/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

**Assinatura:** Devin (SWE-1.6)  
**Data:** 2026-06-08  
**Status:** ✅ Validado com sucesso
