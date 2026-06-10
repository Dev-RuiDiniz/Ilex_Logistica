"""Audit Log service for BETA-017A."""

from typing import Any

from sqlalchemy.orm import Session

from app.modules.audit.models import OperationalAuditLog
from app.modules.audit.schemas import AuditLogCreateRequest, AuditLogSummaryResponse


class AuditLogService:
    """Service for managing operational audit logs."""

    @staticmethod
    def create_log(
        db: Session,
        log_data: AuditLogCreateRequest,
    ) -> OperationalAuditLog:
        """Create a new audit log entry.

        Args:
            db: Database session
            log_data: Audit log data to create

        Returns:
            Created audit log entry
        """
        log = OperationalAuditLog(**log_data.model_dump())
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_logs(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        event_type: str | None = None,
        entity_type: str | None = None,
        entity_id: int | None = None,
        action: str | None = None,
        actor_user_id: int | None = None,
        severity: str | None = None,
        status: str | None = None,
    ) -> tuple[list[OperationalAuditLog], int]:
        """Get audit logs with optional filters.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            event_type: Filter by event type
            entity_type: Filter by entity type
            entity_id: Filter by entity ID
            action: Filter by action
            actor_user_id: Filter by actor user ID
            severity: Filter by severity
            status: Filter by status

        Returns:
            Tuple of (list of audit logs, total count)
        """
        query = db.query(OperationalAuditLog)

        if event_type:
            query = query.filter(OperationalAuditLog.event_type == event_type)
        if entity_type:
            query = query.filter(OperationalAuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(OperationalAuditLog.entity_id == entity_id)
        if action:
            query = query.filter(OperationalAuditLog.action == action)
        if actor_user_id:
            query = query.filter(OperationalAuditLog.actor_user_id == actor_user_id)
        if severity:
            query = query.filter(OperationalAuditLog.severity == severity)
        if status:
            query = query.filter(OperationalAuditLog.status == status)

        total = query.count()
        logs = query.order_by(OperationalAuditLog.created_at.desc()).offset(skip).limit(limit).all()

        return list(logs), total

    @staticmethod
    def get_log_by_id(db: Session, log_id: int) -> OperationalAuditLog | None:
        """Get a specific audit log by ID.

        Args:
            db: Database session
            log_id: Audit log ID

        Returns:
            Audit log entry or None if not found
        """
        return db.query(OperationalAuditLog).filter(OperationalAuditLog.id == log_id).first()

    @staticmethod
    def get_summary(db: Session) -> AuditLogSummaryResponse:
        """Get audit log summary statistics.

        Args:
            db: Database session

        Returns:
            Audit log summary with statistics
        """
        # Get all logs
        logs = db.query(OperationalAuditLog).all()

        total_logs = len(logs)

        # Count by status
        success_count = sum(1 for log in logs if log.status == "success")
        failed_count = sum(1 for log in logs if log.status == "failed")
        skipped_count = sum(1 for log in logs if log.status == "skipped")

        # Count by severity
        critical_count = sum(1 for log in logs if log.severity == "critical")
        warning_count = sum(1 for log in logs if log.severity == "warning")
        info_count = sum(1 for log in logs if log.severity == "info")

        # Count by action
        create_count = sum(1 for log in logs if log.action == "create")
        update_count = sum(1 for log in logs if log.action == "update")
        delete_count = sum(1 for log in logs if log.action == "delete")
        read_count = sum(1 for log in logs if log.action == "read")

        return AuditLogSummaryResponse(
            total_logs=total_logs,
            success_count=success_count,
            failed_count=failed_count,
            skipped_count=skipped_count,
            critical_count=critical_count,
            warning_count=warning_count,
            info_count=info_count,
            create_count=create_count,
            update_count=update_count,
            delete_count=delete_count,
            read_count=read_count,
        )
