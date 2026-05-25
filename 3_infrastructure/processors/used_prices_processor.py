from __future__ import annotations

import pandas as pd

from ._common import (
    coerce_numeric,
    drop_missing,
    ensure_columns,
    normalize_currency,
    normalize_date,
    normalize_model_id,
    normalize_text,
)

REQUIRED_COLUMNS = ["model_id", "price_pen", "currency", "source", "as_of"]


def clean_used_prices_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza precios usados."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()

    if "model_name" in data.columns:
        model_source = data["model_id"].where(
            data["model_id"].notna() & data["model_id"].astype(str).str.strip().ne(""),
            data["model_name"],
        )
        data["model_id"] = normalize_model_id(model_source)
    else:
        data["model_id"] = normalize_model_id(data["model_id"])

    data["price_pen"] = coerce_numeric(data["price_pen"])
    data["currency"] = normalize_currency(data["currency"])
    data["source"] = normalize_text(data["source"]).str.lower()
    data["as_of"] = normalize_date(data["as_of"])

    data = drop_missing(data, ["model_id", "price_pen", "currency", "as_of"], "precios usados")
    data = data[data["currency"] == "PEN"]
    data = drop_missing(data, ["model_id", "price_pen"], "precios usados")

    return data[REQUIRED_COLUMNS]
