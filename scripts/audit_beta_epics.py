#!/usr/bin/env python3
"""
Auditoria Funcional Automatizada dos 12 Épicos do Roadmap Beta

Este script inspeciona a estrutura do repositório para identificar,
com evidência técnica, o que já está implementado, o que está parcialmente
implementado e o que ainda falta para cada um dos 12 épicos do roadmap.

NÃO implementa funcionalidades novas. Apenas audita o estado atual.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Configuração
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
API_DIR = PROJECT_ROOT / "apps/api"
WEB_DIR = PROJECT_ROOT / "apps/web"
DOCS_DIR = PROJECT_ROOT / "docs"

# Estados possíveis
STATUS_IMPLEMENTED = "IMPLEMENTADO"
STATUS_PARTIAL = "PARCIAL"
STATUS_ABSENT = "AUSENTE"
STATUS_NOT_APPLICABLE = "NÃO APLICÁVEL"
STATUS_INCONCLUSIVE = "INCONCLUSIVO"


class EpicAudit:
    """Auditoria de um épico específico"""

    def __init__(self, epic_id: str, epic_name: str, criteria: List[str]):
        self.epic_id = epic_id
        self.epic_name = epic_name
        self.criteria = criteria
        self.implemented_items = []
        self.partial_items = []
        self.missing_items = []
        self.evidence_paths = []
        self.test_paths = []
        self.doc_paths = []

    def add_evidence(self, item: str, status: str, path: Optional[str] = None):
        """Adiciona evidência para um item do épico"""
        if status == STATUS_IMPLEMENTED:
            self.implemented_items.append(item)
        elif status == STATUS_PARTIAL:
            self.partial_items.append(item)
        elif status == STATUS_ABSENT:
            self.missing_items.append(item)
        elif status == STATUS_NOT_APPLICABLE:
            pass  # Não adiciona
        elif status == STATUS_INCONCLUSIVE:
            self.partial_items.append(f"{item} (inconclusivo)")

        if path:
            self.evidence_paths.append(path)

    def calculate_status(self) -> str:
        """Calcula o status geral do épico"""
        total = len(self.criteria)
        implemented = len(self.implemented_items)
        partial = len(self.partial_items)
        missing = len(self.missing_items)

        if implemented == total:
            return STATUS_IMPLEMENTED
        elif implemented > 0 or partial > 0:
            return STATUS_PARTIAL
        else:
            return STATUS_ABSENT

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            "epic_id": self.epic_id,
            "epic_name": self.epic_name,
            "status": self.calculate_status(),
            "implemented_items": self.implemented_items,
            "partial_items": self.partial_items,
            "missing_items": self.missing_items,
            "evidence_paths": self.evidence_paths,
            "test_paths": self.test_paths,
            "doc_paths": self.doc_paths,
            "recommended_next_pr": self.get_recommended_pr(),
            "priority": self.get_priority(),
        }

    def get_recommended_pr(self) -> str:
        """Retorna o PR recomendado para este épico"""
        pr_map = {
            "1": "BETA-013",
            "2": "BETA-012",
            "3": "BETA-011",
            "4": "BETA-014",
            "5": "BETA-015",
            "6": "BETA-016",
            "7": "BETA-019",
            "8": "BETA-020",
            "9": "BETA-017",
            "10": "BETA-018",
            "11": "N/A (já implementado)",
            "12": "BETA-021",
        }
        return pr_map.get(self.epic_id, "N/A")

    def get_priority(self) -> str:
        """Retorna a prioridade deste épico"""
        priority_map = {
            "1": "ALTA",
            "2": "ALTA",
            "3": "ALTA",
            "4": "ALTA",
            "5": "MÉDIA",
            "6": "MÉDIA",
            "7": "BAIXA",
            "8": "BAIXA",
            "9": "MÉDIA",
            "10": "BAIXA",
            "11": "N/A",
            "12": "BAIXA",
        }
        return priority_map.get(self.epic_id, "N/A")


def search_in_files(pattern: str, directory: Path, extensions: List[str]) -> List[Path]:
    """Busca padrão em conteúdo de arquivos"""
    results = []
    if not directory.exists():
        return results

    for ext in extensions:
        for file_path in directory.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if pattern.lower() in content.lower():
                    results.append(file_path)
            except:
                pass

    return results
    """Busca padrão em conteúdo de arquivos"""
    results = []
    if not directory.exists():
        return results

    for ext in extensions:
        for file_path in directory.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if pattern.lower() in content.lower():
                    results.append(file_path)
            except:
                pass

    return results


def audit_epic_1_sla() -> EpicAudit:
    """Épico 1 — SLA, atraso e criticidade"""
    epic = EpicAudit(
        "1",
        "SLA, atraso e criticidade",
        [
            "módulo backend sla ou equivalente",
            "model/tabela de regras SLA",
            "endpoint CRUD ou service",
            "cálculo de atraso/criticidade",
            "reprocessamento",
            "auditoria",
            "testes backend",
            "tela/frontend",
            "testes frontend",
            "docs",
        ],
    )

    # Buscar módulo SLA
    sla_files = list(API_DIR.rglob("*sla*"))
    if sla_files:
        epic.add_evidence("módulo backend sla ou equivalente", STATUS_IMPLEMENTED, str(sla_files[0]))
    else:
        epic.add_evidence("módulo backend sla ou equivalente", STATUS_ABSENT)

    # Buscar model/tabela SLA
    sla_models = search_in_files("sla", API_DIR / "models", [".py"])
    if sla_models:
        epic.add_evidence("model/tabela de regras SLA", STATUS_IMPLEMENTED, str(sla_models[0]))
    else:
        epic.add_evidence("model/tabela de regras SLA", STATUS_ABSENT)

    # Buscar endpoint SLA
    sla_routers = search_in_files("sla", API_DIR / "routers", [".py"])
    if sla_routers:
        epic.add_evidence("endpoint CRUD ou service", STATUS_IMPLEMENTED, str(sla_routers[0]))
    else:
        epic.add_evidence("endpoint CRUD ou service", STATUS_ABSENT)

    # Buscar cálculo de atraso/criticidade
    delay_files = search_in_files("delay|atraso|criticidade", API_DIR, [".py"])
    if delay_files:
        epic.add_evidence("cálculo de atraso/criticidade", STATUS_PARTIAL, str(delay_files[0]))
    else:
        epic.add_evidence("cálculo de atraso/criticidade", STATUS_ABSENT)

    # Buscar reprocessamento
    reprocess_files = search_in_files("reprocess|retry", API_DIR, [".py"])
    if reprocess_files:
        epic.add_evidence("reprocessamento", STATUS_PARTIAL, str(reprocess_files[0]))
    else:
        epic.add_evidence("reprocessamento", STATUS_ABSENT)

    # Buscar testes SLA
    sla_tests = search_in_files("sla", API_DIR / "tests", [".py"])
    if sla_tests:
        epic.add_evidence("testes backend", STATUS_IMPLEMENTED, str(sla_tests[0]))
        epic.test_paths.append(str(sla_tests[0]))
    else:
        epic.add_evidence("testes backend", STATUS_ABSENT)

    # Buscar tela SLA frontend
    sla_frontend = search_in_files("sla", WEB_DIR / "app", [".tsx", ".ts"])
    if sla_frontend:
        epic.add_evidence("tela/frontend", STATUS_IMPLEMENTED, str(sla_frontend[0]))
    else:
        epic.add_evidence("tela/frontend", STATUS_ABSENT)

    # Buscar testes frontend SLA
    sla_e2e = search_in_files("sla", WEB_DIR / "e2e", [".spec.ts"])
    if sla_e2e:
        epic.add_evidence("testes frontend", STATUS_IMPLEMENTED, str(sla_e2e[0]))
        epic.test_paths.append(str(sla_e2e[0]))
    else:
        epic.add_evidence("testes frontend", STATUS_ABSENT)

    # Buscar docs SLA
    sla_docs = search_in_files("sla", DOCS_DIR, [".md"])
    if sla_docs:
        epic.add_evidence("docs", STATUS_IMPLEMENTED, str(sla_docs[0]))
        epic.doc_paths.append(str(sla_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_2_importacao() -> EpicAudit:
    """Épico 2 — Importação Excel/CSV robusta e importação assistida"""
    epic = EpicAudit(
        "2",
        "Importação Excel/CSV robusta e importação assistida",
        [
            "parser CSV",
            "parser XLSX",
            "preview",
            "confirmação",
            "validação linha a linha",
            "duplicidade",
            "histórico",
            "layout Braspress",
            "testes backend",
            "tela upload",
            "testes frontend",
            "docs",
        ],
    )

    # Buscar parser CSV
    csv_files = search_in_files("csv|pandas|openpyxl", API_DIR, [".py"])
    if csv_files:
        epic.add_evidence("parser CSV", STATUS_PARTIAL, str(csv_files[0]))
    else:
        epic.add_evidence("parser CSV", STATUS_ABSENT)

    # Buscar parser XLSX
    xlsx_files = search_in_files("xlsx|excel|openpyxl", API_DIR, [".py"])
    if xlsx_files:
        epic.add_evidence("parser XLSX", STATUS_PARTIAL, str(xlsx_files[0]))
    else:
        epic.add_evidence("parser XLSX", STATUS_ABSENT)

    # Buscar preview
    preview_files = search_in_files("preview", API_DIR, [".py"])
    if preview_files:
        epic.add_evidence("preview", STATUS_PARTIAL, str(preview_files[0]))
    else:
        epic.add_evidence("preview", STATUS_ABSENT)

    # Buscar validação linha a linha
    validation_files = search_in_files("validation|validar", API_DIR, [".py"])
    if validation_files:
        epic.add_evidence("validação linha a linha", STATUS_PARTIAL, str(validation_files[0]))
    else:
        epic.add_evidence("validação linha a linha", STATUS_ABSENT)

    # Buscar duplicidade
    duplicate_files = search_in_files("duplicate|duplicidade", API_DIR, [".py"])
    if duplicate_files:
        epic.add_evidence("duplicidade", STATUS_PARTIAL, str(duplicate_files[0]))
    else:
        epic.add_evidence("duplicidade", STATUS_ABSENT)

    # Buscar histórico de importação
    import_history = search_in_files("import_history", API_DIR, [".py"])
    if import_history:
        epic.add_evidence("histórico", STATUS_IMPLEMENTED, str(import_history[0]))
    else:
        epic.add_evidence("histórico", STATUS_ABSENT)

    # Buscar layout Braspress
    braspress_files = search_in_files("braspress", API_DIR, [".py"])
    if braspress_files:
        epic.add_evidence("layout Braspress", STATUS_PARTIAL, str(braspress_files[0]))
    else:
        epic.add_evidence("layout Braspress", STATUS_ABSENT)

    # Buscar testes importação
    import_tests = search_in_files("import", API_DIR / "tests", [".py"])
    if import_tests:
        epic.add_evidence("testes backend", STATUS_PARTIAL, str(import_tests[0]))
        epic.test_paths.append(str(import_tests[0]))
    else:
        epic.add_evidence("testes backend", STATUS_ABSENT)

    # Buscar tela upload frontend
    upload_frontend = search_in_files("upload|import", WEB_DIR / "app", [".tsx", ".ts"])
    if upload_frontend:
        epic.add_evidence("tela upload", STATUS_PARTIAL, str(upload_frontend[0]))
    else:
        epic.add_evidence("tela upload", STATUS_ABSENT)

    # Buscar testes frontend importação
    import_e2e = search_in_files("import", WEB_DIR / "e2e", [".spec.ts"])
    if import_e2e:
        epic.add_evidence("testes frontend", STATUS_IMPLEMENTED, str(import_e2e[0]))
        epic.test_paths.append(str(import_e2e[0]))
    else:
        epic.add_evidence("testes frontend", STATUS_ABSENT)

    # Buscar docs importação
    import_docs = search_in_files("import", DOCS_DIR, [".md"])
    if import_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(import_docs[0]))
        epic.doc_paths.append(str(import_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_3_campos_fiscais() -> EpicAudit:
    """Épico 3 — Campos fiscais, financeiros e filtros do Apêndice 1"""
    epic = EpicAudit(
        "3",
        "Campos fiscais, financeiros e filtros do Apêndice 1",
        [
            "invoice_number",
            "invoice_value",
            "freight_value",
            "freight_percentage",
            "collection_departure_date",
            "customer_name",
            "destination_uf",
            "migration",
            "schemas",
            "filtros backend",
            "busca global",
            "importação atualizada",
            "tabela/detalhe frontend",
            "testes backend",
            "testes frontend",
            "docs",
        ],
    )

    # Campos obrigatórios
    required_fields = [
        "invoice_number",
        "invoice_value",
        "freight_value",
        "freight_percentage",
        "collection_departure_date",
        "customer_name",
        "destination_uf",
    ]

    found_fields = []
    for field in required_fields:
        field_files = search_in_files(field, API_DIR, [".py"])
        if field_files:
            found_fields.append(field)

    if found_fields:
        epic.add_evidence("campos fiscais/financeiros", STATUS_PARTIAL, f"Campos encontrados: {', '.join(found_fields)}")
    else:
        epic.add_evidence("campos fiscais/financeiros", STATUS_ABSENT)

    # Buscar migration
    migration_files = list(API_DIR.rglob("*migration*"))
    if migration_files:
        epic.add_evidence("migration", STATUS_IMPLEMENTED, str(migration_files[0]))
    else:
        epic.add_evidence("migration", STATUS_ABSENT)

    # Buscar schemas
    schema_files = search_in_files("schema|pydantic", API_DIR, [".py"])
    if schema_files:
        epic.add_evidence("schemas", STATUS_IMPLEMENTED, str(schema_files[0]))
    else:
        epic.add_evidence("schemas", STATUS_ABSENT)

    # Buscar filtros backend
    filter_files = search_in_files("filter|filtro", API_DIR, [".py"])
    if filter_files:
        epic.add_evidence("filtros backend", STATUS_PARTIAL, str(filter_files[0]))
    else:
        epic.add_evidence("filtros backend", STATUS_ABSENT)

    # Buscar busca global
    search_files = search_in_files("search|busca", API_DIR, [".py"])
    if search_files:
        epic.add_evidence("busca global", STATUS_PARTIAL, str(search_files[0]))
    else:
        epic.add_evidence("busca global", STATUS_ABSENT)

    # Buscar tabela/detalhe frontend
    table_frontend = search_in_files("table|tabela|detail|detalhe", WEB_DIR / "app", [".tsx", ".ts"])
    if table_frontend:
        epic.add_evidence("tabela/detalhe frontend", STATUS_PARTIAL, str(table_frontend[0]))
    else:
        epic.add_evidence("tabela/detalhe frontend", STATUS_ABSENT)

    # Buscar testes backend
    field_tests = search_in_files("invoice|freight", API_DIR / "tests", [".py"])
    if field_tests:
        epic.add_evidence("testes backend", STATUS_PARTIAL, str(field_tests[0]))
        epic.test_paths.append(str(field_tests[0]))
    else:
        epic.add_evidence("testes backend", STATUS_ABSENT)

    # Buscar testes frontend
    field_e2e = search_in_files("invoice|freight", WEB_DIR / "e2e", [".spec.ts"])
    if field_e2e:
        epic.add_evidence("testes frontend", STATUS_PARTIAL, str(field_e2e[0]))
        epic.test_paths.append(str(field_e2e[0]))
    else:
        epic.add_evidence("testes frontend", STATUS_ABSENT)

    # Buscar docs campos
    field_docs = search_in_files("invoice|freight|fiscal", DOCS_DIR, [".md"])
    if field_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(field_docs[0]))
        epic.doc_paths.append(str(field_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_4_eficiencia() -> EpicAudit:
    """Épico 4 — Eficiência por transportadora"""
    epic = EpicAudit(
        "4",
        "Eficiência por transportadora",
        [
            "endpoint ou service de agregação",
            "total de NFs",
            "entregas no prazo/atrasadas/extraviadas",
            "percentuais",
            "frete total",
            "ranking",
            "filtros",
            "componente frontend",
            "testes",
            "docs",
        ],
    )

    # Buscar agregação/eficiência
    efficiency_files = search_in_files("efficiency|eficiencia|aggregation|agregacao", API_DIR, [".py"])
    if efficiency_files:
        epic.add_evidence("endpoint ou service de agregação", STATUS_PARTIAL, str(efficiency_files[0]))
    else:
        epic.add_evidence("endpoint ou service de agregação", STATUS_ABSENT)

    # Buscar entregas prazo/atrasadas
    delivery_files = search_in_files("delivery|entrega|atraso", API_DIR, [".py"])
    if delivery_files:
        epic.add_evidence("entregas no prazo/atrasadas/extraviadas", STATUS_PARTIAL, str(delivery_files[0]))
    else:
        epic.add_evidence("entregas no prazo/atrasadas/extraviadas", STATUS_ABSENT)

    # Buscar ranking
    ranking_files = search_in_files("ranking|percentual", API_DIR, [".py"])
    if ranking_files:
        epic.add_evidence("ranking/percentuais", STATUS_PARTIAL, str(ranking_files[0]))
    else:
        epic.add_evidence("ranking/percentuais", STATUS_ABSENT)

    # Buscar componente frontend
    efficiency_frontend = search_in_files("efficiency|eficiencia|ranking", WEB_DIR / "app", [".tsx", ".ts"])
    if efficiency_frontend:
        epic.add_evidence("componente frontend", STATUS_PARTIAL, str(efficiency_frontend[0]))
    else:
        epic.add_evidence("componente frontend", STATUS_ABSENT)

    # Buscar testes
    efficiency_tests = search_in_files("efficiency|eficiencia|ranking", API_DIR / "tests", [".py"])
    if efficiency_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(efficiency_tests[0]))
        epic.test_paths.append(str(efficiency_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs
    efficiency_docs = search_in_files("efficiency|eficiencia|ranking", DOCS_DIR, [".md"])
    if efficiency_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(efficiency_docs[0]))
        epic.doc_paths.append(str(efficiency_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_5_alertas() -> EpicAudit:
    """Épico 5 — Alertas e notificações"""
    epic = EpicAudit(
        "5",
        "Alertas e notificações",
        [
            "model Alert",
            "AlertDeliveryLog",
            "geração para crítico/sem atualização/falha",
            "deduplicação",
            "marcar lido/resolvido",
            "e-mail mockável",
            "logs",
            "painel/badge frontend",
            "testes",
            "docs",
        ],
    )

    # Buscar model Alert
    alert_files = search_in_files("alert", API_DIR, [".py"])
    if alert_files:
        epic.add_evidence("model Alert", STATUS_PARTIAL, str(alert_files[0]))
    else:
        epic.add_evidence("model Alert", STATUS_ABSENT)

    # Buscar AlertDeliveryLog
    alert_log_files = search_in_files("alert.*log|AlertDeliveryLog", API_DIR, [".py"])
    if alert_log_files:
        epic.add_evidence("AlertDeliveryLog", STATUS_PARTIAL, str(alert_log_files[0]))
    else:
        epic.add_evidence("AlertDeliveryLog", STATUS_ABSENT)

    # Buscar geração de alertas
    alert_generation = search_in_files("generate.*alert|criar.*alert", API_DIR, [".py"])
    if alert_generation:
        epic.add_evidence("geração para crítico/sem atualização/falha", STATUS_PARTIAL, str(alert_generation[0]))
    else:
        epic.add_evidence("geração para crítico/sem atualização/falha", STATUS_ABSENT)

    # Buscar deduplicação
    dedup_files = search_in_files("dedup|duplicate", API_DIR, [".py"])
    if dedup_files:
        epic.add_evidence("deduplicação", STATUS_PARTIAL, str(dedup_files[0]))
    else:
        epic.add_evidence("deduplicação", STATUS_ABSENT)

    # Buscar painel/badge frontend
    alert_frontend = search_in_files("alert", WEB_DIR / "app", [".tsx", ".ts"])
    if alert_frontend:
        epic.add_evidence("painel/badge frontend", STATUS_PARTIAL, str(alert_frontend[0]))
    else:
        epic.add_evidence("painel/badge frontend", STATUS_ABSENT)

    # Buscar testes
    alert_tests = search_in_files("alert", API_DIR / "tests", [".py"])
    if alert_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(alert_tests[0]))
        epic.test_paths.append(str(alert_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs
    alert_docs = search_in_files("alert", DOCS_DIR, [".md"])
    if alert_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(alert_docs[0]))
        epic.doc_paths.append(str(alert_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_6_relatorio_diario() -> EpicAudit:
    """Épico 6 — Relatório diário automático"""
    epic = EpicAudit(
        "6",
        "Relatório diário automático",
        [
            "DailyReport",
            "DailyReportDelivery",
            "geração manual",
            "geração agendada ou mecanismo compatível",
            "histórico",
            "envio e-mail mockável",
            "export/download",
            "métricas exigidas",
            "tela frontend",
            "testes",
            "docs",
        ],
    )

    # Buscar DailyReport
    daily_report_files = search_in_files("daily.*report|DailyReport", API_DIR, [".py"])
    if daily_report_files:
        epic.add_evidence("DailyReport", STATUS_PARTIAL, str(daily_report_files[0]))
    else:
        epic.add_evidence("DailyReport", STATUS_ABSENT)

    # Buscar DailyReportDelivery
    daily_delivery_files = search_in_files("DailyReportDelivery", API_DIR, [".py"])
    if daily_delivery_files:
        epic.add_evidence("DailyReportDelivery", STATUS_PARTIAL, str(daily_delivery_files[0]))
    else:
        epic.add_evidence("DailyReportDelivery", STATUS_ABSENT)

    # Buscar geração manual
    manual_generation = search_in_files("generate.*report|gerar.*relatorio", API_DIR, [".py"])
    if manual_generation:
        epic.add_evidence("geração manual", STATUS_PARTIAL, str(manual_generation[0]))
    else:
        epic.add_evidence("geração manual", STATUS_ABSENT)

    # Buscar tela frontend
    report_frontend = search_in_files("report|relatorio", WEB_DIR / "app", [".tsx", ".ts"])
    if report_frontend:
        epic.add_evidence("tela frontend", STATUS_PARTIAL, str(report_frontend[0]))
    else:
        epic.add_evidence("tela frontend", STATUS_ABSENT)

    # Buscar testes
    report_tests = search_in_files("report|relatorio", API_DIR / "tests", [".py"])
    if report_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(report_tests[0]))
        epic.test_paths.append(str(report_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs
    report_docs = search_in_files("report|relatorio", DOCS_DIR, [".md"])
    if report_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(report_docs[0]))
        epic.doc_paths.append(str(report_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_7_logs_auditoria() -> EpicAudit:
    """Épico 7 — Logs de coleta, importação e auditoria operacional"""
    epic = EpicAudit(
        "7",
        "Logs de coleta, importação e auditoria operacional",
        [
            "módulo audit",
            "eventos críticos",
            "sanitização de metadados",
            "filtros por período/usuário/tipo",
            "RBAC",
            "collection logs",
            "telas",
            "testes",
            "docs",
        ],
    )

    # Buscar módulo audit
    audit_files = search_in_files("audit", API_DIR, [".py"])
    if audit_files:
        epic.add_evidence("módulo audit", STATUS_PARTIAL, str(audit_files[0]))
    else:
        epic.add_evidence("módulo audit", STATUS_ABSENT)

    # Buscar logs
    log_files = search_in_files("log", API_DIR, [".py"])
    if log_files:
        epic.add_evidence("eventos críticos/collection logs", STATUS_PARTIAL, str(log_files[0]))
    else:
        epic.add_evidence("eventos críticos/collection logs", STATUS_ABSENT)

    # Buscar RBAC
    rbac_files = search_in_files("rbac|permission|role", API_DIR, [".py"])
    if rbac_files:
        epic.add_evidence("RBAC", STATUS_PARTIAL, str(rbac_files[0]))
    else:
        epic.add_evidence("RBAC", STATUS_ABSENT)

    # Buscar testes
    audit_tests = search_in_files("audit|log", API_DIR / "tests", [".py"])
    if audit_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(audit_tests[0]))
        epic.test_paths.append(str(audit_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs
    audit_docs = search_in_files("audit|log", DOCS_DIR, [".md"])
    if audit_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(audit_docs[0]))
        epic.doc_paths.append(str(audit_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_8_integracoes() -> EpicAudit:
    """Épico 8 — Integrações assistidas e conectores preparados"""
    epic = EpicAudit(
        "8",
        "Integrações assistidas e conectores preparados",
        [
            "contrato base de conector",
            "fake connector",
            "parser Braspress",
            "docs Braspress",
            "padrão de erro",
            "logs/retries",
            "sem secrets",
            "testes",
            "docs",
        ],
    )

    # Buscar conectores
    connector_files = search_in_files("connector", API_DIR, [".py"])
    if connector_files:
        epic.add_evidence("contrato base de conector", STATUS_PARTIAL, str(connector_files[0]))
    else:
        epic.add_evidence("contrato base de conector", STATUS_ABSENT)

    # Buscar parser Braspress
    braspress_files = search_in_files("braspress", API_DIR, [".py"])
    if braspress_files:
        epic.add_evidence("parser Braspress", STATUS_PARTIAL, str(braspress_files[0]))
    else:
        epic.add_evidence("parser Braspress", STATUS_ABSENT)

    # Buscar docs Braspress
    braspress_docs = search_in_files("braspress", DOCS_DIR, [".md"])
    if braspress_docs:
        epic.add_evidence("docs Braspress", STATUS_PARTIAL, str(braspress_docs[0]))
        epic.doc_paths.append(str(braspress_docs[0]))
    else:
        epic.add_evidence("docs Braspress", STATUS_ABSENT)

    # Buscar testes
    connector_tests = search_in_files("connector|braspress", API_DIR / "tests", [".py"])
    if connector_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(connector_tests[0]))
        epic.test_paths.append(str(connector_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    return epic


def audit_epic_9_usuarios_permissoes() -> EpicAudit:
    """Épico 9 — Gestão de usuários, permissões e segurança beta"""
    epic = EpicAudit(
        "9",
        "Gestão de usuários, permissões e segurança beta",
        [
            "hash senha",
            "JWT/refresh",
            "logout/revogação",
            "rate limit",
            "bloqueio tentativas inválidas",
            "política senha",
            "CORS/headers",
            "RBAC por endpoint/tela",
            "users CRUD/inativação",
            "testes",
            "docs",
        ],
    )

    # Buscar hash senha
    password_files = search_in_files("password|hash|bcrypt", API_DIR, [".py"])
    if password_files:
        epic.add_evidence("hash senha", STATUS_IMPLEMENTED, str(password_files[0]))
    else:
        epic.add_evidence("hash senha", STATUS_ABSENT)

    # Buscar JWT
    jwt_files = search_in_files("jwt|token", API_DIR, [".py"])
    if jwt_files:
        epic.add_evidence("JWT/refresh", STATUS_IMPLEMENTED, str(jwt_files[0]))
    else:
        epic.add_evidence("JWT/refresh", STATUS_ABSENT)

    # Buscar logout
    logout_files = search_in_files("logout", API_DIR, [".py"])
    if logout_files:
        epic.add_evidence("logout/revogação", STATUS_PARTIAL, str(logout_files[0]))
    else:
        epic.add_evidence("logout/revogação", STATUS_ABSENT)

    # Buscar rate limit
    rate_limit_files = search_in_files("rate.*limit|limiter", API_DIR, [".py"])
    if rate_limit_files:
        epic.add_evidence("rate limit", STATUS_PARTIAL, str(rate_limit_files[0]))
    else:
        epic.add_evidence("rate limit", STATUS_ABSENT)

    # Buscar RBAC
    rbac_files = search_in_files("rbac|permission|role", API_DIR, [".py"])
    if rbac_files:
        epic.add_evidence("RBAC por endpoint/tela", STATUS_PARTIAL, str(rbac_files[0]))
    else:
        epic.add_evidence("RBAC por endpoint/tela", STATUS_ABSENT)

    # Buscar users CRUD
    user_files = search_in_files("user", API_DIR, [".py"])
    if user_files:
        epic.add_evidence("users CRUD/inativação", STATUS_IMPLEMENTED, str(user_files[0]))
    else:
        epic.add_evidence("users CRUD/inativação", STATUS_ABSENT)

    # Buscar testes
    auth_tests = search_in_files("auth|user|password", API_DIR / "tests", [".py"])
    if auth_tests:
        epic.add_evidence("testes", STATUS_PARTIAL, str(auth_tests[0]))
        epic.test_paths.append(str(auth_tests[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs
    auth_docs = search_in_files("auth|user|permission", DOCS_DIR, [".md"])
    if auth_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(auth_docs[0]))
        epic.doc_paths.append(str(auth_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_10_dashboard() -> EpicAudit:
    """Épico 10 — Dashboard beta e UX operacional"""
    epic = EpicAudit(
        "10",
        "Dashboard beta e UX operacional",
        [
            "endpoint dashboard summary",
            "KPIs reais",
            "filtros",
            "alertas ativos",
            "eficiência por transportadora",
            "últimas tratativas",
            "loading/erro/vazio/sucesso",
            "responsividade",
            "testes",
            "docs",
        ],
    )

    # Buscar endpoint dashboard
    dashboard_files = search_in_files("dashboard", API_DIR, [".py"])
    if dashboard_files:
        epic.add_evidence("endpoint dashboard summary", STATUS_PARTIAL, str(dashboard_files[0]))
    else:
        epic.add_evidence("endpoint dashboard summary", STATUS_ABSENT)

    # Buscar tela dashboard frontend
    dashboard_frontend = search_in_files("dashboard", WEB_DIR / "app", [".tsx", ".ts"])
    if dashboard_frontend:
        epic.add_evidence("tela dashboard/KPIs", STATUS_PARTIAL, str(dashboard_frontend[0]))
    else:
        epic.add_evidence("tela dashboard/KPIs", STATUS_ABSENT)

    # Buscar testes E2E dashboard
    dashboard_e2e = search_in_files("dashboard", WEB_DIR / "e2e", [".spec.ts"])
    if dashboard_e2e:
        epic.add_evidence("testes", STATUS_IMPLEMENTED, str(dashboard_e2e[0]))
        epic.test_paths.append(str(dashboard_e2e[0]))
    else:
        epic.add_evidence("testes", STATUS_ABSENT)

    # Buscar docs dashboard
    dashboard_docs = search_in_files("dashboard", DOCS_DIR, [".md"])
    if dashboard_docs:
        epic.add_evidence("docs", STATUS_PARTIAL, str(dashboard_docs[0]))
        epic.doc_paths.append(str(dashboard_docs[0]))
    else:
        epic.add_evidence("docs", STATUS_ABSENT)

    return epic


def audit_epic_11_qa_ci_cd() -> EpicAudit:
    """Épico 11 — QA, CI/CD e validação de beta"""
    epic = EpicAudit(
        "11",
        "QA, CI/CD e validação de beta",
        [
            "CI base",
            "secret scan",
            "migrations validation",
            "docs validation",
            "E2E",
            "coverage",
            "beta_validate",
            "artefatos seguros",
            "rollback",
            "docs",
        ],
    )

    # Buscar CI base
    ci_files = list((PROJECT_ROOT / ".github" / "workflows").rglob("*ci*.yml"))
    if ci_files:
        epic.add_evidence("CI base", STATUS_IMPLEMENTED, str(ci_files[0]))
    else:
        epic.add_evidence("CI base", STATUS_ABSENT)

    # Buscar secret scan
    secret_files = list(SCRIPT_DIR.rglob("check_secrets.py"))
    if secret_files:
        epic.add_evidence("secret scan", STATUS_IMPLEMENTED, str(secret_files[0]))
    else:
        epic.add_evidence("secret scan", STATUS_ABSENT)

    # Buscar migrations validation
    migration_files = list(SCRIPT_DIR.rglob("validate_migrations.py"))
    if migration_files:
        epic.add_evidence("migrations validation", STATUS_IMPLEMENTED, str(migration_files[0]))
    else:
        epic.add_evidence("migrations validation", STATUS_ABSENT)

    # Buscar docs validation
    docs_files = list(SCRIPT_DIR.rglob("validate_docs.py"))
    if docs_files:
        epic.add_evidence("docs validation", STATUS_IMPLEMENTED, str(docs_files[0]))
    else:
        epic.add_evidence("docs validation", STATUS_ABSENT)

    # Buscar beta_validate
    beta_files = list(SCRIPT_DIR.rglob("beta_validate.py"))
    if beta_files:
        epic.add_evidence("beta_validate", STATUS_IMPLEMENTED, str(beta_files[0]))
    else:
        epic.add_evidence("beta_validate", STATUS_ABSENT)

    # Buscar E2E
    e2e_files = list((WEB_DIR / "e2e").rglob("*.spec.ts"))
    if e2e_files:
        epic.add_evidence("E2E", STATUS_IMPLEMENTED, f"{len(e2e_files)} testes E2E")
    else:
        epic.add_evidence("E2E", STATUS_ABSENT)

    # Buscar coverage
    coverage_files = list(API_DIR.rglob("coverage*"))
    if coverage_files:
        epic.add_evidence("coverage", STATUS_IMPLEMENTED, str(coverage_files[0]))
    else:
        epic.add_evidence("coverage", STATUS_ABSENT)

    # Buscar docs rollback
    rollback_docs = search_in_files("rollback", DOCS_DIR, [".md"])
    if rollback_docs:
        epic.add_evidence("rollback/docs", STATUS_IMPLEMENTED, str(rollback_docs[0]))
        epic.doc_paths.append(str(rollback_docs[0]))
    else:
        epic.add_evidence("rollback/docs", STATUS_ABSENT)

    return epic


def audit_epic_12_documentacao() -> EpicAudit:
    """Épico 12 — Documentação beta"""
    epic = EpicAudit(
        "12",
        "Documentação beta",
        [
            "README",
            "API README",
            "Web README",
            "setup local",
            "homologação",
            "rollback",
            "checklist",
            "manual usuário",
            "importação",
            "Braspress",
            "permissões",
            "alertas/relatório",
            "auditoria/logs",
            "roadmap pós-beta",
        ],
    )

    # Buscar README
    readme_files = list(PROJECT_ROOT.rglob("README.md"))
    if readme_files:
        epic.add_evidence("README", STATUS_IMPLEMENTED, str(readme_files[0]))
        epic.doc_paths.append(str(readme_files[0]))
    else:
        epic.add_evidence("README", STATUS_ABSENT)

    # Buscar API README
    api_readme = list(API_DIR.rglob("README.md"))
    if api_readme:
        epic.add_evidence("API README", STATUS_IMPLEMENTED, str(api_readme[0]))
        epic.doc_paths.append(str(api_readme[0]))
    else:
        epic.add_evidence("API README", STATUS_ABSENT)

    # Buscar Web README
    web_readme = list(WEB_DIR.rglob("README.md"))
    if web_readme:
        epic.add_evidence("Web README", STATUS_IMPLEMENTED, str(web_readme[0]))
        epic.doc_paths.append(str(web_readme[0]))
    else:
        epic.add_evidence("Web README", STATUS_ABSENT)

    # Buscar docs beta
    beta_docs = list(DOCS_DIR.rglob("BETA_*.md"))
    if beta_docs:
        epic.add_evidence("documentação beta", STATUS_IMPLEMENTED, f"{len(beta_docs)} documentos beta")
        for doc in beta_docs:
            epic.doc_paths.append(str(doc))
    else:
        epic.add_evidence("documentação beta", STATUS_ABSENT)

    # Buscar checklist
    checklist_docs = list(DOCS_DIR.rglob("*CHECKLIST*.md"))
    if checklist_docs:
        epic.add_evidence("checklist", STATUS_IMPLEMENTED, str(checklist_docs[0]))
        epic.doc_paths.append(str(checklist_docs[0]))
    else:
        epic.add_evidence("checklist", STATUS_ABSENT)

    return epic


def main():
    """Função principal"""
    print("=" * 80)
    print("AUDITORIA FUNCIONAL AUTOMATIZADA DOS 12 ÉPICOS DO ROADMAP BETA")
    print("=" * 80)
    print()

    # Executar auditorias
    epics = [
        audit_epic_1_sla(),
        audit_epic_2_importacao(),
        audit_epic_3_campos_fiscais(),
        audit_epic_4_eficiencia(),
        audit_epic_5_alertas(),
        audit_epic_6_relatorio_diario(),
        audit_epic_7_logs_auditoria(),
        audit_epic_8_integracoes(),
        audit_epic_9_usuarios_permissoes(),
        audit_epic_10_dashboard(),
        audit_epic_11_qa_ci_cd(),
        audit_epic_12_documentacao(),
    ]

    # Imprimir resultados
    for epic in epics:
        print(f"Épico {epic.epic_id}: {epic.epic_name}")
        print(f"Status: {epic.calculate_status()}")
        print(f"Implementados: {len(epic.implemented_items)}")
        print(f"Parciais: {len(epic.partial_items)}")
        print(f"Ausentes: {len(epic.missing_items)}")
        print()

    # Gerar JSON
    json_output = [epic.to_dict() for epic in epics]
    json_path = DOCS_DIR / "BETA_FUNCTIONAL_EPIC_AUDIT.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)

    print(f"JSON gerado: {json_path}")
    print()

    # Resumo
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    implemented_count = sum(1 for epic in epics if epic.calculate_status() == STATUS_IMPLEMENTED)
    partial_count = sum(1 for epic in epics if epic.calculate_status() == STATUS_PARTIAL)
    absent_count = sum(1 for epic in epics if epic.calculate_status() == STATUS_ABSENT)

    print(f"Implementados: {implemented_count}/12")
    print(f"Parciais: {partial_count}/12")
    print(f"Ausentes: {absent_count}/12")
    print()

    print("Esta auditoria NÃO implementou funcionalidades novas.")
    print("Apenas identificou gaps para orientar os próximos PRs funcionais.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
