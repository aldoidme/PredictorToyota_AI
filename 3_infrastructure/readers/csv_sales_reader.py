from __future__ import annotations

from pathlib import Path

import pandas as pd

from ._common import ReaderError, ensure_not_empty, normalize_columns, validate_columns

DEFAULT_PATH = Path("1_data/raw/sales_monthly.csv")
REQUIRED_COLUMNS = ["model_id", "region", "period", "units_sold", "channel", "source"]


def read_sales_csv(path: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    """Lee ventas mensuales desde un CSV local."""

    path = Path(path)
    try:
        df = pd.read_csv(path, parse_dates=["period"])
    except FileNotFoundError as exc:
        raise ReaderError(f"No se encontro el archivo: {path}") from exc
    except Exception as exc:
        raise ReaderError(f"Error leyendo ventas: {exc}") from exc

    df = normalize_columns(df)
    validate_columns(df, REQUIRED_COLUMNS)
    ensure_not_empty(df, f"ventas ({path})")

    return df[REQUIRED_COLUMNS]
