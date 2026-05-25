from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

from ._common import drop_missing, normalize_date


def to_time_series(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    group_cols: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """Prepara una serie temporal con indice de fecha."""

    data = df.copy()
    data[date_col] = normalize_date(data[date_col])
    data = drop_missing(data, [date_col, value_col], "serie temporal")

    if group_cols:
        grouped = (
            data.groupby(list(group_cols) + [date_col], dropna=False)[value_col]
            .sum()
            .reset_index()
        )
    else:
        grouped = data[[date_col, value_col]].copy()

    return grouped.set_index(date_col).sort_index()
