from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass(frozen=True)
class Recommendation:
    """Recomendacion accionable del sistema."""

    rec_id: str  # id de la recomendacion
    target_type: str  # tipo (accion, auto_nuevo, auto_usado)
    target_id: Optional[str]  # id del objetivo si aplica
    action: str  # accion sugerida (comprar, mantener, vender)
    rationale: str  # explicacion principal
    confidence: float  # nivel de confianza (0-1)
    created_at: datetime  # fecha de creacion
    metadata: Optional[Dict[str, str]]  # datos extra
