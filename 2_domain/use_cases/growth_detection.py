from __future__ import annotations

from typing import Optional

import pandas as pd


def detect_growth(
    series: pd.Series,
    window: int = 3,
    threshold: float = 0.05,
) -> dict:
    """Detecta crecimiento o caida usando ventanas simples."""

    data = pd.to_numeric(series, errors="coerce").dropna()
    if len(data) < window:
        return {
            "trend": "insuficiente",
            "pct_change": None,
            "last_mean": None,
            "prev_mean": None,
            "window": window,
        }

    last = data.tail(window).mean()
    prev = data.iloc[-(2 * window) : -window].mean() if len(data) >= 2 * window else None

    if prev in (None, 0):
        pct_change = None
        trend = "crece" if last > 0 else "estable"
    else:
        pct_change = (last - prev) / prev
        if pct_change >= threshold:
            trend = "crece"
        elif pct_change <= -threshold:
            trend = "cae"
        else:
            trend = "estable"

    return {
        "trend": trend,
        "pct_change": pct_change,
        "last_mean": float(last) if last is not None else None,
        "prev_mean": float(prev) if prev is not None else None,
        "window": window,
    }
