"""Layout mapper for CSV/XLSX import columns.

This module provides column name mapping to normalize different column naming conventions
from various import sources to the internal field names.
"""

import unicodedata
from typing import Dict


# BETA-012A: Layout mapper for fiscal/financial fields
# Maps various column name variations to standard internal field names
COLUMN_MAPPER: Dict[str, str] = {
    # Tracking code variations
    "tracking_code": "tracking_code",
    "trackingcode": "tracking_code",
    "tracking": "tracking_code",
    "rastreio": "tracking_code",
    "codigo_rastreio": "tracking_code",
    "cod_rastreio": "tracking_code",
    "codigo_de_rastreio": "tracking_code",
    
    # Carrier ID variations
    "carrier_id": "carrier_id",
    "carrierid": "carrier_id",
    "transportadora_id": "carrier_id",
    "transportadoraid": "carrier_id",
    "id_transportadora": "carrier_id",
    "idtransportadora": "carrier_id",
    
    # Invoice number variations
    "invoice_number": "invoice_number",
    "invoicenumber": "invoice_number",
    "nf": "invoice_number",
    "nota_fiscal": "invoice_number",
    "notafiscal": "invoice_number",
    "numero_nf": "invoice_number",
    "numeronf": "invoice_number",
    "numero_nota_fiscal": "invoice_number",
    
    # Invoice value variations
    "invoice_value": "invoice_value",
    "invoicevalue": "invoice_value",
    "valor_nf": "invoice_value",
    "valornf": "invoice_value",
    "valor_nota_fiscal": "invoice_value",
    "valor_nota": "invoice_value",
    "valornota": "invoice_value",
    "valor_mercadoria": "invoice_value",
    "valormercadoria": "invoice_value",
    
    # Freight value variations
    "freight_value": "freight_value",
    "freightvalue": "freight_value",
    "valor_frete": "freight_value",
    "valorfrete": "freight_value",
    "frete": "freight_value",
    "vlr_frete": "freight_value",
    "vlrfrete": "freight_value",
    
    # Collection departure date variations
    "collection_departure_date": "collection_departure_date",
    "collectiondeparturedate": "collection_departure_date",
    "data_coleta": "collection_departure_date",
    "datacoleta": "collection_departure_date",
    "data_de_coleta": "collection_departure_date",
    "dt_coleta": "collection_departure_date",
    "dtcoleta": "collection_departure_date",
    
    # Customer name variations
    "customer_name": "customer_name",
    "customername": "customer_name",
    "cliente": "customer_name",
    "nome_cliente": "customer_name",
    "nomecliente": "customer_name",
    "destinatario": "customer_name",
    "nome_destinatario": "customer_name",
    
    # Destination UF variations
    "destination_uf": "destination_uf",
    "destinationuf": "destination_uf",
    "uf": "destination_uf",
    "uf_destino": "destination_uf",
    "ufdestino": "destination_uf",
    "estado": "destination_uf",
    "estado_destino": "destination_uf",
    
    # Legacy fields (for backward compatibility)
    "transportadora": "carrier_name",  # Will be resolved to carrier_id
    "percentual_frete": "freight_percentage",  # Will be calculated from freight_value/invoice_value
    
    # BETA-012C: Braspress assisted layout specific mappings
    # These are Brazilian Portuguese column names commonly used in Braspress exports
    "numero_da_entrega_ou_rastreio": "tracking_code",
    "numero_da_entrega": "tracking_code",
    "numero_rastreio": "tracking_code",
    "numero_do_rastreio": "tracking_code",
    
    "numero_da_nf": "invoice_number",
    "nome_do_cliente": "customer_name",
    
    "data_coleta_saida": "collection_departure_date",
    "data_de_coleta_saida": "collection_departure_date",
    "data_saida": "collection_departure_date",
    
    "nome_transportadora": "carrier_name",
    
    # BETA-012C: Optional fields for Braspress
    "previsao_de_entrega": "expected_delivery_date",
    "data_prevista_entrega": "expected_delivery_date",
    "previsao_entrega": "expected_delivery_date",
    
    "status": "status",
    "situacao": "status",
}


def normalize_column_name(column_name: str) -> str:
    """Normalize column name to standard format.
    
    Args:
        column_name: Raw column name from CSV/XLSX
        
    Returns:
        Normalized column name (lowercase, no accents, underscores instead of spaces)
    """
    if not column_name:
        return ""
    
    # Convert to lowercase
    normalized = column_name.lower().strip()
    
    # Remove accents
    normalized = unicodedata.normalize("NFD", normalized)
    normalized = "".join(
        char for char in normalized 
        if unicodedata.category(char) != "Mn"
    )
    
    # Replace spaces and special chars with underscores
    normalized = "".join(
        char if char.isalnum() else "_" 
        for char in normalized
    )
    
    # Remove consecutive underscores
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    
    # Strip leading/trailing underscores
    normalized = normalized.strip("_")
    
    return normalized


def map_column(column_name: str) -> str:
    """Map a column name to the internal field name.
    
    Args:
        column_name: Raw column name from CSV/XLSX
        
    Returns:
        Internal field name (e.g., "tracking_code", "invoice_number")
    """
    normalized = normalize_column_name(column_name)
    
    # Return mapped name if exists, otherwise return normalized
    return COLUMN_MAPPER.get(normalized, normalized)


def get_required_columns() -> set[str]:
    """Get the set of required columns for import.
    
    Returns:
        Set of required internal field names
    """
    return {
        "tracking_code",
        "carrier_id",
        "invoice_number",
        "invoice_value",
        "freight_value",
        "collection_departure_date",
        "customer_name",
        "destination_uf",
    }


def get_optional_columns() -> set[str]:
    """Get the set of optional columns for import.
    
    Returns:
        Set of optional internal field names
    """
    return {
        "expected_delivery_date",  # BETA-012C: Optional for Braspress
        "status",  # BETA-012C: Optional for Braspress
    }
