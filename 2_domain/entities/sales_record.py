from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class SalesRecord:
    """Registro de ventas por modelo en Peru."""

    model_id: str  # referencia al catalogo
    region: str  # region o ciudad
    period: date  # periodo del reporte
    units_sold: int  # unidades vendidas
    channel: Optional[str]  # canal (concesionario, online, etc.)
    source: str  # fuente de datos
