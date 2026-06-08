# Importação Assistida Braspress - BETA-012C

## Objetivo

Este documento define o layout beta para importação assistida de arquivos Braspress. O layout é baseado nos campos necessários do sistema e deve ser validado com amostra real sanitizada antes do piloto.

**IMPORTANTE:** Este layout NÃO contém dados reais. Todos os exemplos usam dados fictícios para fins de desenvolvimento e teste.

## Escopo Beta

O que está incluído:
- Layout assistido para importação manual de arquivos Braspress
- Mapeamento de colunas Braspress para campos internos do sistema
- Validação de dados obrigatórios
- Detecção de duplicidades
- Preview antes da confirmação
- Persistência de shipments com campos fiscais/financeiros

O que NÃO está incluído (fora do escopo beta):
- Integração automática com API Braspress
- Scraping/bot para coleta automática
- SLA por transportadora
- Eficiência por transportadora
- Alertas ou relatório diário
- Automação completa

## O que é "Assistido"

A importação assistida significa que:
- O usuário faz upload manual de um arquivo (CSV ou XLSX)
- O arquivo segue um layout pré-definido
- O sistema valida os dados antes de persistir
- O usuário pode revisar o preview antes de confirmar
- A confirmação é manual (não automática)

Não é automático porque:
- Não há integração direta com sistemas Braspress
- Não há coleta automática de dados
- O usuário mantém controle sobre o que é importado

## Formatos Aceitos

- **CSV**: Delimitado por vírgula ou ponto-e-vírgula, codificação UTF-8 ou UTF-8-BOM
- **XLSX**: Planilha Excel (apenas primeira aba)

## Colunas Obrigatórias

| Coluna (Layout Braspress) | Campo Interno | Descrição | Exemplo |
|---------------------------|---------------|-----------|---------|
| Número da entrega ou rastreio | `tracking_code` | Código de rastreio da entrega | BP123456789BR |
| Número da NF | `invoice_number` | Número da nota fiscal | NF001234567 |
| Cliente | `customer_name` | Nome do cliente/destinatário | Empresa Exemplo Ltda |
| UF destino | `destination_uf` | UF de destino (2 letras) | SP |
| Data coleta/saída | `collection_departure_date` | Data de coleta (DD/MM/YYYY) | 15/01/2025 |
| Valor NF | `invoice_value` | Valor da nota fiscal (R$) | 1.234,56 |
| Valor frete | `freight_value` | Valor do frete (R$) | 123,45 |
| Transportadora | `carrier_id` ou `carrier_name` | ID ou nome da transportadora | 1 ou Braspress |

## Colunas Opcionais

| Coluna (Layout Braspress) | Campo Interno | Descrição | Exemplo |
|---------------------------|---------------|-----------|---------|
| Previsão de entrega | `expected_delivery_date` | Data prevista de entrega | 20/01/2025 |
| Status | `status` | Status do envio (se suportado) | Em trânsito |

## Exemplo de Cabeçalho CSV (Fake)

```csv
Número da entrega ou rastreio,Número da NF,Cliente,UF destino,Data coleta/saída,Valor NF,Valor frete,Transportadora
BP123456789BR,NF001234567,Empresa Exemplo Ltda,SP,15/01/2025,1.234,56,123,45,Braspress
BP987654321BR,NF009876543,Outra Empresa SA,RJ,16/01/2025,2.345,67,234,56,Braspress
```

**NOTA:** Este é um exemplo FICTÍCIO. Não use dados reais de clientes.

## Variações de Cabeçalho Aceitas

O sistema aceita variações de nomes de colunas. O mapper normaliza automaticamente:

### Para tracking_code:
- Número da entrega ou rastreio
- tracking_code
- rastreio
- codigo_rastreio
- tracking

### Para invoice_number:
- Número da NF
- invoice_number
- nf
- nota_fiscal
- numero_nf

### Para customer_name:
- Cliente
- customer_name
- cliente
- nome_cliente
- destinatario

### Para destination_uf:
- UF destino
- destination_uf
- uf
- uf_destino
- estado_destino

### Para collection_departure_date:
- Data coleta/saída
- collection_departure_date
- data_coleta
- dt_coleta

### Para invoice_value:
- Valor NF
- invoice_value
- valor_nf
- valor_nota_fiscal
- valor_mercadoria

### Para freight_value:
- Valor frete
- freight_value
- valor_frete
- frete
- vlr_frete

### Para carrier_id/carrier_name:
- Transportadora
- carrier_id
- carrier_name
- transportadora
- id_transportadora

## Regras de Data

- **Formato aceito:** DD/MM/YYYY ou DD-MM-YYYY
- **Exemplos válidos:** 15/01/2025, 15-01-2025, 01/02/2025
- **Exemplos inválidos:** 2025-01-15 (ISO não é padrão Braspress), 15/01/25 (ano 2 dígitos pode falhar)
- **Ano 2 dígitos:** Aceito, mas assume 20xx para anos >= 00

## Regras de Valores Monetários

- **Formato aceito:** Brasileiro com separador de milhar e decimal
- **Exemplos válidos:** 1.234,56, 1234,56, R$ 1.234,56, R$1234,56
- **Exemplos inválidos:** 1234.56 (formato americano), 1,234.56
- **Símbolo R$:** Opcional, é removido automaticamente
- **Separador decimal:** Deve ser vírgula (,)
- **Separador de milhar:** Deve ser ponto (.)

## Regras de Duplicidade

