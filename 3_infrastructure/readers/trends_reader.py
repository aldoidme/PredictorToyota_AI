from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd
from pytrends.request import TrendReq

from ._common import ReaderError, ensure_not_empty, normalize_columns, validate_columns

DEFAULT_PATH = Path("1_data/raw/trends_toyota.csv")
REQUIRED_COLUMNS = ["keyword", "region", "date", "value", "source"]


def read_trends_csv(path: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    """Lee tendencias desde un CSV local."""

    path = Path(path)
    try:
        df = pd.read_csv(path, parse_dates=["date"])
    except FileNotFoundError as exc:
        raise ReaderError(f"No se encontro el archivo: {path}") from exc
    except Exception as exc:
        raise ReaderError(f"Error leyendo tendencias: {exc}") from exc

    df = normalize_columns(df)
    validate_columns(df, REQUIRED_COLUMNS)
    ensure_not_empty(df, f"tendencias ({path})")

    return df[REQUIRED_COLUMNS]


def fetch_trends(
    keywords: Sequence[str],
    geo: str = "PE",
    timeframe: str = "today 5-y",
) -> pd.DataFrame:
    """Lee tendencias reales desde Google Trends usando pytrends."""

    try:
        trend = TrendReq(hl="es-PE", tz=300)
        trend.build_payload(list(keywords), geo=geo, timeframe=timeframe)
        data = trend.interest_over_time()
    except Exception as exc:
        raise ReaderError(f"Error leyendo Google Trends: {exc}") from exc

    ensure_not_empty(data, f"Google Trends ({geo})")

    if "isPartial" in data.columns:
        data = data.drop(columns=["isPartial"])

    data = data.reset_index()
    data = data.melt(id_vars=["date"], var_name="keyword", value_name="value")
    data["region"] = geo
    data["source"] = "pytrends"

    data = normalize_columns(data)
    validate_columns(data, REQUIRED_COLUMNS)

    return data[REQUIRED_COLUMNS]
