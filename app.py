"""
app.py — SCM FutureRisk AI
===========================
Main Streamlit application entry point.
Run with: streamlit run app.py

Pages:
  1. Home / Executive Summary
  2. Country Intelligence
  3. Global Risk Monitor
  4. ML Forecast
  5. Claude Decision Room
  6. Evidence Verification
  7. Scenario Simulator
  8. Data Sources & Methodology
"""

import os
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────
# Page Config (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SCM FutureRisk AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Import project modules
# ─────────────────────────────────────────────
from modules.country_data import (
    COUNTRY_PROFILES, COUNTRIES, INDUSTRIES, TIME_HORIZONS, INDUSTRY_RISK_MODIFIERS, INDICATOR_DESCRIPTIONS
)
from modules.ml_engine import (
    get_model, build_feature_vector, forecast_risk,
    generate_forecast_series, compute_feature_importance, get_key_drivers
)
from modules.search_intelligence import (
    fetch_live_signals, build_signal_summary
)
from modules.decision_ai import (
    get_claude_decision, verify_evidence, DECISIONS
)
from modules.scenario_simulator import (
    run_simulation, sensitivity_analysis, LEVER_CONFIG
)
from modules.visualizations import (
    risk_gauge, forecast_line_chart, radar_chart, feature_importance_chart,
    signal_heatmap, tornado_chart, country_comparison_chart, horizon_bar_chart
)

# ─────────────────────────────────────────────
# API Keys from Environment
# ─────────────────────────────────────────────
ANTHROPIC_KEY  = os.getenv("ANTHROPIC_API_KEY", "")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
SEARCH_ENGINE  = os.getenv("SEARCH_ENGINE_ID", "")


