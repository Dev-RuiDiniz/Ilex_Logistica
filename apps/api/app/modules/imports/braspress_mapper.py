"""Braspress assisted import mapper for BETA-012C.

This module provides specific column mapping for Braspress assisted imports.
It extends the generic mapper with Braspress-specific column variations and validation.
"""

from typing import Dict

from app.modules.imports.mapper import (
    get_optional_columns,
    get_required_columns,
    map_column,
    normalize_column_name,
)


# BETA-012C: Braspress-specific column variations
# These are column names that are commonly used in Braspress exports
BRASPRESS_COLUMN_VARIATIONS: Dict[str, str] = {
    # Tracking code - Braspress specific
    "numero_da_entrega_ou_rastreio": "tracking_code",
    "numero_da_entrega": "tracking_code",
    "numero_rastreio": "tracking_code",
    "numero_do_rastreio": "tracking_code",
    
    # Invoice number - Braspress specific
    "numero_da_nf": "invoice_number",
    "numero_nf": "invoice_number",
    
    # Customer name - Braspress specific
    "cliente": "customer_name",
    "nome_do_cliente": "customer_name",
    "destinatario": "customer_name",
    "nome_destinatario": "customer_name",
    
    # Destination UF - Braspress specific
    "uf_destino": "destination_uf",
    "uf": "destination_uf",
    "estado_destino": "destination_uf",
    "estado": "destination_uf",
    
    # Collection departure date - Braspress specific
    "data_coleta_saida": "collection_departure_date",
    "data_de_coleta_saida": "collection_departure_date",
    "data_saida": "collection_departure_date",
    
    # Invoice value - Braspress specific
    "valor_nf": "invoice_value",
    "valor_nota_fiscal": "invoice_value",
    "valor_nota": "invoice_value",
    "valor_mercadoria": "invoice_value",
    
    # Freight value - Braspress specific
    "valor_frete": "freight_value",
    "vlr_frete": "freight_value",
    
    # Carrier - Braspress specific
    "transportadora": "carrier_name",
    "nome_transportadora": "carrier_name",
    
    # Optional fields - Braspress specific
    "previsao_de_entrega": "expected_delivery_date",
    "data_prevista_entrega": "expected_delivery_date",
    "previsao_entrega": "expected_delivery_date",
    
    "status": "status",
    "situacao": "status",
}


def map_braspress_column(column_name: str) -> str:
    """Map a Braspress column name to the internal field name.
    
    This function first tries the Braspress-specific mappings,
    then falls back to the generic mapper.
    
    Args:
        column_name: Raw column name from Braspress CSV/XLSX
        
    Returns:
        Internal field name (e.g., "tracking_code", "invoice_number")
    """
    normalized = normalize_column_name(column_name)
    
    # Try Braspress-specific mapping first
    if normalized in BRASPRESS_COLUMN_VARIATIONS:
        return BRASPRESS_COLUMN_VARIATIONS[normalized]
    
    # Fall back to generic mapper
    return map_column(column_name)


def get_braspress_required_columns() -> set[str]:
    """Get the set of required columns for Braspress import.
    
    Returns:
        Set of required internal field names for Braspress
    """
    # Braspress uses the same required columns as generic import
    return get_required_columns()


def get_braspress_optional_columns() -> set[str]:
    """Get the set of optional columns for Braspress import.
    
    Returns:
        Set of optional internal field names for Braspress
    """
    # Braspress has additional optional columns
    braspress_optional = get_optional_columns().copy()
    braspress_optional.update({
        "expected_delivery_date",
        "status",
    })
    return braspress_optional


def validate_braspress_headers(headers: list[str]) -> tuple[bool, list[str]]:
    """Validate that the headers contain all required Braspress columns.
    
    Args:
        headers: List of raw column headers from the file
        
    Returns:
        Tuple of (is_valid, list_of_missing_columns)
    """
    required = get_braspress_required_columns()
    mapped_headers = {map_braspress_column(h) for h in headers if h and h.strip()}
    
    missing = required - mapped_headers
    return len(missing) == 0, sorted(missing)


def get_braspress_source() -> str:
    """Get the source identifier for Braspress imports.
    
    Returns:
        Source string for ImportHistory
    """
    return "braspress_assisted"
