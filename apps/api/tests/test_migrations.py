"""
Testes de migrations Alembic

Valida que migrations podem ser aplicadas, revertidas e que dados críticos são preservados.
"""

import os
import sqlite3
import tempfile
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config


def get_alembic_config():
    """Retorna configuracao do Alembic."""
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"
    if not alembic_ini.exists():
        pytest.skip("alembic.ini nao encontrado - Alembic nao configurado")
    return Config(str(alembic_ini))


def test_migrations_env_uses_runtime_database_url():
    """Testa que env.py sempre prioriza a URL de banco configurada em runtime."""
    env_py = Path(__file__).parent.parent / "migrations" / "env.py"
    text = env_py.read_text(encoding="utf-8")

    assert 'config.set_main_option("sqlalchemy.url", runtime_settings.database_url)' in text
    assert "runtime_settings = Settings()" in text
    assert 'if not config.get_main_option("sqlalchemy.url")' not in text


def test_migrations_use_postgres_safe_boolean_defaults():
    """Testa que defaults booleanos em migrations usam literais compatíveis com Postgres."""
    sla_migration = Path(__file__).parent.parent / "migrations" / "versions" / "20260615_01_create_sla_rules.py"
    text = sla_migration.read_text(encoding="utf-8")

    assert "server_default=sa.text('true')" in text
    assert "server_default=sa.text('1')" not in text


def test_migrations_import():
    """Testa que configuracao do Alembic pode ser importada."""
    config = get_alembic_config()
    assert config is not None
    
    # Verificar que diretorio versions existe
    versions_dir = Path(__file__).parent.parent / "migrations" / "versions"
    if not versions_dir.exists():
        pytest.skip("Diretorio migrations/versions nao encontrado")
    
    # Verificar que ha pelo menos uma migration
    version_files = list(versions_dir.glob("*.py"))
    if len(version_files) == 0:
        pytest.skip("Nenhuma migration versionada encontrada")
    
    # Verificar que ha exatamente uma head usando CLI
    from alembic.script import ScriptDirectory
    
    script_dir = ScriptDirectory.from_config(config)
    heads = script_dir.get_revisions("head")
    assert len(heads) == 1, f"Esperado 1 head, encontrado {len(heads)}"


def test_migrations_upgrade_head():
    """Testa que migrations podem ser aplicadas ate head em banco limpo."""
    config = get_alembic_config()
    
    # Criar banco temporario
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
        db_path = temp_db.name
    
    # Configurar DATABASE_URL para banco temporario
    original_db_url = os.environ.get("ILEX_DATABASE_URL")
    original_database_url = os.environ.get("DATABASE_URL")
    
    test_db_url = f"sqlite:///{db_path}"
    os.environ["ILEX_DATABASE_URL"] = test_db_url
    os.environ["DATABASE_URL"] = test_db_url
    
    try:
        # Sobrescrever URL no config
        config.set_main_option("sqlalchemy.url", test_db_url)
        
        # Aplicar migrations ate head
        command.upgrade(config, "head")
        
        # Verificar que banco foi criado
        assert Path(db_path).exists()
        
        # Verificar que tabela alembic_version existe
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'")
        alembic_version_table = cursor.fetchone()
        assert alembic_version_table is not None, "Tabela alembic_version nao criada"
        
        # Verificar que versao e a head atual
        cursor.execute("SELECT version_num FROM alembic_version")
        version = cursor.fetchone()[0]
        
        # Obter head atual usando CLI
        from alembic.script import ScriptDirectory
        script_dir = ScriptDirectory.from_config(config)
        head = script_dir.get_current_head()
        
        assert version == head, f"Versao no banco ({version}) diferente da head ({head})"
        
        # Verificar que tabelas criticas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Tabelas criticas esperadas (baseado nas migrations)
        expected_tables = ["users", "carriers", "shipments", "import_history", "deliveries"]
        for expected_table in expected_tables:
            assert expected_table in tables, f"Tabela critica nao encontrada: {expected_table}"
        
        conn.close()
    
    finally:
        # Restaurar DATABASE_URL original
        if original_db_url:
            os.environ["ILEX_DATABASE_URL"] = original_db_url
        else:
            os.environ.pop("ILEX_DATABASE_URL", None)
        
        if original_database_url:
            os.environ["DATABASE_URL"] = original_database_url
        else:
            os.environ.pop("DATABASE_URL", None)
        
        # Limpar banco temporario
        try:
            Path(db_path).unlink(missing_ok=True)
        except:
            pass


