from __future__ import annotations

import pandas as pd

REQUIRED_USED = ["listing_id", "model_id", "model_name", "posted_date", "price_pen"]
REQUIRED_SALES = ["model_id", "period", "units_sold"]


def compare_new_vs_used(
    used_df: pd.DataFrame,
    sales_df: pd.DataFrame,
    months: int = 3,
) -> pd.DataFrame:
    """Compara actividad de usados vs ventas nuevas en un periodo."""

    for col in REQUIRED_USED:
        if col not in used_df.columns:
            raise ValueError(f"Falta columna requerida en usados: {col}")
    for col in REQUIRED_SALES:
        if col not in sales_df.columns:
            raise ValueError(f"Falta columna requerida en ventas: {col}")

    used = used_df.copy()
    sales = sales_df.copy()
    used["posted_date"] = pd.to_datetime(used["posted_date"], errors="coerce")
    sales["period"] = pd.to_datetime(sales["period"], errors="coerce")

    end_date = max(used["posted_date"].max(), sales["period"].max())
    if pd.isna(end_date):
        raise ValueError("No hay fechas validas para comparar nuevo vs usado.")

    start_date = end_date - pd.DateOffset(months=months)

    used_recent = used[used["posted_date"] >= start_date]
    sales_recent = sales[sales["period"] >= start_date]

    used_counts = (
        used_recent.groupby("model_id", dropna=False)["listing_id"].nunique().rename("used_count")
    )
    new_units = (
        sales_recent.groupby("model_id", dropna=False)["units_sold"].sum().rename("new_units")
    )

    summary = pd.concat([used_counts, new_units], axis=1).fillna(0)
    summary = summary.reset_index()

    summary["ratio_used_new"] = summary.apply(
        lambda row: row["used_count"] / row["new_units"]
        if row["new_units"] > 0
        else None,
        axis=1,
    )

    def _recommend(row: pd.Series) -> str:
        used_count = row["used_count"]
        new_units = row["new_units"]
        ratio = row["ratio_used_new"]

        if new_units == 0 and used_count > 0:
            return "recomendable usado"
        if used_count == 0 and new_units > 0:
            return "recomendable nuevo"
        if ratio is None:
            return "mantener"
        if ratio >= 1.2:
            return "recomendable usado"
        if ratio <= 0.8:
            return "recomendable nuevo"
        return "mantener"

    summary["recommendation"] = summary.apply(_recommend, axis=1)

    return summary
