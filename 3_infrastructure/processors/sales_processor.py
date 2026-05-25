from __future__ import annotations

import pandas as pd

from ._common import (
    coerce_numeric,
    drop_missing,
    ensure_columns,
    normalize_date,
    normalize_text,
)

REQUIRED_COLUMNS = ["model_id", "region", "period", "units_sold", "channel", "source"]


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza ventas mensuales."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["period"] = normalize_date(data["period"])
    data["units_sold"] = coerce_numeric(data["units_sold"])

    data["model_id"] = normalize_text(data["model_id"]).str.upper()
    data["region"] = normalize_text(data["region"]).str.title()
    data["channel"] = normalize_text(data["channel"]).str.lower()
    data["source"] = normalize_text(data["source"]).str.lower()

    data = drop_missing(data, ["model_id", "region", "period", "units_sold"], "ventas")

    return data


def aggregate_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa ventas por mes y calcula variaciones."""

    data = clean_sales_data(df)
    data["period"] = data["period"].dt.to_period("M").dt.to_timestamp()

    grouped = (
        data.groupby(["model_id", "region", "channel", "period"], dropna=False)[
            "units_sold"
        ]
        .sum()
        .reset_index()
    )

    grouped = grouped.sort_values(["model_id", "region", "period"], kind="mergesort")
    grouped["units_change"] = grouped.groupby(["model_id", "region"])["units_sold"].diff()
    grouped["units_pct_change"] = grouped.groupby(["model_id", "region"])[
        "units_sold"
    ].pct_change()

    return grouped