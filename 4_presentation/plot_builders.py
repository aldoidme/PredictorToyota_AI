from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = ["#e53946", "#fca311", "#35d49a", "#9aa4b2"]


def _to_html(fig: go.Figure, div_id: str | None = None) -> str:
    return pio.to_html(fig, full_html=False, include_plotlyjs=False, div_id=div_id)


def build_stock_chart(df: pd.DataFrame) -> str:
    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["close"] = pd.to_numeric(data["close"], errors="coerce")
    data = data.dropna(subset=["date", "close"])

    fig = px.line(
        data,
        x="date",
        y="close",
        color="symbol",
        title="Precio de cierre",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=360)
    return _to_html(fig)


def build_demand_chart(df: pd.DataFrame) -> str:
    data = df.copy()
    data["period"] = pd.to_datetime(data["period"], errors="coerce")
    data["units_sold"] = pd.to_numeric(data["units_sold"], errors="coerce")
    data = data.dropna(subset=["period", "units_sold", "model_id"])
    data = data.sort_values(["model_id", "period"], kind="mergesort")

    data["pct_change"] = data.groupby("model_id")["units_sold"].pct_change()

    def _state(value: float | None) -> str:
        if value is None or pd.isna(value):
            return "estable"
        if value >= 0.03:
            return "crece"
        if value <= -0.03:
            return "cae"
        return "estable"

    data["state"] = data["pct_change"].apply(_state)
    color_map = {"crece": "#22c55e", "cae": "#ef4444", "estable": "#facc15"}

    fig = go.Figure()
    for model_id, group in data.groupby("model_id"):
        fig.add_trace(
            go.Scatter(
                x=group["period"],
                y=group["units_sold"],
                mode="lines",
                name=str(model_id),
                legendgroup=str(model_id),
                line=dict(width=2),
                hovertemplate="%{x|%Y-%m}<br>Unidades: %{y}<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=group["period"],
                y=group["units_sold"],
                mode="markers",
                name=f"{model_id} estado",
                legendgroup=str(model_id),
                showlegend=False,
                marker=dict(
                    size=7,
                    color=[color_map[state] for state in group["state"]],
                ),
                hovertemplate="%{x|%Y-%m}<br>%{text}<extra></extra>",
                text=[
                    "Crecimiento" if state == "crece" else "Caida" if state == "cae" else "Estable"
                    for state in group["state"]
                ],
            )
        )

    fig.update_layout(
        title="Ventas historicas y variacion",
        margin=dict(l=20, r=20, t=40, b=20),
        height=360,
        showlegend=False,
    )
    fig.update_yaxes(title="Unidades")
    fig.update_xaxes(title="Mes")

    return _to_html(fig, div_id="chart-demand")


def build_new_vs_used_chart(df: pd.DataFrame) -> str:
    data = df.copy()
    fig = px.bar(
        data,
        x="model_id",
        y=["used_count", "new_units"],
        barmode="group",
        title="Actividad nuevo vs usado",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=360)
    return _to_html(fig)


def build_trends_chart(df: pd.DataFrame) -> str:
    data = df.copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    data = data.dropna(subset=["date", "value"])

    fig = px.line(
        data,
        x="date",
        y="value",
        color="keyword",
        title="Indice de tendencias",
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=360)
    return _to_html(fig)


def build_predictions_chart(
    stock_pred: Optional[pd.DataFrame],
    demand_pred: Optional[pd.DataFrame],
) -> str:
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Acciones (prob subida)", "Demanda (unidades)"]
    )

    if stock_pred is not None and not stock_pred.empty:
        fig.add_trace(
            go.Bar(
                x=stock_pred["symbol"],
                y=stock_pred["prob_up"],
                name="Prob. subida",
            ),
            row=1,
            col=1,
        )

    if demand_pred is not None and not demand_pred.empty:
        fig.add_trace(
            go.Bar(
                x=demand_pred["model_id"],
                y=demand_pred["predicted_units"],
                name="Unidades",
            ),
            row=1,
            col=2,
        )

    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=360,
        showlegend=False,
    )
    return _to_html(fig)
