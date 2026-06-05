# LOG-007 — Revisão do Importador CSV/Excel

## Data/Hora
2026-06-03

## Branch Utilizada
- **Branch**: `feature/revisa-importador-entregas`
- **Base**: `main` (hash: `d5ac1f775ab018548af85189b1e09fb379f01c57`)
- **Independente** de LOG-A02, LOG-A03, LOG-A04, LOG-A05

---

## Contexto

Revisar e estabilizar o fluxo de importação CSV/Excel validando upload, leitura, parsing e respostas para arquivos válidos e inválidos. Identificar lacunas de cobertura e fechar com testes Red→Green.

---

## Arquitetura do Importador

### Arquivos do Módulo

| Arquivo | Responsabilidade |
|---------|-----------------|
| `app/modules/imports/router.py` | Endpoints `/imports/upload` e `/imports/history` |
| `app/modules/imports/service.py` | Parsing CSV/XLSX, validações, persistência |
| `app/modules/imports/schemas.py` | `ImportPreviewResponse`, `ImportHistoryResponse` |
| `app/modules/imports/models.py` | `ImportHistory`, `Delivery` (SQLAlchemy ORM) |
| `tests/test_imports.py` | Testes de integração via TestClient |

### Fluxo do Upload

```
POST /api/v1/imports/upload
        │
        ▼
parse_uploaded_file(file)
        │
        ├─ Verificar extensão (.csv | .xlsx)
        ├─ Verificar bytes não vazios
        ├─ _parse_csv() ou _parse_xlsx()
        │       ├─ Normalizar cabeçalho (acentos, espaços → snake_case)
        │       └─ _validate_required_columns()
        ├─ _validate_duplicate_nf()
        └─ _validate_financial_fields()
                ├─ valor_frete >= 0
                ├─ percentual_frete [0, 100]
                └─ data_coleta formato AAAA-MM-DD
        │
        ▼
persist_deliveries(db, rows)
persist_import_history(db, ...)
        │
        ▼
ImportPreviewResponse(filename, rows_received, columns_detected, preview[:5])
```

### Extensões Suportadas
```python
SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}
```

### Colunas Obrigatórias
```python
REQUIRED_COLUMNS = {"nf", "transportadora", "data_coleta", "valor_frete", "percentual_frete"}
```

### Parsing XLSX
Implementado manualmente via `ZipFile` + `ElementTree` — sem dependência de `openpyxl` ou `xlrd`. Lê `xl/worksheets/sheet1.xml` diretamente.

### Encoding CSV
`utf-8-sig` (suporte a BOM). Latin-1 com caracteres acima de ASCII (>127) é rejeitado como erro de decodificação.

---

## Baseline Antes de Alterar

| Comando | Resultado |
|---------|-----------|
| `pytest --tb=short -q` | ✅ **71/71** passando |
| `ruff check .` | ✅ All checks passed |
| `pytest tests -k import -v` | ✅ **27/27** passando |

### Testes de importação existentes (baseline)

| Teste | Cenário |
|-------|---------|
| `test_upload_csv_retorna_resumo` | CSV válido → 200 com resumo |
| `test_upload_sem_arquivo_retorna_422` | Sem arquivo → 422 |
| `test_upload_extensao_invalida_retorna_400` | `.txt` → 400 |
| `test_upload_arquivo_vazio_retorna_400` | Bytes vazios → 400 |
| `test_upload_xlsx_retorna_resumo` | XLSX válido → 200 |
| `test_upload_csv_normaliza_cabecalho_com_acento_e_espacos` | Acentos/espaços → normalizado |
| `test_upload_rejeita_sem_nf` | Sem coluna `nf` → 400 |
| `test_upload_rejeita_sem_transportadora` | Sem coluna `transportadora` → 400 |
| `test_upload_rejeita_csv_com_nf_duplicado` | NF duplicado CSV → 400 |
| `test_upload_rejeita_xlsx_com_nf_duplicado` | NF duplicado XLSX → 400 |
| `test_upload_valido_persiste_historico_success` | Histórico persistido |
| `test_upload_xlsx_persiste_historico_com_file_type_xlsx` | `file_type == "xlsx"` |
| `test_file_hash_consistente_para_mesmo_conteudo` | SHA-256 determinístico |
| `test_history_retorna_ordenado_desc_por_criacao` | Histórico ordenado DESC |
| `test_upload_persiste_entrega_campos_fiscais_financeiros` | Campos numéricos corretos |
| `test_upload_rejeita_valor_frete_negativo` | Frete < 0 → 400 |
| `test_upload_rejeita_percentual_fora_da_faixa` | Percentual > 100 → 400 |

