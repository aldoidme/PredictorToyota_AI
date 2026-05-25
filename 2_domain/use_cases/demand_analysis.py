from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ["model_id", "region", "period", "units_sold"]


def analyze_model_demand(
    df: pd.DataFrame, window: int = 3, threshold: float = 0.1
) -> pd.DataFrame:
    """Analiza demanda por modelo y region con ventanas simples."""

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Falta columna requerida: {col}")

    data = df.copy()
    data["period"] = pd.to_datetime(data["period"], errors="coerce")
    data["units_sold"] = pd.to_numeric(data["units_sold"], errors="coerce")
    data = data.dropna(subset=["model_id", "region", "period", "units_sold"])
    data = data.sort_values(["model_id", "region", "period"], kind="mergesort")

    rows = []
    for (model_id, region), group in data.groupby(["model_id", "region"]):
        group = group.sort_values("period")
        last_period = group["period"].max()

        if len(group) < window:
            last_sum = group["units_sold"].sum()
            rows.append(
                {
                    "model_id": model_id,
                    "region": region,
                    "last_period": last_period,
                    "last_units": last_sum,
                    "prev_units": None,
                    "pct_change": None,
                    "demand_trend": "insuficiente",
                }
            )
            continue

        last_slice = group.tail(window)
        prev_slice = group.iloc[-(2 * window) : -window]
        last_sum = last_slice["units_sold"].sum()
        prev_sum = prev_slice["units_sold"].sum() if len(prev_slice) else None

        if prev_sum in (None, 0):
            pct_change = None
            demand_trend = "crece" if last_sum > 0 else "estable"
        else:
            pct_change = (last_sum - prev_sum) / prev_sum
            if pct_change >= threshold:
                demand_trend = "crece"
            elif pct_change <= -threshold:
                demand_trend = "cae"
            else:
                demand_trend = "estable"

        rows.append(
            {
                "model_id": model_id,
                "region": region,
                "last_period": last_period,
                "last_units": last_sum,
                "prev_units": prev_sum,
                "pct_change": pct_change,
                "demand_trend": demand_trend,
            }
        )

    return pd.DataFrame(rows)
