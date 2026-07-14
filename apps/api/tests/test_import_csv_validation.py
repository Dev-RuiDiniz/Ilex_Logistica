"""Tests for CSV import validation - BETA-012A."""

import pytest
from io import BytesIO
from fastapi import UploadFile

from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from conftest import create_user_with_roles


@pytest.fixture(autouse=True)
def _auth_admin(db_session):
    """Autentica todos os testes deste módulo como admin (endpoints exigem RBAC)."""
    admin = create_user_with_roles(db_session, "admin_csvval@ilex.com", "123456", ["admin"])

    def _override() -> User:
        return admin

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(autouse=True)
def authenticated_requests(client, auth_headers):
    client.headers.update(auth_headers)


def _create_upload_file(content: bytes, filename: str = "test.csv") -> UploadFile:
    """Helper to create an UploadFile for testing."""
    file = BytesIO(content)
    upload = UploadFile(filename=filename, file=file)
    return upload


def test_parse_brazilian_date_dd_mm_yyyy():
    """Test parsing Brazilian date format DD/MM/YYYY."""
    from app.modules.imports.service_v2 import parse_brazilian_date
    
    # Valid Brazilian date
    result = parse_brazilian_date("15/06/2026")
    assert result is not None
    assert result.day == 15
    assert result.month == 6
    assert result.year == 2026


def test_parse_brazilian_date_dd_mm_yy():
    """Test parsing Brazilian date format DD/MM/YY (2-digit year)."""
    from app.modules.imports.service_v2 import parse_brazilian_date
    
    # Valid Brazilian date with 2-digit year
    result = parse_brazilian_date("15/06/26")
    assert result is not None
    assert result.day == 15
    assert result.month == 6
    assert result.year == 2026


def test_parse_brazilian_date_with_hyphens():
    """Test parsing Brazilian date format DD-MM-YYYY."""
    from app.modules.imports.service_v2 import parse_brazilian_date
    
    # Valid Brazilian date with hyphens
    result = parse_brazilian_date("15-06-2026")
    assert result is not None
    assert result.day == 15
    assert result.month == 6
    assert result.year == 2026


def test_parse_brazilian_date_iso_format():
    """Test parsing ISO date format YYYY-MM-DD."""
    from app.modules.imports.service_v2 import parse_brazilian_date
    
    # Valid ISO date
    result = parse_brazilian_date("2026-06-15")
    assert result is not None
    assert result.day == 15
    assert result.month == 6
    assert result.year == 2026


def test_parse_brazilian_date_invalid():
    """Test parsing invalid date returns None."""
    from app.modules.imports.service_v2 import parse_brazilian_date
    
    # Invalid date
    result = parse_brazilian_date("32/13/2026")
    assert result is None
    
    # Invalid format
    result = parse_brazilian_date("invalid")
    assert result is None
    
    # Empty string
    result = parse_brazilian_date("")
    assert result is None


def test_parse_brazilian_monetary_with_thousands():
    """Test parsing Brazilian monetary format with thousands separator."""
    from app.modules.imports.service_v2 import parse_brazilian_monetary
    from decimal import Decimal
    
    # Valid Brazilian monetary with thousands separator
    result = parse_brazilian_monetary("1.234,56")
    assert result is not None
    assert result == Decimal("1234.56")


def test_parse_brazilian_monetary_without_thousands():
    """Test parsing Brazilian monetary format without thousands separator."""
    from app.modules.imports.service_v2 import parse_brazilian_monetary
    from decimal import Decimal
    
    # Valid Brazilian monetary without thousands separator
    result = parse_brazilian_monetary("1234,56")
    assert result is not None
    assert result == Decimal("1234.56")


def test_parse_brazilian_monetary_with_r_prefix():
    """Test parsing Brazilian monetary format with R$ prefix."""
    from app.modules.imports.service_v2 import parse_brazilian_monetary
    from decimal import Decimal
    
    # Valid Brazilian monetary with R$ prefix
    result = parse_brazilian_monetary("R$ 1.234,56")
    assert result is not None
    assert result == Decimal("1234.56")


