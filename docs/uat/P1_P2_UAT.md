# UAT técnico — P1 e P2

**Data:** 2026-07-03  
**Estado:** evidência técnica aprovada; aceite humano e E2E com backend preparado pendentes

## Regras aprovadas

- Timezone `America/Sao_Paulo`, dias corridos e sem desconto de feriados.
- No prazo até o fim da data prevista; atraso após a data prevista.
- Extravio somente por status explícito `lost`.
- Ranking por maior percentual no prazo; desempate por menor extravio, menor percentual médio de frete e nome.
- Média financeira somente com NF positiva e frete informado.

## Evidências controladas

- `test_p1_metrics_reconciliation.py`: listagem, dashboard e eficiência reconciliam o mesmo universo filtrado.
- `test_carrier_efficiency_report.py`: extravio, frete total, população financeira e ranking determinístico.
- `test_exceptions_panel_sla.py`: não contém testes vazios e cobre classificação, prioridade, filtros e payload.
- Fixtures Braspress CSV e XLSX sanitizadas; 69 testes de importação/Braspress aprovados na execução focada.
- Suites RBAC por domínio cobrem sucesso, ausência de credencial (`401`) e permissão insuficiente (`403`).
- `test_auth_policies.py`: senha, expiração e rotação/revogação por versão.
- `test_operational_policies.py`: timezone, retry, canais, agenda e retenção.

## E2E

As specs de XLSX e tratativas são coletadas pelo Playwright e a autenticação fictícia usa o contrato atual de sessão. A execução contra a Web local alcançou as páginas privadas, mas não concluiu porque o Playwright inicia apenas o Next.js e não provisiona API/seed em `localhost:8000`. Portanto, E2E operacional e aceite humano não são declarados como aprovados.

## Aceite humano pendente

- validar amostra real sanitizada Braspress;
- validar transportadoras, alertas, relatórios e auditoria com representantes dos perfis;
- executar Playwright em ambiente integrado com API, banco migrado e seed E2E descartável.
