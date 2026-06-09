"""add fiscal/financial fields to shipments - BETA-011A

Revision ID: 20260608_01
Revises: 20260515_04
Create Date: 2026-06-08
"""

from alembic import op
import sqlalchemy as sa


revision = "20260608_01"
down_revision = "20260515_04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar campos fiscais/financeiros faltantes
    op.add_column("shipments", sa.Column("freight_value", sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column("shipments", sa.Column("invoice_value", sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column("shipments", sa.Column("freight_percentage", sa.Numeric(precision=5, scale=2), nullable=True))
    op.add_column("shipments", sa.Column("collection_departure_date", sa.DateTime(), nullable=True))
    op.add_column("shipments", sa.Column("customer_name", sa.String(length=255), nullable=True))
    op.add_column("shipments", sa.Column("destination_uf", sa.String(length=2), nullable=True))
    
    # Criar índices para novos campos (apenas para campos que não têm índice no model)
    op.create_index("ix_shipments_customer_name", "shipments", ["customer_name"])
    op.create_index("ix_shipments_destination_uf", "shipments", ["destination_uf"])
    op.create_index("ix_shipments_invoice_number", "shipments", ["invoice_number"])
    # Nota: status, criticality, estimated_delivery já têm índices no model


def downgrade() -> None:
    # Remover índices
    op.drop_index("ix_shipments_invoice_number", table_name="shipments")
    op.drop_index("ix_shipments_destination_uf", table_name="shipments")
    op.drop_index("ix_shipments_customer_name", table_name="shipments")
    
    # Remover campos
    op.drop_column("shipments", "destination_uf")
    op.drop_column("shipments", "customer_name")
    op.drop_column("shipments", "collection_departure_date")
    op.drop_column("shipments", "freight_percentage")
    op.drop_column("shipments", "invoice_value")
    op.drop_column("shipments", "freight_value")
