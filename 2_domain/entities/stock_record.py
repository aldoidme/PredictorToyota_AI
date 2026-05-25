from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class StockRecord:
    """Registro diario de acciones de Toyota."""

    symbol: str  # ticker de la accion
    date: date  # fecha del registro
    open: float  # precio de apertura
    high: float  # precio maximo del dia
    low: float  # precio minimo del dia
    close: float  # precio de cierre
    adj_close: Optional[float]  # cierre ajustado si aplica
    volume: int  # volumen negociado
    currency: str  # moneda (ej: JPY, USD)
    source: str  # fuente de datos
