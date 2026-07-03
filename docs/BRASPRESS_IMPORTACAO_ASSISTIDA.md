# Importação Assistida Braspress — Beta

## Objetivo

Orientar a importação segura de relatório exportado manualmente do portal Braspress. Este documento usa somente dados de exemplo e não contém dados reais.

## Escopo Beta

O beta cobre CSV/XLSX, preview, validação, duplicidades e confirmação. API real, automação de portal e integração automática estão fora do escopo beta.

## Colunas Obrigatórias

`tracking_code`, `invoice_number`, `customer_name`, `destination_uf`, `collection_departure_date`, `invoice_value` e `freight_value`.

## Colunas Opcionais

Status, previsão de entrega e demais campos reconhecidos pelo mapper podem ser informados quando disponíveis.

## Exemplo de Cabeçalho CSV

```csv
tracking_code,invoice_number,customer_name,destination_uf,collection_departure_date,invoice_value,freight_value
BP000000001,NF-EXEMPLO-001,Empresa Exemplo,SP,01/07/2026,"1.234,56","123,45"
```

## Regras de Data

Datas brasileiras usam `DD/MM/YYYY`; valores inválidos são rejeitados por linha.

## Regras de Valores Monetários

O formato brasileiro `1.234,56` é normalizado para decimal. Valores vazios não são inventados.

## Regras de Duplicidade

O preview detecta duplicidades no arquivo e a confirmação verifica registros existentes antes de persistir.

## Como Usar no Sistema

Exporte o relatório, selecione a origem Braspress, envie o arquivo, revise o preview e confirme somente quando não houver erros bloqueantes.

## Comportamento do Preview

O preview não persiste entregas. Ele apresenta linhas válidas, erros, contagens e duplicidades.

## Comportamento da Confirmação

A confirmação é transacional e registra histórico, origem e contadores da importação.

## Erros Comuns

Coluna ausente, data inválida, valor monetário inválido, rastreio vazio e registro duplicado.

## Limitações

O layout v1 está validado por amostras sanitizadas CSV/XLSX versionadas no repositório. A homologação final deve ser validada com amostra real sanitizada fornecida pelo cliente. Mudanças no relatório exigem nova versão e revisão do mapper.

## Segurança e LGPD

Não registrar credenciais, dados pessoais desnecessários ou conteúdo real em fixtures e documentação. Arquivos devem seguir a política de retenção aprovada.

## Comandos de Teste

```powershell
cd apps/api
python -m pytest -q tests/test_braspress_assisted_import.py tests/test_braspress_documented_flow.py
```

Fixtures fictícias ficam em `tests/fixtures/imports`; os cenários principais estão em `test_braspress_assisted_import.py` e `test_braspress_documented_flow.py`.
