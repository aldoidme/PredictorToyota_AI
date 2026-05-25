from __future__ import annotations

from typing import List

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from .confidence_utils import confidence_from_probability

REQUIRED_COLUMNS = ["symbol", "date", "close"]


def _build_features(group: pd.DataFrame) -> pd.DataFrame:
    data = group.copy()
    data = data.sort_values("date")
    data["close"] = pd.to_numeric(data["close"], errors="coerce")
    data["return_1"] = data["close"].pct_change()
    data["return_5"] = data["close"].pct_change(5)
    data["ma_5"] = data["close"].rolling(5).mean()
    data["std_5"] = data["close"].rolling(5).std()
    return data


def build_stock_trend_predictions(
    df: pd.DataFrame,
    min_rows: int = 20,
    prob_threshold: float = 0.55,
) -> pd.DataFrame:
    """Predice tendencia de acciones con RandomForest."""

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Falta columna requerida: {col}")

    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["symbol", "date", "close"])

    results: List[dict] = []

    for symbol, group in data.groupby("symbol"):
        group = _build_features(group)
        group["target"] = (group["close"].shift(-1) > group["close"]).astype(int)
        group = group.dropna(subset=["return_1", "return_5", "ma_5", "std_5", "target"])

        if len(group) < min_rows:
            results.append(
                {
                    "symbol": symbol,
                    "last_date": group["date"].max() if not group.empty else None,
                    "prob_up": None,
                    "trend": "insuficiente",
                    "confidence": 0.4,
                }
            )
            continue

        features = group[["return_1", "return_5", "ma_5", "std_5"]]
        target = group["target"]

        model = RandomForestClassifier(
            n_estimators=200, random_state=42, min_samples_leaf=2
        )
        model.fit(features, target)

        last_features = features.tail(1)
        prob_up = float(model.predict_proba(last_features)[0][1])

        if prob_up >= prob_threshold:
            trend = "sube"
        elif prob_up <= 1.0 - prob_threshold:
            trend = "baja"
        else:
            trend = "estable"

        results.append(
            {
                "symbol": symbol,
                "last_date": group["date"].max(),
                "prob_up": prob_up,
                "trend": trend,
                "confidence": confidence_from_probability(prob_up),
            }
        )

    return pd.DataFrame(results)
