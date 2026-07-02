# SPEC-02 — Transportadoras

**Estado:** Confirmado

## Objetivo e contexto

Manter o cadastro de transportadoras usado por entregas, imports, SLA, eficiência e futuras cotações. Atores: administrador para escrita; perfis operacionais/gerenciais conforme permissão para leitura.

## Estado atual e evidências

API possui model, schemas e rotas de criar, listar, editar e inativar; o Web possui página e testes de transportadoras.

## Entradas, saídas e fluxo

Cadastro recebe identificação e atributos suportados pelo schema vigente. Listagem retorna registros autorizados. Edição altera somente campos permitidos. Inativação preserva referências históricas.

## Regras, dados e permissões

- Identificadores exigidos devem ser únicos conforme constraints existentes.
- Transportadora inativa não deve ser oferecida em novos vínculos ou cotações.
- Entregas históricas continuam exibindo a transportadora inativada.
- CRUD exige permissões específicas; leitura analítica não concede escrita.

## Falhas esperadas

Duplicidade, registro inexistente, payload inválido e tentativa sem permissão não podem gerar alteração parcial.

## Critérios de aceite

- Criar, listar, editar e inativar funcionam com respostas coerentes.
- Inativação não apaga histórico.
- Páginas tratam carregamento, vazio, erro, `401` e `403`.

## Cenários TDD

1. RED/GREEN para CRUD, duplicidade e inativação idempotente.
2. Testes RBAC de leitura e escrita.
3. Teste Web de formulário, listagem e erro da API.

## Riscos, dependências e rastreabilidade

Campos de contrato, CNPJ e credenciais de integração não podem ser inferidos. Dependências: imports, shipments e SPEC-07/SPEC-12. Evidência: `modules/carriers` e página `carriers`.
