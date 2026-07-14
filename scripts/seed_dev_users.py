from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "apps" / "api"
INFRA_ENV = ROOT / "infra" / ".env"


def _load_local_env() -> None:
    if not INFRA_ENV.exists():
        return

    env_values: dict[str, str] = {}
    for raw_line in INFRA_ENV.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env_values[key.strip()] = value.strip()

    if "ILEX_DATABASE_URL" not in os.environ and "ILEX_DATABASE_URL" in env_values:
        database_url = env_values["ILEX_DATABASE_URL"]
        if "@db:5432" in database_url:
            host_port = env_values.get("POSTGRES_PORT", "5432")
            database_url = database_url.replace("@db:5432", f"@127.0.0.1:{host_port}")
        os.environ["ILEX_DATABASE_URL"] = database_url


_load_local_env()

if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.database.session import SessionLocal  # noqa: E402
from app.modules.users.seed_dev_users import (  # noqa: E402
    DEFAULT_DEV_PASSWORD,
    DEFAULT_DEV_USERS,
    seed_dev_users,
)


def main() -> int:
    db = SessionLocal()
    try:
        summary = seed_dev_users(db)
    finally:
        db.close()

    print("Usuarios seed atualizados com sucesso.")
    print(f"Criados: {summary['created']} | Atualizados: {summary['updated']}")
    print("")
    print("Acessos de desenvolvimento:")
    for user in DEFAULT_DEV_USERS:
        roles = ", ".join(user["roles"])
        print(f"- {user['email']} | senha: {DEFAULT_DEV_PASSWORD} | perfis: {roles}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
