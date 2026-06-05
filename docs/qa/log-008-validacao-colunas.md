# LOG-008 — Validação de Colunas Obrigatórias

## Data/Hora
2026-06-03

## Branch Utilizada
- **Branch**: `feature/validacao-colunas-importacao`
- **Branch base**: `feature/revisa-importador-entregas` (LOG-007)
- **Commit base**: `bd0b22f` — `feat(imports): estabiliza importador csv e excel`
- **Dependência**: LOG-008 depende tecnicamente de LOG-007 — branch empilhada
- **Independente de main** — não houve merge da branch LOG-007 na main

---

## Contexto

Fortalecer a validação das colunas obrigatórias do importador antes do processamento, garantindo mensagens claras, seguras e específicas para colunas ausentes, tipos inválidos, formatos incorretos e inconsistências previsíveis.

---

## Arquitetura de Validação Encontrada

### Colunas Obrigatórias (Confirmado no Código)
```python
REQUIRED_COLUMNS = {"nf", "transportadora", "data_coleta", "valor_frete", "percentual_frete"}
```

### Fluxo de Validação Atual (Antes do LOG-008)

```
parse_uploaded_file()
  ├─ Verificar extensão (.csv | .xlsx)
  ├─ Verificar bytes não vazios
  ├─ _parse_csv() ou _parse_xlsx()
  │       ├─ Normalizar cabeçalho
  │       └─ _validate_required_columns()  # colunas presentes no cabeçalho
  ├─ _validate_duplicate_nf()
  └─ _validate_financial_fields()
          ├─ valor_frete >= 0
          ├─ percentual_frete [0, 100]
          └─ data_coleta formato AAAA-MM-DD
```

### Lacunas Identificadas

| # | Lacuna | Impacto | Status Pré-LOG-008 |
|---|--------|---------|-------------------|
| 1 | `nf` presente mas vazia (coluna existe, valor vazio) | Alto — persiste string vazia | ❌ Não validado |
| 2 | `transportadora` presente mas vazia | Alto — persiste string vazia | ❌ Não validado |
| 3 | `percentual_frete` negativo | Médio | ✅ Já validado (LOG-007) |
| 4 | `percentual_frete` não numérico | Médio | ✅ Já validado (LOG-007) |
| 5 | Multiplas colunas ausentes — lista completa no erro | Baixo | ✅ Já validado |
| 6 | XLSX sem coluna `nf` | Médio | ✅ Já validado |
| 7 | Erro contém nome do campo afetado | Alto — UX | ✅ Já validado |

**Lacunas reais confirmadas**: 2 (itens 1 e 2 acima)

---

## Baseline Antes de Alterar

| Comando | Resultado |
|---------|-----------|
| `pytest tests -k import -v` | ✅ **35/35** passando |
| `pytest --tb=short -q` | ✅ **79/79** passando |
| `ruff check .` | ✅ All checks passed |

**Testes de importação existentes (baseline)**: 35 (incluindo 8 do LOG-007)

---

## Testes Red Criados

Adicionados 7 novos testes na seção `# LOG-008` em `tests/test_imports.py`:

### Red Inicial

| Teste | Esperado | Obtido | Status Red |
|-------|----------|--------|------------|
| `test_upload_csv_nf_vazia_retorna_400` | 400 | **200** | ❌ **FAIL** |
| `test_upload_csv_transportadora_vazia_retorna_400` | 400 | **200** | ❌ **FAIL** |
| `test_upload_csv_percentual_frete_negativo_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_percentual_frete_nao_numerico_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_multiplas_colunas_ausentes_retorna_400_com_lista` | 400 com lista | 400 com lista | ✅ Green direto |
| `test_upload_xlsx_sem_coluna_nf_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_erro_contem_nome_do_campo_afetado` | campo no detail | campo no detail | ✅ Green direto |

**2 falhas Red confirmadas** — evidência de lacunas reais.

---

## Implementação Green

### Arquivo: `app/modules/imports/service.py`

**Adição 1** — Nova função `_validate_required_fields()`:
```python
def _validate_required_fields(rows: list[dict[str, str]]) -> None:
    # LOG-008: validar campos obrigatorios com valor nao vazio por linha
    for row in rows:
        nf = (row.get("nf") or "").strip()
        if not nf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="nf obrigatoria: campo nf nao pode ser vazio",
            )
        transportadora = (row.get("transportadora") or "").strip()
        if not transportadora:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="transportadora obrigatoria: campo transportadora nao pode ser vazio",
            )
```

**Adição 2** — Chamada em `parse_uploaded_file()`:
```python
# Antes:
_validate_duplicate_nf(rows)
_validate_financial_fields(rows)
return columns, rows, ...

# Depois:
_validate_duplicate_nf(rows)
_validate_required_fields(rows)  # LOG-008
_validate_financial_fields(rows)
return columns, rows, ...
```

