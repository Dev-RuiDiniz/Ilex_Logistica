# Ilex Logistica

> Plataforma operacional para empresas que precisam enxergar, priorizar e agir sobre entregas em risco antes que o atraso vire custo, retrabalho ou desgaste com o cliente.

**Status atual:** beta funcional consolidada, com stack completa local (`api` + `db` + `web`) e perfis seed para desenvolvimento e homologacao.

---

## Visao Comercial

O **Ilex Logistica** foi desenhado para operadores logisticos, embarcadores e times de torre de controle que hoje dependem de planilhas, consultas manuais em portais de transportadoras e acompanhamento reativo de SLA.

Na pratica, a plataforma transforma o processo operacional em um fluxo unico:

1. **Recebe cargas e remessas** por cadastro ou importacao assistida.
2. **Normaliza e valida os dados** antes de entrar na operacao.
3. **Calcula SLA, atraso e criticidade** automaticamente.
4. **Prioriza excecoes** com alertas e filas de trabalho.
5. **Entrega visibilidade gerencial** com dashboards, relatorios e auditoria.

O resultado esperado e simples de explicar para negocio:

- Menos tempo gasto consolidando status manualmente
- Deteccao antecipada de desvios operacionais
- Melhor governanca sobre importacoes, tratativas e usuarios
- Mais previsibilidade para transportadoras, gestores e auditoria

---

## O Que a Plataforma Faz

| Frente | Como gera valor |
|--------|------------------|
| **Rastreio e visibilidade** | Centraliza envios em um unico painel com filtros, status e consulta rapida |
| **Gestao de excecoes** | Mostra entregas atrasadas, com risco de SLA ou sem atualizacao relevante |
| **Importacao operacional** | Recebe CSV/XLSX com validacao, preview, deteccao de duplicidade e suporte a layout Braspress |
| **Regras de SLA** | Permite parametrizar prazos e deixar o calculo de atraso automatizado |
| **Alertas** | Sinaliza ocorrencias que exigem acao do time operacional |
| **Relatorios** | Resume desempenho diario, falhas, excecoes e indicadores para acompanhamento |
| **RBAC e auditoria** | Controla quem pode ver ou alterar cada area, com trilha para operacao e compliance |

---

## Para Quem o Ilex Serve

- Operacoes logisticas internas
- Torres de controle
- Transportadoras com necessidade de governanca operacional
- Times de gestao que precisam de KPI, SLA e visibilidade de gargalos
- Auditoria e liderancas que precisam rastrear quem fez o que

---

## Como Funciona no Dia a Dia

1. O time importa ou registra os envios.
2. A API processa, valida e grava a base operacional.
3. O motor de regras calcula SLA e classifica criticidade.
4. O frontend organiza a fila por prioridade operacional.
5. Gestores e auditores acompanham indicadores, historico e excecoes.

---

## Modulos Principais

| Modulo | Status | Resumo |
|--------|--------|--------|
| **Auth e usuarios** | Implementado | Login JWT, refresh token, RBAC por permissao e perfis operacionais |
| **Envios** | Implementado | Cadastro, filtros, listagem, detalhe, campos financeiros/fiscais e status |
| **Importacoes** | Implementado | Preview, confirmacao, suporte CSV/XLSX e layout Braspress |
| **Transportadoras** | Implementado | Cadastro, inativacao, consulta e eficiencia por transportadora |
| **SLA** | Implementado | Regras configuraveis, atraso e criticidade automatizados |
| **Alertas** | Implementado | Gatilhos operacionais e visao de pendencias |
| **Relatorios** | Implementado | Relatorio diario e KPIs operacionais |
| **Dashboard** | Implementado | Visao consolidada da operacao |
| **Auditoria** | Parcial | Logs e trilhas operacionais ja existentes, com expansao administrativa pendente |

---

## Stack do Monorepo

```text
.
├── apps/
│   ├── api/      # FastAPI + SQLAlchemy + Alembic
│   └── web/      # Next.js + React + TypeScript
├── infra/        # Docker Compose, banco e artefatos operacionais
├── scripts/      # Validacoes e automacoes locais
└── docs/         # Especificacoes, auditorias e historico do produto
```

### Tecnologias

| Camada | Stack |
|--------|-------|
| **Backend** | Python 3.12+, FastAPI, SQLAlchemy 2, Alembic, Pydantic |
| **Frontend** | Next.js 16, React 19, TypeScript 5, Tailwind CSS 4 |
| **Banco** | PostgreSQL 16 na stack Docker, SQLite em cenarios locais isolados |
| **Seguranca** | JWT, hash de senha, RBAC por role/permissao |
| **Qualidade** | pytest, Vitest, Playwright, validacao de migrations e secret scan |

---

## Setup Local Rapido

```bash
# API + banco
cd infra
docker compose up --build -d

# frontend
cd ../apps/web
npm install
npm run dev
```

### Enderecos locais

- API: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- API health: `http://127.0.0.1:8000/health`
- API v1 health: `http://127.0.0.1:8000/api/v1/health`
- Web: `http://localhost:3000`

Se a porta `3000` estiver ocupada no host, o Next.js sobe automaticamente em outra porta livre, como `http://localhost:3002`.

Para detalhes completos do ambiente, consulte [`infra/LOCAL_SETUP.md`](infra/LOCAL_SETUP.md).

---

## Seeds de Desenvolvimento

O repositório agora inclui um seed oficial para acessos locais:

```bash
python scripts/seed_dev_users.py
```

### Usuarios seed

| Perfil | E-mail | Senha |
|--------|--------|-------|
| **Admin** | `admin@ilex.com` | `123456` |
| **Manager** | `manager@ilex.com` | `123456` |
| **Operator** | `operator@ilex.com` | `123456` |
| **Viewer** | `viewer@ilex.com` | `123456` |
| **Logistica** | `logistica@ilex.com` | `123456` |
| **Gestor** | `gestor@ilex.com` | `123456` |
| **Auditoria** | `audit@ilex.com` | `123456` |

Uso recomendado: ambiente local, QA tecnico e homologacao controlada. Nao usar essas credenciais em producao.

---

## Validacao e Qualidade

```bash
cd apps/api && python -m pytest -q
cd apps/web && npm test
python scripts/validate_migrations.py
python scripts/check_secrets.py --repo-root . --self-test
```

---

## Roadmap Imediato

1. Completar a tela administrativa de usuarios
2. Expandir auditoria operacional e administrativa
3. Evoluir conectores com transportadoras
4. Ampliar E2E e automacoes de release

---

## Contato

Desenvolvido por [Dev-RuiDiniz](https://github.com/Dev-RuiDiniz).
