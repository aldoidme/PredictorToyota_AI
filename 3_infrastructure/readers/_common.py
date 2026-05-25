from __future__ import annotations

from typing import Sequence

import pandas as pd


class ReaderError(RuntimeError):
    """Error controlado de lectura de datos."""


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]
    return df


def validate_columns(df: pd.DataFrame, required: Sequence[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        missing_list = ", ".join(missing)
        raise ReaderError(f"Faltan columnas requeridas: {missing_list}")


def ensure_not_empty(df: pd.DataFrame, context: str) -> None:
    if df.empty:
        raise ReaderError(f"No hay datos en {context}.")
