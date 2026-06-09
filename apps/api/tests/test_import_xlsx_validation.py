"""Tests for XLSX import validation - BETA-012A."""

import pytest
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


def build_xlsx_bytes_v2(
    tracking_code: str = "BR123456789",
    carrier_id: str = "1",
    invoice_number: str = "NF12345",
    invoice_value: str = "1234.56",
    freight_value: str = "123.45",
    collection_date: str = "2026-06-15",
    customer_name: str = "Cliente Teste",
    destination_uf: str = "SP",
    duplicate_tracking: bool = False,
) -> bytes:
    """Helper to build XLSX bytes for testing."""
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""
    workbook = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""
    workbook_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
"""
    
    extra_row = ""
    if duplicate_tracking:
        extra_row = f"""
    <row r="3">
      <c r="A3" t="inlineStr"><is><t>{tracking_code}</t></is></c>
      <c r="B3" t="inlineStr"><is><t>{carrier_id}</t></is></c>
      <c r="C3" t="inlineStr"><is><t>NF99999</t></is></c>
      <c r="D3" t="inlineStr"><is><t>{invoice_value}</t></is></c>
      <c r="E3" t="inlineStr"><is><t>{freight_value}</t></is></c>
      <c r="F3" t="inlineStr"><is><t>{collection_date}</t></is></c>
      <c r="G3" t="inlineStr"><is><t>{customer_name}</t></is></c>
      <c r="H3" t="inlineStr"><is><t>{destination_uf}</t></is></c>
    </row>"""

    sheet = f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>tracking_code</t></is></c>
      <c r="B1" t="inlineStr"><is><t>carrier_id</t></is></c>
      <c r="C1" t="inlineStr"><is><t>invoice_number</t></is></c>
      <c r="D1" t="inlineStr"><is><t>invoice_value</t></is></c>
      <c r="E1" t="inlineStr"><is><t>freight_value</t></is></c>
      <c r="F1" t="inlineStr"><is><t>collection_departure_date</t></is></c>
      <c r="G1" t="inlineStr"><is><t>customer_name</t></is></c>
      <c r="H1" t="inlineStr"><is><t>destination_uf</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>{tracking_code}</t></is></c>
      <c r="B2" t="inlineStr"><is><t>{carrier_id}</t></is></c>
      <c r="C2" t="inlineStr"><is><t>{invoice_number}</t></is></c>
      <c r="D2" t="inlineStr"><is><t>{invoice_value}</t></is></c>
      <c r="E2" t="inlineStr"><is><t>{freight_value}</t></is></c>
      <c r="F2" t="inlineStr"><is><t>{collection_date}</t></is></c>
      <c r="G2" t="inlineStr"><is><t>{customer_name}</t></is></c>
      <c r="H2" t="inlineStr"><is><t>{destination_uf}</t></is></c>
    </row>
    {extra_row}
  </sheetData>
</worksheet>
"""
    out = BytesIO()
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    return out.getvalue()


def test_parse_xlsx_v2_valid():
    """Test parsing valid XLSX with column mapping."""
    from app.modules.imports.service_v2 import _parse_xlsx_v2
    
    xlsx_bytes = build_xlsx_bytes_v2()
    columns, rows = _parse_xlsx_v2(xlsx_bytes)
    
    assert len(columns) == 8
    assert len(rows) == 1
    assert "tracking_code" in columns
    assert rows[0]["tracking_code"] == "BR123456789"


def test_parse_xlsx_v2_empty_file():
    """Test parsing empty XLSX raises error."""
    from app.modules.imports.service_v2 import _parse_xlsx_v2
    from fastapi import HTTPException
    
    # Create empty XLSX structure
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""
    workbook = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""
    workbook_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
"""
    sheet = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
  </sheetData>
</worksheet>
"""
    
    out = BytesIO()
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    
    with pytest.raises(HTTPException) as exc_info:
        _parse_xlsx_v2(out.getvalue())
    
    assert "vazio" in str(exc_info.value.detail).lower()


def test_parse_xlsx_v2_with_brazilian_date():
    """Test parsing XLSX with Brazilian date format."""
    from app.modules.imports.service_v2 import _parse_xlsx_v2
    
    xlsx_bytes = build_xlsx_bytes_v2(collection_date="15/06/2026")
    columns, rows = _parse_xlsx_v2(xlsx_bytes)
    
    assert len(rows) == 1
    assert rows[0]["collection_departure_date"] == "15/06/2026"


