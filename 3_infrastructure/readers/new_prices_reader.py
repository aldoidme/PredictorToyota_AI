from __future__ import annotations

from pathlib import Path

import pandas as pd

from ._common import ReaderError, ensure_not_empty, normalize_columns, validate_columns

DEFAULT_PATH = Path("1_data/raw/new_prices.csv")
REQUIRED_COLUMNS = ["model_id", "price_pen", "currency", "source", "as_of"]


def read_new_prices_csv(path: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    """Lee precios nuevos desde un CSV local."""

    path = Path(path)
    try:
        df = pd.read_csv(path, parse_dates=["as_of"])
    except FileNotFoundError as exc:
        raise ReaderError(f"No se encontro el archivo: {path}") from exc
    except Exception as exc:
        raise ReaderError(f"Error leyendo precios nuevos: {exc}") from exc

    df = normalize_columns(df)
    validate_columns(df, REQUIRED_COLUMNS)
    ensure_not_empty(df, f"precios nuevos ({path})")

    return df[REQUIRED_COLUMNS]
