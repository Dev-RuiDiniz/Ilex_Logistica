from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_production_compose_keeps_data_services_private_and_pins_images() -> None:
    content = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    assert "postgres:16.4-alpine" in content
    assert "redis:7.2-alpine" in content
    db_block = content.split("  db:", 1)[1].split("  redis:", 1)[0]
    redis_block = content.split("  redis:", 1)[1].split("  api:", 1)[0]
    assert "ports:" not in db_block
    assert "ports:" not in redis_block
    assert "ilex-postgres-data:" in content
    assert "ilex-redis-data:" in content


def test_continuity_scripts_enforce_backup_checksum_and_healthcheck() -> None:
    scripts = ROOT / "scripts"
    backup = (scripts / "backup_postgres.sh").read_text(encoding="utf-8")
    restore = (scripts / "restore_postgres.sh").read_text(encoding="utf-8")
    deploy = (scripts / "deploy_vps.sh").read_text(encoding="utf-8")
    rollback = (scripts / "rollback_vps.sh").read_text(encoding="utf-8")
    assert "pg_dump" in backup and "sha256sum" in backup and "RETENTION_DAYS" in backup
    assert "sha256sum -c" in restore and "ilex_restore_" in restore
    assert "backup_postgres.sh" in deploy and "--entrypoint alembic" in deploy and "upgrade head" in deploy
    assert "/health/ready" in deploy
    assert "REVERSIBLE_DOWNGRADE" in rollback and "--entrypoint alembic" in rollback and "downgrade" in rollback