def test_parse_brazilian_monetary_standard_format():
    """Test parsing standard decimal format."""
    from app.modules.imports.service_v2 import parse_brazilian_monetary
    from decimal import Decimal
    
    # Valid standard decimal format
    result = parse_brazilian_monetary("1234.56")
    assert result is not None
    assert result == Decimal("1234.56")


def test_parse_brazilian_monetary_invalid():
    """Test parsing invalid monetary value returns None."""
    from app.modules.imports.service_v2 import parse_brazilian_monetary
    
    # Invalid format
    result = parse_brazilian_monetary("invalid")
    assert result is None
    
    # Empty string
    result = parse_brazilian_monetary("")
    assert result is None


def test_normalize_column_name_basic():
    """Test basic column name normalization."""
    from app.modules.imports.mapper import normalize_column_name
    
    # Basic normalization
    assert normalize_column_name("Tracking Code") == "tracking_code"
    assert normalize_column_name("INVOICE_NUMBER") == "invoice_number"
    assert normalize_column_name("  Data Coleta  ") == "data_coleta"


def test_normalize_column_name_with_accents():
    """Test column name normalization with accents."""
    from app.modules.imports.mapper import normalize_column_name
    
    # Remove accents
    assert normalize_column_name("Trânsportádora") == "transportadora"
    assert normalize_column_name("Nota Fiscal") == "nota_fiscal"


def test_map_column_tracking_code():
    """Test mapping tracking_code column variations."""
    from app.modules.imports.mapper import map_column
    
    assert map_column("tracking_code") == "tracking_code"
    assert map_column("Tracking Code") == "tracking_code"
    assert map_column("Rastreio") == "tracking_code"
    assert map_column("codigo_rastreio") == "tracking_code"


def test_map_column_invoice_number():
    """Test mapping invoice_number column variations."""
    from app.modules.imports.mapper import map_column
    
    assert map_column("invoice_number") == "invoice_number"
    assert map_column("NF") == "invoice_number"
    assert map_column("Nota Fiscal") == "invoice_number"
    assert map_column("numero_nf") == "invoice_number"


def test_map_column_freight_value():
    """Test mapping freight_value column variations."""
    from app.modules.imports.mapper import map_column
    
    assert map_column("freight_value") == "freight_value"
    assert map_column("Valor Frete") == "freight_value"
    assert map_column("valor_frete") == "freight_value"
    assert map_column("Frete") == "freight_value"


def test_map_column_destination_uf():
    """Test mapping destination_uf column variations."""
    from app.modules.imports.mapper import map_column
    
    assert map_column("destination_uf") == "destination_uf"
    assert map_column("UF") == "destination_uf"
    assert map_column("uf_destino") == "destination_uf"
    assert map_column("Estado") == "destination_uf"


def test_validate_row_valid_data():
    """Test validating a row with valid data."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "tracking_code": "BR123456789",
        "carrier_id": "1",
        "invoice_number": "NF12345",
        "invoice_value": "1.234,56",
        "freight_value": "123,45",
        "collection_departure_date": "15/06/2026",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP",
    }
    
    validated = validate_row(row, row_number=2)
    assert validated.is_valid
    assert len(validated.errors) == 0
    assert validated.data["tracking_code"] == "BR123456789"
    assert validated.data["carrier_id"] == 1
    assert validated.data["invoice_value"] == 1234.56
    assert validated.data["freight_value"] == 123.45


def test_validate_row_missing_tracking_code():
    """Test validating a row with missing tracking_code."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "carrier_id": "1",
        "invoice_number": "NF12345",
        "invoice_value": "1.234,56",
        "freight_value": "123,45",
        "collection_departure_date": "15/06/2026",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP",
    }
    
    validated = validate_row(row, row_number=2)
    assert not validated.is_valid
    assert len(validated.errors) > 0
    assert any(error.field == "tracking_code" for error in validated.errors)


