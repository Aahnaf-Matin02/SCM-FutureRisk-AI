"""
modules/decision_ai.py
=======================
Claude-powered strategic decision-making layer for SCM FutureRisk AI.
Generates structured supply chain recommendations using the Anthropic API.
Falls back to rule-based logic when the API key is unavailable.
"""

import os
import json
import re
import anthropic
import streamlit as st

# ─────────────────────────────────────────────
# Possible Decisions
# ─────────────────────────────────────────────

DECISIONS = [
    "Continue sourcing",
    "Diversify suppliers",
    "Increase safety stock",
    "Reroute shipments",
    "Nearshore production",
    "Hedge freight/currency exposure",
    "Reduce dependency",
    "Avoid new sourcing contracts",
    "Monitor only",
]

# ─────────────────────────────────────────────
# Claude API Call
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600)
def get_claude_decision(
    country: str,
    industry: str,
    time_horizon: str,
    forecast: dict,
    signals: dict,
    country_profile: dict,
    feature_drivers: list,
    api_key: str = None,
) -> dict:
    """
    Call Claude API to generate a strategic supply chain decision.
    Returns structured dict with recommendation and reasoning.
    Falls back to rule-based logic if API key is unavailable.
    """
    if not api_key or api_key == "YOUR_ANTHROPIC_API_KEY":
        return _rule_based_decision(country, industry, time_horizon, forecast, signals, country_profile)

    client = anthropic.Anthropic(api_key=api_key)

    # Build structured prompt
    driver_text = "\n".join(
        f"  - {d[0]}: {d[2]} pts ({d[1]})"
        for d in feature_drivers[:5]
    )
    articles_text = "\n".join(
        f"  [{a['sentiment'].upper()}] {a['title']}"
        for a in signals.get("articles", [])[:4]
    )

    prompt = f"""You are a senior supply chain risk analyst and strategic consultant.

## Situation Brief
- **Country:** {country}
- **Industry:** {industry}
- **Analysis Horizon:** {time_horizon}
- **Current Risk Score:** {forecast['current_risk']}/100 ({forecast['risk_label']})
- **Risk Direction:** {forecast['direction']}
- **30-Day Forecast:** {forecast['risk_30']}/100 ({forecast['label_30']})
- **90-Day Forecast:** {forecast['risk_90']}/100 ({forecast['label_90']})
- **6-Month Forecast:** {forecast['risk_180']}/100 ({forecast['label_180']})

## Country Profile Highlights
- Bargaining Power: {country_profile.get('bargaining_power', 50)}/100
- Economic Weight: {country_profile.get('economic_weight', 50)}/100
- Trade Leverage: {country_profile.get('trade_leverage', 50)}/100
- Security Flashpoints: {country_profile.get('security_flashpoints', 50)}/100
- Domestic Unrest: {country_profile.get('domestic_unrest', 50)}/100
- Port Efficiency: {country_profile.get('port_efficiency', 60)}/100

## Top ML Risk Drivers
{driver_text}

## Real-Time Market Signals
- News Sentiment: {signals.get('sentiment', 0):+.2f} (range -1 to +1)
- Oil Price Pressure: {signals.get('oil_pressure', 0.5):.0%}
- Freight Cost Index: {signals.get('freight_index', 0.5):.0%}
- Tariff Intensity: {signals.get('tariff_intensity', 0.4):.0%}
- Geopolitical Conflict: {signals.get('conflict_index', 0.4):.0%}

## Recent News Headlines
{articles_text}

---

Analyze this situation and produce a structured JSON response ONLY — no extra text outside the JSON.

Return this exact JSON structure:
{{
  "situation_summary": "2-3 sentence executive summary of the current supply chain situation",
  "outlook_30": "30-day outlook in 1-2 sentences",
  "outlook_90": "90-day outlook in 1-2 sentences",
  "outlook_180": "6-month outlook in 1-2 sentences",
  "main_risks": ["risk 1", "risk 2", "risk 3", "risk 4"],
  "main_opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
  "recommended_decision": "One of the exact phrases: Continue sourcing | Diversify suppliers | Increase safety stock | Reroute shipments | Nearshore production | Hedge freight/currency exposure | Reduce dependency | Avoid new sourcing contracts | Monitor only",
  "action_plan": ["step 1", "step 2", "step 3", "step 4", "step 5"],
  "decision_rationale": "2-3 sentences explaining why this decision was chosen",
  "confidence_level": "Low | Medium | Medium-High | High",
  "confidence_explanation": "1 sentence on why this confidence level was assigned",
  "evidence_verified": true,
  "unsupported_assumptions": ["assumption 1 if any"],
  "verification_notes": "1 sentence on how well the recommendation aligns with available evidence"
}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown fences if present
        raw = re.sub(r"^```json\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"```\s*$", "", raw, flags=re.MULTILINE)
        result = json.loads(raw)
        result["_source"] = "claude"
        return result
    except Exception as e:
        # Fall back to rule-based on any error
        result = _rule_based_decision(country, industry, time_horizon, forecast, signals, country_profile)
        result["_error"] = str(e)
        return result


# ─────────────────────────────────────────────
# Rule-Based Fallback Decision Engine
# ─────────────────────────────────────────────

def _rule_based_decision(
    country: str,
    industry: str,
    time_horizon: str,
    forecast: dict,
    signals: dict,
    country_profile: dict,
) -> dict:
    """
    Deterministic rule-based fallback when Claude API is unavailable.
    Uses risk score, direction, and key signals to produce a structured output.
    """
    risk = forecast["current_risk"]
    direction = forecast["direction"]
    tariff = signals.get("tariff_intensity", 0.4)
    conflict = signals.get("conflict_index", 0.4)
    freight = signals.get("freight_index", 0.5)
    oil = signals.get("oil_pressure", 0.5)
    sentiment = signals.get("sentiment", 0)
    bargain = country_profile.get("bargaining_power", 50)
    unrest = country_profile.get("domestic_unrest", 30)

    # Determine decision
    if risk >= 70 and "Deteriorating" in direction:
        decision = "Avoid new sourcing contracts"
        rationale = (
            f"Critical risk level ({risk}/100) and deteriorating trajectory demand an immediate halt "
            f"to new sourcing commitments. Existing contracts should be reviewed for exit clauses while "
            f"alternative supply sources are identified and qualified."
        )
    elif risk >= 60 or tariff > 0.65 or conflict > 0.65:
        decision = "Diversify suppliers"
        rationale = (
            f"Elevated risk ({risk}/100) driven by high tariff intensity ({tariff:.0%}) and/or geopolitical "
            f"conflict ({conflict:.0%}) makes single-source dependency dangerous. A multi-source strategy "
            f"across lower-risk regions provides resilience without abandoning existing relationships."
        )
    elif risk >= 50 and freight > 0.60:
        decision = "Increase safety stock"
        rationale = (
            f"Moderate-to-high risk ({risk}/100) combined with elevated freight costs ({freight:.0%}) suggest "
            f"lead-time extensions are likely. Building 4-6 weeks of additional safety stock for critical "
            f"SKUs hedges against supply disruption without requiring supplier changes."
        )
    elif freight > 0.65 or oil > 0.70:
        decision = "Hedge freight/currency exposure"
        rationale = (
            f"Freight ({freight:.0%}) and oil ({oil:.0%}) pressure are the primary drivers. Forward freight "
            f"agreements and currency hedges can lock in today's rates and protect margins while operational "
            f"supply chain changes are evaluated."
        )
    elif unrest > 55 and risk >= 45:
        decision = "Nearshore production"
        rationale = (
            f"High domestic unrest ({unrest}/100) in {country} combined with moderate risk ({risk}/100) "
            f"favors shifting production to nearer, more stable markets. This reduces political exposure "
            f"while maintaining supply chain responsiveness."
        )
    elif risk >= 40 and bargain < 50:
        decision = "Reduce dependency"
        rationale = (
            f"{country}'s moderate risk ({risk}/100) and limited bargaining power ({bargain}/100) mean "
            f"supply chain concentration here carries outsized risk without the leverage needed to negotiate "
            f"favorable terms during disruptions. Gradual dependency reduction is prudent."
        )
    elif risk < 30 and "Improving" in direction:
        decision = "Continue sourcing"
        rationale = (
            f"Low risk ({risk}/100) and an improving trajectory create favorable conditions to maintain "
            f"current sourcing strategy. Standard monitoring protocols are sufficient with no structural "
            f"changes warranted at this time."
        )
    else:
        decision = "Monitor only"
        rationale = (
            f"Risk is at a manageable level ({risk}/100) with no single signal severe enough to trigger "
            f"structural action. Weekly monitoring of tariff, freight, and geopolitical signals is recommended "
            f"with pre-defined escalation thresholds."
        )

    # Risks
    risks = []
    if tariff > 0.55: risks.append(f"Tariff escalation risk ({tariff:.0%} intensity) on {industry} inputs")
    if conflict > 0.55: risks.append(f"Geopolitical conflict disrupting trade routes ({conflict:.0%})")
    if freight > 0.60: risks.append(f"Freight cost surge ({freight:.0%}) extending lead times")
    if oil > 0.65: risks.append(f"Oil price pressure ({oil:.0%}) raising logistics costs")
    if unrest > 45: risks.append(f"Domestic unrest in {country} ({unrest}/100) threatening supplier reliability")
    if "Deteriorating" in direction: risks.append("Risk trajectory is deteriorating — proactive action window is narrowing")
    risks = (risks + ["Monitor currency and FX volatility for cost inflation impact"])[:4]

    # Opportunities
    opps = []
    if bargain > 70: opps.append(f"{country}'s high bargaining power ({bargain}/100) enables favorable long-term contract terms")
    if "Improving" in direction: opps.append("Improving risk direction signals potential for locking in better rates soon")
    if sentiment > -0.1: opps.append("Neutral-to-positive news sentiment suggests market conditions may stabilize")
    opps += [
        f"Nearshoring and China+1 diversification creating new supplier options for {industry}",
        "Green and resilient supply chain certification programs offer competitive differentiation",
    ]
    opps = opps[:3]

    # Action plan
    actions = [
        f"Audit current {country}-based supplier contracts for risk concentration and exit provisions",
        f"Map {industry} sub-tier supplier exposure to identify hidden single-source dependencies",
        f"Set up real-time monitoring dashboard for tariff, freight, and geopolitical signals",
        "Engage procurement team to identify and pre-qualify backup supplier candidates in safer regions",
        f"Review safety stock levels for critical {industry} components against revised lead-time scenarios",
    ]

    confidence = "Medium" if not signals.get("news_available") else "Medium-High"

    return {
        "situation_summary": (
            f"{country}'s supply chain risk score stands at {risk}/100 ({forecast['risk_label']}), "
            f"with a {direction.lower()} trajectory over the next {time_horizon}. "
            f"The {industry} sector faces particular pressure from tariff intensity ({tariff:.0%}) "
            f"and geopolitical signals ({conflict:.0%}), while country bargaining power ({bargain}/100) "
            f"provides some structural buffer."
        ),
        "outlook_30": (
            f"30-day risk is forecast at {forecast['risk_30']}/100 ({forecast['label_30']}). "
            f"Freight and energy costs are the near-term swing factors."
        ),
        "outlook_90": (
            f"90-day risk is forecast at {forecast['risk_90']}/100 ({forecast['label_90']}). "
            f"Tariff and geopolitical developments will be the dominant drivers."
        ),
        "outlook_180": (
            f"6-month risk is forecast at {forecast['risk_180']}/100 ({forecast['label_180']}). "
            f"Structural supply chain adjustments initiated now will begin to pay off at this horizon."
        ),
        "main_risks": risks,
        "main_opportunities": opps,
        "recommended_decision": decision,
        "action_plan": actions,
        "decision_rationale": rationale,
        "confidence_level": confidence,
        "confidence_explanation": (
            "Confidence reflects model signal quality. Live news data would increase accuracy."
            if not signals.get("news_available")
            else "Confidence reflects alignment between ML forecast, country indicators, and live news signals."
        ),
        "evidence_verified": signals.get("news_available", False),
        "unsupported_assumptions": [
            "Global freight rate baseline assumed at current index levels",
            "No sudden policy reversal or black swan events modeled",
        ],
        "verification_notes": (
            "Recommendation aligns with macro signals but should be validated against "
            "company-specific supplier contracts and inventory positioning."
        ),
        "_source": "rule_based",
    }


# ─────────────────────────────────────────────
# Evidence Verification Layer
# ─────────────────────────────────────────────

def verify_evidence(decision: dict, signals: dict) -> dict:
    """
    Cross-check AI decision against available news/signal evidence.
    Returns verification metadata.
    """
    articles = signals.get("articles", [])
    rec = decision.get("recommended_decision", "")
    risks = decision.get("main_risks", [])

    # Check how many risk claims are supported by article keywords
    all_article_text = " ".join(
        (a.get("title", "") + " " + a.get("snippet", "")).lower()
        for a in articles
    )

    evidence_hits = 0
    for risk_text in risks:
        words = risk_text.lower().split()
        if any(w in all_article_text for w in words if len(w) > 4):
            evidence_hits += 1

    support_ratio = evidence_hits / max(len(risks), 1)

    if support_ratio >= 0.75:
        evidence_quality = "High"
        evidence_color = "#22c55e"
    elif support_ratio >= 0.40:
        evidence_quality = "Moderate"
        evidence_color = "#f59e0b"
    else:
        evidence_quality = "Low"
        evidence_color = "#ef4444"

    return {
        "evidence_quality":    evidence_quality,
        "evidence_color":      evidence_color,
        "support_ratio":       round(support_ratio * 100),
        "articles_reviewed":   len(articles),
        "claims_supported":    evidence_hits,
        "claims_total":        len(risks),
        "source_type":         "Live API" if signals.get("news_available") else "Demo Data",
        "verified_timestamp":  "2025 Q2",
    }
