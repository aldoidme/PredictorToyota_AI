from __future__ import annotations

from pathlib import Path

from readers import (
    read_sales_csv,
    read_stock_csv,
    read_toyota_catalog_csv,
    read_trends_csv,
    read_used_cars_csv,
)

RAW_DIR = Path("1_data/raw")


def test_read_stock_csv() -> None:
    df = read_stock_csv(RAW_DIR / "stock_toyota.csv")
    assert not df.empty
    assert {"symbol", "date", "close"}.issubset(df.columns)


def test_read_sales_csv() -> None:
    df = read_sales_csv(RAW_DIR / "sales_monthly.csv")
    assert not df.empty
    assert {"model_id", "period", "units_sold"}.issubset(df.columns)


def test_read_catalog_csv() -> None:
    df = read_toyota_catalog_csv(RAW_DIR / "toyota_catalog.csv")
    assert not df.empty
    assert {"model_id", "brand", "name"}.issubset(df.columns)


def test_read_used_cars_csv() -> None:
    df = read_used_cars_csv(RAW_DIR / "used_listings.csv")
    assert not df.empty
    assert {"listing_id", "model_name", "price_pen"}.issubset(df.columns)


def test_read_trends_csv() -> None:
    df = read_trends_csv(RAW_DIR / "trends_toyota.csv")
    assert not df.empty
    assert {"keyword", "date", "value"}.issubset(df.columns)
