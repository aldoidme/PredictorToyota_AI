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
    "symbol",
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "currency",
    "source",
]


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza precios de acciones."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["date"] = normalize_date(data["date"])
    for col in ["open", "high", "low", "close", "adj_close", "volume"]:
        data[col] = coerce_numeric(data[col])

    data["symbol"] = normalize_text(data["symbol"]).str.upper()
    data["currency"] = normalize_text(data["currency"]).str.upper()
    data["source"] = normalize_text(data["source"]).str.lower()

    data = drop_missing(data, ["symbol", "date", "close"], "acciones")
    data = data.sort_values(["symbol", "date"], kind="mergesort")

    data["close_change"] = data.groupby("symbol")["close"].diff()
    data["close_pct_change"] = data.groupby("symbol")["close"].pct_change()

    return data


def prepare_stock_time_series(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara serie temporal ordenada por simbolo y fecha."""

    data = clean_stock_data(df)
    return data.set_index("date").sort_index()
