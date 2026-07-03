"""Generate deterministic, sanitized CSV/XLSX order datasets for E2E and load tests."""

import csv
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

HEADERS = [
    "source", "external_number", "order_date", "customer_name", "origin_zip", "origin_uf",
    "destination_zip", "destination_uf", "weight_kg", "volume_count", "goods_value", "currency",
]
SIZES = (10, 1_000, 10_000)
ROOT = Path(__file__).parent


def rows(size: int) -> list[list[str]]:
    return [
        ["fixture", f"PED-{size}-{index:05d}", "2026-07-03", f"Cliente {index:05d}", "01310100", "SP",
         "20040002", "RJ", "10.500", "2", "1200.00", "BRL"]
        for index in range(1, size + 1)
    ]


def write_csv(size: int, data: list[list[str]]) -> None:
    with (ROOT / f"orders_{size}.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(HEADERS)
        writer.writerows(data)


def write_xlsx(size: int, data: list[list[str]]) -> None:
    matrix = [HEADERS, *data]
    xml_rows = []
    for row_number, values in enumerate(matrix, start=1):
        cells = "".join(f'<c t="inlineStr"><is><t>{escape(value)}</t></is></c>' for value in values)
        xml_rows.append(f'<row r="{row_number}">{cells}</row>')
    sheet = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
        + "".join(xml_rows)
        + "</sheetData></worksheet>"
    )
    with ZipFile(ROOT / f"orders_{size}.xlsx", "w", ZIP_DEFLATED) as archive:
        archive.writestr("xl/worksheets/sheet1.xml", sheet)


if __name__ == "__main__":
    for fixture_size in SIZES:
        fixture_rows = rows(fixture_size)
        write_csv(fixture_size, fixture_rows)
        write_xlsx(fixture_size, fixture_rows)
