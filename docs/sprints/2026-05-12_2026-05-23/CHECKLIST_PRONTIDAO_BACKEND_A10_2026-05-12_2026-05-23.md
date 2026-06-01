# Checklist de Prontidao Backend A-10 (2026-05-12 a 2026-05-23)

## Criticos (P0)
- [x] A-01 Health endpoint e estrutura base
- [x] A-02 Sessao e fallback de conexao
- [x] A-03 Migration upgrade/downgrade
- [x] A-04 Login JWT e erro 401
- [x] A-05 RBAC com bloqueio 403
- [x] A-06 CRUD de transportadoras

## Qualidade (P1)
- [x] A-07 Erro 422 padronizado
- [x] A-08 Suite minima automatizada
- [x] A-09 Contrato tecnico publicado

## Evidencia de verificacao final
- Comando: `pytest -q`
- Resultado esperado: suite verde sem falhas
- Rastreio: Issues A-01..A-10 com card `Done`
