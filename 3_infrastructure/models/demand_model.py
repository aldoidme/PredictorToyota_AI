from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from .confidence_utils import confidence_from_r2, growth_probability

REQUIRED_COLUMNS = ["model_id", "region", "period", "units_sold"]


def build_demand_predictions(
    df: pd.DataFrame,
    min_rows: int = 6,
    threshold: float = 0.05,
) -> pd.DataFrame:
    """Predice demanda con regresion lineal simple."""

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Falta columna requerida: {col}")

    data = df.copy()
    data["period"] = pd.to_datetime(data["period"], errors="coerce")
    data["units_sold"] = pd.to_numeric(data["units_sold"], errors="coerce")
    data = data.dropna(subset=["model_id", "region", "period", "units_sold"])

    results: List[dict] = []

    for (model_id, region), group in data.groupby(["model_id", "region"]):
        group = group.sort_values("period")

        if len(group) < min_rows:
            results.append(
                {
                    "model_id": model_id,
                    "region": region,
                    "next_period": None,
                    "predicted_units": None,
                    "pct_change": None,
                    "trend": "insuficiente",
                    "prob_growth": None,
                    "confidence": 0.4,
                }
            )
            continue

        y = group["units_sold"].to_numpy()
        X = np.arange(len(y)).reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        next_index = np.array([[len(y)]])
        predicted_units = float(model.predict(next_index)[0])
        last_units = float(y[-1])
        pct_change = (predicted_units - last_units) / last_units if last_units else None

        if pct_change is None:
            trend = "insuficiente"
        elif pct_change >= threshold:
            trend = "crece"
        elif pct_change <= -threshold:
            trend = "cae"
        else:
            trend = "estable"

        r2 = model.score(X, y) if len(y) >= 3 else None
        prob_growth = growth_probability(pct_change)
        confidence = confidence_from_r2(r2)

        next_period = group["period"].max() + pd.DateOffset(months=1)

        results.append(
            {
                "model_id": model_id,
                "region": region,
                "next_period": next_period,
                "predicted_units": predicted_units,
                "pct_change": pct_change,
                "trend": trend,
                "prob_growth": prob_growth,
                "confidence": confidence,
            }
        )

    return pd.DataFrame(results)
