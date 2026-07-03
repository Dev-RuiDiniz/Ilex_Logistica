# UAT técnico — P1 e P2

**Data:** 2026-07-03  
**Estado:** evidência técnica e fluxos críticos Chromium aprovados; aceite humano pendente

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

As specs usam sessão fictícia e respostas HTTP controladas somente nos limites externos. No Chromium passaram 1 cenário XLSX e 7 cenários de tratativas, cobrindo upload, preview, confirmação, detalhe, formulário, criação, atualização do histórico, validação e bloqueio por perfil. A matriz completa Chromium/Firefox/WebKit/Mobile excedeu a janela de cinco minutos e permanece para P4 cross-browser.

## Aceite humano pendente

- validar amostra real sanitizada Braspress;
- validar transportadoras, alertas, relatórios e auditoria com representantes dos perfis;
- executar UAT em ambiente integrado com API, banco migrado e seed descartável;
- concluir a matriz cross-browser de P4.
