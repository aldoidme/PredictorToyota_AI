from __future__ import annotations

from typing import Optional

import pandas as pd
import yfinance as yf

from ._common import ReaderError, ensure_not_empty, validate_columns

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


def fetch_yahoo_finance(
    symbol: str,
    start: str,
    end: Optional[str] = None,
    currency: Optional[str] = None,
) -> pd.DataFrame:
    """Lee precios reales desde Yahoo Finance usando yfinance."""

    try:
        df = yf.download(symbol, start=start, end=end, auto_adjust=False, progress=False)
    except Exception as exc:
        raise ReaderError(f"Error leyendo Yahoo Finance: {exc}") from exc

    ensure_not_empty(df, f"Yahoo Finance ({symbol})")

    df = df.reset_index()
    source_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    missing = [col for col in source_columns if col not in df.columns]
    if missing:
        missing_list = ", ".join(missing)
        raise ReaderError(f"Faltan columnas en Yahoo Finance: {missing_list}")

    df = df.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
    )

    df["symbol"] = symbol
    df["currency"] = currency
    df["source"] = "yfinance"

    validate_columns(df, REQUIRED_COLUMNS)
    return df[REQUIRED_COLUMNS]
