import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def test_alembic_upgrade_and_downgrade() -> None:
    db_path = Path("migration_test.db")
    if db_path.exists():
        db_path.unlink()

    cfg = Config("alembic.ini")
    cfg.set_main_option("script_location", "migrations")
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.resolve()}")

    command.upgrade(cfg, "head")
    engine = create_engine(f"sqlite:///{db_path.resolve()}")
    inspector = inspect(engine)
    assert "users" in inspector.get_table_names()
    assert "roles" in inspector.get_table_names()

    command.downgrade(cfg, "base")
    inspector = inspect(engine)
    assert "users" not in inspector.get_table_names()
    engine.dispose()
    os.remove(db_path)
