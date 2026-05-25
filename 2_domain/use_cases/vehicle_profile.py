from __future__ import annotations

from typing import Any

import pandas as pd


def _latest_price_map(df: pd.DataFrame | None) -> dict[str, float]:
    if df is None or df.empty:
        return {}
    data = df.copy()
    if "as_of" in data.columns:
        data["as_of"] = pd.to_datetime(data["as_of"], errors="coerce")
    data = data.dropna(subset=["model_id", "price_pen"])
    data = data.sort_values(["model_id", "as_of"], kind="mergesort")
    latest = data.groupby("model_id").tail(1)
    return dict(zip(latest["model_id"], latest["price_pen"]))


def _sales_summary_map(df: pd.DataFrame | None) -> dict[str, dict[str, Any]]:
    if df is None or df.empty:
        return {}
    data = df.copy()
    if "period" in data.columns:
        data["period"] = pd.to_datetime(data["period"], errors="coerce")
    data = data.dropna(subset=["model_id", "units_sold"])
    data = data.sort_values(["model_id", "period"], kind="mergesort")

    summary: dict[str, dict[str, Any]] = {}
    for model_id, group in data.groupby("model_id"):
        total_units = float(group["units_sold"].sum())
        last_period = group["period"].max()
        last_units = (
            float(group.loc[group["period"] == last_period, "units_sold"].sum())
            if pd.notna(last_period)
            else None
        )
        summary[model_id] = {
            "sales_total": total_units,
            "sales_last_period": last_units,
            "sales_last_period_date": last_period,
        }
    return summary


def _trend_from_inputs(demand_trend: str | None, prediction_trend: str | None) -> str:
    if prediction_trend:
        return prediction_trend
    if demand_trend:
        return demand_trend
    return "estable"


def _status_from_inputs(demand_trend: str | None, recommendation: str | None) -> str:
    if demand_trend == "crece":
        return "positivo"
    if demand_trend == "cae":
        return "negativo"
    if recommendation in {"recomendable nuevo", "recomendable usado"}:
        return "positivo"
    return "estable"


def build_vehicle_profiles(
    catalog_df: pd.DataFrame,
    demand_summary: pd.DataFrame,
    new_vs_used: pd.DataFrame,
    sales_history: pd.DataFrame | None = None,
    new_prices: pd.DataFrame | None = None,
    used_prices: pd.DataFrame | None = None,
    demand_predictions: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    """Construye un perfil unificado por modelo Toyota."""

    if "model_id" not in catalog_df.columns:
        raise ValueError("Falta columna requerida: model_id")
    if "name" not in catalog_df.columns:
        raise ValueError("Falta columna requerida: name")

    price_new_map = _latest_price_map(new_prices)
    price_used_map = _latest_price_map(used_prices)
    sales_summary_map = _sales_summary_map(sales_history)

    demand_map = {}
    if demand_summary is not None and not demand_summary.empty:
        for _, row in demand_summary.iterrows():
            demand_map[row.get("model_id")] = row

    compare_map = {}
    if new_vs_used is not None and not new_vs_used.empty:
        for _, row in new_vs_used.iterrows():
            compare_map[row.get("model_id")] = row

    prediction_map = {}
    if demand_predictions is not None and not demand_predictions.empty:
        for _, row in demand_predictions.iterrows():
            prediction_map[row.get("model_id")] = row

    profiles: list[dict[str, Any]] = []
    for _, row in catalog_df.iterrows():
        model_id = row.get("model_id")
        name = row.get("name")

        demand_row = demand_map.get(model_id)
        compare_row = compare_map.get(model_id)
        prediction_row = prediction_map.get(model_id)
        sales_summary = sales_summary_map.get(model_id, {})

        demand_trend = demand_row.get("demand_trend") if demand_row is not None else None
        prediction_trend = prediction_row.get("trend") if prediction_row is not None else None
        recommendation = compare_row.get("recommendation") if compare_row is not None else "mantener"

        profiles.append(
            {
                "model_id": model_id,
                "name": name,
                "price_new": price_new_map.get(model_id),
                "price_used": price_used_map.get(model_id),
                "demand_trend": demand_trend,
                "sales_total": sales_summary.get("sales_total"),
                "sales_last_period": sales_summary.get("sales_last_period"),
                "sales_last_period_date": sales_summary.get("sales_last_period_date"),
                "trend": _trend_from_inputs(demand_trend, prediction_trend),
                "recommendation": recommendation,
                "status": _status_from_inputs(demand_trend, recommendation),
            }
        )

    return profiles
