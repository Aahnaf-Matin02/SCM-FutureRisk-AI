"""
modules/visualizations.py
===========================
Plotly chart factories for SCM FutureRisk AI.

FIX v1.1: Removed `margin` from BASE_LAYOUT to prevent
           "TypeError: got multiple values for keyword argument 'margin'"
           Each chart now specifies margin via the _layout() helper.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np


COLORS = {
    "primary":    "#6366f1",
    "success":    "#22c55e",
    "warning":    "#f59e0b",
    "danger":     "#ef4444",
    "orange":     "#f97316",
    "blue":       "#3b82f6",
    "gray":       "#6b7280",
    "light_gray": "#f3f4f6",
    "white":      "#ffffff",
    "text":       "#111827",
    "grid":       "rgba(0,0,0,0.06)",
}

# margin deliberately excluded — specified per chart via _layout()
BASE_LAYOUT = dict(
    font=dict(family="Inter, system-ui, sans-serif", color=COLORS["text"]),
    paper_bgcolor=COLORS["white"],
    plot_bgcolor=COLORS["white"],
    showlegend=True,
)


def _layout(**overrides) -> dict:
    """Safely merge BASE_LAYOUT with per-chart keyword overrides."""
    return {**BASE_LAYOUT, **overrides}


# ── Gauge ────────────────────────────────────────────────────────────────────

def risk_gauge(score: float, title: str = "Supply Chain Risk Score") -> go.Figure:
    color = (COLORS["success"] if score < 25 else
             COLORS["warning"] if score < 50 else
             COLORS["orange"]  if score < 70 else
             COLORS["danger"])

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": title, "font": {"size": 14, "color": COLORS["gray"]}},
        number={"font": {"size": 40, "color": color}, "suffix": "/100"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": COLORS["gray"]},
            "bar":  {"color": color, "thickness": 0.25},
            "bgcolor": COLORS["light_gray"],
            "borderwidth": 0,
            "steps": [
                {"range": [0,  25],  "color": "rgba(34,197,94,0.12)"},
                {"range": [25, 50],  "color": "rgba(245,158,11,0.12)"},
                {"range": [50, 70],  "color": "rgba(249,115,22,0.12)"},
                {"range": [70, 100], "color": "rgba(239,68,68,0.12)"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.75, "value": score},
        },
    ))
    fig.update_layout(**_layout(height=260, margin=dict(l=30, r=30, t=50, b=10)))
    return fig


# ── Forecast Line ─────────────────────────────────────────────────────────────

def forecast_line_chart(series: dict, country: str) -> go.Figure:
    dates  = series["dates"]
    values = series["values"]
    arr    = np.array(values)
    upper  = np.clip(arr + np.linspace(1, 8, len(arr)), 0, 100)
    lower  = np.clip(arr - np.linspace(1, 8, len(arr)), 0, 100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1], y=list(upper) + list(lower[::-1]),
        fill="toself", fillcolor="rgba(99,102,241,0.10)",
        line=dict(color="rgba(99,102,241,0)"), name="Confidence Band", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=values, mode="lines", name="Risk Score",
        line=dict(color=COLORS["primary"], width=2.5, shape="spline"),
        hovertemplate="<b>%{x}</b><br>Risk: %{y:.1f}/100<extra></extra>",
    ))
    fig.add_hrect(y0=0,  y1=25,  fillcolor="rgba(34,197,94,0.05)",  line_width=0, annotation_text="Low",      annotation_position="left")
    fig.add_hrect(y0=25, y1=50,  fillcolor="rgba(245,158,11,0.05)", line_width=0, annotation_text="Moderate", annotation_position="left")
    fig.add_hrect(y0=50, y1=70,  fillcolor="rgba(249,115,22,0.05)", line_width=0, annotation_text="High",     annotation_position="left")
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.05)",  line_width=0, annotation_text="Critical", annotation_position="left")

    fig.update_layout(**_layout(
        title=dict(text=f"{country} — 180-Day Risk Forecast", font=dict(size=14)),
        xaxis=dict(title="", showgrid=True, gridcolor=COLORS["grid"]),
        yaxis=dict(title="Risk Score (0–100)", range=[0, 100], showgrid=True, gridcolor=COLORS["grid"]),
        height=350, margin=dict(l=20, r=20, t=40, b=20),
    ))
    return fig


# ── Radar ─────────────────────────────────────────────────────────────────────

def radar_chart(country_profile: dict) -> go.Figure:
    dimensions = ["Bargaining Power","Economic Weight","Trade Leverage","Strategic Position",
                  "Infrastructure","Port Efficiency","Currency Stability","Regulatory Stability"]
    keys       = ["bargaining_power","economic_weight","trade_leverage","strategic_position",
                  "infrastructure_quality","port_efficiency","currency_stability","regulatory_stability"]
    vals       = [country_profile.get(k, 50) for k in keys]
    vals       += [vals[0]]
    dimensions += [dimensions[0]]

    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=dimensions, fill="toself",
        fillcolor="rgba(99,102,241,0.15)",
        line=dict(color=COLORS["primary"], width=2),
        name=country_profile.get("name", "Country"),
    ))
    fig.update_layout(**_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9)),
            angularaxis=dict(tickfont=dict(size=10)),
        ),
        height=380, margin=dict(l=20, r=20, t=30, b=20), showlegend=False,
    ))
    return fig


# ── Feature Importance ────────────────────────────────────────────────────────

def feature_importance_chart(feature_importance: dict) -> go.Figure:
    items  = list(feature_importance.items())[:8]
    labels = [k.replace("_", " ").title() for k, _ in items]
    values = [v for _, v in items]
    colors = [COLORS["danger"] if v > 0 else COLORS["success"] for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, opacity=0.85),
        text=[f"{v:+.1f}" for v in values], textposition="outside",
    ))
    fig.update_layout(**_layout(
        title=dict(text="ML Feature Impact on Risk Score", font=dict(size=13)),
        xaxis=dict(title="Risk Impact (pts)", zeroline=True, zerolinecolor=COLORS["gray"],
                   showgrid=True, gridcolor=COLORS["grid"]),
        yaxis=dict(title="", autorange="reversed"),
        height=320, margin=dict(l=20, r=60, t=40, b=20), showlegend=False,
    ))
    return fig


# ── Signal Heatmap ────────────────────────────────────────────────────────────

def signal_heatmap(signals: dict) -> go.Figure:
    signal_keys   = ["oil_pressure", "freight_index", "tariff_intensity", "conflict_index"]
    signal_labels = ["Oil Pressure", "Freight Cost", "Tariff Intensity", "Conflict Risk"]
    z_vals = [[signals.get(k, 0.5) for k in signal_keys]]

    fig = go.Figure(go.Heatmap(
        z=z_vals, x=signal_labels, y=["Signal Intensity"],
        colorscale=[[0.0,"rgba(34,197,94,0.7)"],[0.5,"rgba(245,158,11,0.7)"],[1.0,"rgba(239,68,68,0.7)"]],
        zmin=0, zmax=1,
        text=[[f"{v:.0%}" for v in z_vals[0]]], texttemplate="%{text}",
        showscale=True, colorbar=dict(title="Intensity", thickness=12),
    ))
    fig.update_layout(**_layout(height=140, margin=dict(l=20, r=80, t=20, b=20), showlegend=False))
    return fig


# ── Tornado Chart ─────────────────────────────────────────────────────────────

def tornado_chart(sensitivity_data: list) -> go.Figure:
    labels = [f"{d['icon']} {d['lever']}" for d in sensitivity_data[:8]]
    deltas = [d["delta"] for d in sensitivity_data[:8]]
    colors = [COLORS["danger"] if d > 0 else COLORS["success"] for d in deltas]

    fig = go.Figure(go.Bar(
        x=deltas, y=labels, orientation="h",
        marker=dict(color=colors, opacity=0.80),
        text=[f"{d:+.1f} pts" for d in deltas], textposition="outside",
    ))
    fig.update_layout(**_layout(
        title=dict(text="Lever Sensitivity — Risk Score Impact (per 25% increase)", font=dict(size=13)),
        xaxis=dict(title="Risk Score Change (pts)", zeroline=True, zerolinecolor=COLORS["gray"],
                   showgrid=True, gridcolor=COLORS["grid"]),
        yaxis=dict(autorange="reversed"),
        height=340, margin=dict(l=20, r=60, t=40, b=20), showlegend=False,
    ))
    return fig


# ── Country Comparison ────────────────────────────────────────────────────────

def country_comparison_chart(profiles: dict, metric: str = "baseline_risk") -> go.Figure:
    countries = list(profiles.keys())
    values    = [profiles[c].get(metric, 50) for c in countries]
    flags     = [profiles[c].get("flag", "") for c in countries]
    labels    = [f"{flags[i]} {countries[i]}" for i in range(len(countries))]

    if "risk" in metric:
        colors = [COLORS["success"] if v < 30 else COLORS["warning"] if v < 50 else
                  COLORS["orange"]  if v < 70 else COLORS["danger"] for v in values]
    else:
        colors = [COLORS["primary"]] * len(values)

    sorted_items = sorted(zip(labels, values, colors), key=lambda x: x[1])
    labels, values, colors = zip(*sorted_items)

    fig = go.Figure(go.Bar(
        x=list(values), y=list(labels), orientation="h",
        marker=dict(color=list(colors), opacity=0.80),
        text=[f"{v}" for v in values], textposition="outside",
    ))
    fig.update_layout(**_layout(
        title=dict(text=f"Country Comparison — {metric.replace('_',' ').title()}", font=dict(size=13)),
        xaxis=dict(range=[0, 115], showgrid=True, gridcolor=COLORS["grid"]),
        yaxis=dict(title=""),
        height=380, margin=dict(l=20, r=60, t=40, b=20), showlegend=False,
    ))
    return fig


# ── Horizon Bar ───────────────────────────────────────────────────────────────

def horizon_bar_chart(forecast: dict) -> go.Figure:
    labels = ["Current", "30-Day", "90-Day", "6-Month"]
    values = [forecast["current_risk"], forecast["risk_30"], forecast["risk_90"], forecast["risk_180"]]
    colors = [COLORS["success"] if v < 30 else COLORS["warning"] if v < 50 else
              COLORS["orange"]  if v < 70 else COLORS["danger"] for v in values]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker=dict(color=colors, opacity=0.82),
        text=[f"{v}" for v in values], textposition="outside",
    ))
    fig.update_layout(**_layout(
        title=dict(text="Risk Score by Time Horizon", font=dict(size=13)),
        yaxis=dict(range=[0, 110], title="Risk Score", showgrid=True, gridcolor=COLORS["grid"]),
        xaxis=dict(showgrid=False),
        height=280, margin=dict(l=20, r=20, t=40, b=20), showlegend=False,
    ))
    return fig
