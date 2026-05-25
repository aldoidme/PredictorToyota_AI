from __future__ import annotations

from typing import Optional


def growth_probability(pct_change: Optional[float], scale: float = 0.3) -> float:
    """Probabilidad simple de crecimiento segun el cambio porcentual."""

    if pct_change is None:
        return 0.5

    magnitude = min(abs(pct_change) / scale, 1.0)
    base = 0.5 + (0.4 * magnitude)
    return base if pct_change >= 0 else 1.0 - base


def confidence_from_probability(prob: float, min_conf: float = 0.5, max_conf: float = 0.85) -> float:
    """Confianza basada en la distancia a 0.5."""

    distance = min(abs(prob - 0.5) / 0.5, 1.0)
    return min_conf + (max_conf - min_conf) * distance


def confidence_from_r2(r2: Optional[float], min_conf: float = 0.4, max_conf: float = 0.85) -> float:
    """Confianza basada en r2 del modelo."""

    if r2 is None:
        return min_conf

    value = max(0.0, min(1.0, r2))
    return min_conf + (max_conf - min_conf) * value
