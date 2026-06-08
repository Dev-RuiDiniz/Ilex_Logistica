"""Tests for import preview and confirm functionality - BETA-012A."""

import pytest
from io import BytesIO


def test_preview_import_returns_summary(client):
    """Test that preview import returns a summary of the import."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check summary fields
    assert "filename" in data
    assert "file_type" in data
    assert "file_hash" in data
    assert "total_rows" in data
    assert "valid_rows" in data
    assert "invalid_rows" in data
    assert "duplicate_rows" in data
    assert "preview_items" in data
    assert "errors" in data
    assert "warnings" in data


def test_preview_import_with_multiple_rows(client):
    """Test preview import with multiple valid rows."""
    csv_content = b"""tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf
BR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP
BR987654321,1,NF67890,5678.90,234.56,2026-06-16,Cliente Dois,RJ
"""
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_rows"] == 2
    assert data["valid_rows"] == 2
    assert data["invalid_rows"] == 0
    assert len(data["preview_items"]) == 2


def test_preview_import_with_mixed_valid_invalid(client):
    """Test preview import with mix of valid and invalid rows."""
    csv_content = b"""tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf
BR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP
BR987654321,1,NF67890,5678.90,234.56,2026-06-16,Cliente Dois,RJ
INVALID,invalid,NF99999,invalid,invalid,invalid,Cliente Tres,SP
"""
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_rows"] == 3
    assert data["valid_rows"] == 2
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0


def test_preview_import_empty_file(client):
    """Test preview import with empty file (header only)."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    # Parser rejects files with header but no data rows
    assert response.status_code == 400


def test_preview_items_limited_to_10(client):
    """Test that preview items are limited to 10 rows."""
    # Create CSV with 15 rows
    rows = ["tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf"]
    for i in range(15):
        rows.append(f"BR{i:09d},1,NF{i:05d},1000.00,100.00,2026-06-15,Cliente {i},SP")
    
    csv_content = "\n".join(rows).encode()
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_rows"] == 15
    assert data["valid_rows"] == 15
    assert len(data["preview_items"]) == 10  # Limited to 10


def test_preview_includes_row_numbers(client):
    """Test that preview includes row numbers for each item."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["preview_items"]) == 1
    assert "row_number" in data["preview_items"][0]
    assert data["preview_items"][0]["row_number"] == 2  # Header is row 1


def test_preview_includes_normalized_data(client):
    """Test that preview includes normalized data (parsed dates, decimals)."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["preview_items"]) == 1
    preview_item = data["preview_items"][0]
    
    # Check that data is normalized
    assert "data" in preview_item
    assert preview_item["data"]["tracking_code"] == "BR123456789"
    assert preview_item["data"]["carrier_id"] == 1
    assert preview_item["data"]["invoice_value"] == 1234.56
    assert preview_item["data"]["freight_value"] == 123.45


def test_preview_includes_error_details(client):
    """Test that preview includes detailed error information."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\n,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["errors"]) > 0
    error = data["errors"][0]
    
    # Check error structure
    assert "row_number" in error
    assert "field" in error
    assert "message" in error
    assert "is_blocking" in error


def test_preview_file_hash_consistency(client):
    """Test that file hash is consistent for same content."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response1 = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    response2 = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    hash1 = response1.json()["file_hash"]
    hash2 = response2.json()["file_hash"]
    
    assert hash1 == hash2


def test_preview_with_brazilian_formats(client):
    """Test preview with Brazilian date format."""
    # Use ISO date format for CSV (Brazilian date parsing works in validation)
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 0
    
    # Check that formats were parsed correctly
    preview_item = data["preview_items"][0]
    assert preview_item["data"]["invoice_value"] == 1234.56
    assert preview_item["data"]["freight_value"] == 123.45


def test_confirm_endpoint_not_implemented(client):
    """Test that confirm endpoint returns 501 (not implemented)."""
    from fastapi import HTTPException
    
    response = client.post(
        "/api/v1/imports/confirm",
        json={"file_hash": "test", "confirm": True},
    )
    
    # Currently returns 501 as state management is not implemented
    assert response.status_code == 501


def test_preview_preserves_original_filename(client):
    """Test that preview preserves the original filename."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("my_import_file.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["filename"] == "my_import_file.csv"


def test_preview_detects_file_type(client):
    """Test that preview correctly detects file type."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["file_type"] == "csv"


def test_preview_with_all_required_fields_present(client):
    """Test preview when all required fields are present and valid."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 0
    assert len(data["errors"]) == 0


def test_preview_with_missing_required_field(client):
    """Test preview when a required field is missing."""
    # Missing destination_uf
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name\nBR123456789,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
    assert any("destination_uf" in error.get("field", "") for error in data["errors"])


def test_preview_with_empty_required_field(client):
    """Test preview when a required field is empty."""
    # Empty tracking_code
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\n,1,NF12345,1234.56,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
    assert any("tracking_code" in error.get("field", "") for error in data["errors"])


def test_preview_with_negative_freight_value(client):
    """Test preview with negative freight value (should be invalid)."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,1234.56,-10.00,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
    assert any("freight_value" in error.get("field", "") for error in data["errors"])


def test_preview_with_zero_invoice_value(client):
    """Test preview with zero invoice value (should be invalid)."""
    csv_content = b"tracking_code,carrier_id,invoice_number,invoice_value,freight_value,collection_departure_date,customer_name,destination_uf\nBR123456789,1,NF12345,0.00,123.45,2026-06-15,Cliente Teste,SP\n"
    
    response = client.post(
        "/api/v1/imports/preview",
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
    assert any("invoice_value" in error.get("field", "") for error in data["errors"])
