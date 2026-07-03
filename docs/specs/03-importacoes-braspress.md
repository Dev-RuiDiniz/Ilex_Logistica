# SPEC-03 — Importações CSV/XLSX e Braspress

**Estado:** Confirmado; layouts externos sujeitos a validação
**Rastreabilidade:** LOG-037, LOG-041

## Objetivo e contexto

Receber dados operacionais por arquivo de forma assistida, validável, idempotente e auditável. Atores: equipe de logística e administrador.

## Estado atual e evidências

O módulo imports implementa upload/preview/confirm, histórico, deliveries, promoção, validação por linha, duplicidades e mapper Braspress; existem fixtures e testes CSV/XLSX/Braspress. A importação de pedidos ERP ainda é planejada.

## Entradas, saídas e fluxo

1. Usuário seleciona CSV/XLSX.
2. Sistema identifica/mapeia colunas sem executar persistência no preview.
3. Cada linha recebe estado válido ou erros acionáveis.
4. Confirmação persiste somente o conjunto aprovado e registra histórico/contadores.
5. Delivery válida pode ser promovida a shipment explicitamente.

Saídas: resumo, linhas válidas, erros por linha, duplicidades e identificador do histórico.

## Regras, dados e permissões

- Validar extensão, estrutura, colunas obrigatórias, tipos, datas e valores.
- Normalizar cabeçalhos conhecidos sem aceitar ambiguidade silenciosa.
- Detectar duplicidade dentro do arquivo e contra a base pela chave vigente.
- Preview não persiste domínio; confirmação deve ser transacional e idempotente.
- Arquivos e erros não podem expor credenciais ou fórmulas executáveis.
- Braspress começa por exportação manual do portal; não automatizar captcha/login.

## Falhas esperadas

Arquivo corrompido, layout desconhecido, coluna ausente, encoding inválido, linha duplicada e falha de persistência retornam mensagem operacional; rollback evita confirmação parcial não declarada.

## Critérios de aceite

- CSV e XLSX válidos produzem preview e confirmação coerentes.
- Erros apontam linha/campo sem persistir linhas inválidas.
- Reenvio não cria duplicatas.
- Fluxo Braspress funciona sem credenciais no repositório.
- Futuro arquivo ERP só será aceito após contrato da SPEC-12.

## Cenários TDD

Fixtures para arquivo válido, coluna ausente, tipos inválidos, duplicidade interna/externa, Braspress e rollback. Web cobre seleção, preview, confirmação e erros.

## Riscos, dependências e rastreabilidade

O layout assistido homologável usa os cabeçalhos versionados em `BRASPRESS_IMPORTACAO_ASSISTIDA.md`; mudanças externas exigem nova versão do mapper. A fixture XLSX sanitizada e os testes API/E2E comprovam upload, preview e confirmação. Retenção do arquivo original permanece dependente da política de privacidade do cliente.
