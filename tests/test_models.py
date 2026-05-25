from __future__ import annotations

from pathlib import Path

from readers import read_sales_csv, read_stock_csv
from processors import aggregate_monthly_sales, clean_stock_data
from models import build_demand_predictions, build_stock_trend_predictions

RAW_DIR = Path("1_data/raw")


def test_build_stock_trend_predictions() -> None:
    raw = read_stock_csv(RAW_DIR / "stock_toyota.csv")
    cleaned = clean_stock_data(raw)
    preds = build_stock_trend_predictions(cleaned)
    assert not preds.empty
    assert {"symbol", "trend", "confidence"}.issubset(preds.columns)


def test_build_demand_predictions() -> None:
    raw = read_sales_csv(RAW_DIR / "sales_monthly.csv")
    monthly = aggregate_monthly_sales(raw)
    preds = build_demand_predictions(monthly)
    assert not preds.empty
    assert {"model_id", "trend", "confidence"}.issubset(preds.columns)
