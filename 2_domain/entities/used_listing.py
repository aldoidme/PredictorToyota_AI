from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class UsedListing:
    """Aviso de auto Toyota usado en Peru."""

    listing_id: str  # id del aviso
    model_id: Optional[str]  # referencia al catalogo si existe
    model_name: str  # nombre del modelo publicado
    year: int  # anio del vehiculo
    mileage_km: Optional[int]  # kilometraje
    price_pen: float  # precio en soles
    location: str  # ubicacion del aviso
    condition: Optional[str]  # estado (bueno, regular, etc.)
    posted_date: date  # fecha de publicacion
    source_url: Optional[str]  # enlace del aviso
    source: str  # fuente de datos
