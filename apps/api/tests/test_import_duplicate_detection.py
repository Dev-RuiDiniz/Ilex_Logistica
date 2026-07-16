"""Tests for duplicate detection in imports - BETA-012A."""

import pytest

from app.main import app
from app.modules.auth.dependencies import get_current_user
from app.modules.users.models import User
from conftest import create_user_with_roles


@pytest.fixture(autouse=True)
def authenticated_requests(client, auth_headers):
    client.headers.update(auth_headers)


@pytest.fixture(autouse=True)
def _auth_admin(db_session):
    """Autentica todos os testes deste módulo como admin (endpoints exigem RBAC)."""
    admin = create_user_with_roles(db_session, "admin_dupdet@ilex.com", "123456", ["admin"])

    def _override() -> User:
        return admin

    app.dependency_overrides[get_current_user] = _override
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_detect_duplicates_in_file_tracking_code():
    """Test detecting duplicates by tracking_code within file."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    # Create validated rows with duplicate tracking_code
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": "NF3"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 1  # One duplicate (BR123 appears twice)


def test_detect_duplicates_in_file_invoice_number():
    """Test detecting duplicates by invoice_number within file."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    # Create validated rows with duplicate invoice_number
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR789", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 1  # One duplicate (NF1 appears twice)


def test_detect_duplicates_in_file_no_duplicates():
    """Test detecting no duplicates when all rows are unique."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    # Create validated rows with no duplicates
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR789", "carrier_id": 1, "invoice_number": "NF3"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 0


def test_detect_duplicates_in_file_multiple_duplicates():
    """Test detecting multiple duplicates within file."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    # Create validated rows with multiple duplicates
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=5,
            data={"tracking_code": "BR789", "carrier_id": 1, "invoice_number": "NF3"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 2  # Two duplicates (BR123 and NF1)


def test_detect_duplicates_in_file_ignores_invalid_rows():
    """Test that invalid rows are ignored in duplicate detection."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow, RowValidationError
    
    # Create validated rows with some invalid
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[RowValidationError(row_number=3, field="tracking_code", message="error")],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": "NF3"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 0  # Invalid row ignored, no duplicates detected


def test_detect_duplicates_in_db_tracking_code(db_session):
    """Test detecting duplicates by tracking_code against database."""
    from app.modules.imports.service_v2 import detect_duplicates_in_db, ValidatedRow
    from datetime import datetime, UTC
    
    # First, create a shipment in the database
    from app.modules.shipments.models import Shipment
    
    # Create a test shipment
    shipment = Shipment(
        tracking_code="BR123456789",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test",
        recipient_phone="1234567890",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()
    
    # Now test duplicate detection
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123456789", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR987654321", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_db(db_session, rows)
    assert duplicate_count == 1  # One duplicate (BR123456789 exists in DB)


def test_detect_duplicates_in_db_invoice_number(db_session):
    """Test detecting duplicates by invoice_number against database."""
    from app.modules.imports.service_v2 import detect_duplicates_in_db, ValidatedRow
    from app.modules.shipments.models import Shipment
    from datetime import datetime, UTC
    
    # Create a test shipment with invoice_number
    shipment = Shipment(
        tracking_code="BR123456789",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test",
        recipient_phone="1234567890",
        origin_address="Origin",
        destination_address="Destination",
        invoice_number="NF12345",
    )
    db_session.add(shipment)
    db_session.commit()
    
    # Now test duplicate detection
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR987654321", "carrier_id": 1, "invoice_number": "NF12345"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR555555555", "carrier_id": 1, "invoice_number": "NF67890"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_db(db_session, rows)
    assert duplicate_count == 1  # One duplicate (NF12345 exists in DB)


def test_detect_duplicates_in_db_no_duplicates(db_session):
    """Test detecting no duplicates when database has no matching records."""
    from app.modules.imports.service_v2 import detect_duplicates_in_db, ValidatedRow
    
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123456789", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR987654321", "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_db(db_session, rows)
    assert duplicate_count == 0
    assert duplicate_count == 0


def test_detect_duplicates_in_db_empty_rows(db_session):
    """Test duplicate detection with empty rows list."""
    from app.modules.imports.service_v2 import detect_duplicates_in_db
    
    duplicate_count = detect_duplicates_in_db(db_session, [])
    assert duplicate_count == 0


def test_preview_includes_duplicate_count(client, db_session):
    """Test that preview includes duplicate count in summary."""
    # First, create a shipment in the database
    from app.modules.shipments.models import Shipment
    from datetime import datetime, UTC
    
    shipment = Shipment(
        tracking_code="BR123456789",
        carrier_id=1,
        status="pending",
        estimated_delivery=datetime.now(UTC),
        recipient_name="Test",
        recipient_phone="1234567890",
        origin_address="Origin",
        destination_address="Destination",
    )
    db_session.add(shipment)
    db_session.commit()
    
    # Now test preview with duplicate
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "duplicate_rows" in data
    assert data["duplicate_rows"] >= 1  # At least one duplicate in DB


def test_preview_detects_in_file_duplicates(client):
    """Test that preview detects duplicates within the file."""
    csv_content = b"""tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf
BR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP
BR123456789,1,NF67890,5678.90,234.56,2026-06-16,Cliente Dois,RJ
"""
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "duplicate_rows" in data
    assert data["duplicate_rows"] >= 1  # At least one duplicate in file


def test_duplicate_detection_with_different_carriers():
    """Test that same tracking_code with different carrier_id is not considered duplicate."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": "BR123", "carrier_id": 2, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 0  # Not duplicate because carrier_id is different


def test_duplicate_detection_with_missing_fields():
    """Test duplicate detection when some rows have missing fields."""
    from app.modules.imports.service_v2 import detect_duplicates_in_file, ValidatedRow
    
    rows = [
        ValidatedRow(
            row_number=2,
            data={"tracking_code": "BR123", "carrier_id": 1, "invoice_number": "NF1"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=3,
            data={"tracking_code": None, "carrier_id": 1, "invoice_number": "NF2"},
            errors=[],
            warnings=[],
        ),
        ValidatedRow(
            row_number=4,
            data={"tracking_code": "BR456", "carrier_id": 1, "invoice_number": None},
            errors=[],
            warnings=[],
        ),
    ]
    
    duplicate_count = detect_duplicates_in_file(rows)
    assert duplicate_count == 0  # No duplicates due to missing fields