def test_validate_row_invalid_carrier_id():
    """Test validating a row with invalid carrier_id."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "tracking_code": "BR123456789",
        "carrier_id": "invalid",
        "invoice_number": "NF12345",
        "invoice_value": "1.234,56",
        "freight_value": "123,45",
        "collection_departure_date": "15/06/2026",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP",
    }
    
    validated = validate_row(row, row_number=2)
    assert not validated.is_valid
    assert len(validated.errors) > 0
    assert any(error.field == "carrier_id" for error in validated.errors)


def test_validate_row_invalid_invoice_value():
    """Test validating a row with invalid invoice_value."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "tracking_code": "BR123456789",
        "carrier_id": "1",
        "invoice_number": "NF12345",
        "invoice_value": "invalid",
        "freight_value": "123,45",
        "collection_departure_date": "15/06/2026",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP",
    }
    
    validated = validate_row(row, row_number=2)
    assert not validated.is_valid
    assert len(validated.errors) > 0
    assert any(error.field == "invoice_value" for error in validated.errors)


def test_validate_row_invalid_date():
    """Test validating a row with invalid date."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "tracking_code": "BR123456789",
        "carrier_id": "1",
        "invoice_number": "NF12345",
        "invoice_value": "1.234,56",
        "freight_value": "123,45",
        "collection_departure_date": "invalid",
        "customer_name": "Cliente Teste",
        "destination_uf": "SP",
    }
    
    validated = validate_row(row, row_number=2)
    assert not validated.is_valid
    assert len(validated.errors) > 0
    assert any(error.field == "collection_departure_date" for error in validated.errors)


def test_validate_row_invalid_uf():
    """Test validating a row with invalid UF (not 2 characters)."""
    from app.modules.imports.service_v2 import validate_row
    
    row = {
        "tracking_code": "BR123456789",
        "carrier_id": "1",
        "invoice_number": "NF12345",
        "invoice_value": "1.234,56",
        "freight_value": "123,45",
        "collection_departure_date": "15/06/2026",
        "customer_name": "Cliente Teste",
        "destination_uf": "SAO",  # 3 characters instead of 2
    }
    
    validated = validate_row(row, row_number=2)
    assert not validated.is_valid
    assert len(validated.errors) > 0
    assert any(error.field == "destination_uf" for error in validated.errors)


def test_parse_csv_v2_with_mapped_columns():
    """Test parsing CSV with column mapping."""
    from app.modules.imports.service_v2 import _parse_csv_v2
    
    csv_content = b"Rastreio,ID Transportadora,NF,Valor NF,Valor Frete,Data Coleta,Cliente,UF\nBR123,1,NF123,1.234,56,123,45,15/06/2026,Cliente Teste,SP\n"
    
    columns, rows = _parse_csv_v2(csv_content)
    
    assert len(columns) > 0
    assert len(rows) == 1
    # Check that columns were mapped
    assert "tracking_code" in columns or "rastreio" in columns


def test_parse_csv_v2_empty_file():
    """Test parsing empty CSV raises error."""
    from app.modules.imports.service_v2 import _parse_csv_v2
    from fastapi import HTTPException
    
    csv_content = b"Rastreio,ID Transportadora\n"
    
    with pytest.raises(HTTPException) as exc_info:
        _parse_csv_v2(csv_content)
    
    assert "sem dados" in str(exc_info.value.detail).lower()


def test_preview_import_valid_csv(client):
    """Test preview import with valid CSV."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 1
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 0
    assert len(data["preview_items"]) == 1


def test_preview_import_invalid_csv(client):
    """Test preview import with invalid CSV (missing required field)."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste\n"  # Missing destination_uf
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 1
    assert data["valid_rows"] == 0
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
