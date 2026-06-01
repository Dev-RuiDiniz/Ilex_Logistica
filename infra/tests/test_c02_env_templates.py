from pathlib import Path

from infra_checks import env_template_keys


def test_c02_env_templates_have_required_keys():
    root = Path(__file__).resolve().parents[1]
    keys = env_template_keys(
        root / ".env.example",
        root / "env" / "api.env.example",
        root / "env" / "web.env.example",
    )

    assert "ILEX_DATABASE_URL" in keys["root"]
    assert "ILEX_DATABASE_URL" in keys["api"]
    assert "NEXT_PUBLIC_API_URL" in keys["root"]
    assert "NEXT_PUBLIC_API_URL" in keys["web"]
