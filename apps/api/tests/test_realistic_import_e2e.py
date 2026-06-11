"""
Teste E2E de importação realista com arquivo sintético.

Este teste valida a importação via arquivo CSV sintético realista,
usando UploadFile compatível com o framework FastAPI.
"""

import pytest
from io import BytesIO
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.modules.imports.service_v2 import preview_import, confirm_import
from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment


@pytest.fixture
def db_session():
    """Get database session for testing using SQLite test database."""
    from tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    try:
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture
def seed_braspress_carrier(db_session: Session):
    """Seed a test carrier for import tests."""
    carrier = Carrier(name="Braspress")
    db_session.add(carrier)
    db_session.commit()
    db_session.refresh(carrier)
    return carrier


def create_upload_file(content: bytes, filename: str = "test.csv") -> UploadFile:
    """Create an UploadFile from bytes."""
    return UploadFile(filename=filename, file=BytesIO(content))


class TestRealisticImportE2E:
    """Teste E2E de importação realista com arquivo sintético."""

    def test_realistic_csv_import_with_uploadfile(
        self,
        db_session: Session,
        seed_braspress_carrier,
    ):
        """
        Teste de importação realista usando UploadFile com arquivo CSV sintético.
        
        Cenário:
        1. Criar arquivo CSV sintético realista em memória
        2. Construir UploadFile compatível
        3. Chamar preview_import
        4. Validar preview (valid_rows, invalid_rows, errors, warnings)
        5. Chamar confirm_import
        6. Validar persistência de shipments
        7. Validar campos fiscais/financeiros
        8. Validar transportadora Braspress
        """
        # Step 1: Criar arquivo CSV sintético realista (formato Braspress)
        csv_content = """Número da entrega ou rastreio,Número da NF,Cliente,UF destino,Data coleta/saída,Valor NF,Valor frete,Transportadora
SYNTH-REAL-001,INV-REAL-001,Cliente Realista 1,SP,01/01/2026,1000.00,50.00,Braspress
SYNTH-REAL-002,INV-REAL-002,Cliente Realista 2,RJ,02/01/2026,2000.00,100.00,Braspress
SYNTH-REAL-003,INV-REAL-003,Cliente Realista 3,MG,03/01/2026,1500.00,75.00,Braspress
"""
        csv_bytes = csv_content.encode('utf-8')
        
        # Step 2: Construir UploadFile compatível
        upload = create_upload_file(csv_bytes, "synthetic_realistic.csv")
        
        # Step 3: Chamar preview_import
        preview = preview_import(db_session, upload, source="braspress_assisted")
        
        # Step 4: Validar preview
        assert preview is not None, "Preview deve ser gerado"
        assert preview.valid_rows >= 3, f"Deve ter pelo menos 3 linhas válidas, got {preview.valid_rows}"
        assert preview.invalid_rows == 0, f"Não deve ter linhas inválidas, got {preview.invalid_rows}"
        assert len(preview.errors) == 0, f"Não deve ter erros, got {len(preview.errors)}"
        assert preview.file_type == "csv", "Tipo de arquivo deve ser csv"
        assert preview.total_rows >= 3, f"Deve ter pelo menos 3 linhas totais, got {preview.total_rows}"
        assert preview.import_id is not None, "Preview deve ter import_id"
        
        # Step 5: Chamar confirm_import
        import_result = confirm_import(db_session, preview.import_id)
        
        # Step 6: Validar resultado da importação
        assert import_result is not None, "Importação deve ser confirmada"
        assert import_result.imported_count >= 3, f"Deve importar pelo menos 3 shipments, got {import_result.imported_count}"
        assert import_result.status == "completed", f"Status deve ser completed, got {import_result.status}"
        
        # Step 7: Validar persistência de shipments
        shipments = db_session.query(Shipment).filter(
            Shipment.tracking_code.like("SYNTH-REAL-%")
        ).all()
        
        assert len(shipments) >= 3, f"Deve ter pelo menos 3 shipments persistidos, got {len(shipments)}"
        
        for shipment in shipments:
            # Validar campos fiscais/financeiros
            assert shipment.invoice_number is not None, f"Shipment {shipment.tracking_code} deve ter invoice_number"
            assert shipment.invoice_value is not None, f"Shipment {shipment.tracking_code} deve ter invoice_value"
            assert shipment.freight_value is not None, f"Shipment {shipment.tracking_code} deve ter freight_value"
            assert shipment.invoice_value > 0, f"invoice_value deve ser positivo, got {shipment.invoice_value}"
            assert shipment.freight_value > 0, f"freight_value deve ser positivo, got {shipment.freight_value}"
            
            # Validar campos de cliente
            assert shipment.customer_name is not None, f"Shipment {shipment.tracking_code} deve ter customer_name"
            assert shipment.destination_uf is not None, f"Shipment {shipment.tracking_code} deve ter destination_uf"
            assert len(shipment.destination_uf) == 2, f"UF deve ter 2 caracteres, got {shipment.destination_uf}"
            
            # Validar transportadora
            assert shipment.carrier_id is not None, f"Shipment {shipment.tracking_code} deve ter carrier_id"
            carrier = db_session.query(Carrier).filter(Carrier.id == shipment.carrier_id).first()
            assert carrier is not None, f"Transportadora deve existir"
            assert carrier.name == "Braspress", f"Transportadora deve ser Braspress, got {carrier.name}"
