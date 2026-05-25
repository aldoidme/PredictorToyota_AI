from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Prediction:
    """Resultado numerico de una prediccion."""

    pred_id: str  # id de la prediccion
    target_type: str  # tipo (accion, demanda, precio_usado)
    target_id: Optional[str]  # id del objetivo si aplica
    horizon: str  # horizonte temporal (ej: 3M, 6M)
    predicted_value: float  # valor estimado
    unit: str  # unidad del valor
    created_at: datetime  # fecha de creacion
    model_version: Optional[str]  # version del modelo
    features_ref: Optional[str]  # referencia de features
