from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ["symbol", "date", "close"]


def _classify_change(pct_change: float | None, threshold: float) -> str:
    if pct_change is None:
        return "insuficiente"
    if pct_change >= threshold:
        return "sube"
    if pct_change <= -threshold:
        return "baja"
    return "estable"


def analyze_stock_trend(df: pd.DataFrame, threshold: float = 0.02) -> pd.DataFrame:
    """Analiza tendencia basica de acciones por simbolo."""

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Falta columna requerida: {col}")

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["close"] = pd.to_numeric(data["close"], errors="coerce")
    data = data.dropna(subset=["symbol", "date", "close"])
    data = data.sort_values(["symbol", "date"], kind="mergesort")

    def _calc(group: pd.DataFrame) -> pd.Series:
        symbol = group.name if "symbol" not in group.columns else group["symbol"].iloc[-1]
        if len(group) < 2:
            last_row = group.iloc[-1]
            return pd.Series(
                {
                    "symbol": symbol,
                    "last_date": last_row["date"],
                    "last_close": last_row["close"],
                    "prev_close": None,
                    "change": None,
                    "pct_change": None,
                    "trend": "insuficiente",
                }
            )

        last = group.iloc[-1]
        prev = group.iloc[-2]
        prev_close = prev["close"]
        change = last["close"] - prev_close
        pct_change = change / prev_close if prev_close else None
        trend = _classify_change(pct_change, threshold)

        return pd.Series(
            {
            "symbol": symbol,
                "last_date": last["date"],
                "last_close": last["close"],
                "prev_close": prev_close,
                "change": change,
                "pct_change": pct_change,
                "trend": trend,
            }
        )

    summary = data.groupby("symbol", as_index=False).apply(_calc)
    return summary.reset_index(drop=True)
