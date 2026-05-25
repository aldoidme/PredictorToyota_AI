from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, List
from uuid import uuid4

import pandas as pd

try:
    from entities import Recommendation
except ImportError:  # pragma: no cover
    from ..entities import Recommendation


def _confidence_from_pct(pct_change: float | None) -> float:
    if pct_change is None:
        return 0.4
    magnitude = min(abs(pct_change), 0.2)
    return float(min(0.85, 0.5 + (magnitude / 0.2) * 0.35))


def _new_recommendation(
    target_type: str,
    target_id: str | None,
    action: str,
    rationale: str,
    confidence: float,
    metadata: dict | None = None,
) -> Recommendation:
    return Recommendation(
        rec_id=f"rec-{uuid4().hex[:10]}",
        target_type=target_type,
        target_id=target_id,
        action=action,
        rationale=rationale,
        confidence=confidence,
        created_at=datetime.now(timezone.utc),
        metadata=metadata,
    )


def _build_stock_recommendations(stock_trends: pd.DataFrame) -> List[Recommendation]:
    recs: List[Recommendation] = []
    for _, row in stock_trends.iterrows():
        trend = row.get("trend")
        symbol = row.get("symbol")
        pct_change = row.get("pct_change")

        if trend == "sube":
            action = "comprar"
            rationale = "Precio en subida en el ultimo tramo."
        elif trend == "baja":
            action = "vender"
            rationale = "Precio en caida en el ultimo tramo."
        else:
            action = "mantener"
            rationale = "Variacion estable o insuficiente."

        recs.append(
            _new_recommendation(
                target_type="accion",
                target_id=str(symbol) if symbol is not None else None,
                action=action,
                rationale=rationale,
                confidence=_confidence_from_pct(pct_change),
                metadata={"pct_change": str(pct_change)} if pct_change is not None else None,
            )
        )
    return recs


def _build_demand_recommendations(demand_summary: pd.DataFrame) -> List[Recommendation]:
    recs: List[Recommendation] = []
    for _, row in demand_summary.iterrows():
        trend = row.get("demand_trend")
        model_id = row.get("model_id")
        pct_change = row.get("pct_change")

        if trend == "crece":
            action = "comprar"
            rationale = "Demanda en crecimiento."
        elif trend == "cae":
            action = "vender"
            rationale = "Demanda en caida."
        else:
            action = "mantener"
            rationale = "Demanda estable o insuficiente."

        recs.append(
            _new_recommendation(
                target_type="demanda",
                target_id=str(model_id) if model_id is not None else None,
                action=action,
                rationale=rationale,
                confidence=_confidence_from_pct(pct_change),
                metadata={"pct_change": str(pct_change)} if pct_change is not None else None,
            )
        )
    return recs


def _build_new_vs_used_recommendations(compare_df: pd.DataFrame) -> List[Recommendation]:
    recs: List[Recommendation] = []
    for _, row in compare_df.iterrows():
        model_id = row.get("model_id")
        action = row.get("recommendation")
        ratio = row.get("ratio_used_new")

        if action == "recomendable usado":
            rationale = "Mayor actividad de usados en el periodo."
        elif action == "recomendable nuevo":
            rationale = "Mayor actividad de nuevos en el periodo."
        else:
            rationale = "Comparacion equilibrada o insuficiente."

        recs.append(
            _new_recommendation(
                target_type="auto",
                target_id=str(model_id) if model_id is not None else None,
                action=str(action) if action is not None else "mantener",
                rationale=rationale,
                confidence=0.55,
                metadata={"ratio_used_new": str(ratio)} if ratio is not None else None,
            )
        )
    return recs


def build_recommendations(
    stock_trends: pd.DataFrame | None = None,
    demand_summary: pd.DataFrame | None = None,
    new_vs_used: pd.DataFrame | None = None,
) -> List[Recommendation]:
    """Genera recomendaciones simples basadas en reglas."""

    recs: List[Recommendation] = []
    if stock_trends is not None and not stock_trends.empty:
        recs.extend(_build_stock_recommendations(stock_trends))
    if demand_summary is not None and not demand_summary.empty:
        recs.extend(_build_demand_recommendations(demand_summary))
    if new_vs_used is not None and not new_vs_used.empty:
        recs.extend(_build_new_vs_used_recommendations(new_vs_used))

    return recs
