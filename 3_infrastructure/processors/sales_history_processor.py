from __future__ import annotations

import pandas as pd

from ._common import (
    coerce_numeric,
    drop_missing,
    ensure_columns,
    normalize_date,
    normalize_model_id,
    normalize_text,
)

REQUIRED_COLUMNS = ["model_id", "region", "period", "units_sold", "source"]


def clean_sales_history_data(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y normaliza ventas historicas."""

    ensure_columns(df, REQUIRED_COLUMNS)

    data = df.copy()
    data["model_id"] = normalize_model_id(data["model_id"])
    data["region"] = normalize_text(data["region"]).str.title()
    data["period"] = normalize_date(data["period"])
    data["units_sold"] = coerce_numeric(data["units_sold"])
    data["source"] = normalize_text(data["source"]).str.lower()

    data = drop_missing(data, ["model_id", "region", "period", "units_sold"], "ventas historicas")

    return data[REQUIRED_COLUMNS]
