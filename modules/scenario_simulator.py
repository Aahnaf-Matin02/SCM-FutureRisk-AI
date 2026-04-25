"""
modules/scenario_simulator.py
===============================
Scenario simulation engine for SCM FutureRisk AI.
Lets users adjust 9 supply chain levers and see how they affect risk outputs.
"""

import numpy as np


# ─────────────────────────────────────────────
# Scenario Weights (how each lever affects risk)
# ─────────────────────────────────────────────

LEVER_CONFIG = {
    "tariff_increase": {
        "label": "Tariff Level Increase (%)",
        "min": 0, "max": 100, "default": 20, "step": 5,
        "icon": "🏷️",
        "help": "Percentage increase in tariffs on key goods",
        "risk_weight": 0.22,
        "lead_time_weight": 0.10,
        "cost_weight": 0.28,
    },
    "oil_price_increase": {
        "label": "Oil Price Increase (%)",
        "min": 0, "max": 150, "default": 15, "step": 5,
        "icon": "🛢️",
        "help": "Percentage rise in crude oil benchmark price",
        "risk_weight": 0.15,
        "lead_time_weight": 0.08,
        "cost_weight": 0.22,
    },
    "freight_cost_increase": {
        "label": "Freight Cost Increase (%)",
        "min": 0, "max": 200, "default": 25, "step": 5,
        "icon": "🚢",
        "help": "Percentage increase in container shipping rates",
        "risk_weight": 0.18,
        "lead_time_weight": 0.20,
        "cost_weight": 0.25,
    },
    "geopolitical_risk": {
        "label": "Geopolitical / War Risk (0–10)",
        "min": 0, "max": 10, "default": 3, "step": 1,
        "icon": "⚔️",
        "help": "Severity of geopolitical conflict affecting trade routes",
        "risk_weight": 0.20,
        "lead_time_weight": 0.15,
        "cost_weight": 0.12,
    },
    "port_congestion": {
        "label": "Port Congestion (0–10)",
        "min": 0, "max": 10, "default": 3, "step": 1,
        "icon": "⚓",
        "help": "Severity of port and terminal congestion",
        "risk_weight": 0.16,
        "lead_time_weight": 0.28,
        "cost_weight": 0.18,
    },
    "supplier_delay": {
        "label": "Supplier Delay Risk (0–10)",
        "min": 0, "max": 10, "default": 2, "step": 1,
        "icon": "🏭",
        "help": "Likelihood and severity of upstream supplier delays",
        "risk_weight": 0.18,
        "lead_time_weight": 0.25,
        "cost_weight": 0.15,
    },
    "currency_volatility": {
        "label": "Currency Volatility (0–10)",
        "min": 0, "max": 10, "default": 3, "step": 1,
        "icon": "💱",
        "help": "Degree of exchange rate fluctuation affecting sourcing costs",
        "risk_weight": 0.12,
        "lead_time_weight": 0.03,
        "cost_weight": 0.20,
    },
    "demand_shock": {
        "label": "Demand Shock (% change)",
        "min": -50, "max": 100, "default": 0, "step": 5,
        "icon": "📈",
        "help": "Unexpected demand change (positive = surge, negative = collapse)",
        "risk_weight": 0.14,
        "lead_time_weight": 0.12,
        "cost_weight": 0.10,
    },
    "inventory_level": {
        "label": "Inventory Buffer (weeks on hand)",
        "min": 0, "max": 26, "default": 4, "step": 1,
        "icon": "📦",
        "help": "Current weeks of inventory on hand (higher = better buffer)",
        "risk_weight": -0.15,  # negative = reduces risk
        "lead_time_weight": -0.20,
        "cost_weight": 0.08,
    },
}


# ─────────────────────────────────────────────
# Simulation Engine
# ─────────────────────────────────────────────

