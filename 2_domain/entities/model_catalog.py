from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelCatalog:
    """Catalogo de modelos Toyota para Peru."""

    model_id: str  # id interno del modelo
    brand: str  # marca (Toyota)
    name: str  # nombre comercial del modelo
    segment: str  # segmento (SUV, sedan, etc.)
    year_start: Optional[int]  # anio de inicio en Peru
    year_end: Optional[int]  # anio de fin si aplica
    fuel_type: Optional[str]  # tipo de combustible
    transmission: Optional[str]  # tipo de transmision
    body_type: Optional[str]  # tipo de carroceria
    notes: Optional[str]  # notas adicionales
