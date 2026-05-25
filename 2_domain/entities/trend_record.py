from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TrendRecord:
    """Serie de tendencias de busqueda para Toyota en Peru."""

    keyword: str  # palabra clave consultada
    region: str  # region geografica
    date: date  # fecha del registro
    value: int  # indice de tendencia (0-100)
    source: str  # fuente de datos