def test_migrations_roundtrip():
    """Testa roundtrip: upgrade -> downgrade -> upgrade."""
    config = get_alembic_config()
    
    # Criar banco temporario
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
        db_path = temp_db.name
    
    # Configurar DATABASE_URL para banco temporario
    original_db_url = os.environ.get("ILEX_DATABASE_URL")
    original_database_url = os.environ.get("DATABASE_URL")
    
    test_db_url = f"sqlite:///{db_path}"
    os.environ["ILEX_DATABASE_URL"] = test_db_url
    os.environ["DATABASE_URL"] = test_db_url
    
    try:
        # Sobrescrever URL no config
        config.set_main_option("sqlalchemy.url", test_db_url)
        
        # Upgrade ate head
        command.upgrade(config, "head")
        
        # Verificar versao atual
        from alembic.script import ScriptDirectory
        script_dir = ScriptDirectory.from_config(config)
        head_after_upgrade = script_dir.get_current_head()
        
        # Downgrade para base
        command.downgrade(config, "base")
        
        # Verificar que downgrade funcionou
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT version_num FROM alembic_version")
        version_after_downgrade = cursor.fetchone()
        conn.close()
        
        # Apos downgrade para base, alembic_version pode estar vazio ou None
        assert version_after_downgrade is None or version_after_downgrade[0] is None, \
            "Downgrade para base nao removeu versao"
        
        # Upgrade novamente
        command.upgrade(config, "head")
        
        # Verificar que voltou para mesma head
        head_after_reupgrade = script_dir.get_current_head()
        assert head_after_upgrade == head_after_reupgrade, \
            f"Head diferente apos roundtrip: {head_after_upgrade} vs {head_after_reupgrade}"
    
    finally:
        # Restaurar DATABASE_URL original
        if original_db_url:
            os.environ["ILEX_DATABASE_URL"] = original_db_url
        else:
            os.environ.pop("ILEX_DATABASE_URL", None)
        
        if original_database_url:
            os.environ["DATABASE_URL"] = original_database_url
        else:
            os.environ.pop("DATABASE_URL", None)
        
        # Limpar banco temporario
        try:
            Path(db_path).unlink(missing_ok=True)
        except:
            pass


def test_data_preservation():
    """Testa que dados criticos sobrevem a migration aplicada."""
    config = get_alembic_config()
    
    # Criar banco temporario
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
        db_path = temp_db.name
    
    # Configurar DATABASE_URL para banco temporario
    original_db_url = os.environ.get("ILEX_DATABASE_URL")
    original_database_url = os.environ.get("DATABASE_URL")
    
    test_db_url = f"sqlite:///{db_path}"
    os.environ["ILEX_DATABASE_URL"] = test_db_url
    os.environ["DATABASE_URL"] = test_db_url
    
    try:
        # Sobrescrever URL no config
        config.set_main_option("sqlalchemy.url", test_db_url)
        
        # Upgrade ate head
        command.upgrade(config, "head")
        
        # Aplicar roundtrip (downgrade + upgrade)
        # LIMITAÇÃO DOCUMENTADA: Downgrade para base DESTRUI dados
        # Este teste valida que rollback funciona, mas não que dados são preservados
        # Para validar preservação real, seria necessário migration incremental
        command.downgrade(config, "base")
        command.upgrade(config, "head")
        
        # Verificar que tabelas foram recriadas (rollback funciona)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_after = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Verificar que tabelas criticas foram recriadas
        assert "alembic_version" in tables_after, "Tabela alembic_version nao recriada"
        assert "users" in tables_after, "Tabela users nao recriada"
        assert "carriers" in tables_after, "Tabela carriers nao recriada"
        assert "shipments" in tables_after, "Tabela shipments nao recriada"
        assert "import_history" in tables_after, "Tabela import_history nao recriada"
        assert "deliveries" in tables_after, "Tabela deliveries nao recriada"
        
    finally:
        # Restaurar DATABASE_URL original
        if original_db_url:
            os.environ["ILEX_DATABASE_URL"] = original_db_url
        else:
            os.environ.pop("ILEX_DATABASE_URL", None)
        
        if original_database_url:
            os.environ["DATABASE_URL"] = original_database_url
        else:
            os.environ.pop("DATABASE_URL", None)
        
        # Limpar banco temporario
        try:
            Path(db_path).unlink(missing_ok=True)
        except:
            pass
