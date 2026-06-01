# -*- coding: utf-8 -*-
"""Generate the Ilex Logistica Scrum + TDD completion roadmap PDF.

The document is intentionally data-driven so the roadmap can be regenerated
after future scope or repository evidence changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "Docs" / "roadmaps"
OUTPUT_PDF = OUTPUT_DIR / "Roadmap_Conclusao_Projeto_Ilex_Logistica.pdf"
PAGE_SIZE = landscape(A4)


PROJECT = "Ilex Logística"
ORG = "ilex-logistica"
REPOS = ["Api", "Web", "Infra", "Integrations", "Docs", ".github"]
PERIOD_START = "18/05/2026"
PERIOD_END = "10/07/2026"
GENERATED_AT = date(2026, 5, 19).strftime("%d/%m/%Y")
VERSION = "1.0"


STATUS_COLORS = {
    "OK": colors.HexColor("#16A34A"),
    "PARCIAL": colors.HexColor("#F59E0B"),
    "PENDENTE": colors.HexColor("#DC2626"),
    "QUEBRADO": colors.HexColor("#B91C1C"),
    "NÃO IDENTIFICADO": colors.HexColor("#64748B"),
}


@dataclass(frozen=True)
class Sprint:
    name: str
    period: str
    objective: str
    capacity: str
    team: str
    deliverables: str
    dependencies: str


@dataclass(init=False)
class Task:
    id: str
    sprint: str
    title: str
    priority: str
    kind: str
    repo: str
    area: str
    module: str
    description: str
    justification: str
    dependencies: str
    order: str
    points: int
    tests: str
    acceptance: tuple[str, str, str]
    risks: str
    mitigation: str
    evidence: str

    def __init__(self, *args):
        fields = [
            "id",
            "sprint",
            "title",
            "priority",
            "kind",
            "repo",
            "area",
            "module",
            "description",
            "justification",
            "dependencies",
            "order",
            "points",
            "tests",
            "acceptance",
            "risks",
            "mitigation",
            "evidence",
        ]
        values = list(args)
        if len(values) == len(fields) - 1:
            values.insert(7, values[6])
        if len(values) != len(fields):
            raise TypeError(f"Task expected {len(fields)} or {len(fields) - 1} values, got {len(values)}")
        for field, value in zip(fields, values, strict=True):
            setattr(self, field, value)


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=colors.HexColor("#050505"),
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base["Normal"],
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#111827"),
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#B91C1C"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontSize=8.2,
            leading=11.2,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontSize=7,
            leading=9,
            textColor=colors.HexColor("#334155"),
        ),
        "table": ParagraphStyle(
            "Table",
            parent=base["BodyText"],
            fontSize=6.7,
            leading=8.4,
            textColor=colors.HexColor("#1F2937"),
        ),
        "table_bold": ParagraphStyle(
            "TableBold",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=6.7,
            leading=8.4,
            textColor=colors.HexColor("#111827"),
        ),
        "right": ParagraphStyle(
            "Right",
            parent=base["BodyText"],
            fontSize=7,
            leading=9,
            alignment=TA_RIGHT,
            textColor=colors.HexColor("#64748B"),
        ),
        "toc": ParagraphStyle(
            "TOC",
            parent=base["BodyText"],
            fontSize=9,
            leading=12,
            leftIndent=8,
        ),
    }


S = styles()


def p(text: object, style: str = "body") -> Paragraph:
    value = "" if text is None else str(text)
    value = value.replace("\n", "<br/>")
    return Paragraph(value, S[style])


def bullet_list(items: Iterable[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, "body"), leftIndent=10) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=12,
    )


def table(rows: list[list[object]], widths: list[float] | None = None, header: bool = True) -> Table:
    converted = []
    for row in rows:
        converted.append([cell if hasattr(cell, "wrap") else p(cell, "table_bold" if header and not converted else "table") for cell in row])
    tbl = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ]
    tbl.setStyle(TableStyle(style))
    return tbl


def section(title: str, level: int = 1) -> Paragraph:
    style = "h1" if level == 1 else "h2" if level == 2 else "h3"
    para = p(title, style)
    para._bookmarkName = title.replace(" ", "_").replace("/", "_")
    return para


DIAGNOSIS = [
    ["Backend", "PARCIAL", "FastAPI, SQLAlchemy, Alembic, auth JWT, RBAC inicial, carriers, imports e shipments com testes passando.", "Regras de SLA, tratativas, exceções, relatórios, auditoria e cotação ainda não estão completos.", "Concluir módulos críticos com TDD e contratos de API."],
    ["Frontend", "PARCIAL", "Next.js App Router, login, layout privado, transportadoras, importação e envios com Vitest.", "Dashboard ainda é textual, UX operacional e telas do escopo estão incompletas.", "Priorizar fluxos reais de operação logística e estados de erro/sucesso."],
    ["Mobile", "NÃO IDENTIFICADO", "O PDF declara mobile fora do MVP.", "Item não aplicável conforme evidências encontradas no repositório.", "Manter no backlog futuro."],
    ["Banco de dados", "PARCIAL", "Migrations para usuários, roles, carriers, import histories, deliveries e shipments.", "Modelo ainda não cobre eventos, tratativas, regras SLA, pedidos, cotações e auditoria completa.", "Planejar migrations incrementais com testes."],
    ["Autenticação", "OK", "Endpoints de login/refresh, hash de senha, JWT e testes de auth.", "Hardening de sessão, refresh e expiração precisa ser validado em homologação.", "Adicionar testes de autorização e expiração."],
    ["Autorização", "PARCIAL", "RBAC inicial em API/Web e permissões por perfil.", "Nem todos os endpoints e telas futuras têm controle de ação.", "Aplicar matriz Admin, Logística, Gestor e Auditoria."],
    ["Regras de negócio", "PARCIAL", "Funções iniciais de atraso e criticidade em shipments.", "SLA por transportadora/região/tipo e regra de exceção ainda pendentes.", "Formalizar motor de regras com testes unitários."],
    ["Integrações externas", "PENDENTE", "Repositório Integrations contém documentação inicial.", "Não há conector Braspress/API/bot implementado.", "Começar por importação assistida e contrato de conector."],
    ["Testes automatizados", "OK", "Api: 61 testes, Web: 55 testes, Infra: 5 testes em execução local.", "Cobertura E2E e contrato cross-repo ainda pendentes.", "Adicionar testes por camada e pipeline de regressão."],
    ["Infraestrutura", "PARCIAL", "Docker Compose para db/api, exemplos de env, healthchecks e testes de infra.", "Web no compose, homologação, secrets e deploy final pendentes.", "Fechar ambiente reproduzível e CI/CD."],
    ["CI/CD", "PARCIAL", "Workflows identificados para Api e Web.", "Infra, Integrations, Docs e pipeline E2E não estão completos.", "Padronizar GitHub Actions por repositório."],
    ["Segurança", "PARCIAL", "JWT, RBAC e orientação de placeholders.", "Criptografia de credenciais de transportadoras, LGPD e auditoria ainda pendentes.", "Executar hardening e checklist de dados sensíveis."],
    ["Observabilidade", "PARCIAL", "Logs básicos de request e documentação inicial.", "Logs persistidos de coleta, importação, tratativas e alertas ainda pendentes.", "Criar modelo de eventos e dashboards mínimos."],
    ["Documentação", "OK", "Docs possui ADRs, sprints, matriz de rastreio, UAT e PDFs anteriores.", "Documento consolidado de conclusão ainda ausente antes deste trabalho.", "Gerar PDF executivo consolidado."],
    ["Deploy", "PENDENTE", "Infra possui Docker local.", "Não foi encontrada evidência suficiente no repositório para confirmar deploy de homologação/produção.", "Planejar homologação, secrets, rollback e checklist go-live."],
    ["Experiência do usuário", "PARCIAL", "Fluxos fundacionais existem.", "Faltam dashboard real, painel de exceções, eficiência, detalhe, cotação e responsividade polida.", "Executar UAT por tela crítica."],
    ["Admin/backoffice", "PARCIAL", "Transportadoras e permissões iniciais.", "Usuários, logs, auditoria, configurações e integrações pendentes.", "Planejar backoffice mínimo."],
    ["APIs públicas e privadas", "PARCIAL", "Endpoints internos em /api/v1.", "Não há evidência de API pública versionada/documentada para parceiros.", "Documentar contratos internos e adiar API pública se não for MVP."],
    ["Tratamento de erros", "PARCIAL", "Handler de validação e erros de importação.", "Padronização de domínio por módulo ainda incompleta.", "Criar envelope de erro por API."],
    ["Logs", "PARCIAL", "Logs de request no backend.", "Persistência auditável ainda incompleta.", "Criar audit logs e collection logs."],
    ["Validações", "PARCIAL", "Validações de CSV/XLSX, carrier, auth e schemas.", "Validações de SLA, tratativas, cotações e regras pendentes.", "TDD de validação por domínio."],
    ["Variáveis de ambiente", "OK", "Env examples em Infra.", "Secrets reais não devem entrar no repositório.", "Validar por CI sem expor valores."],
    ["Arquitetura geral", "PARCIAL", "Arquitetura modular documentada e repositórios separados.", "Integrações e jobs ainda sem implementação completa.", "Fechar contratos cross-repo."],
    ["Performance", "NÃO IDENTIFICADO", "Não foi encontrada evidência suficiente no repositório para confirmar testes de performance.", "Risco em filtros, importações e relatórios com alto volume.", "Planejar índices, paginação e teste de carga mínimo."],
    ["Escalabilidade", "NÃO IDENTIFICADO", "Não foi encontrada evidência suficiente no repositório para confirmar desenho de escala.", "Jobs e integrações podem crescer em volume.", "Manter arquitetura modular e filas/jobs isolados."],
    ["LGPD/compliance", "PARCIAL", "Escopo exige minimização, controle de acesso e auditoria.", "Implementação completa ainda não comprovada.", "Criar matriz de dados sensíveis e auditoria."],
]


MODULES = [
    ["Autenticação e Permissões", "Api/Web", "PARCIAL", "Login, JWT, sessão, guardas e RBAC inicial.", "Matriz completa por ação/tela, expiração, refresh robusto.", "Usuários, roles e middleware.", "Falha de autorização pode expor dados.", "TASK-01, TASK-08, TASK-40"],
    ["Transportadoras", "Api/Web", "OK", "CRUD e inativação inicial.", "Regras SLA, credenciais seguras, status de integração.", "Auth, banco e integrações.", "Credenciais sensíveis e regras incompletas.", "TASK-09, TASK-27"],
    ["Importação de Entregas", "Api/Web", "PARCIAL", "CSV/XLSX parcial, validações e histórico.", "Prévia unificada, confirmação, arquivo original, Braspress assistida.", "Banco, UI e storage.", "Dados inválidos podem virar base operacional.", "TASK-10, TASK-11, TASK-29"],
    ["Entregas Monitoradas", "Api/Web", "PARCIAL", "Listagem com filtros básicos e campos fiscais parciais.", "Detalhe, timeline, filtros por cliente/UF e eficiência.", "Shipments e carriers.", "Operação sem visão completa.", "TASK-13, TASK-14, TASK-15"],
    ["Dashboard Logístico", "Web/Api", "PENDENTE", "Tela inicial textual.", "KPIs reais, gráficos, atalhos e alertas.", "API agregadora.", "Liderança sem visão executiva.", "TASK-18"],
    ["SLA e Regras de Prazo", "Api/Web", "PENDENTE", "Funções simples de atraso.", "CRUD de regras, aplicação por transportadora/região/tipo.", "Carriers e shipments.", "Classificação incorreta de atraso.", "TASK-21, TASK-22"],
    ["Painel de Exceções", "Api/Web", "PENDENTE", "Não identificado como tela/endpoint completo.", "Fila priorizada, filtros e ações.", "SLA, shipments e tratativas.", "Casos críticos sem visibilidade.", "TASK-23"],
    ["Tratativas", "Api/Web", "PENDENTE", "Não identificada entidade/tela.", "Registro de ação, status, justificativa e histórico.", "Usuários, shipments e auditoria.", "Ausência de rastreabilidade humana.", "TASK-24"],
    ["Relatório Diário", "Api/Web", "PENDENTE", "Previsto no escopo.", "Geração, visualização, envio e log.", "Exceções, alertas e SMTP.", "Rotina logística sem resumo matinal.", "TASK-25, TASK-26"],
    ["Alertas", "Api/Web", "PENDENTE", "Previsto no escopo.", "Alertas de dashboard/e-mail e histórico.", "Relatórios, SLA e notificações.", "Atrasos críticos sem notificação.", "TASK-26"],
    ["Logs e Auditoria", "Api/Infra/Web", "PARCIAL", "Logs de request e documentação.", "Logs persistidos de coleta, tratativas, alterações e relatórios.", "Usuários e módulos críticos.", "Baixa rastreabilidade operacional.", "TASK-28, TASK-39"],
    ["Integração Braspress", "Integrations/Api/Web/Docs", "PENDENTE", "Escopo recomenda importação assistida.", "Template, playbook e mapeador validado.", "Importação e contrato.", "Portal pode mudar ou limitar período.", "TASK-29, TASK-30"],
    ["Cotação de Frete", "Api/Web/Integrations", "PENDENTE", "Decidida como roadmap principal.", "Pedidos, cotações, comparação, ranking e auditoria.", "ERP/planilha e carriers.", "Dependência de dados de ERP/transportadoras.", "TASK-33, TASK-34, TASK-35, TASK-36"],
]


SCREENS = [
    ["W01 Login", "Web", "OK", "Tela pública", "Login integrado.", "Refresh/expiração visual.", "/auth/login", "Risco baixo.", "TASK-08"],
    ["W02 Dashboard Logístico", "Web", "PENDENTE", "Tela autenticada/relatório", "Placeholder textual.", "KPIs reais, gráficos e atalhos.", "Endpoints agregadores.", "Risco de UX e gestão.", "TASK-18"],
    ["W03 Transportadoras", "Web", "OK", "Tela administrativa", "CRUD inicial.", "SLA e credenciais seguras.", "/carriers", "Risco de configuração incompleta.", "TASK-09"],
    ["W04 Importação de Entregas", "Web", "PARCIAL", "Tela operacional", "Upload CSV.", "XLSX, prévia, histórico e Braspress.", "/imports/upload e /shipments/upload", "Risco de divergência entre importadores.", "TASK-10, TASK-11"],
    ["W05 Validação da Importação", "Web", "PARCIAL", "Tela operacional", "Resumo e erros por linha.", "Prévia rica e confirmação unificada.", "/shipments/import", "Risco de dados inválidos.", "TASK-11"],
    ["W06 Entregas Monitoradas", "Web", "PARCIAL", "Tela operacional", "Tabela com filtros básicos.", "NF, cliente, UF, frete, eficiência e filtros completos.", "/shipments", "Risco técnico e UX.", "TASK-13, TASK-14"],
    ["W07 Detalhe da Entrega", "Web", "PENDENTE", "Tela operacional", "Não identificada.", "Timeline, eventos, tratativas e auditoria.", "GET /shipments/{id}", "Risco de suporte operacional.", "TASK-16"],
    ["W08 Painel de Exceções", "Web", "PENDENTE", "Tela operacional", "Não identificado.", "Fila priorizada de atrasos/extravios.", "/exceptions", "Risco de atrasos não tratados.", "TASK-23"],
    ["W09 Regras de Prazo", "Web", "PENDENTE", "Tela de configuração", "Não identificada.", "CRUD de SLA.", "/sla-rules", "Risco de regra manual fora do sistema.", "TASK-21"],
    ["W10 Relatório Diário", "Web", "PENDENTE", "Tela de relatório", "Não identificada.", "Resumo matinal e histórico.", "/reports/daily", "Risco gerencial.", "TASK-25"],
    ["W11 Tratativas", "Web", "PENDENTE", "Tela operacional", "Não identificada.", "Registro de ação e resolução.", "/shipments/{id}/actions", "Risco de auditoria.", "TASK-24"],
    ["W12 Logs de Coleta", "Web", "PENDENTE", "Tela administrativa", "Não identificada.", "Histórico de coletas/falhas.", "/collection-logs", "Risco de operação cega.", "TASK-28"],
    ["W13 Alertas", "Web", "PENDENTE", "Tela operacional", "Não identificada.", "Configuração e acompanhamento.", "/alerts", "Risco de falha crítica silenciosa.", "TASK-26"],
    ["W14 Relatórios", "Web", "PENDENTE", "Tela de relatório", "Não identificada.", "Exportações e filtros.", "/reports", "Risco de baixa prestação de contas.", "TASK-25, TASK-38"],
    ["W15 Usuários e Permissões", "Web", "PENDENTE", "Tela administrativa", "Roles existem no banco/API.", "Gestão de usuários e permissões.", "/users", "Risco de operação manual.", "TASK-08"],
    ["W16 Configurações", "Web", "PENDENTE", "Tela de configuração", "Não identificada.", "Parâmetros gerais, horários e notificações.", "/settings", "Risco operacional.", "TASK-26, TASK-37"],
    ["W17 Integrações", "Web", "PENDENTE", "Tela administrativa", "Não identificada.", "Status e credenciais de conectores.", "/integrations", "Risco de secrets.", "TASK-27, TASK-30"],
    ["W18 Auditoria", "Web", "PENDENTE", "Tela administrativa", "Não identificada.", "Busca de eventos e alterações.", "/audit", "Risco LGPD/compliance.", "TASK-28, TASK-39"],
    ["Cotação de Frete por Pedido", "Web/Api", "PENDENTE", "Tela operacional", "Incluída por decisão do roadmap.", "Tabela comparativa e ranking.", "/freight-quotes", "Risco cross-repo/ERP.", "TASK-33, TASK-34, TASK-35, TASK-36"],
]


API_ENDPOINTS = [
    ["POST", "/api/v1/auth/login", "Auth", "Implementado", "email, password", "access_token, refresh_token", "Usuários/roles", "Credenciais obrigatórias", "Unitário, integração, autorização", "Hardening de expiração."],
    ["POST", "/api/v1/auth/refresh", "Auth", "Implementado", "refresh_token", "tokens", "JWT secret", "Token válido", "Unitário, erro", "Validar rotação."],
    ["GET", "/health e /api/v1/health", "Health", "Implementado", "-", "status", "Infra", "-", "Integração", "OK."],
    ["GET/POST/PUT/POST", "/api/v1/carriers", "Transportadoras", "Implementado", "Carrier payload", "Carrier", "Auth/RBAC", "Nome único e metadata JSON", "Unitário, integração, autorização", "Adicionar SLA/credenciais."],
    ["POST", "/api/v1/imports/upload", "Importações", "Parcial", "CSV/XLSX", "preview + histórico", "Delivery", "Colunas obrigatórias e duplicidade NF", "Integração, borda, erro", "Sem auth no router atual; precisa proteção."],
    ["GET", "/api/v1/imports/history", "Importações", "Parcial", "limit", "lista", "ImportHistory", "limit 1..200", "Integração", "Adicionar filtros e autorização."],
    ["POST", "/api/v1/shipments/upload", "Shipments", "Parcial", "CSV", "validação", "Carriers e usuário", "Campos obrigatórios e datas", "Integração, erro", "Diverge de /imports/upload."],
    ["POST", "/api/v1/shipments/import", "Shipments", "Parcial", "import_id, confirm", "resultado", "ImportHistory", "confirm true", "Integração", "Unificar fluxo."],
    ["GET", "/api/v1/shipments", "Shipments", "Parcial", "filtros/paginação", "lista", "Shipments", "Filtros básicos", "Integração, contrato", "Faltam cliente, UF, eficiência."],
    ["GET", "/api/v1/shipments/{id}", "Detalhe", "Pendente", "id", "detalhe/timeline", "Eventos/tratativas", "Autorização", "Contrato, integração", "Criar."],
    ["GET/POST/PUT", "/api/v1/sla-rules", "SLA", "Pendente", "regra", "regra", "Carriers/regiões", "Validação de faixa", "Unitário, integração", "Criar."],
    ["GET", "/api/v1/exceptions", "Exceções", "Pendente", "filtros", "fila", "SLA e shipments", "Status/criticidade", "Integração, regressão", "Criar."],
    ["POST/GET", "/api/v1/shipments/{id}/actions", "Tratativas", "Pendente", "ação", "histórico", "Usuários", "Justificativa", "Autorização, auditoria", "Criar."],
    ["GET/POST", "/api/v1/reports/daily", "Relatórios", "Pendente", "período", "relatório", "Exceções", "Período obrigatório", "Integração, contrato", "Criar."],
    ["GET/POST", "/api/v1/alerts", "Alertas", "Pendente", "regra/status", "alerta", "SMTP/dashboard", "Destinatários", "Contrato, erro", "Criar."],
    ["GET", "/api/v1/audit/events", "Auditoria", "Pendente", "filtros", "eventos", "Usuários", "Autorização auditoria", "Segurança", "Criar."],
    ["POST/GET", "/api/v1/orders/import", "Pedidos", "Pendente", "CSV/XLSX ERP", "pedidos", "Cotação", "Campos mínimos", "Integração, erro", "Criar."],
    ["POST/GET", "/api/v1/freight-quotes", "Cotação", "Pendente", "pedido/transportadoras", "ranking", "Orders/carriers", "Valores e status", "Contrato, integração", "Criar."],
]


DATABASE = [
    ["users", "roles, user_roles", "Inicial", "email, password_hash, is_active", "email unique", "Seed roles", "Gestão web pendente."],
    ["roles", "users", "Inicial", "name", "name unique", "Seed admin/logistica/gestor/auditoria", "Matriz por ação pendente."],
    ["carriers", "shipments", "Inicial", "name, external_code, integration_metadata, is_active", "name index/unique", "Não identificado", "Adicionar SLA e credenciais criptografadas."],
    ["shipments", "carriers/users", "Parcial", "tracking_code, carrier_id, status, estimated_delivery, invoice_number, amount, due_date, delay_days, criticality", "tracking_code unique; status/criticality indexes", "Não identificado", "Adicionar cliente, UF, invoice_value, freight_value, freight_percentage, collection_departure_date."],
    ["import_history/import_histories", "users/deliveries", "Parcial", "filename, status, counts, hash, errors", "file_hash index", "Não identificado", "Há dois modelos de histórico; unificar."],
    ["deliveries", "Nenhum explícito", "Parcial", "nf, transportadora, data_coleta, valor_frete, percentual_frete", "nf/data_coleta index", "Não identificado", "Relacionar a shipment/carrier ou consolidar."],
    ["shipment_events", "shipments", "Pendente", "status, source, occurred_at, payload", "shipment_id/date", "Pendente", "Necessário para timeline."],
    ["sla_rules", "carriers", "Pendente", "carrier_id, uf, delivery_type, days, priority", "carrier/uf/type", "Pendente", "Necessário para cálculo real."],
    ["shipment_actions", "shipments/users", "Pendente", "action, note, next_status, created_by", "shipment/date", "Pendente", "Necessário para tratativas."],
    ["audit_events", "users", "Pendente", "actor, entity, action, before, after", "entity/date", "Pendente", "Necessário para LGPD/compliance."],
    ["orders", "freight_quotes", "Pendente", "external_order_number, client, uf, value", "external_order_number", "Pendente", "Necessário para cotação."],
    ["freight_quotes", "orders/carriers", "Pendente", "quoted_value, status, message, expires_at", "order/carrier", "Pendente", "Necessário para ranking."],
]


INTEGRATIONS = [
    ["Braspress importação assistida", "Integrations/Api/Web/Docs", "PENDENTE", "Template CSV/XLSX, mapeador e playbook.", "Nenhuma credencial em repositório; arquivo exportado do portal.", "Mudança de layout, limite de período e dados sensíveis.", "Contrato, importação, erro, UAT", "TASK-29, TASK-30"],
    ["APIs de transportadoras", "Integrations/Api", "PENDENTE", "Interface de conector, retries, timeout e status.", "Documentação/API por transportadora.", "APIs ausentes ou instáveis.", "Contrato, integração, retry", "TASK-27"],
    ["Bots/scraping controlado", "Integrations", "PENDENTE", "Estrutura isolada e apenas quando necessário.", "Ambiente controlado e autorização.", "Captcha/bloqueio/mudança de portal.", "Contrato, segurança", "Backlog futuro se não for essencial."],
    ["SMTP/provedor de e-mail", "Api/Infra", "PENDENTE", "Envio de relatório diário.", "Secrets de SMTP em ambiente.", "Falha de entrega e vazamento de destinatários.", "Integração, erro", "TASK-26"],
    ["Storage de arquivos", "Api/Infra", "PENDENTE", "Guardar planilhas originais e relatórios.", "Definição local/S3 compatível.", "Perda de evidências.", "Integração, segurança", "TASK-11, TASK-37"],
    ["ERP por planilha/API", "Api/Web/Integrations", "PENDENTE", "Importação de pedidos para cotação.", "Campos e homologação do ERP.", "Sem documentação do ERP.", "Contrato, importação", "TASK-33"],
]


SPRINTS = [
    Sprint("Sprint 1 - Replanejamento, Diagnóstico e Hardening Base", "18/05/2026 a 22/05/2026", "Consolidar evidências, corrigir bloqueios técnicos, unificar contratos e preparar o projeto para execução rastreável.", "Capacidade alvo: 55 a 75 pontos com 1 fullstack, 1 QA parcial, 1 Tech Lead e apoio DevOps.", "Tech Lead, Fullstack, QA e DevOps parcial.", "Roadmap, contratos mínimos, CI/base estável e matriz de rastreio.", "Nenhuma dependência externa crítica; depende de acesso aos repositórios e escopo."),
    Sprint("Sprint 2 - Modelo Logístico, Importação e Campos Fiscais", "25/05/2026 a 29/05/2026", "Completar modelo de entregas, importação, campos fiscais/financeiros e consistência entre importadores.", "Capacidade alvo: 60 a 80 pontos. A capacidade estimada desta sprint pode exigir mais de um desenvolvedor ou redução de escopo.", "Backend, Frontend, QA e Tech Lead.", "Importação unificada, campos fiscais e migrations testadas.", "Depende da Sprint 1 e das regras de campos do apêndice."),
    Sprint("Sprint 3 - Entregas Monitoradas, Filtros e Eficiência", "01/06/2026 a 05/06/2026", "Transformar a tela de logística em operação real com filtros, busca ampliada, detalhe e quadro de eficiência.", "Capacidade alvo: 55 a 75 pontos.", "Fullstack, QA e UX.", "Tabela principal revisada, eficiência por transportadora e dashboard inicial.", "Depende de campos fiscais e filtros da API."),
    Sprint("Sprint 4 - SLA, Exceções e Tratativas", "08/06/2026 a 12/06/2026", "Implementar regras de prazo, cálculo de atraso, painel de exceções e registro de tratativas.", "Capacidade alvo: 60 a 80 pontos. Esta sprint possui dependências críticas e deve ser executada seguindo a ordem sugerida.", "Backend, Frontend, QA e Tech Lead.", "Motor SLA, exceções priorizadas e tratativas auditáveis.", "Depende de entregas monitoradas, regras operacionais e usuários."),
    Sprint("Sprint 5 - Relatório Diário, Alertas, Logs e Auditoria", "15/06/2026 a 19/06/2026", "Fechar rotinas de gestão diária, alertas, logs persistidos e trilha de auditoria.", "Capacidade alvo: 60 a 80 pontos.", "Backend, Frontend, QA, DevOps parcial.", "Relatório diário, alertas e auditoria operacional.", "Depende de exceções, tratativas e SMTP/storage."),
    Sprint("Sprint 6 - Integrações Assistidas, Braspress e Operação", "22/06/2026 a 26/06/2026", "Entregar integração assistida Braspress, conectores base e playbooks de operação.", "Capacidade alvo: 50 a 70 pontos.", "Backend, Integrations, QA, Docs e Tech Lead.", "Playbook Braspress, templates, conectores e monitoramento de coleta.", "Depende do fluxo de importação e dos exemplos de arquivo do cliente."),
    Sprint("Sprint 7 - Cotação de Frete por Pedido", "29/06/2026 a 03/07/2026", "Criar subaba de cotação com importação de pedidos, comparação por transportadora, ranking e histórico.", "Capacidade alvo: 65 a 85 pontos. A capacidade estimada desta sprint pode exigir mais de um desenvolvedor ou redução de escopo.", "Backend, Frontend, Integrations, QA e Tech Lead.", "Cotação por pedido operacional em MVP assistido/automatizável.", "Depende da definição mínima de campos de ERP e transportadoras habilitadas."),
    Sprint("Sprint 8 - Segurança, QA, Deploy, Homologação e Entrega Final", "06/07/2026 a 10/07/2026", "Executar hardening, testes finais, deploy de homologação, documentação e pacote de entrega.", "Capacidade alvo: 60 a 80 pontos. Esta sprint possui dependências críticas e deve ser executada seguindo a ordem sugerida.", "QA, DevOps, Tech Lead, Fullstack e Product Owner.", "Pipeline verde, homologação validada, manual e plano de rollback.", "Depende da estabilização das sprints anteriores."),
]


TASKS = [
    Task("TASK-01", SPRINTS[0].name, "Consolidar diagnóstico técnico e matriz de escopo", "P0", "Documentation", "Docs", "Roadmap/Governança", "Planejamento", "Consolidar diagnóstico com base em código, testes, escopo PDF e documentação existente.", "Remove ambiguidade antes da execução e evita backlog inventado.", "Acesso aos repositórios e PDF de escopo.", "Primeira tarefa.", 5, "Teste de documentação: validar presença das seções obrigatórias e rastreio das evidências antes da publicação.", ("Dado que o time consulta o roadmap", "Quando buscar status por área", "Então encontra status, evidência, risco e recomendação."), "Informação incompleta gerar decisão errada.", "Declarar suposições e lacunas explicitamente.", "PDF com diagnóstico e seção de suposições."),
    Task("TASK-02", SPRINTS[0].name, "Unificar contratos e nomenclatura entre escopo e repositórios reais", "P0", "Architecture", "Docs/Api/Web", "Contratos", "Documentar reconciliação entre ilex-logistics-* do escopo e repos reais Api/Web/Infra/Integrations/Docs.", "Evita issues e PRs apontando para repositórios incorretos.", "TASK-01.", "Após diagnóstico.", 3, "Teste de documentação: revisão cruzada de nomes em sumário, dependências e tarefas.", ("Dado que uma tarefa referencia um repo", "Quando ela for transformada em issue", "Então o repositório responsável existe na org ilex-logistica."), "Rastreamento cross-repo quebrado.", "Padronizar nomes no documento e nos templates.", "Tabela de repositórios analisados."),
    Task("TASK-03", SPRINTS[0].name, "Padronizar Definition of Done e evidências TDD", "P0", "QA", "Docs/.github", "Qualidade", "Criar padrão de DoD por tarefa com Red, Green, Refactor, evidência de testes e PR revisável.", "TDD é requisito obrigatório do projeto.", "TASK-01.", "Antes das tarefas técnicas.", 3, "Teste de processo: checklist confirma que toda tarefa técnica tem estratégia TDD e testes obrigatórios.", ("Dado que uma tarefa técnica é aberta", "Quando o dev iniciar execução", "Então há teste falhando planejado antes do código."), "Tarefas concluídas sem teste.", "Bloquear DoD sem evidência de teste.", "Checklist TDD/QA no PDF."),
    Task("TASK-04", SPRINTS[0].name, "Corrigir divergência entre importadores /imports e /shipments", "P0", "Architecture", "Api", "Importação", "Definir contrato único para upload, preview, confirmação e histórico, reduzindo duplicidade entre módulos.", "Há evidência de dois fluxos de importação com responsabilidades sobrepostas.", "TASK-02.", "Antes de expandir importação.", 8, "Red: testes de contrato para fluxo único e rejeição de rotas divergentes; Green: adaptar serviço mínimo; Refactor: extrair serviço comum.", ("Dado que o usuário importa arquivo", "Quando usa o fluxo oficial", "Então preview, validação, persistência e histórico seguem o mesmo contrato."), "Quebra de compatibilidade Web/API.", "Versionar endpoint e manter fallback temporário se necessário.", "Testes Api passando e contrato documentado."),
    Task("TASK-05", SPRINTS[0].name, "Fortalecer CI local e GitHub Actions por repositório", "P0", "DevOps", "Api/Web/Infra/.github", "CI/CD", "Garantir jobs de lint, teste e build para Api, Web e Infra, com padrão de status para PR.", "Pipeline parcial aumenta risco de regressão.", "TASK-03.", "Antes de sprints de feature intensiva.", 5, "Red: workflow falha sem comandos obrigatórios; Green: adicionar comandos mínimos; Refactor: reutilizar templates.", ("Dado que um PR é aberto", "Quando o CI executa", "Então lint/test/build relevantes rodam e bloqueiam falhas."), "CI lento ou inconsistente.", "Separar jobs por repo e cachear dependências.", "Pipeline verde ou execução local equivalente."),
    Task("TASK-06", SPRINTS[0].name, "Criar seeds e fixture operacional mínima", "P0", "Test", "Api", "Banco/Auth", "Gerar dados de usuários, roles, transportadoras e envios mínimos para testes e homologação.", "Fluxos críticos dependem de dados consistentes.", "TASK-04.", "Antes de UAT Web.", 5, "Red: teste de seed idempotente falha; Green: criar seed mínimo; Refactor: isolar fixtures.", ("Dado que o ambiente local inicia", "Quando seeds são executadas", "Então usuários/perfis e transportadora base existem sem duplicar dados."), "Dados sensíveis em seed.", "Usar apenas placeholders e senhas locais documentadas.", "Testes de seed e instrução de execução."),
    Task("TASK-07", SPRINTS[0].name, "Criar baseline E2E de login e navegação privada", "P1", "QA", "Web/Api", "E2E", "Planejar e implementar teste E2E mínimo para login, rota privada e navegação principal.", "Evita regressões no fluxo de entrada do sistema.", "TASK-05, TASK-06.", "Após ambiente local estável.", 5, "Red: teste E2E falha sem usuário/servidor; Green: configurar cenário mínimo; Refactor: extrair helpers.", ("Dado que o usuário possui credencial válida", "Quando acessa login", "Então entra no dashboard e vê navegação privada."), "Flakiness de teste de UI.", "Usar fixtures controladas e waits sem sleeps fixos.", "Relatório E2E e screenshot."),
    Task("TASK-08", SPRINTS[0].name, "Completar matriz de autorização por perfil", "P0", "Security", "Api/Web/Docs", "Auth/RBAC", "Definir e testar permissões para Admin, Logística, Gestor e Auditoria em endpoints e telas.", "O escopo exige controle por perfil.", "TASK-03.", "Antes de expor novas telas.", 8, "Red: testes de acesso negado por perfil; Green: aplicar guards/dependencies; Refactor: centralizar permissões.", ("Dado que um auditor acessa ação administrativa", "Quando tentar alterar dados", "Então o sistema bloqueia com resposta autorizativa clara."), "Exposição indevida de dados.", "Aplicar deny-by-default e testes por perfil.", "Matriz e testes de autorização passando."),
    Task("TASK-09", SPRINTS[1].name, "Adicionar regras SLA vinculadas a transportadoras", "P0", "Feature", "Api/Web", "Transportadoras/SLA", "Estender transportadoras com parâmetros de SLA por região/tipo sem expor credenciais.", "Regras de atraso dependem desses parâmetros.", "TASK-08.", "Antes do motor de atraso real.", 8, "Red: testes de criação/edição de regra SLA; Green: migration, schema e UI mínima; Refactor: separar domínio SLA.", ("Dado que uma transportadora tem regra para UF", "Quando a regra é salva", "Então ela fica disponível para cálculo de atraso."), "Modelagem insuficiente para regras futuras.", "Começar com campos mínimos e versionar regras.", "Migration, endpoints e tela testados."),
    Task("TASK-10", SPRINTS[1].name, "Unificar importação CSV/XLSX de entregas", "P0", "Feature", "Api/Web", "Importação", "Consolidar upload, preview, validação e confirmação em um fluxo único com suporte CSV/XLSX.", "A operação depende de importação confiável.", "TASK-04.", "Após contrato único.", 13, "Red: testes falham para CSV, XLSX, duplicidade e confirmação; Green: serviço único; Refactor: parsers isolados.", ("Dado que o arquivo válido é enviado", "Quando o usuário confirma importação", "Então entregas são persistidas e histórico registra sucesso."), "Perda de dados ou duplicidade.", "Transação, idempotência por hash e validação antes da persistência.", "Testes de importação e preview na UI."),
    Task("TASK-11", SPRINTS[1].name, "Persistir arquivo original e histórico auditável de importação", "P1", "Feature", "Api/Infra", "Importação/Auditoria", "Guardar metadados, hash, usuário, erros, status e referência ao arquivo original.", "Importações precisam ser auditáveis.", "TASK-10.", "Após fluxo unificado.", 5, "Red: teste exige hash, usuário e status; Green: adicionar persistência; Refactor: storage adapter.", ("Dado que um arquivo é importado", "Quando a importação termina", "Então histórico mostra status, usuário, hash e erros."), "Storage indefinido.", "Usar storage local no MVP e interface para S3 futuro.", "Histórico consultável e testes passando."),
    Task("TASK-12", SPRINTS[1].name, "Completar campos fiscais e financeiros na entidade logística", "P0", "Feature", "Api/Web", "Shipments", "Adicionar NF, valor NF, valor frete, percentual frete, data coleta, cliente e UF à entrega principal.", "Apêndice exige esses campos no MVP.", "TASK-10.", "Antes da tabela revisada.", 13, "Red: testes de migration/schema/listagem falham; Green: campos e cálculo; Refactor: normalizar conversões monetárias.", ("Dado que uma entrega possui valor NF e frete", "Quando é importada", "Então o percentual de frete é calculado sem divisão por zero."), "Campos duplicados entre Delivery e Shipment.", "Consolidar fonte canônica e migration de compatibilidade.", "Migration validada e API retornando campos."),
    Task("TASK-13", SPRINTS[2].name, "Revisar tabela de Entregas Monitoradas", "P0", "UX", "Web", "Entregas", "Exibir rastreio, NF, cliente, transportadora, UF, destino, coleta, previsão, status, valor NF, frete e percentual.", "A tela principal precisa refletir o apêndice.", "TASK-12.", "Primeira tarefa da Sprint 3.", 8, "Red: testes de componente esperam colunas; Green: renderizar tabela; Refactor: componentes de célula/status.", ("Dado que há entregas importadas", "Quando a tela carrega", "Então as colunas fiscais e logísticas aparecem formatadas."), "Tabela larga e ilegível.", "Usar layout responsivo, scroll horizontal e densidade operacional.", "Teste de componente e screenshot UAT."),
    Task("TASK-14", SPRINTS[2].name, "Expandir busca e filtros logísticos", "P0", "Feature", "Api/Web", "Filtros", "Busca por NF, cliente, rastreio, UF e transportadora; filtros por status, transportadora, cliente, UF, mês, ano e todo período.", "Critério explícito do apêndice.", "TASK-12, TASK-13.", "Após tabela revisada.", 8, "Red: testes de query combinada; Green: API e UI de filtros; Refactor: builder de parâmetros.", ("Dado que filtros são combinados", "Quando o usuário aplica período e UF", "Então tabela e totais refletem apenas os registros filtrados."), "Filtros lentos com volume.", "Índices e paginação obrigatória.", "Testes de API e Web para filtros combinados."),
    Task("TASK-15", SPRINTS[2].name, "Criar eficiência por transportadora", "P0", "Feature", "Api/Web", "Indicadores", "Criar agregação e quadro por transportadora com total NF, no prazo, atrasadas, extraviadas, frete total e percentual médio.", "Apêndice define como valor gerencial do MVP.", "TASK-14.", "Após filtros.", 13, "Red: testes de agregação por carrier e filtros; Green: endpoint e quadro; Refactor: serviço de métricas.", ("Dado que há entregas filtradas", "Quando o quadro é recalculado", "Então percentuais conferem com o total da transportadora."), "Cálculo errado afeta decisão gerencial.", "Cobrir casos com zero registros e valores nulos.", "Endpoint, quadro e testes de agregação."),
    Task("TASK-16", SPRINTS[2].name, "Criar detalhe da entrega com timeline", "P1", "Feature", "Api/Web", "Detalhe", "Implementar página individual com dados, eventos, importações, status e origem.", "Suporte operacional precisa investigar caso a caso.", "TASK-12.", "Paralelo ao quadro de eficiência.", 8, "Red: testes de GET detalhe e componente; Green: endpoint/página; Refactor: componente timeline.", ("Dado que o usuário abre uma entrega", "Quando há eventos associados", "Então a timeline mostra data, origem e status."), "Eventos ainda pendentes.", "Criar timeline preparada para eventos futuros e exibir dados conhecidos.", "Tela validada e contrato documentado."),
    Task("TASK-17", SPRINTS[2].name, "Criar histórico visual de importações", "P1", "Feature", "Web/Api", "Importação", "Exibir histórico de arquivos, status, erros e acesso ao resumo da importação.", "Operação precisa rastrear origem dos dados.", "TASK-11.", "Após histórico auditável.", 5, "Red: testes de listagem e filtros de histórico; Green: endpoint/UI; Refactor: componentes compartilhados.", ("Dado que existem importações anteriores", "Quando o usuário acessa histórico", "Então visualiza arquivo, data, usuário, status e erros."), "Histórico grande.", "Paginação e filtros por período/status.", "Teste de componente e endpoint."),
    Task("TASK-18", SPRINTS[2].name, "Substituir placeholder por dashboard logístico real", "P1", "Feature", "Api/Web", "Dashboard", "Criar KPIs de total, atrasados, críticos, sem atualização, resolvidos e frete agregado.", "Dashboard textual atual não atende o escopo.", "TASK-15.", "Após agregações.", 8, "Red: testes de endpoint de KPIs e cards; Green: serviço agregador; Refactor: cards reutilizáveis.", ("Dado que existem entregas no período", "Quando o dashboard abre", "Então KPIs mostram números reais e coerentes."), "Dados inconsistentes por filtro.", "Reutilizar serviço de métricas e filtros globais.", "Cards com dados reais e testes passando."),
    Task("TASK-19", SPRINTS[2].name, "Criar checklist UAT das telas logísticas", "P1", "QA", "Docs/Web", "UAT", "Documentar cenários de homologação para importação, entregas, filtros, eficiência e dashboard.", "Cliente precisa validar valor operacional.", "TASK-13 a TASK-18.", "Fim da Sprint 3.", 3, "Teste de documentação: checklist cobre telas e critérios do apêndice.", ("Dado que a sprint vai para review", "Quando o PO executa UAT", "Então cada fluxo tem passos e evidências esperadas."), "Homologação subjetiva.", "Critérios Dado/Quando/Então e prints obrigatórios.", "Checklist UAT versionado."),
    Task("TASK-20", SPRINTS[2].name, "Criar índices e revisão de performance dos filtros", "P1", "Performance", "Api", "Banco", "Adicionar índices coerentes para status, carrier, UF, cliente, datas, NF e criticidade.", "Filtros e agregações podem degradar com volume.", "TASK-14, TASK-15.", "Após queries finais.", 5, "Red: teste/plano de query exige índices; Green: migration de índices; Refactor: revisar consultas.", ("Dado que há volume de entregas", "Quando filtros comuns são executados", "Então consultas usam índices previstos."), "Índices excessivos aumentam custo de escrita.", "Criar apenas índices dos filtros do MVP.", "Migration e documentação de performance."),
    Task("TASK-21", SPRINTS[3].name, "Implementar CRUD de regras de prazo/SLA", "P0", "Feature", "Api/Web", "SLA", "Criar regras por transportadora, região/UF, tipo e prazo com versionamento simples.", "Sem SLA configurável não há atraso confiável.", "TASK-09.", "Primeira tarefa da Sprint 4.", 13, "Red: testes de CRUD e validação de regra; Green: API e UI; Refactor: domain service.", ("Dado que uma regra SLA existe", "Quando uma entrega da UF correspondente é avaliada", "Então o prazo correto é aplicado."), "Regra ambígua.", "Definir precedência explícita: carrier+UF antes de regra geral.", "CRUD testado e documentado."),
    Task("TASK-22", SPRINTS[3].name, "Criar motor de atraso e criticidade", "P0", "Feature", "Api", "Regras de negócio", "Calcular atraso, criticidade e status operacional com base em SLA, datas e status.", "É núcleo do monitoramento logístico.", "TASK-21.", "Antes do painel de exceções.", 13, "Red: testes unitários para normal, atenção, crítico, resolvido e extraviado; Green: motor mínimo; Refactor: separar regras.", ("Dado que uma entrega ultrapassou SLA", "Quando o motor recalcula", "Então atraso e criticidade são atualizados corretamente."), "Cálculo incorreto gera operação errada.", "Cobrir casos de borda, sem data e dados inválidos.", "Testes unitários e job/endpoint de recálculo."),
    Task("TASK-23", SPRINTS[3].name, "Criar painel de exceções priorizado", "P0", "Feature", "Api/Web", "Exceções", "Listar entregas críticas, atrasadas, sem atualização ou extraviadas com prioridade.", "Escopo prioriza ação humana em exceções.", "TASK-22.", "Após motor de atraso.", 13, "Red: testes de endpoint e tela filtrando apenas exceções; Green: API/UI; Refactor: componente de fila.", ("Dado que há entregas críticas", "Quando o usuário abre o painel", "Então apenas casos que exigem ação aparecem priorizados."), "Ruído operacional.", "Ranking por criticidade, dias de atraso e valor.", "Tela, endpoint e UAT."),
    Task("TASK-24", SPRINTS[3].name, "Criar registro de tratativas por entrega", "P0", "Feature", "Api/Web", "Tratativas", "Permitir registrar ação, observação, responsável, próximo status e data.", "Tratativas documentam acompanhamento humano.", "TASK-16, TASK-23.", "Após detalhe e exceções.", 8, "Red: testes de criação/listagem/autorização; Green: entidade, endpoint e UI; Refactor: audit hook.", ("Dado que uma entrega está crítica", "Quando a logística registra tratativa", "Então o histórico mostra ação, usuário e data."), "Comentários sensíveis.", "Validar permissão e sanitizar conteúdo.", "Histórico visível no detalhe e testes."),
    Task("TASK-25", SPRINTS[4].name, "Gerar relatório diário matinal", "P0", "Feature", "Api/Web", "Relatórios", "Gerar relatório diário com atrasos, críticos, falhas de coleta e ações pendentes.", "É entrega essencial do escopo original.", "TASK-23, TASK-24.", "Primeira tarefa da Sprint 5.", 13, "Red: testes de geração com base de exceções; Green: endpoint e tela; Refactor: template renderer.", ("Dado que existem exceções no dia", "Quando o relatório é gerado", "Então ele lista prioridades, responsáveis e métricas principais."), "Relatório incompleto ou divergente.", "Usar mesma fonte do painel de exceções.", "PDF/HTML interno ou tela validada e testes."),
    Task("TASK-26", SPRINTS[4].name, "Criar alertas por dashboard e e-mail", "P1", "Feature", "Api/Web/Infra", "Alertas", "Configurar alertas de atraso crítico, falha de coleta e relatório diário por e-mail/dashboard.", "Notificação reduz risco de atraso não percebido.", "TASK-25.", "Após relatório diário.", 8, "Red: testes de regra de alerta e falha de SMTP; Green: adapter de e-mail e UI; Refactor: fila de notificação.", ("Dado que há entrega crítica nova", "Quando o job de alertas executa", "Então alerta é registrado e enviado quando SMTP está configurado."), "Falha de SMTP ou spam.", "Retry, logs e fallback para dashboard.", "Log de envio e teste de erro."),
    Task("TASK-27", SPRINTS[4].name, "Criar interface padrão de conectores", "P1", "Architecture", "Integrations/Api", "Integrações", "Definir contrato para API de transportadora com fetch status, fetch quote, health e normalize.", "Evita acoplamento por transportadora.", "TASK-26.", "Antes de Braspress/cotação.", 8, "Red: testes de contrato para conector fake; Green: interface e adapter base; Refactor: separar mappers.", ("Dado que um conector implementa contrato", "Quando é executado em teste", "Então retorna payload normalizado ou erro padronizado."), "Excesso de abstração.", "Criar apenas métodos usados no MVP.", "Contrato e teste fake connector."),
    Task("TASK-28", SPRINTS[4].name, "Persistir logs operacionais e auditoria inicial", "P0", "Security", "Api/Web", "Logs/Auditoria", "Registrar importações, coletas, relatórios, tratativas, alterações de regra e falhas.", "Escopo exige logs e auditoria.", "TASK-24, TASK-26.", "Após eventos principais.", 13, "Red: testes exigem audit_event por ação crítica; Green: modelo e hook; Refactor: serviço central.", ("Dado que uma regra SLA é alterada", "Quando a alteração é salva", "Então auditoria registra usuário, data, antes e depois."), "Crescimento de log e dados sensíveis.", "Mascarar valores sensíveis e paginar auditoria.", "Tela/endpoint de auditoria e testes."),
    Task("TASK-29", SPRINTS[5].name, "Documentar e implementar fluxo Braspress assistido", "P0", "Feature", "Docs/Integrations/Api/Web", "Braspress", "Criar template, mapeador e instrução de importação assistida por planilha exportada.", "Apêndice recomenda esta abordagem inicial.", "TASK-10, TASK-27.", "Primeira tarefa da Sprint 6.", 8, "Red: teste de parser Braspress com fixture; Green: mapper para contrato único; Refactor: separar colunas por versão.", ("Dado que o arquivo Braspress segue template", "Quando é importado", "Então campos são normalizados para entregas monitoradas."), "Portal muda colunas ou limita período.", "Versionar templates e validar colunas com mensagem clara.", "Fixture, playbook e teste de importação."),
    Task("TASK-30", SPRINTS[5].name, "Criar tela de status de integrações/coletas", "P1", "Feature", "Api/Web/Integrations", "Integrações", "Exibir última coleta, origem, status, erro e próxima ação por transportadora.", "Operação precisa saber se dados externos falharam.", "TASK-28, TASK-29.", "Após logs de coleta.", 8, "Red: testes de status por conector; Green: endpoint/tela; Refactor: componente de status.", ("Dado que uma coleta falhou", "Quando o usuário abre integrações", "Então vê erro, horário e orientação operacional."), "Mensagem técnica demais para operador.", "Separar detalhe técnico de mensagem operacional.", "Tela validada e logs demonstrados."),
    Task("TASK-31", SPRINTS[5].name, "Criar jobs agendados de coleta e recálculo", "P1", "Infra", "Api/Infra/Integrations", "Jobs", "Planejar e implementar jobs mínimos para coleta assistida/recálculo de atraso/geração de relatório.", "Fluxos recorrentes são parte do escopo.", "TASK-22, TASK-25, TASK-27.", "Após conectores e relatórios.", 13, "Red: testes de job idempotente; Green: scheduler simples; Refactor: adapter para Celery/RQ futuro.", ("Dado que o job de recálculo roda duas vezes", "Quando não há alteração de dados", "Então o resultado permanece idempotente."), "Jobs duplicados ou concorrentes.", "Lock simples e idempotência por período.", "Logs de job e testes."),
    Task("TASK-32", SPRINTS[5].name, "Criar playbook operacional de falhas", "P1", "Documentation", "Docs/Infra", "Operação", "Documentar falha de importação, falha de coleta, relatório não enviado, rollback e suporte.", "Time precisa operar sem depender do desenvolvedor.", "TASK-30, TASK-31.", "Fim da Sprint 6.", 5, "Teste de documentação: cada falha crítica tem diagnóstico, ação e evidência.", ("Dado que uma coleta falha", "Quando o operador consulta o playbook", "Então encontra causa provável, logs e próximo passo."), "Playbook ficar desatualizado.", "Vincular a telas/logs reais e revisar em UAT.", "Playbook versionado."),
    Task("TASK-33", SPRINTS[6].name, "Criar importador de pedidos do ERP por planilha", "P0", "Feature", "Api/Web/Integrations", "Cotação/Pedidos", "Importar pedidos novos com número, cliente, UF, destino, valor e metadados mínimos.", "Cotação no roadmap principal depende de pedidos.", "TASK-27.", "Primeira tarefa da Sprint 7.", 13, "Red: testes de CSV/XLSX de pedidos e campos obrigatórios; Green: parser e tela; Refactor: contrato ERP.", ("Dado que um arquivo de pedidos é enviado", "Quando a importação é confirmada", "Então pedidos aparecem na aba de cotação."), "Campos ERP não confirmados.", "Começar por planilha MVP e documentar contrato.", "Pedidos persistidos e tela com histórico."),
    Task("TASK-34", SPRINTS[6].name, "Criar modelo e API de cotações de frete", "P0", "Feature", "Api", "Cotação", "Criar freight_quotes por pedido/transportadora com valor, status, mensagem, validade e histórico.", "Necessário para comparar transportadoras.", "TASK-33.", "Após pedidos.", 13, "Red: testes de criação/listagem/status de cotação; Green: modelo/API; Refactor: serviço de cotação.", ("Dado que um pedido possui transportadoras habilitadas", "Quando cotações são registradas", "Então cada transportadora tem status e valor auditável."), "Dados manuais divergentes.", "Auditoria e validação monetária.", "Endpoints e testes de contrato."),
    Task("TASK-35", SPRINTS[6].name, "Criar motor comparativo e ranking de melhor frete", "P0", "Feature", "Api/Web", "Cotação", "Comparar valores por transportadora e destacar melhor opção por menor preço com regra configurável preparada.", "Critério explícito da subaba.", "TASK-34.", "Após API de cotações.", 8, "Red: testes para menor preço, indisponível, empate e erro; Green: ranking; Refactor: strategy de regra.", ("Dado que há quatro cotações válidas", "Quando o ranking é calculado", "Então a menor cotação válida é destacada como melhor opção."), "Preço menor nem sempre melhor prazo.", "MVP usa preço; regra futura considera prazo/eficiência.", "Ranking testado e documentado."),
    Task("TASK-36", SPRINTS[6].name, "Criar subaba Cotação de Frete por Pedido", "P0", "Feature", "Web", "Cotação", "Implementar tabela comparativa com pedidos, transportadoras A/B/C/D, melhor opção, status e histórico.", "Usuário decidiu incluir cotação no roadmap principal.", "TASK-33, TASK-34, TASK-35.", "Após motor comparativo.", 13, "Red: testes de componente para tabela e destaque; Green: UI integrada; Refactor: componentes de cotação.", ("Dado que pedidos importados têm cotações", "Quando o usuário abre a subaba", "Então valores por transportadora e melhor opção aparecem."), "Tela complexa e dependência de API.", "Entregar MVP assistido com estados vazio/erro/loading.", "Tela validada por UAT e testes."),
    Task("TASK-37", SPRINTS[7].name, "Preparar ambiente de homologação e deploy", "P0", "DevOps", "Infra/Api/Web", "Deploy", "Configurar ambiente com Docker/CI, variáveis, secrets, banco, web e API.", "Entrega final exige homologação.", "TASK-31, TASK-36.", "Primeira tarefa da Sprint 8.", 13, "Red: checklist falha sem env/secrets/build; Green: ambiente sobe; Refactor: scripts reproduzíveis.", ("Dado que o deploy de homologação é executado", "Quando healthchecks rodam", "Então API, Web e banco ficam acessíveis."), "Secrets ou ambiente incompleto.", "Usar placeholders no repo e secrets no ambiente.", "URL de homologação, healthcheck e logs."),
    Task("TASK-38", SPRINTS[7].name, "Executar regressão E2E dos fluxos críticos", "P0", "QA", "Todos", "Fluxos críticos", "QA/E2E", "QA de login, transportadoras, importação, entregas, eficiência, exceções, relatório, Braspress e cotação.", "Projeto só pode ser concluído com evidência de regressão.", "TASK-37.", "Após deploy/homologação.", 13, "Red: cenários E2E falham antes do fluxo completo; Green: corrigir integração; Refactor: suíte organizada.", ("Dado que o ambiente está em homologação", "Quando a suíte crítica executa", "Então os fluxos principais passam sem regressão."), "Flakiness e dados inconsistentes.", "Fixtures controladas e reset de ambiente.", "Relatório QA, prints e pipeline verde."),
    Task("TASK-39", SPRINTS[7].name, "Executar hardening de segurança, LGPD e observabilidade", "P0", "Security", "Api/Web/Infra", "Segurança", "Validar autorização, dados sensíveis, logs mascarados, headers, erros e auditoria.", "Requisito de segurança e compliance do escopo.", "TASK-28, TASK-37.", "Antes do go-live.", 8, "Red: testes de acesso indevido e dados sensíveis; Green: hardening; Refactor: checklist automatizado.", ("Dado que um usuário sem permissão tenta acessar dado restrito", "Quando faz requisição direta", "Então a API bloqueia e registra evento sem vazar dado sensível."), "Falso senso de segurança.", "Checklist manual + testes automatizados + revisão de diff.", "Relatório de segurança e testes."),
    Task("TASK-40", SPRINTS[7].name, "Consolidar documentação final, treinamento e aceite", "P0", "Documentation", "Docs", "Entrega Final", "Entregar manual, guia técnico, plano de rollback, checklist de produção, matriz de riscos e aceite final.", "Cliente/liderança precisam de pacote final.", "TASK-38, TASK-39.", "Última tarefa.", 8, "Teste de documentação: checklist final cobre instalação, operação, suporte e rollback.", ("Dado que o projeto é entregue", "Quando o cliente consulta a documentação", "Então consegue operar, validar e acionar suporte."), "Documentação não refletir sistema real.", "Revisar contra ambiente homologado e evidências QA.", "Pacote final com PDFs, links, evidências e aceite."),
]


DEPENDENCIES = [
    ["Web", "Api", "Auth, carriers, shipments, imports, exceptions, reports, quotes", "Contrato HTTP + token JWT", "TASK-07, TASK-13, TASK-36", "Mudança de payload quebra telas.", "Versionar contratos e testes de integração."],
    ["Api", "Infra", "Banco, env, jobs, deploy", "Variáveis, PostgreSQL, CI/CD", "TASK-05, TASK-37", "Ambiente não reproduzível.", "Docker Compose e env examples validados."],
    ["Api", "Docs", "Regras de negócio e contratos", "Documentação funcional", "TASK-01, TASK-21, TASK-34", "Regras implementadas sem aceite.", "Rastreio Docs -> issue -> PR."],
    ["Integrations", "Api", "Braspress e conectores", "Payload normalizado", "TASK-27, TASK-29", "Conector incompatível com importação.", "Contrato fake connector e fixtures."],
    ["Web", "Integrations", "Status de coletas e cotação", "Dados via Api", "TASK-30, TASK-36", "UI depender de detalhes externos.", "Web só consome API interna normalizada."],
    [".github", "Todos", "Templates, PRs e CI", "Governança", "TASK-03, TASK-05", "PR sem evidência TDD.", "Templates obrigatórios e checks."],
    ["Docs", "Todos", "UAT, riscos e entrega", "Evidências", "TASK-19, TASK-40", "Aceite sem rastreabilidade.", "Checklist por sprint e pacote final."],
]


RISKS = [
    ["R-01", "Dois fluxos de importação divergentes", "Alto", "Alta", "Crítica", "Unificar contrato e testes", "Sprint 1/2", "TASK-04, TASK-10"],
    ["R-02", "Campos fiscais/financeiros parcialmente modelados", "Alto", "Média", "Alta", "Migration canônica em shipments", "Sprint 2", "TASK-12"],
    ["R-03", "SLA não validado pela operação", "Alto", "Média", "Alta", "UAT com regras por transportadora/UF", "Sprint 4", "TASK-21, TASK-22"],
    ["R-04", "Cotação depende de dados de ERP/transportadoras", "Alto", "Alta", "Crítica", "MVP por planilha + contrato documentado", "Sprint 7", "TASK-33 a TASK-36"],
    ["R-05", "Credenciais de transportadoras expostas", "Alto", "Baixa", "Crítica", "Secrets fora do repo e criptografia/mascaramento", "Sprint 5/8", "TASK-27, TASK-39"],
    ["R-06", "Deploy/homologação sem pipeline completo", "Alto", "Média", "Alta", "CI/CD e checklist de homologação", "Sprint 8", "TASK-37"],
    ["R-07", "Baixa cobertura E2E", "Médio", "Alta", "Alta", "Suíte crítica e evidências UAT", "Sprint 8", "TASK-38"],
    ["R-08", "Performance ruim em filtros/agregações", "Médio", "Média", "Média", "Índices e teste de volume mínimo", "Sprint 3", "TASK-20"],
    ["R-09", "Ausência de auditoria completa", "Alto", "Média", "Alta", "Audit events para ações críticas", "Sprint 5/8", "TASK-28, TASK-39"],
    ["R-10", "Scraping/bots instáveis", "Médio", "Alta", "Alta", "Priorizar importação assistida e API oficial", "Sprint 6", "TASK-29, TASK-30"],
    ["R-11", "Documentação desatualizada", "Médio", "Média", "Média", "Rastreio e revisão a cada sprint", "Todas", "TASK-01, TASK-40"],
    ["R-12", "Capacidade semanal insuficiente", "Alto", "Média", "Alta", "Mais de um dev ou redução controlada de escopo", "Sprint 2/7/8", "Todas P0"],
]


FUTURE_BACKLOG = [
    "Aplicativo mobile para notificações e conferência em campo.",
    "Integração automatizada com todas as transportadoras do mercado.",
    "Bots avançados para portais com captcha ou mudanças frequentes.",
    "BI avançado com data warehouse e analytics preditivo.",
    "Machine learning para previsão de atraso.",
    "WhatsApp automático e integrações Teams/Slack além do e-mail/dashboard.",
    "Roteirização de entregas e controle de frota própria.",
    "Integração profunda com módulo de crédito Ilex, financeiro e ERP completo.",
    "Internacionalização e multiempresa avançado para SaaS amplo.",
    "Performance avançada com carga massiva e particionamento de tabelas.",
]


ASSUMPTIONS = [
    "O roadmap principal começa em 18/05/2026 e termina em 10/07/2026, conforme solicitação atual.",
    "Cotação de Frete por Pedido é tratada como escopo principal, apesar do apêndice classificá-la como fase 2/módulo adicional.",
    "Os repositórios oficiais analisados são Api, Web, Infra, Integrations, Docs e .github da organização ilex-logistica.",
    "A nomenclatura ilex-logistics-* do PDF original foi reconciliada com os repositórios reais existentes.",
    "Quando uma funcionalidade não foi encontrada no código, o documento a classifica como PENDENTE ou NÃO IDENTIFICADO, sem inventar implementação.",
    "Não foram lidos arquivos sensíveis como .env, chaves, certificados ou credenciais.",
    "A capacidade por sprint considera time mínimo com pelo menos um fullstack, apoio de QA, Tech Lead e DevOps parcial; sprints de alta carga podem exigir mais pessoas.",
]


def task_tests(task: Task) -> str:
    technical = task.kind not in {"Documentation"}
    if not technical:
        return task.tests
    return (
        "Red: criar teste falhando antes da implementação. "
        "Green: implementar o mínimo para passar. "
        "Refactor: melhorar sem quebrar a suíte. "
        f"Testes obrigatórios: {task.tests}."
    )


def task_dod(task: Task) -> str:
    return (
        "Testes automatizados criados/atualizados; critérios de aceite validados; "
        "sem regressão conhecida; código revisável por PR; evidência anexada; "
        "logs/tratamento de erro aplicados quando houver fluxo operacional."
    )


def render_task(task: Task) -> list:
    rows = [
        ["ID da tarefa:", task.id],
        ["Sprint:", task.sprint],
        ["Prioridade:", task.priority],
        ["Tipo:", task.kind],
        ["Repositório responsável:", task.repo],
        ["Página/Tela/Área impactada:", task.area],
        ["Função/Módulo:", task.module],
        ["Descrição da entrega:", task.description],
        ["Justificativa:", task.justification],
        ["Dependências:", task.dependencies],
        ["Ordem de execução:", task.order],
        ["Story points:", str(task.points)],
        ["Estratégia TDD:", task_tests(task)],
        ["Testes obrigatórios:", task.tests],
        ["Definition of Done:", task_dod(task)],
        ["Critérios de aceite testáveis:", f"- Dado que {task.acceptance[0].removeprefix('Dado que ')}<br/>- Quando {task.acceptance[1].removeprefix('Quando ')}<br/>- Então {task.acceptance[2].removeprefix('Então ')}"],
        ["Riscos:", task.risks],
        ["Mitigação:", task.mitigation],
        ["Evidência esperada:", task.evidence],
    ]
    return [
        p(f"{task.id} - {task.title}", "h3"),
        table(rows, widths=[4.0 * cm, 12.5 * cm], header=False),
        Spacer(1, 0.16 * cm),
    ]


def sprint_task_stats(sprint_name: str) -> tuple[int, int]:
    sprint_tasks = [task for task in TASKS if task.sprint == sprint_name]
    return len(sprint_tasks), sum(task.points for task in sprint_tasks)


class RoadmapDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style_name = flowable.style.name
            if style_name == "Heading1":
                self.notify("TOCEntry", (0, text, self.page))
            elif style_name == "Heading2":
                self.notify("TOCEntry", (1, text, self.page))


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = PAGE_SIZE
    canvas.setFillColor(colors.HexColor("#050505"))
    canvas.rect(0, height - 1.15 * cm, width, 1.15 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(1.4 * cm, height - 0.72 * cm, "Ilex Logística - Roadmap Scrum + TDD")
    canvas.setFont("Helvetica", 7)
    canvas.drawRightString(width - 1.4 * cm, height - 0.72 * cm, f"Versão {VERSION} | Gerado em {GENERATED_AT}")
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.setFont("Helvetica", 7)
    canvas.drawString(1.4 * cm, 0.75 * cm, "DB Tecnologia | Documento técnico e executivo")
    canvas.drawRightString(width - 1.4 * cm, 0.75 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build_story() -> list:
    total_tasks = len(TASKS)
    total_points = sum(task.points for task in TASKS)
    story = []

    story += [
        Spacer(1, 2.0 * cm),
        p("Roadmap Scrum + TDD para Conclusão do Projeto", "cover_title"),
        p("Ilex Logística", "cover_title"),
        Spacer(1, 0.4 * cm),
        p(f"Organização GitHub: {ORG}", "cover_subtitle"),
        p(f"Repositórios analisados: {', '.join(REPOS)}", "cover_subtitle"),
        p(f"Período inicial do planejamento: {PERIOD_START} a {PERIOD_END}", "cover_subtitle"),
        p(f"Data de geração: {GENERATED_AT} | Versão: {VERSION}", "cover_subtitle"),
        Spacer(1, 1.1 * cm),
        table(
            [
                ["Indicador", "Valor"],
                ["Total de sprints planejadas", str(len(SPRINTS))],
                ["Total de tarefas planejadas", str(total_tasks)],
                ["Total estimado de story points", str(total_points)],
                ["Estimativa geral de duração", f"{PERIOD_START} a {PERIOD_END}"],
                ["Abordagem de qualidade", "TDD obrigatório em todas as tarefas técnicas"],
            ],
            widths=[7 * cm, 8 * cm],
        ),
        PageBreak(),
        section("Sumário"),
    ]
    toc = TableOfContents()
    toc.levelStyles = [S["toc"], ParagraphStyle("TOC2", parent=S["toc"], leftIndent=22, fontSize=8)]
    story += [toc, PageBreak()]

    story += [
        section("1. Resumo Executivo"),
        p(
            "O projeto Ilex Logística possui uma fundação técnica funcional em Api, Web, Infra, Integrations e Docs, "
            "com autenticação, RBAC inicial, cadastro de transportadoras, importações parciais, envios monitorados "
            "e documentação Scrum já iniciados. A análise do escopo original e do Apêndice 1 mostra que ainda faltam "
            "módulos centrais para concluir 100% do objetivo: dashboard real, detalhe de entrega, regras SLA, painel "
            "de exceções, tratativas, relatório diário, alertas, auditoria, eficiência por transportadora, Braspress "
            "assistida, cotação de frete por pedido, deploy de homologação e pacote final de QA."
        ),
        p(
            f"Este roadmap planeja {len(SPRINTS)} sprints semanais, {total_tasks} tarefas e {total_points} story points "
            f"entre {PERIOD_START} e {PERIOD_END}. A execução deve priorizar P0, caminho crítico cross-repo e TDD. "
            "A capacidade estimada exige atenção especial nas sprints 2, 7 e 8, que concentram integrações, cotação e entrega final."
        ),
        table(
            [
                ["Métrica", "Resultado"],
                ["Estado geral", "PARCIAL - fundação pronta, escopo operacional ainda incompleto"],
                ["Sprints planejadas", len(SPRINTS)],
                ["Tarefas planejadas", total_tasks],
                ["Story points", total_points],
                ["Principais riscos", "Importação divergente, SLA pendente, cotação dependente de ERP, deploy e segurança"],
                ["Resultado esperado", "MVP avançado homologado, com fluxos críticos testados e documentação final"],
            ],
            widths=[5 * cm, 11.5 * cm],
        ),
        section("2. Diagnóstico Técnico"),
        table([["Área", "Status", "Evidência encontrada", "Risco", "Recomendação"], *DIAGNOSIS], widths=[2.6 * cm, 2.1 * cm, 4.2 * cm, 3.8 * cm, 3.8 * cm]),
        section("3. Mapeamento Funcional"),
        section("3.1 Módulos", 2),
        table([["Módulo", "Repo", "Status", "Existente", "Faltante", "Dependências", "Riscos", "Tarefas"], *MODULES], widths=[2.7 * cm, 1.8 * cm, 1.6 * cm, 3.0 * cm, 3.0 * cm, 2.6 * cm, 2.8 * cm, 2.0 * cm]),
        section("3.2 Páginas, Telas e Fluxos", 2),
        table([["Tela", "Repo", "Status", "Classificação", "Existente", "Faltante", "APIs/serviços", "Risco", "Tarefas"], *SCREENS], widths=[2.6 * cm, 1.5 * cm, 1.5 * cm, 2.3 * cm, 2.7 * cm, 3.0 * cm, 2.7 * cm, 2.3 * cm, 1.8 * cm]),
        section("3.3 APIs e Endpoints", 2),
        table([["Método", "Endpoint", "Módulo", "Status", "Payload", "Retorno", "Dependências", "Validações", "Testes", "Riscos/Melhorias"], *API_ENDPOINTS], widths=[1.2 * cm, 3.1 * cm, 1.8 * cm, 1.8 * cm, 2.1 * cm, 2.1 * cm, 2.2 * cm, 2.2 * cm, 2.2 * cm, 2.6 * cm]),
        section("3.4 Banco de Dados", 2),
        table([["Entidade", "Relacionamentos", "Status", "Campos críticos", "Índices", "Seeds", "Pendências/Riscos"], *DATABASE], widths=[2.6 * cm, 2.5 * cm, 1.8 * cm, 4.4 * cm, 2.4 * cm, 2.2 * cm, 4.0 * cm]),
        section("3.5 Integrações", 2),
        table([["Integração", "Repo", "Status", "Configurações", "Variáveis/Dependências", "Riscos", "Testes", "Tarefas"], *INTEGRATIONS], widths=[3.0 * cm, 2.4 * cm, 1.7 * cm, 3.1 * cm, 3.1 * cm, 3.0 * cm, 2.1 * cm, 1.8 * cm]),
        section("4. Roadmap Geral"),
        table(
            [["Sprint", "Período", "Objetivo", "Tarefas", "SP", "Principais entregáveis", "Dependências"]] + [
                [s.name, s.period, s.objective, sprint_task_stats(s.name)[0], sprint_task_stats(s.name)[1], s.deliverables, s.dependencies]
                for s in SPRINTS
            ],
            widths=[3.5 * cm, 2.3 * cm, 4.1 * cm, 1.2 * cm, 1.0 * cm, 3.3 * cm, 3.1 * cm],
        ),
    ]

    story += [PageBreak(), section("5. Sprints Detalhadas")]
    for sprint in SPRINTS:
        count, points = sprint_task_stats(sprint.name)
        story += [
            section(sprint.name, 2),
            table(
                [
                    ["Período estimado", sprint.period],
                    ["Objetivo", sprint.objective],
                    ["Capacidade estimada", sprint.capacity],
                    ["Perfil recomendado do time", sprint.team],
                    ["Total de tarefas", count],
                    ["Total de story points", points],
                    ["Entregáveis esperados", sprint.deliverables],
                    ["Dependências críticas", sprint.dependencies],
                    ["Critérios de sucesso da sprint", "Tarefas P0 concluídas, testes planejados executados, PRs revisados e evidências anexadas."],
                ],
                widths=[4.0 * cm, 12.5 * cm],
                header=False,
            ),
            Spacer(1, 0.2 * cm),
        ]
        for task in [task for task in TASKS if task.sprint == sprint.name]:
            story += render_task(task)
        story.append(PageBreak())

    story += [
        section("6. Dependências Cross-Repo"),
        table([["Origem", "Destino", "Módulo", "Tipo", "Tarefas", "Risco", "Mitigação"], *DEPENDENCIES], widths=[2.1 * cm, 2.1 * cm, 3.2 * cm, 3.0 * cm, 2.2 * cm, 3.2 * cm, 3.7 * cm]),
        section("7. Estratégia TDD e QA"),
        p("Todas as tarefas técnicas devem seguir Red, Green e Refactor. O teste falhando deve ser criado antes da implementação, a solução deve ser mínima para passar, e a refatoração deve manter a suíte verde."),
        bullet_list(
            [
                "Testes unitários para regras de negócio, validações, ranking, SLA e cálculo financeiro.",
                "Testes de integração para endpoints, banco, importação, relatórios, alertas e auditoria.",
                "Testes de contrato para Web-Api, Integrations-Api e conectores de transportadora.",
                "Testes de componente para telas Next.js, estados de loading, erro, vazio e sucesso.",
                "Testes E2E para login, importação, entregas, exceções, relatório e cotação.",
                "Testes de segurança para autorização, dados sensíveis e acesso indevido.",
                "Testes de performance mínimos para filtros, agregações e importações.",
            ]
        ),
        p("Evidências esperadas: logs de testes, prints/UAT, pipeline verde, PR aprovado, contrato atualizado, tela validada ou endpoint funcionando com payload documentado."),
        section("8. Riscos e Mitigações"),
        table([["ID", "Descrição", "Impacto", "Probabilidade", "Severidade", "Mitigação", "Sprint", "Tarefas"], *RISKS], widths=[1.1 * cm, 4.2 * cm, 1.5 * cm, 1.9 * cm, 1.7 * cm, 4.1 * cm, 2.3 * cm, 2.2 * cm]),
        section("9. Backlog Futuro"),
        section("9.1 Escopo das Sprints Planejadas", 2),
        p("As sprints planejadas cobrem o caminho crítico de conclusão: fundação, importação, campos fiscais, entregas monitoradas, eficiência, SLA, exceções, tratativas, relatórios, alertas, auditoria, Braspress assistida, cotação, QA, segurança, deploy e entrega final."),
        section("9.2 Backlog Futuro", 2),
        bullet_list(FUTURE_BACKLOG),
        section("10. Recomendações Finais"),
        bullet_list(
            [
                "Transformar cada TASK-XX em issue GitHub no repositório responsável, mantendo vínculo com Docs e milestone.",
                "Executar por prioridade P0 antes de P1/P2 e bloquear merge sem evidência TDD.",
                "Criar PRs pequenos por módulo, evitando misturar migrations, UI e documentação sem necessidade.",
                "Manter matriz de rastreio Docs -> Issue -> PR -> Evidência.",
                "Revisar capacidade semanal antes de iniciar sprints com mais de 70 pontos.",
                "Preparar homologação com dados fictícios, seeds controlados e checklist UAT.",
                "Separar secrets reais do repositório e validar rollback antes de produção.",
            ]
        ),
        section("11. Lista Final de Entregáveis"),
        table(
            [
                ["Entregável", "Descrição"],
                ["Arquivo PDF", str(OUTPUT_PDF)],
                ["Nome do arquivo", OUTPUT_PDF.name],
                ["Data de geração", GENERATED_AT],
                ["Sprints", len(SPRINTS)],
                ["Tarefas", total_tasks],
                ["Story points", total_points],
                ["Observações", "Documento gerado com base em evidências locais, PDF de escopo e suposições declaradas."],
            ],
            widths=[4.0 * cm, 12.5 * cm],
        ),
        section("12. Suposições Adotadas"),
        bullet_list(ASSUMPTIONS),
    ]
    return story


def build_pdf() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = RoadmapDocTemplate(
        str(OUTPUT_PDF),
        pagesize=PAGE_SIZE,
        leftMargin=1.35 * cm,
        rightMargin=1.35 * cm,
        topMargin=1.75 * cm,
        bottomMargin=1.35 * cm,
        title="Roadmap Scrum + TDD para Conclusão do Projeto - Ilex Logística",
        author="DB Tecnologia",
        subject="Roadmap Scrum + TDD",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])
    doc.multiBuild(build_story())


if __name__ == "__main__":
    build_pdf()
    print(str(OUTPUT_PDF))
