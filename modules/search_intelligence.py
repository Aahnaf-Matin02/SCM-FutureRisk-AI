"""
modules/search_intelligence.py
================================
Search intelligence layer for SCM FutureRisk AI.
Collects real-time supply chain signals from Google Custom Search API.
Falls back to curated demo data when API keys are unavailable.
"""

import os
import json
import time
import requests
from datetime import datetime
import streamlit as st

# ─────────────────────────────────────────────
# Demo / Fallback Data
# ─────────────────────────────────────────────

DEMO_SIGNALS = {
    "United States": {
        "sentiment": -0.25,
        "oil_pressure": 0.62,
        "freight_index": 0.55,
        "tariff_intensity": 0.68,
        "conflict_index": 0.45,
        "gscpi": 0.8,
        "news_available": True,
        "articles": [
            {
                "title": "U.S. semiconductor tariffs on China reach new highs amid export restrictions",
                "snippet": "Washington expands chip export controls, raising costs for electronics manufacturers.",
                "source": "Reuters",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["tariff", "semiconductor", "China", "export controls"],
            },
            {
                "title": "Freight rates surge as Panama Canal drought reduces capacity",
                "snippet": "Container shipping costs jump 28% as drought disrupts canal throughput.",
                "source": "Bloomberg",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["freight", "Panama Canal", "capacity", "shipping"],
            },
            {
                "title": "U.S. Manufacturing PMI holds at 49.2, signaling contraction",
                "snippet": "Factory activity remains below expansion threshold for fourth consecutive month.",
                "source": "ISM",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["PMI", "manufacturing", "contraction", "factory"],
            },
            {
                "title": "Nearshoring to Mexico accelerates as companies de-risk from Asia",
                "snippet": "Cross-border manufacturing investment rises 34% YoY as firms diversify supply chains.",
                "source": "WSJ",
                "url": "#",
                "sentiment": "positive",
                "keywords": ["nearshoring", "Mexico", "diversification", "investment"],
            },
        ],
    },
    "China": {
        "sentiment": -0.40,
        "oil_pressure": 0.58,
        "freight_index": 0.50,
        "tariff_intensity": 0.80,
        "conflict_index": 0.70,
        "gscpi": 1.2,
        "news_available": True,
        "articles": [
            {
                "title": "China faces escalating U.S. tariffs on $350B of goods as trade talks stall",
                "snippet": "Bilateral trade tensions deepen with no resolution in sight for major goods categories.",
                "source": "FT",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["tariff", "trade war", "bilateral", "US-China"],
            },
            {
                "title": "South China Sea tensions raise shipping risk premiums",
                "snippet": "Insurance costs for vessels transiting disputed waters rise as military activity increases.",
                "source": "Lloyd's",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["South China Sea", "shipping", "insurance", "military"],
            },
            {
                "title": "Chinese factory output recovers but global buyers accelerate China+1 strategy",
                "snippet": "Production rebounds post-lockdowns, but multinationals continue dual-sourcing strategies.",
                "source": "Bloomberg",
                "url": "#",
                "sentiment": "neutral",
                "keywords": ["manufacturing", "China+1", "dual sourcing", "FDI"],
            },
        ],
    },
    "Bangladesh": {
        "sentiment": -0.30,
        "oil_pressure": 0.70,
        "freight_index": 0.65,
        "tariff_intensity": 0.35,
        "conflict_index": 0.35,
        "gscpi": 0.5,
        "news_available": True,
        "articles": [
            {
                "title": "Bangladesh garment exports face EU sustainability compliance pressure",
                "snippet": "New EU deforestation and due diligence rules affect RMG supply chain compliance costs.",
                "source": "Apparel Insider",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["garment", "EU", "compliance", "sustainability"],
            },
            {
                "title": "Chittagong port congestion worsens during peak season",
                "snippet": "Vessel waiting times at Chittagong reach 8-10 days, up from 3 days baseline.",
                "source": "Drewry",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["Chittagong", "port", "congestion", "delay"],
            },
            {
                "title": "Bangladesh taka under pressure as forex reserves decline",
                "snippet": "Central bank reserve coverage drops to 3.8 months of imports, below recommended threshold.",
                "source": "IMF",
                "url": "#",
                "sentiment": "negative",
                "keywords": ["taka", "forex", "reserves", "currency"],
            },
        ],
    },
}