---

## Análise de Lacunas (Pré-Red)

Após inspeção do código e dos testes existentes, identificadas as seguintes lacunas:

| # | Lacuna | Impacto | Existia? |
|---|--------|---------|----------|
| 1 | CSV com apenas cabeçalho (0 linhas de dados) retorna 200 | Alto — importa zero entregas silenciosamente | ❌ Não testado |
| 2 | CSV Latin-1 com acento real (byte > 127) — comportamento sob falha de decode | Médio — erro de encoding não coberto | ❌ Não testado |
| 3 | `data_coleta` em formato não-ISO (DD/MM/AAAA) | Médio — dado incorreto rejeitado | ✅ Comportamento OK |
| 4 | Resposta de erro não expõe stack trace | Alto — segurança | ✅ Comportamento OK |
| 5 | XLSX sem `sheet1.xml` | Médio — ZIP válido mas sem worksheet | ✅ Comportamento OK |
| 6 | XLSX com bytes corrompidos (não-ZIP) | Médio — arquivo inválido | ✅ Comportamento OK |
| 7 | `valor_frete` com valor textual não-numérico | Médio | ✅ Comportamento OK |
| 8 | `data_coleta` ausente (campo vazio) | Alto | ✅ Comportamento OK |

**Lacunas reais confirmadas**: 2 (itens 1 e 2 acima)

---

## Testes Red Criados

Adicionados 8 novos testes na seção `# LOG-007` em `tests/test_imports.py`:

### Red Inicial

| Teste | Esperado | Obtido | Status Red |
|-------|----------|--------|------------|
| `test_upload_csv_data_coleta_formato_invalido_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_somente_cabecalho_sem_dados_retorna_400` | 400 | **200** | ❌ **FAIL** |
| `test_upload_csv_encoding_latin1_retorna_400` | 400 | **200** (ASCII puro) | ❌ **FAIL** → corrigido para usar acento real |
| `test_upload_resposta_nao_expoe_stack_trace` | 400 sem traceback | 400 sem traceback | ✅ Green direto |
| `test_upload_xlsx_sem_worksheet_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_xlsx_corrompido_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_valor_frete_nao_numerico_retorna_400` | 400 | 400 | ✅ Green direto |
| `test_upload_csv_data_coleta_ausente_retorna_400` | 400 | 400 | ✅ Green direto |

**Falhas Red confirmadas**: 2
1. `test_upload_csv_somente_cabecalho_sem_dados_retorna_400` — recebia 200
2. `test_upload_csv_encoding_latin1_retorna_400` — teste usava ASCII puro; corrigido para usar `"São Paulo"` com acento real (byte 0xe3)

---

## Implementação Green

### Arquivo: `app/modules/imports/service.py`

**Bug 1 corrigido**: CSV com apenas cabeçalho e zero linhas de dados retornava 200.

```python
# Antes — sem validação de linhas vazias:
rows = [
    {_normalize_header(k): (v or "").strip() for k, v in row.items() if k and k.strip()}
    for row in reader
]
return columns, rows

# Depois — LOG-007: rejeitar CSV com cabecalho mas sem linhas de dados:
rows = [
    {_normalize_header(k): (v or "").strip() for k, v in row.items() if k and k.strip()}
    for row in reader
]
# LOG-007: rejeitar CSV com cabecalho mas sem linhas de dados
if not rows:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv sem dados: nenhuma linha encontrada")
return columns, rows
```

**Por que Latin-1 passou após correção do teste**: O teste original usava "Sao Paulo" (ASCII puro, subconjunto de UTF-8), que decodificava sem erro. Corrigido para `"São Paulo"` em Latin-1 (byte `0xe3` para `ã`) que causa `UnicodeDecodeError` na decodificação UTF-8-SIG. O tratamento já existia no service:
```python
except UnicodeDecodeError as exc:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv invalido") from exc
```

---

## Arquivos Alterados

| Arquivo | Tipo | Alterações |
|---------|------|------------|
| `app/modules/imports/service.py` | **Modificado** | +3 linhas (validação de CSV vazio) |
| `tests/test_imports.py` | **Modificado** | +91 linhas (8 novos testes LOG-007) |
| `docs/qa/log-007-importador-csv-excel.md` | **Criado** | Este arquivo |

