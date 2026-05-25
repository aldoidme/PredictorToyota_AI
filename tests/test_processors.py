from __future__ import annotations

from pathlib import Path

from readers import (
    read_sales_csv,
    read_stock_csv,
    read_toyota_catalog_csv,
    read_trends_csv,
    read_used_cars_csv,
)
from processors import (
    aggregate_monthly_sales,
    clean_catalog_data,
    clean_sales_data,
    clean_stock_data,
    clean_trends_data,
    clean_used_cars_data,
)

RAW_DIR = Path("1_data/raw")


def test_clean_stock_data() -> None:
    raw = read_stock_csv(RAW_DIR / "stock_toyota.csv")
    cleaned = clean_stock_data(raw)
    assert not cleaned.empty
    assert cleaned["date"].isna().sum() == 0
    assert {"close", "close_change", "close_pct_change"}.issubset(cleaned.columns)


def test_aggregate_monthly_sales() -> None:
    raw = read_sales_csv(RAW_DIR / "sales_monthly.csv")
    cleaned = clean_sales_data(raw)
    monthly = aggregate_monthly_sales(cleaned)
    assert not monthly.empty
    assert {"units_change", "units_pct_change"}.issubset(monthly.columns)


def test_clean_catalog_data() -> None:
    raw = read_toyota_catalog_csv(RAW_DIR / "toyota_catalog.csv")
    cleaned = clean_catalog_data(raw)
    assert not cleaned.empty
    assert cleaned["model_id"].isna().sum() == 0


def test_clean_used_cars_data() -> None:
    raw = read_used_cars_csv(RAW_DIR / "used_listings.csv")
    cleaned = clean_used_cars_data(raw)
    assert not cleaned.empty
    assert cleaned["price_pen"].isna().sum() == 0


def test_clean_trends_data() -> None:
    raw = read_trends_csv(RAW_DIR / "trends_toyota.csv")
    cleaned = clean_trends_data(raw)
    assert not cleaned.empty
    assert cleaned["value"].isna().sum() == 0