# Generic fallback for countries not in demo data
DEFAULT_SIGNALS = {
    "sentiment": -0.10,
    "oil_pressure": 0.55,
    "freight_index": 0.52,
    "tariff_intensity": 0.42,
    "conflict_index": 0.38,
    "gscpi": 0.4,
    "news_available": False,
    "articles": [
        {
            "title": "Global supply chain pressure index shows moderate elevation",
            "snippet": "GSCPI readings indicate above-average stress in global logistics networks.",
            "source": "NY Fed",
            "url": "https://www.newyorkfed.org/research/policy/gscpi",
            "sentiment": "negative",
            "keywords": ["GSCPI", "logistics", "pressure", "global"],
        },
        {
            "title": "Red Sea shipping diversions continue to add 10-14 days to Europe routes",
            "snippet": "Houthi attacks force container ships around Cape of Good Hope, raising freight costs.",
            "source": "Freightos",
            "url": "#",
            "sentiment": "negative",
            "keywords": ["Red Sea", "freight", "diversion", "shipping"],
        },
    ],
}


# ─────────────────────────────────────────────
# Live Google Custom Search API
# ─────────────────────────────────────────────

SEARCH_QUERIES = [
    "{country} supply chain disruption 2025",
    "{country} tariff trade restriction 2025",
    "{country} port congestion freight cost",
    "{country} geopolitical risk manufacturing",
    "{country} import export inflation PMI",
]


@st.cache_data(ttl=1800)  # Cache 30 minutes
def fetch_live_signals(country: str, api_key: str = None, engine_id: str = None) -> dict:
    """
    Fetch live supply chain signals from Google Custom Search API.
    Falls back to demo data if keys unavailable or on error.
    """
    if not api_key or not engine_id or api_key == "YOUR_GOOGLE_SEARCH_API_KEY":
        return _get_demo_signals(country)

    articles = []
    for query_template in SEARCH_QUERIES[:3]:  # Limit to 3 queries to save quota
        query = query_template.format(country=country)
        try:
            resp = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={
                    "key": api_key,
                    "cx": engine_id,
                    "q": query,
                    "num": 3,
                    "dateRestrict": "m3",  # Last 3 months
                },
                timeout=8,
            )
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get("items", []):
                    articles.append({
                        "title":    item.get("title", ""),
                        "snippet":  item.get("snippet", ""),
                        "source":   item.get("displayLink", ""),
                        "url":      item.get("link", "#"),
                        "sentiment": _quick_sentiment(item.get("title", "") + " " + item.get("snippet", "")),
                        "keywords": _extract_keywords(item.get("snippet", "")),
                    })
            time.sleep(0.3)  # Respect rate limits
        except Exception:
            continue

    if not articles:
        return _get_demo_signals(country)

    signals = _aggregate_signals(articles)
    signals["articles"] = articles[:8]
    signals["news_available"] = True
    return signals


def _get_demo_signals(country: str) -> dict:
    """Return demo signals, falling back to default if country not in demo data."""
    return DEMO_SIGNALS.get(country, DEFAULT_SIGNALS).copy()


def _quick_sentiment(text: str) -> str:
    """Rule-based sentiment from keywords."""
    neg = ["risk", "crisis", "disruption", "delay", "tariff", "sanction", "conflict",
           "shortage", "surge", "congestion", "inflation", "restrict", "block", "war"]
    pos = ["recovery", "growth", "opportunity", "stable", "improve", "invest", "boost",
           "agreement", "resolve", "open", "expand", "partner"]
    text_lower = text.lower()
    neg_count = sum(1 for w in neg if w in text_lower)
    pos_count = sum(1 for w in pos if w in text_lower)
    if neg_count > pos_count:
        return "negative"
    elif pos_count > neg_count:
        return "positive"
    return "neutral"


def _extract_keywords(text: str) -> list:
    """Extract simple risk-related keywords from text."""
    risk_keywords = [
        "tariff", "sanction", "disruption", "conflict", "shortage", "congestion",
        "delay", "inflation", "PMI", "freight", "port", "oil", "geopolitical",
        "recession", "ban", "export control", "manufacturing", "capacity",
    ]
    found = [kw for kw in risk_keywords if kw.lower() in text.lower()]
    return found[:5]