**Escopo respeitado**: Nenhum arquivo fora de `apps/api/`, `tests/` e `docs/qa/` foi alterado.

---

## Comandos Executados

```bash
# Passo 1 — Baseline
cd apps/api
pytest --tb=short -q                        # 71/71 ✅
ruff check .                                # All checks passed ✅
pytest tests -k import -v                   # 27/27 ✅

# Passo 2 — Red
pytest tests -k "somente_cabecalho or encoding_latin1 ..." -v
# 2 FAILED (somente_cabecalho, encoding_latin1)

# Passo 3 — Green
# Correção em service.py + correção do teste Latin-1

# Passo 4 — Validação
pytest tests -k import -v                   # 35/35 ✅  (+8 novos)
pytest --tb=short -q                        # 79/79 ✅
ruff check .                                # All checks passed ✅
```

---

## Evidência de pytest (Green Final)

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
collected 79 items

tests/test_imports.py::test_upload_csv_data_coleta_formato_invalido_retorna_400   PASSED
tests/test_imports.py::test_upload_csv_somente_cabecalho_sem_dados_retorna_400    PASSED
tests/test_imports.py::test_upload_csv_encoding_latin1_retorna_400                PASSED
tests/test_imports.py::test_upload_resposta_nao_expoe_stack_trace                 PASSED
tests/test_imports.py::test_upload_xlsx_sem_worksheet_retorna_400                 PASSED
tests/test_imports.py::test_upload_xlsx_corrompido_retorna_400                    PASSED
tests/test_imports.py::test_upload_csv_valor_frete_nao_numerico_retorna_400       PASSED
tests/test_imports.py::test_upload_csv_data_coleta_ausente_retorna_400            PASSED

79 passed, 1 warning in 21.08s
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
| Após LOG-007 | **35** (+8) | **79** (+8) |

---

## Riscos e Pendências

| Risco/Pendência | Status | Nota |
|-----------------|--------|------|
| XLSX com múltiplas sheets | ⚠️ Pendente | Apenas `sheet1.xml` lido — comportamento documentado |
| XLSX com shared strings (`sharedStrings.xml`) | ⚠️ Pendente | Células numéricas com tipo `s` não resolvidas para texto — LOG-008 |
| Limite de tamanho de arquivo | ⚠️ Ausente | Sem validação de `Content-Length` ou `file.size` |
| MIME type não validado | ℹ️ Aceito | Validação por extensão é suficiente para escopo atual |
| Encoding UTF-16 | ⚠️ Não testado | Retorna 400 via UnicodeDecodeError, comportamento aceitável |
| Colunas extras além das obrigatórias | ✅ Aceitas | Normalização silenciosa — comportamento correto |
| Linha completamente vazia no CSV | ✅ Ignorada | DictReader ignora linhas vazias |
| Reprocessamento do mesmo arquivo | ✅ Permitido | Hash registrado mas sem bloqueio de duplicata de arquivo |

---

## Limite de Escopo — Separação LOG-007 / LOG-008 / LOG-010

| Escopo | Task |
|--------|------|
| Upload, parsing, validação básica de CSV/XLSX | ✅ **LOG-007** (esta task) |
| Validação avançada de colunas obrigatórias e tipos | ➡️ **LOG-008** |
| Persistência completa de entregas e histórico | ➡️ **LOG-010** |
| XLSX com shared strings (células de texto estilo Excel real) | ➡️ **LOG-008** |
| Limite de tamanho de arquivo | ➡️ **LOG-008** ou configuração de infra |

---

## Conclusão

✅ **LOG-007 CONCLUÍDO**

O importador CSV/Excel foi revisado. Dois bugs foram identificados via TDD Red→Green:
1. CSV com cabeçalho mas sem dados retornava 200 — **corrigido**
2. Teste Latin-1 usava ASCII puro (não testava o path de erro real) — **corrigido**

Todos os cenários críticos de parsing, validação e resposta segura estão cobertos. A suíte passou de 71 para 79 testes, todos passando com ruff limpo.

---

*Gerado em: 2026-06-03*
*Task: LOG-007 — REVISÃO DO IMPORTADOR CSV/EXCEL ✅*
*Hash Base: d5ac1f775ab018548af85189b1e09fb379f01c57*
*Governança: Merge exclusivo do supervisor humano | PR apenas com orientação explícita*
