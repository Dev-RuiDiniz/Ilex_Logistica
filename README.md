# Ilex Logistica

<<<<<<< HEAD
## Inteligência operacional para uma logística mais previsível

O **Ilex Logística** é uma plataforma desenvolvida para centralizar o acompanhamento de entregas, transformar dados dispersos em informação útil e ajudar equipes a agir antes que atrasos e exceções prejudiquem clientes e operações.
=======
> Plataforma operacional para empresas que precisam enxergar, priorizar e agir sobre entregas em risco antes que o atraso vire custo, retrabalho ou desgaste com o cliente.

**Status atual:** beta funcional consolidada, com stack completa local (`api` + `db` + `web`) e perfis seed para desenvolvimento e homologacao.
>>>>>>> fix/infra-setup-local

Em uma única experiência, a solução reúne importação de dados, monitoramento de envios, análise de prazos, alertas, indicadores e relatórios gerenciais. O resultado é mais visibilidade, melhor priorização e menos dependência de controles manuais.

<<<<<<< HEAD
## O problema que resolvemos

Operações logísticas costumam depender de planilhas, consultas em diferentes portais e conferências repetitivas. Esse cenário dificulta a identificação antecipada de riscos, consome tempo da equipe e limita a visão gerencial.

O Ilex Logística foi concebido para:

- concentrar informações de diferentes transportadoras;
- reduzir consultas e consolidações manuais;
- destacar entregas atrasadas, críticas ou sem atualização;
- organizar tratativas e preservar o histórico operacional;
- comparar desempenho, volume e custo logístico;
- apoiar decisões com indicadores e relatórios consistentes.
=======
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
>>>>>>> fix/infra-setup-local

## Para quem é a plataforma

<<<<<<< HEAD
### Equipe de logística

Uma visão prática das entregas que precisam de atenção, com filtros, alertas e registro de tratativas.
=======
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
>>>>>>> fix/infra-setup-local

### Gestores

<<<<<<< HEAD
Indicadores consolidados para acompanhar prazos, exceções, transportadoras e evolução da operação.

### Administração

Controle de usuários, permissões, transportadoras e parâmetros operacionais.

### Auditoria e backoffice

Consulta segura de históricos e registros relevantes para conferência e rastreabilidade.

## Capacidades da solução

- **Entregas monitoradas:** consulta centralizada de rastreio, cliente, destino, transportadora, status e dados fiscais e financeiros.
- **Importação assistida:** entrada de dados por CSV e Excel, com pré-visualização, validação e identificação de inconsistências.
- **Gestão de SLA:** análise de prazo, atraso e criticidade para priorização operacional.
- **Painel de exceções:** visão direcionada aos casos que exigem intervenção.
- **Eficiência por transportadora:** comparação de volume, cumprimento de prazo, ocorrências e custos disponíveis.
- **Dashboard executivo:** indicadores e tendências para acompanhamento gerencial.
- **Alertas e relatórios:** consolidação das ocorrências relevantes e geração de relatórios diários.
- **Segurança por perfil:** acesso às funcionalidades conforme a responsabilidade de cada usuário.
- **Auditoria operacional:** histórico para apoiar controle, análise e melhoria contínua.

## Como funciona a jornada operacional

```text
Importar dados
      ↓
Validar e organizar entregas
      ↓
Calcular prazos e criticidade
      ↓
Destacar atrasos e exceções
      ↓
Registrar tratativas
      ↓
Acompanhar indicadores e relatórios
```

## Cotações assistidas

Além do monitoramento pós-expedição, o produto possui um **MVP assistido de cotação de frete por pedido**. Ele importa pedidos do ERP por CSV/XLSX, recebe cotações por Web/CSV, destaca a melhor opção determinística, permite override justificado e preserva o histórico da decisão.

Integrações automáticas com ERPs e transportadoras poderão ser incorporadas progressivamente, conforme contratos, disponibilidade técnica e homologação dos parceiros.

## Diferenciais

- visão operacional e gerencial no mesmo ambiente;
- implantação gradual, começando por arquivos já disponíveis na operação;
- arquitetura preparada para novas transportadoras e integrações;
- regras de acesso adequadas a diferentes responsabilidades;
- rastreabilidade das ações e decisões relevantes;
- evolução orientada por especificações, critérios de aceite e validação contínua.

## Segurança e confiabilidade

O produto foi desenhado com separação de perfis, proteção de acesso, validação de dados e preservação de histórico. A preparação para uso produtivo inclui uma etapa formal de homologação, segurança, desempenho, continuidade e aceite do cliente.

## Situação do projeto

O Ilex Logística está em fase de consolidação e homologação do MVP avançado. Os módulos centrais estão estruturados e o trabalho de conclusão está organizado por etapas, priorizando estabilidade, aderência operacional e preparação segura para implantação.

## Próximos passos comerciais

1. Validar regras de SLA, eficiência e dados obrigatórios com a operação.
2. Homologar o fluxo de importação com amostras representativas.
3. Homologar pedidos/cotações com amostras sanitizadas e executar UAT por perfil.
4. Validar PostgreSQL, backup/restore, desempenho e deploy/rollback em VPS.
5. Publicar release candidata somente após os gates e acompanhar o piloto.

---

**Ilex Logística — mais visibilidade para agir, comparar e melhorar a operação.**
=======
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
>>>>>>> fix/infra-setup-local