def _aggregate_signals(articles: list) -> dict:
    """Aggregate articles into numeric risk signals."""
    if not articles:
        return DEFAULT_SIGNALS.copy()

    sentiments = [a["sentiment"] for a in articles]
    neg_ratio = sentiments.count("negative") / len(sentiments)
    pos_ratio = sentiments.count("positive") / len(sentiments)
    sentiment_score = pos_ratio - neg_ratio  # range -1 to +1

    all_kw = [kw for a in articles for kw in a.get("keywords", [])]

    tariff_hit = sum(1 for kw in all_kw if kw in ["tariff", "sanction", "export control"]) / max(len(all_kw), 1)
    conflict_hit = sum(1 for kw in all_kw if kw in ["conflict", "geopolitical", "war"]) / max(len(all_kw), 1)
    freight_hit = sum(1 for kw in all_kw if kw in ["freight", "port", "congestion", "delay"]) / max(len(all_kw), 1)
    oil_hit = sum(1 for kw in all_kw if kw in ["oil", "energy", "inflation"]) / max(len(all_kw), 1)

    return {
        "sentiment": round(sentiment_score, 2),
        "oil_pressure": round(min(0.4 + oil_hit * 3 + neg_ratio * 0.2, 0.95), 2),
        "freight_index": round(min(0.35 + freight_hit * 3 + neg_ratio * 0.2, 0.95), 2),
        "tariff_intensity": round(min(0.3 + tariff_hit * 4 + neg_ratio * 0.15, 0.95), 2),
        "conflict_index": round(min(0.3 + conflict_hit * 4 + neg_ratio * 0.1, 0.95), 2),
        "gscpi": round(neg_ratio * 2.5 - pos_ratio * 1.0, 2),
    }


# ─────────────────────────────────────────────
# Signal Summary Card Data
# ─────────────────────────────────────────────

def build_signal_summary(signals: dict) -> list:
    """
    Build a human-readable list of signal cards from raw signal dict.
    Returns list of {metric, value, status, icon} dicts.
    """
    def status(val, thresholds):
        low, high = thresholds
        if val < low: return "Low", "#22c55e"
        elif val < high: return "Moderate", "#f59e0b"
        else: return "High", "#ef4444"

    sentiment = signals.get("sentiment", 0)
    sent_label = "Positive" if sentiment > 0.1 else ("Negative" if sentiment < -0.1 else "Neutral")
    sent_color = "#22c55e" if sentiment > 0.1 else ("#ef4444" if sentiment < -0.1 else "#f59e0b")

    oil_s, oil_c     = status(signals.get("oil_pressure", 0.5), (0.40, 0.70))
    freight_s, frt_c = status(signals.get("freight_index", 0.5), (0.40, 0.70))
    tariff_s, tar_c  = status(signals.get("tariff_intensity", 0.4), (0.35, 0.65))
    conflict_s, con_c = status(signals.get("conflict_index", 0.4), (0.35, 0.65))

    return [
        {"metric": "News Sentiment",       "value": sent_label,                       "color": sent_color,  "icon": "📰"},
        {"metric": "Oil Price Pressure",   "value": f"{oil_s} ({signals.get('oil_pressure',0.5):.0%})",    "color": oil_c,  "icon": "🛢️"},
        {"metric": "Freight Cost Index",   "value": f"{freight_s} ({signals.get('freight_index',0.5):.0%})","color": frt_c, "icon": "🚢"},
        {"metric": "Tariff Intensity",     "value": f"{tariff_s} ({signals.get('tariff_intensity',0.4):.0%})","color": tar_c,"icon": "🏷️"},
        {"metric": "Geopolitical Conflict","value": f"{conflict_s} ({signals.get('conflict_index',0.4):.0%})","color": con_c,"icon": "⚔️"},
        {"metric": "GSCPI Signal",         "value": f"{signals.get('gscpi', 0.4):+.2f} σ",                "color": "#6366f1","icon": "📊"},
    ]
