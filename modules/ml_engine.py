"""
modules/ml_engine.py
=====================
Machine learning forecasting engine for SCM FutureRisk AI.
Uses a Random Forest model trained on synthetic country-risk data
combined with real-time signals to predict supply chain risk scores.
Also provides SHAP-style feature importance and time-series forecasting.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────
# Synthetic Training Data Generator
# ─────────────────────────────────────────────

def _generate_training_data(n_samples: int = 800) -> tuple:
    """
    Generate synthetic but realistic training data for the risk model.
    Features mirror country_data.py indicators + global signals.
    """
    rng = np.random.default_rng(42)

    features = {
        "bargaining_power":       rng.uniform(20, 100, n_samples),
        "economic_weight":        rng.uniform(30, 100, n_samples),
        "trade_leverage":         rng.uniform(20, 95,  n_samples),
        "strategic_position":     rng.uniform(30, 95,  n_samples),
        "trade_war_pressure":     rng.uniform(10, 90,  n_samples),
        "security_flashpoints":   rng.uniform(5,  85,  n_samples),
        "domestic_unrest":        rng.uniform(5,  70,  n_samples),
        "strategic_rivalry":      rng.uniform(10, 90,  n_samples),
        "infrastructure_quality": rng.uniform(30, 98,  n_samples),
        "port_efficiency":        rng.uniform(30, 98,  n_samples),
        "currency_stability":     rng.uniform(40, 95,  n_samples),
        "news_sentiment_score":   rng.uniform(-1, 1,   n_samples),
        "oil_price_pressure":     rng.uniform(0,  1,   n_samples),
        "freight_cost_index":     rng.uniform(0,  1,   n_samples),
        "tariff_intensity":       rng.uniform(0,  1,   n_samples),
        "geopolitical_conflict":  rng.uniform(0,  1,   n_samples),
        "gscpi_signal":           rng.uniform(-2, 2,   n_samples),
    }

    df = pd.DataFrame(features)

    # Risk formula: higher pressure metrics → higher risk; higher stability → lower risk
    risk = (
        0.15 * (100 - df["bargaining_power"])
        + 0.10 * (100 - df["economic_weight"])
        + 0.10 * (100 - df["trade_leverage"])
        + 0.08 * (100 - df["strategic_position"])
        + 0.10 * df["trade_war_pressure"]
        + 0.10 * df["security_flashpoints"]
        + 0.08 * df["domestic_unrest"]
        + 0.07 * df["strategic_rivalry"]
        + 0.05 * (100 - df["infrastructure_quality"])
        + 0.05 * (100 - df["port_efficiency"])
        + 0.04 * (100 - df["currency_stability"])
        + 0.08 * (-df["news_sentiment_score"] * 30 + 15)  # negative sentiment → risk
        + 0.06 * df["oil_price_pressure"] * 20
        + 0.06 * df["freight_cost_index"] * 20
        + 0.08 * df["tariff_intensity"] * 25
        + 0.09 * df["geopolitical_conflict"] * 20
        + 0.04 * df["gscpi_signal"] * 5
    )

    risk = np.clip(risk + rng.normal(0, 3, n_samples), 5, 95)

    return df, risk


# ─────────────────────────────────────────────
# Model Training
# ─────────────────────────────────────────────

def train_model() -> Pipeline:
    """Train a Gradient Boosting pipeline on synthetic data."""
    X, y = _generate_training_data()
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.08,
            max_depth=4,
            random_state=42,
            subsample=0.85,
        ))
    ])
    pipeline.fit(X, y)
    return pipeline


# Global model instance (trained once per session)
_MODEL = None
_FEATURE_NAMES = [
    "bargaining_power", "economic_weight", "trade_leverage", "strategic_position",
    "trade_war_pressure", "security_flashpoints", "domestic_unrest", "strategic_rivalry",
    "infrastructure_quality", "port_efficiency", "currency_stability",
    "news_sentiment_score", "oil_price_pressure", "freight_cost_index",
    "tariff_intensity", "geopolitical_conflict", "gscpi_signal"
]


def get_model() -> Pipeline:
    global _MODEL
    if _MODEL is None:
        _MODEL = train_model()
    return _MODEL


# ─────────────────────────────────────────────
# Feature Vector Builder
# ─────────────────────────────────────────────

def build_feature_vector(country_profile: dict, global_signals: dict) -> pd.DataFrame:
    """
    Combine country intelligence profile with real-time global signals
    into the ML feature vector.
    """
    features = {
        "bargaining_power":       country_profile.get("bargaining_power", 50),
        "economic_weight":        country_profile.get("economic_weight", 50),
        "trade_leverage":         country_profile.get("trade_leverage", 50),
        "strategic_position":     country_profile.get("strategic_position", 50),
        "trade_war_pressure":     country_profile.get("trade_war_pressure", 50),
        "security_flashpoints":   country_profile.get("security_flashpoints", 50),
        "domestic_unrest":        country_profile.get("domestic_unrest", 50),
        "strategic_rivalry":      country_profile.get("strategic_rivalry", 50),
        "infrastructure_quality": country_profile.get("infrastructure_quality", 60),
        "port_efficiency":        country_profile.get("port_efficiency", 60),
        "currency_stability":     country_profile.get("currency_stability", 65),
        "news_sentiment_score":   global_signals.get("sentiment", 0.0),
        "oil_price_pressure":     global_signals.get("oil_pressure", 0.5),
        "freight_cost_index":     global_signals.get("freight_index", 0.5),
        "tariff_intensity":       global_signals.get("tariff_intensity", 0.4),
        "geopolitical_conflict":  global_signals.get("conflict_index", 0.4),
        "gscpi_signal":           global_signals.get("gscpi", 0.0),
    }
    return pd.DataFrame([features])


# ─────────────────────────────────────────────
# Feature Importance (SHAP-style)
# ─────────────────────────────────────────────

def compute_feature_importance(country_profile: dict, global_signals: dict) -> dict:
    """
    Approximate SHAP-style feature contributions using permutation sensitivity.
    Returns {feature_name: impact_score} sorted by absolute impact.
    """
    model = get_model()
    base_vec = build_feature_vector(country_profile, global_signals)
    base_score = float(model.predict(base_vec)[0])

    importances = {}
    for feat in _FEATURE_NAMES:
        original = base_vec[feat].iloc[0]
        # Perturb by +1 std
        perturbed = base_vec.copy()
        perturbed[feat] = original * 1.15 + 2
        new_score = float(model.predict(perturbed)[0])
        importances[feat] = round(new_score - base_score, 2)

    # Sort by absolute impact
    sorted_imp = dict(sorted(importances.items(), key=lambda x: abs(x[1]), reverse=True))
    return sorted_imp


# ─────────────────────────────────────────────
# Multi-Horizon Forecast
# ─────────────────────────────────────────────

def forecast_risk(
    country_profile: dict,
    global_signals: dict,
    industry_modifier: dict,
    baseline_risk: float,
) -> dict:
    """
    Generate supply chain risk forecasts for 30, 90, and 180-day horizons.
    Returns structured forecast dict with direction and confidence.
    """
    model = get_model()
    fvec = build_feature_vector(country_profile, global_signals)
    current_risk = float(model.predict(fvec)[0])

    # Apply industry modifiers
    tariff_mod = industry_modifier.get("tariff_sensitivity", 0.7)
    geo_mod = industry_modifier.get("geopolitical_sensitivity", 0.7)
    freight_mod = industry_modifier.get("freight_sensitivity", 0.7)

    industry_weight = (tariff_mod + geo_mod + freight_mod) / 3.0
    current_risk = np.clip(current_risk * (0.85 + 0.30 * industry_weight), 5, 95)

    # Time-horizon adjustments using signal trend
    sentiment = global_signals.get("sentiment", 0.0)
    oil = global_signals.get("oil_pressure", 0.5)
    freight = global_signals.get("freight_index", 0.5)

    trend_pressure = (oil * 0.35 + freight * 0.35 + (-sentiment) * 0.30)
    trend_delta_30  = trend_pressure * 4.0
    trend_delta_90  = trend_pressure * 8.0
    trend_delta_180 = trend_pressure * 12.0

    risk_30  = np.clip(current_risk + trend_delta_30,  5, 95)
    risk_90  = np.clip(current_risk + trend_delta_90,  5, 95)
    risk_180 = np.clip(current_risk + trend_delta_180, 5, 95)

    # Risk direction
    if risk_90 - current_risk > 5:
        direction = "Deteriorating ↑"
        direction_color = "#ef4444"
    elif risk_90 - current_risk < -5:
        direction = "Improving ↓"
        direction_color = "#22c55e"
    else:
        direction = "Stable →"
        direction_color = "#f59e0b"

    # Confidence based on data quality
    news_available = global_signals.get("news_available", False)
    if news_available:
        confidence = "Medium-High"
        confidence_pct = 72
    else:
        confidence = "Medium"
        confidence_pct = 55

    # Risk category label
    def _label(r):
        if r < 25: return ("Low", "#22c55e")
        elif r < 50: return ("Moderate", "#f59e0b")
        elif r < 70: return ("High", "#f97316")
        else: return ("Critical", "#ef4444")

    return {
        "current_risk":    round(current_risk, 1),
        "risk_30":         round(risk_30, 1),
        "risk_90":         round(risk_90, 1),
        "risk_180":        round(risk_180, 1),
        "direction":       direction,
        "direction_color": direction_color,
        "confidence":      confidence,
        "confidence_pct":  confidence_pct,
        "risk_label":      _label(current_risk)[0],
        "risk_color":      _label(current_risk)[1],
        "label_30":        _label(risk_30)[0],
        "label_90":        _label(risk_90)[0],
        "label_180":       _label(risk_180)[0],
    }


# ─────────────────────────────────────────────
# 30-Point Time Series (for chart)
# ─────────────────────────────────────────────

def generate_forecast_series(current_risk: float, risk_90: float, risk_180: float) -> dict:
    """
    Generate a 180-day daily risk series interpolating between forecast points.
    Returns {dates: [...], values: [...]} for Plotly charting.
    """
    dates = pd.date_range(start="today", periods=180, freq="D")
    midpoint_90 = risk_90
    endpoint_180 = risk_180

    # Quadratic interpolation
    t = np.linspace(0, 1, 180)
    values = (
        (1 - t) ** 2 * current_risk
        + 2 * (1 - t) * t * midpoint_90
        + t ** 2 * endpoint_180
        + np.random.normal(0, 0.8, 180)  # small noise for realism
    )
    values = np.clip(values, 5, 95)

    return {
        "dates": [d.strftime("%Y-%m-%d") for d in dates],
        "values": [round(v, 1) for v in values],
    }


# ─────────────────────────────────────────────
# Key Drivers Narrative
# ─────────────────────────────────────────────

def get_key_drivers(feature_importance: dict, country_name: str, industry: str) -> list:
    """
    Convert feature importance into human-readable driver statements.
    Returns a list of (driver_text, impact_direction) tuples.
    """
    driver_map = {
        "bargaining_power":       "Country bargaining power and trade negotiation strength",
        "economic_weight":        "GDP size and economic complexity",
        "trade_war_pressure":     "Tariff escalation and trade war exposure",
        "security_flashpoints":   "Proximity to active conflict and security flashpoints",
        "domestic_unrest":        "Political stability and domestic unrest risk",
        "geopolitical_conflict":  "Global geopolitical conflict intensity",
        "tariff_intensity":       f"Tariff pressure on {industry} imports/exports",
        "freight_cost_index":     "Freight and logistics cost movement",
        "oil_price_pressure":     "Oil and energy price pressure on supply chains",
        "news_sentiment_score":   "Recent news sentiment and media risk signals",
        "infrastructure_quality": "Port and logistics infrastructure quality",
        "port_efficiency":        "Port throughput and efficiency rating",
        "gscpi_signal":           "Global Supply Chain Pressure Index signal",
        "currency_stability":     "Currency volatility and exchange rate risk",
        "strategic_rivalry":      "Great-power rivalry affecting trade routes",
        "trade_leverage":         "Export dependency and trade relationship depth",
        "strategic_position":     "Geopolitical importance to trade corridors",
    }

    drivers = []
    for feat, impact in list(feature_importance.items())[:6]:
        text = driver_map.get(feat, feat.replace("_", " ").title())
        direction = "increases risk" if impact > 0 else "reduces risk"
        drivers.append((text, direction, round(abs(impact), 1)))
    return drivers