def test_parse_xlsx_v2_with_brazilian_monetary():
    """Test parsing XLSX with Brazilian monetary format."""
    from app.modules.imports.service_v2 import _parse_xlsx_v2
    
    xlsx_bytes = build_xlsx_bytes_v2(
        invoice_value="1.234,56",
        freight_value="123,45"
    )
    columns, rows = _parse_xlsx_v2(xlsx_bytes)
    
    assert len(rows) == 1
    assert rows[0]["invoice_value"] == "1.234,56"
    assert rows[0]["freight_value"] == "123,45"


def test_parse_xlsx_v2_with_mapped_column_names():
    """Test parsing XLSX with Portuguese column names."""
    from app.modules.imports.service_v2 import _parse_xlsx_v2
    
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""
    workbook = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""
    workbook_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
"""
    sheet = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>Rastreio</t></is></c>
      <c r="B1" t="inlineStr"><is><t>ID Transportadora</t></is></c>
      <c r="C1" t="inlineStr"><is><t>Nota Fiscal</t></is></c>
      <c r="D1" t="inlineStr"><is><t>Valor NF</t></is></c>
      <c r="E1" t="inlineStr"><is><t>Valor Frete</t></is></c>
      <c r="F1" t="inlineStr"><is><t>Data Coleta</t></is></c>
      <c r="G1" t="inlineStr"><is><t>Cliente</t></is></c>
      <c r="H1" t="inlineStr"><is><t>UF</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>BR123456789</t></is></c>
      <c r="B2" t="inlineStr"><is><t>1</t></is></c>
      <c r="C2" t="inlineStr"><is><t>NF12345</t></is></c>
      <c r="D2" t="inlineStr"><is><t>1234.56</t></is></c>
      <c r="E2" t="inlineStr"><is><t>123.45</t></is></c>
      <c r="F2" t="inlineStr"><is><t>15/06/2026</t></is></c>
      <c r="G2" t="inlineStr"><is><t>Cliente Teste</t></is></c>
      <c r="H2" t="inlineStr"><is><t>SP</t></is></c>
    </row>
  </sheetData>
</worksheet>
"""
    
    out = BytesIO()
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    
    columns, rows = _parse_xlsx_v2(out.getvalue())
    
    assert len(columns) == 8
    assert len(rows) == 1
    # Check that columns were mapped
    assert "tracking_code" in columns or "rastreio" in columns


def test_preview_import_valid_xlsx(client):
    """Test preview import with valid XLSX."""
    xlsx_bytes = build_xlsx_bytes_v2()
    
    response = client.post(
        "/api/v1/imports/preview",
        files={
            "file": (
                "test.xlsx",
                xlsx_bytes,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 1
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 0
    assert len(data["preview_items"]) == 1


def test_preview_import_xlsx_invalid_data(client):
    """Test preview import with XLSX containing invalid data."""
    # XLSX with missing destination_uf
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"""
    workbook = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""
    workbook_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
"""
    sheet = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>tracking_code</t></is></c>
      <c r="B1" t="inlineStr"><is><t>carrier_id</t></is></c>
      <c r="C1" t="inlineStr"><is><t>invoice_number</t></is></c>
      <c r="D1" t="inlineStr"><is><t>invoice_value</t></is></c>
      <c r="E1" t="inlineStr"><is><t>freight_value</t></is></c>
      <c r="F1" t="inlineStr"><is><t>collection_departure_date</t></is></c>
      <c r="G1" t="inlineStr"><is><t>customer_name</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>BR123456789</t></is></c>
      <c r="B2" t="inlineStr"><is><t>1</t></is></c>
      <c r="C2" t="inlineStr"><is><t>NF12345</t></is></c>
      <c r="D2" t="inlineStr"><is><t>1234.56</t></is></c>
      <c r="E2" t="inlineStr"><is><t>123.45</t></is></c>
      <c r="F2" t="inlineStr"><is><t>2026-06-15</t></is></c>
      <c r="G2" t="inlineStr"><is><t>Cliente Teste</t></is></c>
    </row>
  </sheetData>
</worksheet>
"""
    
    out = BytesIO()
    with ZipFile(out, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    
    response = client.post(
        "/api/v1/imports/preview",
        files={
            "file": (
                "test.xlsx",
                out.getvalue(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 1
    assert data["valid_rows"] == 0
    assert data["invalid_rows"] == 1
    assert len(data["errors"]) > 0