def run_simulation(base_risk: float, lever_values: dict) -> dict:
    """
    Given a baseline risk score and lever settings,
    compute adjusted supply chain KPIs.
    """
    # Normalize lever values to 0-1 range
    normalized = {}
    for key, config in LEVER_CONFIG.items():
        val = lever_values.get(key, config["default"])
        rng = config["max"] - config["min"]
        if rng == 0:
            normalized[key] = 0
        else:
            normalized[key] = (val - config["min"]) / rng

    # Compute risk delta
    risk_delta = sum(
        normalized[k] * LEVER_CONFIG[k]["risk_weight"] * 60
        for k in normalized
    )

    # Compute lead-time delta (in days)
    lead_time_base = 30  # baseline 30 days
    lead_time_delta = sum(
        normalized[k] * LEVER_CONFIG[k]["lead_time_weight"] * 25
        for k in normalized
    )

    # Compute cost pressure (0–100 scale)
    cost_delta = sum(
        normalized[k] * LEVER_CONFIG[k]["cost_weight"] * 70
        for k in normalized
    )

    # Supplier reliability (inverse of stress)
    supplier_stress = sum(
        normalized[k] * abs(LEVER_CONFIG[k]["risk_weight"]) * 0.5
        for k in ["supplier_delay", "geopolitical_risk", "port_congestion"]
    )
    supplier_reliability = max(20, min(100, 85 - supplier_stress * 80))

    # Safety stock recommendation (weeks)
    demand_shock = lever_values.get("demand_shock", 0)
    base_ss = 2.0
    ss = base_ss + (risk_delta / 30) + (lead_time_delta / 25) + max(0, demand_shock / 40)
    ss = max(1, min(16, ss))

    # Final adjusted risk
    adjusted_risk = np.clip(base_risk + risk_delta, 5, 98)
    adjusted_lead  = max(7, lead_time_base + lead_time_delta)
    adjusted_cost  = np.clip(cost_delta, 0, 100)

    # Decision matrix
    if adjusted_risk >= 75:
        decision = "🔴 Avoid new sourcing contracts"
        decision_color = "#ef4444"
    elif adjusted_risk >= 60:
        decision = "🟠 Diversify suppliers immediately"
        decision_color = "#f97316"
    elif adjusted_risk >= 48:
        decision = "🟡 Increase safety stock + monitor"
        decision_color = "#f59e0b"
    elif adjusted_risk >= 35:
        decision = "🔵 Hedge freight/currency exposure"
        decision_color = "#3b82f6"
    else:
        decision = "🟢 Continue sourcing — monitor weekly"
        decision_color = "#22c55e"

    return {
        "adjusted_risk":         round(adjusted_risk, 1),
        "adjusted_lead_time":    round(adjusted_lead, 1),
        "cost_pressure":         round(adjusted_cost, 1),
        "safety_stock_weeks":    round(ss, 1),
        "supplier_reliability":  round(supplier_reliability, 1),
        "recommended_decision":  decision,
        "decision_color":        decision_color,
        "risk_delta":            round(risk_delta, 1),
        "lead_time_delta":       round(lead_time_delta, 1),
    }


# ─────────────────────────────────────────────
# Sensitivity Analysis
# ─────────────────────────────────────────────

def sensitivity_analysis(base_risk: float, lever_values: dict) -> list:
    """
    For each lever, compute how much a 25% increase changes risk score.
    Returns sorted list of (lever_label, delta) for tornado chart.
    """
    results = []
    for key, config in LEVER_CONFIG.items():
        current_val = lever_values.get(key, config["default"])
        # Test +25% of range
        bump = (config["max"] - config["min"]) * 0.25
        bumped_vals = lever_values.copy()
        bumped_vals[key] = min(config["max"], current_val + bump)

        base_out = run_simulation(base_risk, lever_values)
        bumped_out = run_simulation(base_risk, bumped_vals)
        delta = bumped_out["adjusted_risk"] - base_out["adjusted_risk"]
        results.append({
            "lever": config["label"].split("(")[0].strip(),
            "icon": config["icon"],
            "delta": round(delta, 1),
        })

    results.sort(key=lambda x: abs(x["delta"]), reverse=True)
    return results
