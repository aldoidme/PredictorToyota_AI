from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import sys

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
DOMAIN_DIR = ROOT_DIR / "2_domain"
INFRA_DIR = ROOT_DIR / "3_infrastructure"
PRESENTATION_DIR = ROOT_DIR / "4_presentation"

for path in [ROOT_DIR, DOMAIN_DIR, INFRA_DIR, PRESENTATION_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from config import settings
from readers import (
    fetch_trends,
    fetch_yahoo_finance,
    read_new_prices_csv,
    read_sales_csv,
    read_sales_history_csv,
    read_stock_csv,
    read_toyota_catalog_csv,
    read_trends_csv,
    read_used_cars_csv,
    read_used_prices_csv,
)
from processors import (
    aggregate_monthly_sales,
    clean_catalog_data,
    clean_new_prices_data,
    clean_sales_data,
    clean_sales_history_data,
    clean_stock_data,
    clean_trends_data,
    clean_used_cars_data,
    clean_used_prices_data,
)
from models import build_demand_predictions, build_stock_trend_predictions
from plot_builders import (
    build_demand_chart,
    build_new_vs_used_chart,
    build_predictions_chart,
    build_stock_chart,
    build_trends_chart,
)
from dashboard_renderer import render_dashboard
from use_cases import (
    analyze_model_demand,
    analyze_stock_trend,
    compare_new_vs_used,
    build_recommendations,
    build_vehicle_profiles,
)


def load_config() -> dict[str, Any]:
    """Carga configuracion desde settings."""

    return {
        "raw_dir": Path(settings.RAW_DATA_DIR),
        "dashboard_template": Path(settings.DASHBOARD_TEMPLATE),
        "dashboard_output": Path(settings.DASHBOARD_OUTPUT),
        "stock_source": settings.STOCK_SOURCE,
        "stock_symbol": settings.STOCK_SYMBOL,
        "stock_start": settings.STOCK_START,
        "stock_currency": settings.STOCK_CURRENCY,
        "trends_source": settings.TRENDS_SOURCE,
        "trends_keywords": settings.TRENDS_KEYWORDS,
        "trends_geo": settings.TRENDS_GEO,
        "trends_timeframe": settings.TRENDS_TIMEFRAME,
    }


def read_data(config: dict[str, Any]) -> dict[str, pd.DataFrame]:
    """Lee los datos desde fuentes configuradas."""

    if config["stock_source"] == "yfinance":
        stock_df = fetch_yahoo_finance(
            symbol=config["stock_symbol"],
            start=config["stock_start"],
            end=None,
            currency=config["stock_currency"],
        )
    else:
        stock_df = read_stock_csv(config["raw_dir"] / "stock_toyota.csv")

    if config["trends_source"] == "pytrends":
        trends_df = fetch_trends(
            keywords=config["trends_keywords"],
            geo=config["trends_geo"],
            timeframe=config["trends_timeframe"],
        )
    else:
        trends_df = read_trends_csv(config["raw_dir"] / "trends_toyota.csv")

    return {
        "stock": stock_df,
        "sales": read_sales_csv(config["raw_dir"] / "sales_monthly.csv"),
        "sales_history": read_sales_history_csv(config["raw_dir"] / "sales_history.csv"),
        "catalog": read_toyota_catalog_csv(config["raw_dir"] / "toyota_catalog.csv"),
        "used": read_used_cars_csv(config["raw_dir"] / "used_listings.csv"),
        "new_prices": read_new_prices_csv(config["raw_dir"] / "new_prices.csv"),
        "used_prices": read_used_prices_csv(config["raw_dir"] / "used_prices.csv"),
        "trends": trends_df,
    }


def clean_data(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Limpia y normaliza los datasets."""

    return {
        "stock": clean_stock_data(raw["stock"]),
        "sales": clean_sales_data(raw["sales"]),
        "sales_history": clean_sales_history_data(raw["sales_history"]),
        "catalog": clean_catalog_data(raw["catalog"]),
        "used": clean_used_cars_data(raw["used"]),
        "new_prices": clean_new_prices_data(raw["new_prices"]),
        "used_prices": clean_used_prices_data(raw["used_prices"]),
        "trends": clean_trends_data(raw["trends"]),
    }


def process_data(cleaned: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Procesa datos para analisis y graficos."""

    return {
        "sales_monthly": aggregate_monthly_sales(cleaned["sales"]),
    }


def run_analysis(cleaned: dict[str, pd.DataFrame], processed: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Ejecuta analisis con reglas simples."""

    stock_trends = analyze_stock_trend(cleaned["stock"])
    demand_summary = analyze_model_demand(processed["sales_monthly"])
    new_vs_used = compare_new_vs_used(cleaned["used"], processed["sales_monthly"])

    return {
        "stock_trends": stock_trends,
        "demand_summary": demand_summary,
        "new_vs_used": new_vs_used,
    }


def run_predictions(cleaned: dict[str, pd.DataFrame], processed: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Ejecuta modelos predictivos simples."""

    return {
        "stock_pred": build_stock_trend_predictions(cleaned["stock"]),
        "demand_pred": build_demand_predictions(processed["sales_monthly"]),
    }


def _format_value(value: Any, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "--"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _table_from_df(title: str, df: pd.DataFrame, columns: list[str], max_rows: int = 8) -> dict[str, Any]:
    subset = df.reindex(columns=columns).head(max_rows).copy()
    subset = subset.fillna("--")
    rows = [[_format_value(cell) for cell in row] for row in subset.to_numpy()]
    return {"title": title, "columns": columns, "rows": rows}


def build_context(
    cleaned: dict[str, pd.DataFrame],
    processed: dict[str, pd.DataFrame],
    analysis: dict[str, pd.DataFrame],
    predictions: dict[str, pd.DataFrame],
) -> dict[str, Any]:
    """Construye el contexto para el dashboard."""

    stock_trends = analysis["stock_trends"]
    demand_summary = analysis["demand_summary"]
    new_vs_used = analysis["new_vs_used"]

    recommendations = build_recommendations(stock_trends, demand_summary, new_vs_used)
    vehicle_profiles = build_vehicle_profiles(
        catalog_df=cleaned["catalog"],
        demand_summary=demand_summary,
        new_vs_used=new_vs_used,
        sales_history=cleaned.get("sales_history"),
        new_prices=cleaned.get("new_prices"),
        used_prices=cleaned.get("used_prices"),
        demand_predictions=predictions.get("demand_pred"),
    )

    def _action_class(action: str) -> str:
        action_lower = action.lower()
        if "comprar" in action_lower:
            return "chip-buy"
        if "vender" in action_lower:
            return "chip-sell"
        if "mantener" in action_lower:
            return "chip-hold"
        return "chip-neutral"

    rec_cards = [
        {
            "title": f"{rec.target_type}: {rec.target_id}",
            "action": rec.action,
            "action_class": _action_class(rec.action),
            "detail": rec.rationale,
            "confidence": _format_value(rec.confidence, 2),
        }
        for rec in recommendations[:6]
    ]

    total_models = cleaned["catalog"]["model_id"].nunique()

    stock_sorted = cleaned["stock"].sort_values("date")
    last_close = stock_sorted["close"].iloc[-1] if not stock_sorted.empty else None

    sales_monthly = processed["sales_monthly"]
    last_period = sales_monthly["period"].max() if not sales_monthly.empty else None
    total_units = (
        sales_monthly.query("period == @last_period")["units_sold"].sum()
        if last_period is not None
        else None
    )

    kpis = [
        {
            "label": "Precio cierre",
            "value": _format_value(last_close, 2),
            "delta": "",
            "delta_class": "",
        },
        {
            "label": "Modelos activos",
            "value": _format_value(total_models, 0),
            "delta": "",
            "delta_class": "",
        },
        {
            "label": "Ventas ultimo mes",
            "value": _format_value(total_units, 0),
            "delta": _format_value(last_period.date()) if last_period is not None else "--",
            "delta_class": "",
        },
    ]

    status_points = []
    stock_up = (stock_trends["trend"] == "sube").sum() if not stock_trends.empty else 0
    stock_down = (stock_trends["trend"] == "baja").sum() if not stock_trends.empty else 0
    status_points.append(f"Acciones en subida: {stock_up}")
    status_points.append(f"Acciones en baja: {stock_down}")

    demand_up = (demand_summary["demand_trend"] == "crece").sum() if not demand_summary.empty else 0
    demand_down = (demand_summary["demand_trend"] == "cae").sum() if not demand_summary.empty else 0
    status_points.append(f"Modelos con demanda en crecimiento: {demand_up}")
    status_points.append(f"Modelos con demanda en caida: {demand_down}")

    tables = [
        _table_from_df(
            "Resumen de acciones",
            stock_trends,
            ["symbol", "last_close", "pct_change", "trend"],
        ),
        _table_from_df(
            "Resumen de demanda",
            demand_summary,
            ["model_id", "region", "last_units", "pct_change", "demand_trend"],
        ),
        _table_from_df(
            "Nuevo vs usado",
            new_vs_used,
            ["model_id", "used_count", "new_units", "ratio_used_new", "recommendation"],
        ),
        _table_from_df(
            "Prediccion demanda",
            predictions["demand_pred"],
            ["model_id", "region", "predicted_units", "trend", "confidence"],
        ),
    ]

    return {
        "report_title": "Toyota Peru - Dashboard IDME",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "data_status": "Datos OK",
        "headline": "Panorama Toyota en Peru",
        "summary_text": "Acciones, ventas y tendencias en un solo lugar.",
        "kpis": kpis,
        "status_summary": "Resumen ejecutivo generado con reglas simples.",
        "status_points": status_points,
        "recommendations": rec_cards,
        "plotly_stock": build_stock_chart(cleaned["stock"]),
        "plotly_demand": build_demand_chart(processed["sales_monthly"]),
        "plotly_new_vs_used": build_new_vs_used_chart(new_vs_used),
        "plotly_trends": build_trends_chart(cleaned["trends"]),
        "plotly_predictions": build_predictions_chart(
            predictions.get("stock_pred"),
            predictions.get("demand_pred"),
        ),
        "vehicle_profiles": vehicle_profiles,
        "tables": tables,
    }


def run_pipeline() -> Path:
    """Orquesta el pipeline completo y genera el dashboard final."""

    config = load_config()
    raw = read_data(config)
    cleaned = clean_data(raw)
    processed = process_data(cleaned)
    analysis = run_analysis(cleaned, processed)
    predictions = run_predictions(cleaned, processed)
    context = build_context(cleaned, processed, analysis, predictions)

    return render_dashboard(
        context=context,
        template_path=config["dashboard_template"],
        output_path=config["dashboard_output"],
    )
