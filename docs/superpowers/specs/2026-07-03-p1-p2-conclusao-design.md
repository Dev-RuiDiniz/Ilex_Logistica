# Conclusão de P1 e P2 — Design

**Estado:** aprovado para implementação em 2026-07-03

## Objetivo

Concluir os indicadores e a eficiência de P1 e endurecer os fluxos operacionais de P2 com contratos únicos, testes determinísticos, evidências de UAT técnico e políticas operacionais explícitas.

## Decisões homologáveis

- Timezone operacional: `America/Sao_Paulo`.
- SLA usa dias corridos e não desconta feriados.
- Entrega no prazo é a realizada até o fim da data prevista.
- Entrega atrasada é a não entregue após a data prevista.
- Extravio exige status explícito `lost`; atraso nunca infere extravio.
- Eficiência é o percentual de entregas no prazo sobre a população válida.
- Empate no ranking: menor percentual de extravio, menor percentual médio de frete e nome da transportadora.
- Percentual médio de frete considera somente entregas com nota fiscal positiva e frete informado.
- Aceite automatizado comprova o comportamento técnico; homologação humana continua pendente até aprovação formal do cliente.

## Arquitetura P1

Listagem de envios, dashboard e eficiência reutilizarão a mesma semântica de filtros server-side. O universo filtrado será definido antes da agregação, evitando que KPIs e rankings consultem populações diferentes. Cada resposta informará contagens, somas e população financeira válida necessárias para reconciliação.

O ranking será calculado de forma determinística. A ordenação principal usa maior percentual no prazo; os critérios seguintes são menor percentual de extravio, menor percentual médio de frete e nome estável. Rankings de custo e volume continuarão explícitos, sem substituir o ranking oficial de eficiência.

Um dataset sanitizado e controlado cobrirá datas-limite, atraso, extravio explícito, frete ausente, NF zero, empates e filtros combinados. Testes compararão listagem, dashboard e eficiência sobre a mesma janela.

## Arquitetura P2

Os testes vazios de exceções serão substituídos por cenários reais de serviço e API. O Web receberá fixture XLSX válida e fluxos Playwright para importação e para painel de exceções até o histórico de tratativas.

O layout Braspress será versionado com amostra sanitizada, cabeçalhos obrigatórios e regras de normalização documentadas. Nenhuma credencial ou automação de portal integrará o fluxo.

Uma matriz parametrizada cobrirá sucesso, `401` e `403` nas rotas privadas dos domínios em P2. As políticas de senha, tokens, alertas, relatórios e auditoria serão aplicadas por configuração e contratos testáveis, evitando valores implícitos espalhados.

## Políticas operacionais iniciais

- Senhas: mínimo de 12 caracteres, com letras maiúsculas, minúsculas, número e símbolo; senhas conhecidas de demonstração não são válidas fora do ambiente de desenvolvimento.
- Access token: 15 minutos; refresh token: 7 dias.
- Refresh rotativo: cada renovação emite novo refresh e revoga o anterior; inativação do usuário invalida novas sessões e renovações.
- Alertas internos são obrigatórios; canais externos ficam desabilitados até configuração explícita de destinatários.
- Retry externo: três tentativas com backoff controlado; após esgotamento, estado `failed` e escalonamento operacional interno.
- Relatórios: geração diária às 06:00 no timezone operacional; retenção de 365 dias.
- Auditoria: retenção de 5 anos, append-only na API; descarte requer rotina administrativa auditada futura.

## Erros e segurança

Filtros inválidos falham com validação, sem fallback silencioso. Dados financeiros ausentes permanecem indisponíveis. Upload inválido não persiste domínio. Autoria de tratativas vem da sessão. Erros de canal não apagam alertas. Logs e fixtures não contêm secrets nem dados pessoais reais.

## Estratégia de testes e commits

Cada fatia seguirá RED, GREEN e REFACTOR e terminará em commit próprio:

1. contrato de métricas, filtros e dataset de reconciliação;
2. ranking determinístico e apresentação Web;
3. exceções e tratativas sem testes vazios;
4. XLSX, Braspress e E2E de importação;
5. E2E de exceções e tratativas;
6. matriz RBAC;
7. políticas de autenticação e tokens;
8. políticas de alertas, relatórios e auditoria;
9. UAT técnico, documentação e encerramento de P1/P2.

O push ocorrerá uma vez, ao final, após todos os gates aplicáveis.

## Limites do aceite

O repositório pode comprovar UAT técnico com dataset e ambiente controlados. Aceite operacional de transportadoras, alertas, relatórios e auditoria por representantes do cliente será registrado como pendente enquanto não houver evidência assinada ou decisão explícita posterior.
