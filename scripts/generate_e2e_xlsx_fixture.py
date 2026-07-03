"""Gera a fixture XLSX sanitizada usada pelo Playwright."""

from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def build_fixture() -> bytes:
    files = {
        "[Content_Types].xml": """<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Importacao" sheetId="1" r:id="rId1"/></sheets></workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>""",
        "xl/worksheets/sheet1.xml": """<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>tracking_code</t></is></c><c r="B1" t="inlineStr"><is><t>carrier_id</t></is></c><c r="C1" t="inlineStr"><is><t>invoice_number</t></is></c><c r="D1" t="inlineStr"><is><t>invoice_value</t></is></c><c r="E1" t="inlineStr"><is><t>freight_value</t></is></c><c r="F1" t="inlineStr"><is><t>collection_departure_date</t></is></c><c r="G1" t="inlineStr"><is><t>customer_name</t></is></c><c r="H1" t="inlineStr"><is><t>destination_uf</t></is></c></row><row r="2"><c r="A2" t="inlineStr"><is><t>E2E-XLSX-001</t></is></c><c r="B2" t="inlineStr"><is><t>1</t></is></c><c r="C2" t="inlineStr"><is><t>NF-E2E-XLSX-001</t></is></c><c r="D2" t="inlineStr"><is><t>1000.00</t></is></c><c r="E2" t="inlineStr"><is><t>100.00</t></is></c><c r="F2" t="inlineStr"><is><t>2026-07-03</t></is></c><c r="G2" t="inlineStr"><is><t>Cliente Sanitizado</t></is></c><c r="H2" t="inlineStr"><is><t>SP</t></is></c></row></sheetData></worksheet>""",
    }
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return output.getvalue()


if __name__ == "__main__":
    target = Path(__file__).parents[1] / "apps/web/e2e/fixtures/import-valid.xlsx"
    target.write_bytes(build_fixture())
    print(target)
