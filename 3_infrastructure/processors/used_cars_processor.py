from __future__ import annotations

import pandas as pd

from ._common import (
    coerce_numeric,
    drop_missing,
    ensure_columns,
    normalize_date,
    normalize_text,
)

REQUIRED_COLUMNS = [
    "listing_id",
    "model_id",
    "model_name",
    "year",
    "mileage_km",
    "price_pen",
    "location",
    "condition",
    "posted_date",
    "source_url",
    "source",
]


def clean_used_cars_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza avisos de autos usados."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["posted_date"] = normalize_date(data["posted_date"])
    data["year"] = coerce_numeric(data["year"])
    data["mileage_km"] = coerce_numeric(data["mileage_km"])
    data["price_pen"] = coerce_numeric(data["price_pen"])

    data["listing_id"] = normalize_text(data["listing_id"]).str.upper()
    data["model_id"] = normalize_text(data["model_id"]).str.upper()
    data["model_name"] = normalize_text(data["model_name"]).str.title()
    data["location"] = normalize_text(data["location"]).str.title()
    data["condition"] = normalize_text(data["condition"]).str.lower()
    data["source"] = normalize_text(data["source"]).str.lower()

    data = drop_missing(data, ["listing_id", "model_name", "year", "price_pen"], "usados")

    return data[REQUIRED_COLUMNS]
