from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile


def build_xlsx_bytes(duplicate_nf: bool = False) -> bytes:
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
    if duplicate_nf:
        extra_row = """
    <row r="3">
      <c r="A3" t="inlineStr"><is><t>123</t></is></c>
      <c r="B3" t="inlineStr"><is><t>XPTO2</t></is></c>
    </row>"""

    sheet = f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1">
      <c r="A1" t="inlineStr"><is><t>nf</t></is></c>
      <c r="B1" t="inlineStr"><is><t>transportadora</t></is></c>
    </row>
    <row r="2">
      <c r="A2" t="inlineStr"><is><t>123</t></is></c>
      <c r="B2" t="inlineStr"><is><t>XPTO</t></is></c>
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


def test_upload_csv_retorna_resumo(client) -> None:
    csv_bytes = b"nf,transportadora\n123,XPTO\n"
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "entregas.csv"
    assert data["rows_received"] == 1
    assert data["columns_detected"] == ["nf", "transportadora"]
    assert len(data["preview"]) == 1


def test_upload_sem_arquivo_retorna_422(client) -> None:
    response = client.post("/api/v1/imports/upload")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_upload_extensao_invalida_retorna_400(client) -> None:
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.txt", b"abc", "text/plain")},
    )
    assert response.status_code == 400
    assert "formato" in response.json()["detail"].lower()


def test_upload_arquivo_vazio_retorna_400(client) -> None:
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", b"", "text/csv")},
    )
    assert response.status_code == 400
    assert "vazio" in response.json()["detail"].lower()


def test_upload_xlsx_retorna_resumo(client) -> None:
    response = client.post(
        "/api/v1/imports/upload",
        files={
            "file": (
                "entregas.xlsx",
                build_xlsx_bytes(),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "entregas.xlsx"
    assert data["rows_received"] == 1
    assert data["columns_detected"] == ["nf", "transportadora"]


def test_upload_csv_normaliza_cabecalho_com_acento_e_espacos(client) -> None:
    csv_bytes = " NF , Trânsportádora \n123,XPTO\n".encode("utf-8")
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["columns_detected"] == ["nf", "transportadora"]


def test_upload_rejeita_sem_nf(client) -> None:
    csv_bytes = b"transportadora\nXPTO\n"
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 400
    assert "nf" in response.json()["detail"].lower()


def test_upload_rejeita_sem_transportadora(client) -> None:
    csv_bytes = b"nf\n123\n"
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 400
    assert "transportadora" in response.json()["detail"].lower()


def test_upload_rejeita_csv_com_nf_duplicado(client) -> None:
    csv_bytes = b"nf,transportadora\n123,XPTO\n123,XPTO2\n"
    response = client.post(
        "/api/v1/imports/upload",
        files={"file": ("entregas.csv", csv_bytes, "text/csv")},
    )
    assert response.status_code == 400
    detail = response.json()["detail"].lower()
    assert "duplicidade" in detail
    assert "123" in detail


def test_upload_rejeita_xlsx_com_nf_duplicado(client) -> None:
    xlsx = build_xlsx_bytes(duplicate_nf=True)
    response = client.post(
        "/api/v1/imports/upload",
        files={
            "file": (
                "entregas.xlsx",
                xlsx,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )
    assert response.status_code == 400
    detail = response.json()["detail"].lower()
    assert "duplicidade" in detail
    assert "123" in detail
