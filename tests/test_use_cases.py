from __future__ import annotations

from pathlib import Path

import pandas as pd

from readers import read_sales_csv, read_stock_csv, read_used_cars_csv
from processors import aggregate_monthly_sales, clean_stock_data, clean_used_cars_data
from use_cases import (
    analyze_model_demand,
    analyze_stock_trend,
    build_recommendations,
    compare_new_vs_used,
)

RAW_DIR = Path("1_data/raw")


def test_analyze_stock_trend() -> None:
    raw = read_stock_csv(RAW_DIR / "stock_toyota.csv")
    cleaned = clean_stock_data(raw)
    summary = analyze_stock_trend(cleaned)
    assert not summary.empty
    assert "trend" in summary.columns


def test_analyze_model_demand() -> None:
    raw = read_sales_csv(RAW_DIR / "sales_monthly.csv")
    monthly = aggregate_monthly_sales(raw)
    summary = analyze_model_demand(monthly)
    assert not summary.empty
    assert "demand_trend" in summary.columns


def test_compare_new_vs_used() -> None:
    used_raw = read_used_cars_csv(RAW_DIR / "used_listings.csv")
    sales_raw = read_sales_csv(RAW_DIR / "sales_monthly.csv")
    used_clean = clean_used_cars_data(used_raw)
    sales_monthly = aggregate_monthly_sales(sales_raw)
    comparison = compare_new_vs_used(used_clean, sales_monthly)
    assert not comparison.empty
    assert "recommendation" in comparison.columns


def test_build_recommendations() -> None:
    stock_trends = pd.DataFrame(
        [{"symbol": "7203.T", "trend": "sube", "pct_change": 0.05}]
    )
    demand_summary = pd.DataFrame(
        [
            {
                "model_id": "COROLLA",
                "region": "Lima",
                "demand_trend": "cae",
                "pct_change": -0.1,
            }
        ]
    )
    new_vs_used = pd.DataFrame(
        [{"model_id": "COROLLA", "recommendation": "recomendable usado"}]
    )

    recs = build_recommendations(stock_trends, demand_summary, new_vs_used)
    assert recs
    actions = {rec.action for rec in recs}
    assert {"comprar", "vender", "recomendable usado"}.issuperset(actions)
