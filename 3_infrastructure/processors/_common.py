from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd


class ProcessorError(RuntimeError):
    """Error controlado de procesamiento."""


def ensure_columns(df: pd.DataFrame, required: Sequence[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        missing_list = ", ".join(missing)
        raise ProcessorError(f"Faltan columnas requeridas: {missing_list}")


def ensure_not_empty(df: pd.DataFrame, context: str) -> None:
    if df.empty:
        raise ProcessorError(f"No hay datos en {context}.")


def normalize_text(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()


MODEL_NAME_MAP = {
    "HILUX": "HILUX",
    "YARIS": "YARIS",
    "COROLLA": "COROLLA",
    "AVANZA": "AVANZA",
    "RAV4": "RAV4",
    "ETIOS": "ETIOS",
    "RUSH": "RUSH",
    "FORTUNER": "FORTUNER",
    "RAIZE": "RAIZE",
    "COROLLA CROSS": "COROLLA_CROSS",
}


def normalize_model_name(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip().upper()
    if not cleaned or cleaned == "NAN":
        return None
    for token in ["TOYOTA ", "TOYOTA-"]:
        if cleaned.startswith(token):
            cleaned = cleaned.replace(token, "", 1)
    cleaned = cleaned.replace("_", " ").replace("-", " ")
    cleaned = " ".join(cleaned.split())
    return cleaned


def normalize_model_id(series: pd.Series) -> pd.Series:
    def _map(value: str | None) -> str | None:
        name = normalize_model_name(value)
        if not name:
            return None
        return MODEL_NAME_MAP.get(name, name.replace(" ", "_"))

    return series.apply(_map)


def normalize_currency(series: pd.Series) -> pd.Series:
    def _map(value: str | None) -> str | None:
        if value is None:
            return None
        raw = str(value).strip().upper()
        if raw in {"PEN", "S/", "S/.", "SOLES", "SOL"}:
            return "PEN"
        if raw in {"USD", "US$", "$"}:
            return "USD"
        return None

    return series.apply(_map)


def normalize_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def drop_missing(df: pd.DataFrame, columns: Iterable[str], context: str) -> pd.DataFrame:
    cleaned = df.dropna(subset=list(columns))
    ensure_not_empty(cleaned, context)
    return cleaned
