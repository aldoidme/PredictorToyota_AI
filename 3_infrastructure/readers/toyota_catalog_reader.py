from __future__ import annotations

from pathlib import Path

import pandas as pd

from ._common import ReaderError, ensure_not_empty, normalize_columns, validate_columns

DEFAULT_PATH = Path("1_data/raw/toyota_catalog.csv")
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


def read_toyota_catalog_csv(path: str | Path = DEFAULT_PATH) -> pd.DataFrame:
    """Lee el catalogo Toyota desde un CSV local."""

    path = Path(path)
    try:
        df = pd.read_csv(path)
    except FileNotFoundError as exc:
        raise ReaderError(f"No se encontro el archivo: {path}") from exc
    except Exception as exc:
        raise ReaderError(f"Error leyendo catalogo: {exc}") from exc

    df = normalize_columns(df)
    validate_columns(df, REQUIRED_COLUMNS)
    ensure_not_empty(df, f"catalogo ({path})")

    return df[REQUIRED_COLUMNS]