### Duplicidade no Arquivo
- O sistema detecta linhas duplicadas dentro do mesmo arquivo
- Critério: `tracking_code` duplicado
- Linhas duplicadas são marcadas como erro

### Duplicidade no Banco
- O sistema verifica se `tracking_code` já existe no banco
- Se existir, a linha é rejeitada na confirmação
- O preview mostra avisos de duplicidade

## Como Usar no Sistema

### 1. Preparar o Arquivo
- Exporte dados do sistema Braspress para CSV ou XLSX
- Certifique-se de que as colunas obrigatórias estão presentes
- Use nomes de colunas conforme o layout ou variações aceitas
- **NÃO inclua dados reais sensíveis em arquivos de teste**

### 2. Fazer Upload
- Acesse a tela de importação
- Selecione o layout "Braspress assistido" (se disponível)
- Faça upload do arquivo

### 3. Revisar Preview
- O sistema valida todas as linhas
- Revise erros e avisos
- Verifique se os dados estão corretos
- Confirme a importação apenas se estiver tudo correto

### 4. Confirmar Importação
- Clique em confirmar
- O sistema persiste os shipments válidos
- Linhas com erros não são importadas
- O histórico de importação é registrado

## Comportamento do Preview

- **Não persiste shipments** - Apenas valida
- **Cria ImportHistory com status "pending"**
- **Registra origem como "braspress_assisted"**
- **Retorna:**
  - Total de linhas
  - Linhas válidas
  - Linhas inválidas
  - Duplicidades detectadas
  - Erros por linha
  - Avisos por linha
  - Preview das primeiras 10 linhas

## Comportamento da Confirmação

- **Persiste apenas linhas válidas**
- **Rejeita linhas com erros bloqueantes**
- **Verifica duplicidade no banco antes de persistir**
- **Atualiza ImportHistory:**
  - Status: "completed" (sucesso) ou "failed" (erro)
  - imported_count: número de shipments criados
  - rejected_count: número de linhas rejeitadas
  - metadata: IDs dos shipments criados
- **Registra origem "braspress_assisted" no histórico**

## Erros Comuns

### Coluna Obrigatória Ausente
- **Erro:** "tracking_code obrigatorio"
- **Causa:** Coluna não encontrada ou nome não reconhecido
- **Solução:** Verifique se a coluna existe e usa nome aceito

### Data Inválida
- **Erro:** "collection_departure_date invalido"
- **Causa:** Data não está no formato DD/MM/YYYY
- **Solução:** Use formato brasileiro com 4 dígitos no ano

### Valor Monetário Inválido
- **Erro:** "invoice_value invalido (use formato brasileiro: 1.234,56)"
- **Causa:** Valor não está no formato brasileiro
- **Solução:** Use vírgula como separador decimal

### Duplicidade
- **Erro:** "tracking_code duplicado no arquivo"
- **Causa:** Mesmo tracking_code aparece mais de uma vez
- **Solução:** Remova linhas duplicadas

### Carrier ID Inválido
- **Erro:** "carrier_id deve ser um numero inteiro"
- **Causa:** carrier_id não é um número
- **Solução:** Use ID numérico ou nome da transportadora

## Limitações

- **Sem integração automática:** Upload manual apenas
- **Sem autodetecção de layout:** Usuário deve selecionar layout (se implementado)
- **Sem validação de carrier:** Carrier ID não é validado contra tabela de carriers
- **Sem validação de UF:** UF não é validada contra lista de UFs brasileiras
- **Sem transformação complexa:** Apenas mapeamento direto de colunas
- **Sem suporte a múltiplas abas XLSX:** Apenas primeira aba é processada

## Segurança e LGPD

- **NÃO use dados reais de clientes em arquivos de teste**
- **NÃO compartilhe arquivos com dados sensíveis**
- **Sanitize dados antes de usar em desenvolvimento**
- **Remova informações pessoais (CPF, CNPJ, endereço completo)**
- **Use nomes fictícios e valores fake**
- **Este layout é para fins de desenvolvimento e teste beta**

## Observações Importantes

- **API real Braspress:** Fora do escopo beta
- **Scraping/bot:** Fora do escopo beta
- **Automação completa:** Fora do escopo beta
- **SLA por transportadora:** Fora do escopo beta
- **Eficiência por transportadora:** Fora do escopo beta
- **Alertas ou relatório diário:** Fora do escopo beta

## Comandos de Teste

```bash
# Executar testes de importação Braspress
cd apps/api
pytest tests/test_braspress_assisted_import.py -v

# Executar testes de validação de documentação
pytest tests/test_braspress_documented_flow.py -v

# Executar todos os testes de importação
pytest tests/test_braspress_assisted_import.py tests/test_braspress_documented_flow.py -v
```

## Fixtures de Teste

Os fixtures de teste estão localizados em `apps/api/tests/fixtures/imports/`:
- `braspress_valid.csv` - Arquivo CSV válido com dados fictícios
- `braspress_invalid_missing_required.csv` - Arquivo CSV com coluna obrigatória faltando
- `braspress_duplicates.csv` - Arquivo CSV com linhas duplicadas

Todos os fixtures usam dados fake e não contêm informações reais de clientes.

## Próximos Passos

Após validação com amostra real sanitizada:
1. Ajustar layout conforme necessário
2. Adicionar validações específicas Braspress
3. Implementar integração automática (fase pós-beta)
4. Adicionar SLA e eficiência por transportadora (fase pós-beta)

## Referências

- BETA-012A: Import CSV/XLSX Backend
- BETA-012B: Import Upload Preview Confirm Frontend
- BETA-012C: Importação Assistida Braspress (este documento)
