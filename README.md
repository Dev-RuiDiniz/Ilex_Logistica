# Ilex Logística

> Plataforma inteligente para rastreio de entregas, identificação de atrasos e gestão de exceções operacionais.

**Versão Beta concluída | Pronto para produção**

---

## O que é o Ilex Logística?

O **Ilex Logística** é uma plataforma web completa que centraliza o monitoramento de envios, automatiza a identificação de atrasos e criticidade, e oferece ferramentas avançadas de importação, relatórios e gestão operacional para empresas de logística e transporte.

### Problemas que resolvemos

- **Rastreio fragmentado** — centralize todos os envios em um único painel
- **Atrasos descobertos tarde demais** — alertas automáticos baseados em regras de SLA configuráveis
- **Importação manual de planilhas** — upload de CSV/XLSX com validação automática, detecção de duplicidade e mapeamento inteligente de colunas (incluindo layout Braspress)
- **Falta de visibilidade operacional** — dashboards com KPIs, relatórios diários automáticos e análise de eficiência por transportadora
- **Controle de acesso inexistente** — autenticação JWT com RBAC (4 perfis: admin, logística, gestor, auditoria)

---

## Funcionalidades Principais

| Módulo | O que faz | Status |
|--------|-----------|--------|
| **Envios (Shipments)** | Cadastro, rastreio, filtros avançados, campos fiscais/financeiros e cálculo de SLA | Implementado |
| **Importação** | Upload CSV/XLSX com preview, validação linha a linha, confirmação e layout Braspress assistido | Implementado |
| **Transportadoras** | CRUD completo com análise de eficiência e ranking | Implementado |
| **SLA & Criticidade** | Regras de prazo configuráveis, cálculo automático de atraso e alertas | Implementado |
| **Alertas** | Notificações operacionais por status e criticidade | Implementado |
| **Relatórios** | Relatório diário automático com resumo, KPIs, exceções e falhas de importação | Implementado |
| **Dashboard** | Visão consolidada com indicadores operacionais | Implementado |
| **Usuários & Permissões** | Autenticação JWT, 4 perfis de acesso e controle granular | Implementado |
| **Auditoria** | Logs de coleta e histórico de importações versionado | Parcial |

---

## Arquitetura do Monorepo

```text
.
├── .github/         # Workflows CI/CD, templates e automação
├── apps/
│   ├── api/         # Backend Python (FastAPI) — 489 testes automatizados
│   └── web/         # Frontend Next.js (TypeScript) — build otimizado
├── infra/           # Docker Compose, PostgreSQL, observabilidade
├── integrations/    # Guias de integração com transportadoras
└── docs/            # 50+ documentos: arquitetura, roadmaps, QA
```

## Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic |
| **Frontend** | Next.js 16, React 19, TypeScript 5, Tailwind CSS 4 |
| **Banco de Dados** | PostgreSQL 16 (produção) / SQLite (dev) |
| **Autenticação** | JWT com refresh token, bcrypt, RBAC com 4 perfis |
| **Infraestrutura** | Docker, Docker Compose, GitHub Actions |
| **Testes** | pytest 8.3+ (API), Vitest 4+ (Web), Playwright (E2E) |
| **Governança** | Secret scan, validação de migrations, checklist beta |

---

## Comece em Minutos

```bash
# 1. Clone
git clone https://github.com/Dev-RuiDiniz/Ilex_Logistica.git
cd Ilex_Logistica

# 2. Backend
cd apps/api && pip install -e ".[dev]" && pytest -q

# 3. Frontend
cd apps/web && npm install && npm run build

# 4. Infraestrutura
cd infra && docker compose up -d
```

Para detalhes completos de setup, consulte [`infra/LOCAL_SETUP.md`](infra/LOCAL_SETUP.md).

---

## Qualidade e Testes

- **489 testes automatizados** no backend (pytest)
- **Build do frontend validado** com TypeScript strict
- **Secret scan automatizado** para segurança
- **Migrations versionadas** com testes de roundtrip (upgrade/downgrade)
- **CI/CD** com GitHub Actions para validação contínua

```bash
# Rodar validações localmente
python scripts/check_secrets.py --repo-root .
python scripts/validate_migrations.py
python scripts/beta_validate.py
```

---

## Fluxo de Contribuição

Branches por tipo de mudança:
- `feature/<tema>` — novas funcionalidades
- `fix/<tema>` — correções
- `chore/<tema>` — infraestrutura e configuração

Commits em português com escopo:
- `feat(api): adiciona endpoint de eficiência por transportadora`
- `fix(web): corrige validação de SLA no formulário`

---

## Status e Roadmap

| Fase | Status | Descrição |
|------|--------|-----------|
| **Fase 1** | Concluída | Consolidação do monorepo, 36 PRs mergeados, base técnica sólida |
| **Fase 2** | Em andamento | CI/CD completo, testes E2E, conectores de transportadoras |
| **Fase 3** | Planejada | Otimização de pipelines, versionamento e automações de release |

**Próximos passos priorizados:**
1. Conectores de transportadoras (LOG-021/022)
2. Tela de tratativas operacionais (W11)
3. Envio de relatório diário por e-mail (LOG-019)
4. Cobertura de testes E2E com Playwright

---

## Licença e Contato

Desenvolvido por [Dev-RuiDiniz](https://github.com/Dev-RuiDiniz).

Para dúvidas, sugestões ou parcerias, abra uma issue ou entre em contato pelo GitHub.