---

## Arquivos Alterados

| Arquivo | Tipo | Alterações |
|---------|------|------------|
| `app/modules/imports/service.py` | Modificado | +23 linhas — função `_validate_required_fields()` + chamada |
| `tests/test_imports.py` | Modificado | +118 linhas — 7 novos testes LOG-008 |
| `docs/qa/log-008-validacao-colunas.md` | Criado | Este arquivo |

**Escopo respeitado**: Nenhum arquivo fora de `apps/api/`, `tests/` e `docs/qa/` foi alterado.

---

## Comandos Executados

```bash
# Passo 1 — Baseline
cd apps/api
pytest tests -k import -v                   # 35/35 ✅
pytest --tb=short -q                        # 79/79 ✅
ruff check .                                # All checks passed ✅

# Passo 2 — Red
pytest tests -k "log008 or nf_vazia or transportadora_vazia ..." -v
# 2 FAILED (nf_vazia, transportadora_vazia)

# Passo 3 — Green
# Adição de _validate_required_fields() + chamada em parse_uploaded_file

# Passo 4 — Validação
pytest tests -k import -v                   # 42/42 ✅  (+7 novos)
pytest --tb=short -q                        # 86/86 ✅
ruff check .                                # All checks passed ✅
```

---

## Evidência de pytest (Green Final)

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
collected 86 items

tests/test_imports.py::test_upload_csv_nf_vazia_retorna_400              PASSED
tests/test_imports.py::test_upload_csv_transportadora_vazia_retorna_400  PASSED
tests/test_imports.py::test_upload_csv_percentual_frete_negativo_retorna_400 PASSED
tests/test_imports.py::test_upload_csv_percentual_frete_nao_numerico_retorna_400 PASSED
tests/test_imports.py::test_upload_csv_multiplas_colunas_ausentes_retorna_400_com_lista PASSED
tests/test_imports.py::test_upload_xlsx_sem_coluna_nf_retorna_400        PASSED
tests/test_imports.py::test_upload_csv_erro_contem_nome_do_campo_afetado PASSED

86 passed, 1 warning in 22.22s
```

```
ruff check .
All checks passed!
```

---

## Evolução de Testes

| Ponto | Import | Total |
|-------|--------|-------|
| Baseline (main) | 27 | 71 |
| Após LOG-007 | 35 (+8) | 79 (+8) |
| Após LOG-008 | **42** (+7) | **86** (+7) |

---

## Riscos e Pendências

| Risco/Pendência | Status | Nota |
|-----------------|--------|------|
| XLSX com shared strings (`sharedStrings.xml`) | ⚠️ Pendente | Células de texto estilo Excel real — LOG-008 ou LOG-010 |
| XLSX com múltiplas sheets | ⚠️ Pendente | Apenas `sheet1.xml` lido — documentado |
| Limite de tamanho de arquivo | ⚠️ Pendente | Sem validação de `Content-Length` |
| Validação de formato de `nf` (ex: só números) | ℹ️ Aceito | String aceita — regra de negócio futura |
| Validação de formato de `transportadora` (ex: caracteres especiais) | ℹ️ Aceito | String aceita — regra de negócio futura |
| Colunas extras além das obrigatórias | ✅ Aceitas | Normalização silenciosa — comportamento correto |

---

## Limite de Escopo — Separação LOG-008 / LOG-010

| Escopo | Task |
|--------|------|
| Validação de colunas obrigatórias por linha (vazio) | ✅ **LOG-008** (esta task) |
| Validação de tipos e formatos básicos | ✅ **LOG-008** (já existia + reforçado) |
| Persistência completa de entregas e histórico | ➡️ **LOG-010** |
| XLSX com shared strings (células de texto estilo Excel real) | ➡️ **LOG-008** (pendente) ou LOG-010 |
| Limite de tamanho de arquivo | ➡️ **LOG-008** (pendente) ou configuração de infra |

---

## Conclusão

✅ **LOG-008 CONCLUÍDO**

A validação de colunas obrigatórias foi fortalecida. Duas lacunas reais foram identificadas e fechadas via TDD Red→Green:
1. `nf` presente mas vazia — **corrigido**
2. `transportadora` presente mas vazia — **corrigido**

Todos os cenários críticos de validação por campo estão cobertos. A suíte passou de 79 para 86 testes, todos passando com ruff limpo.

---

*Gerado em: 2026-06-03*
*Task: LOG-008 — VALIDAÇÃO DE COLUNAS OBRIGATÓRIAS ✅*
*Hash Base: bd0b22f (LOG-007)*
*Branch Base: feature/revisa-importador-entregas*
*Branch Atual: feature/validacao-colunas-importacao (empilhada)*
*Governança: Merge exclusivo do supervisor humano | PR apenas com orientação explícita*
