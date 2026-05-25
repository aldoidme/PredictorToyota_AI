from __future__ import annotations

import pandas as pd

from ._common import coerce_numeric, drop_missing, ensure_columns, normalize_text

REQUIRED_COLUMNS = [
    "model_id",
    "brand",
    "name",
    "segment",
    "year_start",
    "year_end",
    "fuel_type",
    "transmission",
    "body_type",
    "notes",
]


def clean_catalog_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza el catalogo Toyota."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["model_id"] = normalize_text(data["model_id"]).str.upper()
    data["brand"] = normalize_text(data["brand"]).str.title()
    data["name"] = normalize_text(data["name"]).str.title()
    data["segment"] = normalize_text(data["segment"]).str.title()
    data["fuel_type"] = normalize_text(data["fuel_type"]).str.title()
    data["transmission"] = normalize_text(data["transmission"]).str.title()
    data["body_type"] = normalize_text(data["body_type"]).str.title()

    data["year_start"] = coerce_numeric(data["year_start"])
    data["year_end"] = coerce_numeric(data["year_end"])

    data = drop_missing(data, ["model_id", "name"], "catalogo")

    return data[REQUIRED_COLUMNS]