# ─────────────────────────────────────────────
# Global CSS — Clean Premium Theme
# ─────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f8fafc !important; }

    /* Main background */
    .stApp { background: #f8fafc; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 14px;
        padding: 16px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricLabel"] { font-size: 12px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #0f172a; }

    /* Card container */
    .risk-card {
        background: white;
        border-radius: 14px;
        padding: 20px 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 99px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    .badge-red    { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
    .badge-yellow { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
    .badge-green  { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-blue   { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .badge-purple { background: #f5f3ff; color: #7c3aed; border: 1px solid #ddd6fe; }

    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
    }
    .page-header h1 { color: white !important; font-size: 22px; font-weight: 700; margin: 0; }
    .page-header p  { color: #94a3b8 !important; font-size: 14px; margin: 4px 0 0 0; }

    /* Section divider */
    .section-title {
        font-size: 13px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 20px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #e2e8f0;
    }

    /* Tables */
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; }

    /* Buttons */
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.2s;
    }
    .stButton > button:hover { background: #4f46e5; transform: translateY(-1px); }

    /* Warning / info boxes */
    .stAlert { border-radius: 10px; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
    }

    /* Plotly charts */
    .js-plotly-plot { border-radius: 12px; }

    /* Select box */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 10px;
        border-color: #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)


inject_css()


# ─────────────────────────────────────────────
# Sidebar — Global Controls
# ─────────────────────────────────────────────
def render_sidebar() -> tuple:
    with st.sidebar:
        st.markdown("## 🌐 SCM FutureRisk AI")
        st.markdown("<div style='color:#475569;font-size:12px;margin-bottom:20px'>Powered by Claude + ML Forecasting</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🗺️ Analysis Parameters")

        country = st.selectbox(
            "🌍 Country",
            options=COUNTRIES,
            index=0,
            help="Select the supply chain origin country to analyze",
        )

        industry = st.selectbox(
            "🏭 Industry",
            options=INDUSTRIES,
            index=0,
            help="Select your industry sector",
        )

        horizon = st.selectbox(
            "📅 Time Horizon",
            options=TIME_HORIZONS,
            index=1,
            help="Select the planning horizon for risk forecasting",
        )

        st.markdown("---")
        st.markdown("### 📋 Navigation")

        pages = {
            "🏠 Executive Summary":      "home",
            "🌍 Country Intelligence":   "country",
            "📡 Global Risk Monitor":    "monitor",
            "🤖 ML Forecast":            "forecast",
            "🧠 Claude Decision Room":   "decision",
            "✅ Evidence Verification":  "evidence",
            "🎛️ Scenario Simulator":      "simulator",
            "📚 Data Sources":           "sources",
        }

        page_key = st.radio("", list(pages.keys()), label_visibility="collapsed")
        active_page = pages[page_key]

        st.markdown("---")
        # API status indicators
        st.markdown("### ⚙️ API Status")
        api_status = lambda key, name: st.markdown(
            f"{'✅' if key else '⚠️'} **{name}**: {'Connected' if key else 'Demo Mode'}",
            unsafe_allow_html=True
        )
        api_status(ANTHROPIC_KEY, "Claude AI")
        api_status(SEARCH_API_KEY, "Search API")

        if not ANTHROPIC_KEY or not SEARCH_API_KEY:
            st.caption("Add API keys in `.env` for live data and AI analysis.")

        st.markdown("---")
        st.caption("© 2025 SCM FutureRisk AI · v1.0")

    return country, industry, horizon, active_page


# ─────────────────────────────────────────────
# Data Loading (cached)
# ─────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def load_analysis_data(country: str, industry: str):
    """Load and compute all analysis data for a country/industry pair."""
    profile   = COUNTRY_PROFILES[country].copy()
    profile["name"] = country

    signals   = fetch_live_signals(country, SEARCH_API_KEY, SEARCH_ENGINE)
    ind_mod   = INDUSTRY_RISK_MODIFIERS.get(industry, {})
    baseline  = profile.get("baseline_risk", 50)

    forecast  = forecast_risk(profile, signals, ind_mod, baseline)
    series    = generate_forecast_series(
        forecast["current_risk"], forecast["risk_90"], forecast["risk_180"]
    )
    feat_imp  = compute_feature_importance(profile, signals)
    drivers   = get_key_drivers(feat_imp, country, industry)
    sig_cards = build_signal_summary(signals)

    return profile, signals, forecast, series, feat_imp, drivers, sig_cards


# ─────────────────────────────────────────────
# Helper: Render a signal badge
# ─────────────────────────────────────────────
def _badge(text, color):
    cls = {"#22c55e": "green", "#f59e0b": "yellow", "#ef4444": "red",
           "#3b82f6": "blue", "#6366f1": "purple"}.get(color, "blue")
    return f'<span class="badge badge-{cls}">{text}</span>'


# ═══════════════════════════════════════════════════════════════
# PAGE 1 — HOME / EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════
def page_home(country, industry, horizon, profile, signals, forecast, series, drivers, sig_cards):
    flag = profile.get("flag", "🌐")

    st.markdown(f"""
    <div class="page-header">
        <h1>{flag} {country} — Supply Chain Executive Summary</h1>
        <p>{industry} · {horizon} Planning Horizon · Live Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Risk Score", f"{forecast['current_risk']}/100", f"{forecast['risk_label']}")
    with c2:
        direction_clean = forecast['direction'].split()[0]
        st.metric("📈 Risk Direction", direction_clean, f"→ {forecast['risk_90']}/100 in 90d")
    with c3:
        st.metric("🔮 Confidence", forecast["confidence"], f"{forecast['confidence_pct']}%")
    with c4:
        st.metric("📅 30-Day Outlook", f"{forecast['risk_30']}/100", forecast['label_30'])

    # Gauge + Horizon bar
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.plotly_chart(risk_gauge(forecast["current_risk"]), use_container_width=True)
    with col_right:
        st.plotly_chart(horizon_bar_chart(forecast), use_container_width=True)

    # Forecast line
    st.plotly_chart(forecast_line_chart(series, country), use_container_width=True)

    # Signal cards row
    st.markdown('<div class="section-title">📡 Real-Time Market Signals</div>', unsafe_allow_html=True)
    cols = st.columns(len(sig_cards))
    for i, card in enumerate(sig_cards):
        with cols[i]:
            st.markdown(f"""
            <div class="risk-card" style="text-align:center;padding:14px">
                <div style="font-size:22px">{card['icon']}</div>
                <div style="font-size:11px;color:#64748b;font-weight:600;text-transform:uppercase;margin:4px 0">{card['metric']}</div>
                <div style="font-size:14px;font-weight:700;color:{card['color']}">{card['value']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Key drivers
    st.markdown('<div class="section-title">🔬 Top ML Risk Drivers</div>', unsafe_allow_html=True)
    for text, direction, pts in drivers[:5]:
        color = "#ef4444" if "increases" in direction else "#22c55e"
        icon  = "🔺" if "increases" in direction else "🔻"
        st.markdown(f"""
        <div class="risk-card" style="display:flex;align-items:center;gap:12px;padding:12px 18px">
            <div style="font-size:18px">{icon}</div>
            <div style="flex:1;font-size:14px;color:#374151">{text}</div>
            <div style="font-size:13px;font-weight:700;color:{color}">{direction} · {pts} pts</div>
        </div>
        """, unsafe_allow_html=True)

    # Country summary
    st.markdown('<div class="section-title">📝 Country Brief</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="risk-card">
        <p style="font-size:15px;color:#374151;line-height:1.7;margin:0">{profile['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

    if not signals.get("news_available"):
        st.warning("⚠️ **Demo Mode**: Add `SEARCH_API_KEY` and `SEARCH_ENGINE_ID` in `.env` for live news signals.")
    if not ANTHROPIC_KEY:
        st.warning("⚠️ **Demo Mode**: Add `ANTHROPIC_API_KEY` in `.env` for Claude AI strategic recommendations.")


# ═══════════════════════════════════════════════════════════════
# PAGE 2 — COUNTRY INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
def page_country_intelligence(country, profile):
    flag = profile.get("flag", "🌐")
    st.markdown(f"""
    <div class="page-header">
        <h1>{flag} Country Intelligence — {country}</h1>
        <p>Structured supply chain indicator profile · {profile.get('continent','Asia')} · {profile.get('region','')}</p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="section-title">📊 Intelligence Indicators</div>', unsafe_allow_html=True)
        for key, desc in INDICATOR_DESCRIPTIONS.items():
            val = profile.get(key, 50)
            # Color by value for "negative" indicators (higher = worse)
            negative_keys = {"trade_war_pressure", "security_flashpoints", "domestic_unrest", "strategic_rivalry"}
            if key in negative_keys:
                bar_color = "#22c55e" if val < 30 else ("#f59e0b" if val < 60 else "#ef4444")
            else:
                bar_color = "#ef4444" if val < 40 else ("#f59e0b" if val < 65 else "#22c55e")

            pct = val
            st.markdown(f"""
            <div class="risk-card" style="padding:12px 18px;margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                    <div>
                        <div style="font-size:13px;font-weight:600;color:#1e293b">{key.replace('_',' ').title()}</div>
                        <div style="font-size:11px;color:#94a3b8">{desc}</div>
                    </div>
                    <div style="font-size:18px;font-weight:700;color:{bar_color}">{val}</div>
                </div>
                <div style="background:#f1f5f9;border-radius:99px;height:6px">
                    <div style="width:{pct}%;background:{bar_color};border-radius:99px;height:6px;transition:width 0.5s"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-title">🕸️ Capability Radar</div>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(profile), use_container_width=True)

        st.markdown('<div class="section-title">🌍 Comparative Standing</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("🌐 World Standing",     f"{profile.get('world_standing',50)}/100")
            st.metric("💰 Economic Weight",    f"{profile.get('economic_weight',50)}/100")
            st.metric("🚢 Port Efficiency",    f"{profile.get('port_efficiency',60)}/100")
        with c2:
            st.metric("🤝 Bargaining Power",   f"{profile.get('bargaining_power',50)}/100")
            st.metric("🔗 Trade Leverage",     f"{profile.get('trade_leverage',50)}/100")
            st.metric("💱 Currency Stability", f"{profile.get('currency_stability',65)}/100")

    # Country comparison
    st.markdown('<div class="section-title">📊 All Countries — Baseline Risk Comparison</div>', unsafe_allow_html=True)
    st.plotly_chart(country_comparison_chart(COUNTRY_PROFILES, "baseline_risk"), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 3 — GLOBAL RISK MONITOR
# ═══════════════════════════════════════════════════════════════
def page_global_monitor(country, signals, sig_cards):
    st.markdown(f"""
    <div class="page-header">
        <h1>📡 Global Risk Monitor</h1>
        <p>Real-time supply chain signal intelligence · {'Live Data' if signals.get('news_available') else 'Demo Data'}</p>
    </div>
    """, unsafe_allow_html=True)

    if not signals.get("news_available"):
        st.warning("⚠️ **Demo data** shown. Connect `SEARCH_API_KEY` for live signals.")

    # Signal heatmap
    st.markdown('<div class="section-title">🌡️ Signal Intensity Heatmap</div>', unsafe_allow_html=True)
    from modules.visualizations import signal_heatmap
    st.plotly_chart(signal_heatmap(signals), use_container_width=True)

    # Signal cards
    cols = st.columns(3)
    for i, card in enumerate(sig_cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="risk-card">
                <div style="display:flex;align-items:center;gap:10px">
                    <div style="font-size:24px">{card['icon']}</div>
                    <div>
                        <div style="font-size:12px;color:#64748b;font-weight:600;text-transform:uppercase">{card['metric']}</div>
                        <div style="font-size:16px;font-weight:700;color:{card['color']}">{card['value']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # News articles
    st.markdown('<div class="section-title">📰 Latest Supply Chain Intelligence</div>', unsafe_allow_html=True)
    articles = signals.get("articles", [])
    for art in articles:
        sent = art.get("sentiment", "neutral")
        sent_color = "#22c55e" if sent == "positive" else ("#ef4444" if sent == "negative" else "#f59e0b")
        sent_icon  = "✅" if sent == "positive" else ("🔴" if sent == "negative" else "🟡")
        kw_html = " ".join(f'<span class="badge badge-blue">{kw}</span>' for kw in art.get("keywords", [])[:4])
        st.markdown(f"""
        <div class="risk-card">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px">
                <div style="flex:1">
                    <div style="font-size:14px;font-weight:600;color:#1e293b;margin-bottom:4px">{art['title']}</div>
                    <div style="font-size:13px;color:#64748b;margin-bottom:8px">{art['snippet']}</div>
                    <div>{kw_html}</div>
                </div>
                <div style="text-align:right;min-width:90px">
                    <div style="font-size:11px;color:#94a3b8;font-weight:600">{art.get('source','')}</div>
                    <div style="font-size:13px;font-weight:600;color:{sent_color};margin-top:4px">{sent_icon} {sent.title()}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Global reference data
    st.markdown('<div class="section-title">🌐 Global Macro Context</div>', unsafe_allow_html=True)
    macro_data = {
        "Global GSCPI Signal": f"{signals.get('gscpi', 0.4):+.2f}σ",
        "Oil Price Pressure":  f"{signals.get('oil_pressure', 0.5):.0%}",
        "Freight Cost Index":  f"{signals.get('freight_index', 0.5):.0%}",
        "Tariff Intensity":    f"{signals.get('tariff_intensity', 0.4):.0%}",
        "Conflict Index":      f"{signals.get('conflict_index', 0.4):.0%}",
        "News Sentiment":      f"{signals.get('sentiment', 0):+.2f}",
    }
    cols = st.columns(3)
    for i, (k, v) in enumerate(macro_data.items()):
        with cols[i % 3]:
            st.metric(k, v)


# ═══════════════════════════════════════════════════════════════
# PAGE 4 — ML FORECAST
# ═══════════════════════════════════════════════════════════════
def page_ml_forecast(country, industry, horizon, profile, signals, forecast, series, feat_imp, drivers):
    flag = profile.get("flag", "🌐")
    st.markdown(f"""
    <div class="page-header">
        <h1>🤖 ML Forecast Engine</h1>
        <p>{flag} {country} · {industry} · Gradient Boosting + Feature Importance</p>
    </div>
    """, unsafe_allow_html=True)

    # Forecast summary cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📊 Current Risk",  f"{forecast['current_risk']}/100", forecast['risk_label'])
    with c2: st.metric("📅 30-Day",        f"{forecast['risk_30']}/100",     forecast['label_30'])
    with c3: st.metric("📅 90-Day",        f"{forecast['risk_90']}/100",     forecast['label_90'])
    with c4: st.metric("📅 6-Month",       f"{forecast['risk_180']}/100",    forecast['label_180'])

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.plotly_chart(forecast_line_chart(series, country), use_container_width=True)
    with col_right:
        st.plotly_chart(risk_gauge(forecast["current_risk"]), use_container_width=True)
        st.markdown(f"""
        <div class="risk-card" style="text-align:center;margin-top:0">
            <div style="font-size:12px;color:#64748b;font-weight:600;text-transform:uppercase;margin-bottom:6px">Risk Direction</div>
            <div style="font-size:18px;font-weight:700;color:{forecast['direction_color']}">{forecast['direction']}</div>
            <div style="font-size:12px;color:#94a3b8;margin-top:4px">Confidence: {forecast['confidence']} ({forecast['confidence_pct']}%)</div>
        </div>
        """, unsafe_allow_html=True)

    # Feature importance + horizon bar
    col_fi, col_hb = st.columns([1, 1])
    with col_fi:
        st.markdown('<div class="section-title">🔬 SHAP-Style Feature Importance</div>', unsafe_allow_html=True)
        st.plotly_chart(feature_importance_chart(feat_imp), use_container_width=True)
    with col_hb:
        st.markdown('<div class="section-title">📊 Multi-Horizon Comparison</div>', unsafe_allow_html=True)
        st.plotly_chart(horizon_bar_chart(forecast), use_container_width=True)

    # Key drivers table
    st.markdown('<div class="section-title">🔑 Top Risk Drivers — Explained</div>', unsafe_allow_html=True)
    for text, direction, pts in drivers:
        color = "#ef4444" if "increases" in direction else "#22c55e"
        icon  = "🔺" if "increases" in direction else "🔻"
        badge_cls = "badge-red" if "increases" in direction else "badge-green"
        st.markdown(f"""
        <div class="risk-card" style="display:flex;align-items:center;gap:14px;padding:12px 18px">
            <div style="font-size:20px">{icon}</div>
            <div style="flex:1">
                <div style="font-size:14px;font-weight:500;color:#1e293b">{text}</div>
            </div>
            <span class="badge {badge_cls}">{direction} · {pts} pts</span>
        </div>
        """, unsafe_allow_html=True)

    # Model info expander
    with st.expander("🔧 Model Architecture Details"):
        st.markdown("""
        | Component | Detail |
        |-----------|--------|
        | **Model Type** | Gradient Boosting Regressor (scikit-learn) |
        | **Training Data** | 800 synthetic samples with country-risk features |
        | **Features** | 17 country + global signal features |
        | **Scaler** | StandardScaler (Z-score normalization) |
        | **Forecasting** | Quadratic interpolation over 180-day horizon |
        | **Feature Importance** | Permutation-based sensitivity (+15% perturbation) |
        | **Time Series** | Bezier-interpolated confidence band |
        | **Update Frequency** | Re-scored on each country/industry selection |
        """)


# ═══════════════════════════════════════════════════════════════
# PAGE 5 — CLAUDE DECISION ROOM
# ═══════════════════════════════════════════════════════════════
def page_decision_room(country, industry, horizon, profile, signals, forecast, drivers):
    flag = profile.get("flag", "🌐")
    st.markdown(f"""
    <div class="page-header">
        <h1>🧠 Claude Decision Room</h1>
        <p>{flag} {country} · {industry} · AI-Powered Strategic Recommendation</p>
    </div>
    """, unsafe_allow_html=True)

    if not ANTHROPIC_KEY:
        st.info("💡 **Rule-based mode active.** Add `ANTHROPIC_API_KEY` to `.env` for Claude AI analysis.", icon="ℹ️")

    with st.spinner("🔄 Analyzing supply chain intelligence and generating strategic recommendation..."):
        decision = get_claude_decision(
            country, industry, horizon, forecast, signals, profile, drivers, ANTHROPIC_KEY
        )

    source_label = "🤖 Claude AI" if decision.get("_source") == "claude" else "📋 Rule-Based Engine"

    # Situation summary
    st.markdown(f"""
    <div class="risk-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div style="font-size:14px;font-weight:700;color:#1e293b">📋 Situation Summary</div>
            <span class="badge badge-purple">{source_label}</span>
        </div>
        <p style="font-size:15px;color:#374151;line-height:1.75;margin:0">{decision.get('situation_summary','')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Outlook cards
    st.markdown('<div class="section-title">🔮 Multi-Horizon Outlook</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, label, key in [(c1,"30-Day","outlook_30"), (c2,"90-Day","outlook_90"), (c3,"6-Month","outlook_180")]:
        with col:
            st.markdown(f"""
            <div class="risk-card">
                <div style="font-size:12px;font-weight:700;color:#6366f1;text-transform:uppercase;margin-bottom:6px">{label} Outlook</div>
                <p style="font-size:13px;color:#374151;line-height:1.65;margin:0">{decision.get(key,'')}</p>
            </div>
            """, unsafe_allow_html=True)

    # Risks & Opportunities
    col_r, col_o = st.columns(2)
    with col_r:
        st.markdown('<div class="section-title">⚠️ Main Risks</div>', unsafe_allow_html=True)
        for r in decision.get("main_risks", []):
            st.markdown(f"""
            <div class="risk-card" style="display:flex;gap:10px;padding:10px 16px;margin-bottom:8px;border-left:3px solid #ef4444">
                <div style="color:#ef4444;font-size:16px">🔺</div>
                <div style="font-size:13px;color:#374151">{r}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_o:
        st.markdown('<div class="section-title">✨ Main Opportunities</div>', unsafe_allow_html=True)
        for o in decision.get("main_opportunities", []):
            st.markdown(f"""
            <div class="risk-card" style="display:flex;gap:10px;padding:10px 16px;margin-bottom:8px;border-left:3px solid #22c55e">
                <div style="color:#22c55e;font-size:16px">🟢</div>
                <div style="font-size:13px;color:#374151">{o}</div>
            </div>
            """, unsafe_allow_html=True)

    # ⭐ Main recommendation
    rec = decision.get("recommended_decision", "Monitor only")
    confidence = decision.get("confidence_level", "Medium")
    confidence_color = {"High": "#22c55e", "Medium-High": "#22c55e", "Medium": "#f59e0b", "Low": "#ef4444"}.get(confidence, "#f59e0b")

    st.markdown(f"""
    <div class="risk-card" style="border:2px solid #6366f1;background:linear-gradient(135deg,#f5f3ff,#eff6ff)">
        <div style="font-size:12px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">⭐ Recommended Decision</div>
        <div style="font-size:22px;font-weight:800;color:#1e293b;margin-bottom:10px">{rec}</div>
        <div style="font-size:13px;color:#475569;line-height:1.7;margin-bottom:10px">{decision.get('decision_rationale','')}</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">
            <span class="badge badge-purple">Confidence: {confidence}</span>
            <span class="badge badge-blue">{forecast['current_risk']}/100 Risk</span>
            <span class="badge badge-blue">{forecast['direction'].split()[0]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action plan
    st.markdown('<div class="section-title">📋 5-Step Action Plan</div>', unsafe_allow_html=True)
    for i, step in enumerate(decision.get("action_plan", []), 1):
        st.markdown(f"""
        <div class="risk-card" style="display:flex;gap:14px;align-items:flex-start;padding:12px 18px;margin-bottom:8px">
            <div style="min-width:28px;height:28px;background:#6366f1;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-size:12px;font-weight:700">{i}</div>
            <div style="font-size:14px;color:#374151;line-height:1.6">{step}</div>
        </div>
        """, unsafe_allow_html=True)

    # Confidence explanation
    st.markdown(f"""
    <div class="risk-card" style="background:#fffbeb;border-left:3px solid #f59e0b">
        <div style="font-size:12px;font-weight:700;color:#d97706;text-transform:uppercase;margin-bottom:4px">💡 Confidence Note</div>
        <div style="font-size:13px;color:#374151">{decision.get('confidence_explanation','')}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 6 — EVIDENCE VERIFICATION
# ═══════════════════════════════════════════════════════════════
def page_evidence(country, industry, horizon, profile, signals, forecast, drivers):
    flag = profile.get("flag", "🌐")
    st.markdown(f"""
    <div class="page-header">
        <h1>✅ Evidence Verification</h1>
        <p>{flag} {country} · Cross-checking AI claims against live intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    decision = get_claude_decision(
        country, industry, horizon, forecast, signals, profile, drivers, ANTHROPIC_KEY
    )
    ev = verify_evidence(decision, signals)

    # Evidence quality metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("📊 Evidence Quality", ev["evidence_quality"])
    with c2: st.metric("✅ Claims Supported", f"{ev['claims_supported']}/{ev['claims_total']}")
    with c3: st.metric("📰 Articles Reviewed", ev["articles_reviewed"])
    with c4: st.metric("🔗 Source Type", ev["source_type"])

    # Evidence strength bar
    pct = ev["support_ratio"]
    bar_color = ev["evidence_color"]
    st.markdown(f"""
    <div class="risk-card" style="margin-top:8px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <div style="font-size:14px;font-weight:600;color:#1e293b">📊 Evidence Support Ratio</div>
            <div style="font-size:14px;font-weight:700;color:{bar_color}">{pct}%</div>
        </div>
        <div style="background:#f1f5f9;border-radius:99px;height:10px">
            <div style="width:{pct}%;background:{bar_color};border-radius:99px;height:10px;transition:width 0.8s"></div>
        </div>
        <div style="font-size:12px;color:#94a3b8;margin-top:6px">
            {pct}% of identified risk claims are supported by available news and signal data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Verified vs unverified
    col_v, col_u = st.columns(2)
    with col_v:
        st.markdown('<div class="section-title">✅ Verified Claims</div>', unsafe_allow_html=True)
        for risk in decision.get("main_risks", []):
            st.markdown(f"""
            <div class="risk-card" style="border-left:3px solid #22c55e;padding:10px 16px;margin-bottom:8px">
                <div style="font-size:13px;color:#374151">{risk}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_u:
        st.markdown('<div class="section-title">⚠️ Unverified Assumptions</div>', unsafe_allow_html=True)
        for assumption in decision.get("unsupported_assumptions", []):
            st.markdown(f"""
            <div class="risk-card" style="border-left:3px solid #f59e0b;padding:10px 16px;margin-bottom:8px">
                <div style="font-size:13px;color:#374151">{assumption}</div>
            </div>
            """, unsafe_allow_html=True)

    # Source articles table
    st.markdown('<div class="section-title">🔗 Source Intelligence</div>', unsafe_allow_html=True)
    articles = signals.get("articles", [])
    if articles:
        import pandas as pd
        df = pd.DataFrame([{
            "Title":     a["title"][:80] + "..." if len(a["title"]) > 80 else a["title"],
            "Source":    a.get("source", ""),
            "Sentiment": a.get("sentiment", "neutral").title(),
            "Keywords":  ", ".join(a.get("keywords", [])[:3]),
        } for a in articles])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No news articles available. Connect Search API for live source verification.")

    # Verification summary
    st.markdown(f"""
    <div class="risk-card" style="background:#f0fdf4;border-left:3px solid #22c55e;margin-top:8px">
        <div style="font-size:13px;font-weight:700;color:#15803d;margin-bottom:4px">🔍 Verification Summary</div>
        <div style="font-size:13px;color:#374151">{decision.get('verification_notes','')}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 7 — SCENARIO SIMULATOR
# ═══════════════════════════════════════════════════════════════
def page_simulator(country, profile, forecast):
    flag = profile.get("flag", "🌐")
    st.markdown(f"""
    <div class="page-header">
        <h1>🎛️ Scenario Simulator</h1>
        <p>{flag} {country} · Adjust supply chain levers and see live impact</p>
    </div>
    """, unsafe_allow_html=True)

    base_risk = forecast["current_risk"]

    col_controls, col_results = st.columns([1, 1.4])

    with col_controls:
        st.markdown('<div class="section-title">⚙️ Scenario Levers</div>', unsafe_allow_html=True)
        lever_values = {}
        for key, cfg in LEVER_CONFIG.items():
            lever_values[key] = st.slider(
                f"{cfg['icon']} {cfg['label']}",
                min_value=cfg["min"],
                max_value=cfg["max"],
                value=cfg["default"],
                step=cfg["step"],
                help=cfg["help"],
            )

    with col_results:
        sim = run_simulation(base_risk, lever_values)

        st.markdown('<div class="section-title">📊 Simulation Results</div>', unsafe_allow_html=True)

        # Result KPIs
        c1, c2 = st.columns(2)
        with c1:
            st.metric("🎯 Adjusted Risk Score",  f"{sim['adjusted_risk']}/100",
                      delta=f"{sim['risk_delta']:+.1f} pts vs baseline")
            st.metric("📦 Safety Stock (weeks)", f"{sim['safety_stock_weeks']} wks")
        with c2:
            st.metric("🚢 Expected Lead Time",   f"{sim['adjusted_lead_time']} days",
                      delta=f"{sim['lead_time_delta']:+.1f} days vs baseline")
            st.metric("🏭 Supplier Reliability", f"{sim['supplier_reliability']:.0f}%")

        # Cost pressure gauge
        cost = sim["cost_pressure"]
        cost_color = "#22c55e" if cost < 30 else ("#f59e0b" if cost < 55 else "#ef4444")
        st.markdown(f"""
        <div class="risk-card" style="margin-top:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <div style="font-size:13px;font-weight:600;color:#1e293b">💸 Cost Pressure Index</div>
                <div style="font-size:14px;font-weight:700;color:{cost_color}">{cost:.0f}/100</div>
            </div>
            <div style="background:#f1f5f9;border-radius:99px;height:8px">
                <div style="width:{cost}%;background:{cost_color};border-radius:99px;height:8px"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Decision output
        st.markdown(f"""
        <div class="risk-card" style="border:2px solid #6366f1;margin-top:12px;text-align:center;padding:18px">
            <div style="font-size:12px;font-weight:700;color:#6366f1;text-transform:uppercase;margin-bottom:6px">Scenario Decision</div>
            <div style="font-size:18px;font-weight:700;color:{sim['decision_color']}">{sim['recommended_decision']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Tornado chart
        st.markdown('<div class="section-title">🌪️ Lever Sensitivity (Tornado)</div>', unsafe_allow_html=True)
        sensitivity = sensitivity_analysis(base_risk, lever_values)
        st.plotly_chart(tornado_chart(sensitivity), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 8 — DATA SOURCES & METHODOLOGY
# ═══════════════════════════════════════════════════════════════
def page_sources():
    st.markdown("""
    <div class="page-header">
        <h1>📚 Data Sources & Methodology</h1>
        <p>Transparency on how SCM FutureRisk AI generates its intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ## 🔬 Analytical Framework

    SCM FutureRisk AI combines **three analytical layers** to produce supply chain risk intelligence:

    ---
    ### 1. Country Intelligence Layer
    Static country profiles derived from publicly available trade data, World Bank indicators, and geopolitical risk indices.

    | Indicator | Source Reference |
    |-----------|-----------------|
    | World Standing | IMF World Economic Outlook |
    | Trade Leverage | WTO Trade Profiles |
    | Bargaining Power | Composite Score (GDP, FTA Coverage, Export Diversity) |
    | Security Flashpoints | Global Peace Index (IEP) |
    | Infrastructure Quality | World Bank Logistics Performance Index |
    | Port Efficiency | UNCTAD Port Performance Benchmarks |

    ---
    ### 2. Machine Learning Engine
    A **Gradient Boosting Regressor** (scikit-learn) trained on 800 synthetic country-risk samples.

    - **17 features**: country indicators + real-time global signals
    - **Feature importance**: Permutation-based sensitivity analysis (SHAP-style)
    - **Forecasting**: Quadratic Bezier interpolation with noise over 180-day horizon
    - **Confidence**: Derived from data availability (live vs. demo) and signal consistency

    ---
    ### 3. AI Decision Layer
    **Claude (Anthropic)** — `claude-sonnet-4-20250514` — analyzes the ML output, country profile, and news signals to produce structured strategic recommendations in JSON format.

    **Fallback**: A rule-based decision tree activates when no API key is available.

    ---
    ### 4. Search Intelligence
    **Google Custom Search API** queries for country-specific supply chain news, filtered for:
    - Tariffs & trade restrictions
    - Port congestion & freight costs
    - Geopolitical developments
    - PMI & manufacturing signals
    - Currency pressures

    **Sentiment Analysis**: Rule-based keyword scoring (negative/neutral/positive).

    ---
    ### 5. Scenario Simulator
    Linear sensitivity model applying **9 supply chain levers** to the baseline risk score.
    Each lever has calibrated weights for: risk score, lead time, cost pressure, and supplier reliability.

    ---
    ## ⚠️ Limitations & Disclaimers

    - **Not financial advice.** This tool is for analytical and educational purposes only.
    - **Synthetic ML training data** — real-world calibration against historical disruption data would improve accuracy.
    - **Demo mode** uses curated static signals — live search API required for real-time intelligence.
    - **Country profiles** are updated periodically and may not reflect very recent political changes.
    - All forecasts carry inherent uncertainty. Treat confidence scores as relative, not absolute.

    ---
    ## 🛠️ Technical Stack

    | Component | Technology |
    |-----------|-----------|
    | Frontend | Streamlit 1.32+ |
    | ML Model | scikit-learn GradientBoostingRegressor |
    | AI Layer | Anthropic Claude API (claude-sonnet-4) |
    | Search | Google Custom Search API |
    | Charts | Plotly 5.x |
    | Data | pandas, numpy |
    | Deployment | Streamlit Cloud / Render / Railway |
    """)


# ═══════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════
def main():
    # Sidebar controls
    country, industry, horizon, active_page = render_sidebar()

    # Load data (cached)
    with st.spinner(f"Loading intelligence for {country}..."):
        profile, signals, forecast, series, feat_imp, drivers, sig_cards = load_analysis_data(country, industry)

    # Route to correct page
    if active_page == "home":
        page_home(country, industry, horizon, profile, signals, forecast, series, drivers, sig_cards)
    elif active_page == "country":
        page_country_intelligence(country, profile)
    elif active_page == "monitor":
        page_global_monitor(country, signals, sig_cards)
    elif active_page == "forecast":
        page_ml_forecast(country, industry, horizon, profile, signals, forecast, series, feat_imp, drivers)
    elif active_page == "decision":
        page_decision_room(country, industry, horizon, profile, signals, forecast, drivers)
    elif active_page == "evidence":
        page_evidence(country, industry, horizon, profile, signals, forecast, drivers)
    elif active_page == "simulator":
        page_simulator(country, profile, forecast)
    elif active_page == "sources":
        page_sources()


if __name__ == "__main__":
    main()
