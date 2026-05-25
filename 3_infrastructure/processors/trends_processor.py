from __future__ import annotations

import pandas as pd

from ._common import (
    coerce_numeric,
    drop_missing,
    ensure_columns,
    normalize_date,
    normalize_text,
)

REQUIRED_COLUMNS = ["keyword", "region", "date", "value", "source"]


def clean_trends_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza series de tendencias."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["date"] = normalize_date(data["date"])
    data["value"] = coerce_numeric(data["value"])

    data["keyword"] = normalize_text(data["keyword"]).str.lower()
    data["region"] = normalize_text(data["region"]).str.upper()
    data["source"] = normalize_text(data["source"]).str.lower()

    data = drop_missing(data, ["keyword", "date", "value"], "tendencias")

    return data[REQUIRED_COLUMNS]
