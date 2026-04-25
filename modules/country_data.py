"""
modules/country_data.py
========================
Static country intelligence profiles for SCM FutureRisk AI.
Each country has structured indicators used as ML features and for display.
Scores are 0–100 unless noted. Higher = more favorable for supply chain.
"""

COUNTRY_PROFILES = {
    "United States": {
        "region": "North America",
        "continent": "Americas",
        "flag": "🇺🇸",
        "continent_standing": 95,
        "world_standing": 97,
        "bargaining_power": 92,
        "economic_weight": 95,
        "trade_leverage": 90,
        "strategic_position": 88,
        "trade_war_pressure": 55,       # lower = more pressure FROM others
        "security_flashpoints": 30,     # lower = fewer flashpoints
        "domestic_unrest": 35,
        "strategic_rivalry": 60,
        # Additional ML features
        "infrastructure_quality": 88,
        "regulatory_stability": 75,
        "currency_stability": 90,
        "labor_reliability": 80,
        "port_efficiency": 82,
        "supplier_base_depth": 88,
        "baseline_risk": 38,
        "summary": (
            "The United States holds the highest global trade leverage, backed by deep "
            "capital markets, technological dominance, and reserve-currency status. "
            "Internal political polarization and rising protectionism add moderate friction."
        ),
    },
    "China": {
        "region": "East Asia",
        "continent": "Asia",
        "flag": "🇨🇳",
        "continent_standing": 98,
        "world_standing": 92,
        "bargaining_power": 88,
        "economic_weight": 93,
        "trade_leverage": 87,
        "strategic_position": 85,
        "trade_war_pressure": 70,
        "security_flashpoints": 65,
        "domestic_unrest": 25,
        "strategic_rivalry": 85,
        "infrastructure_quality": 85,
        "regulatory_stability": 55,
        "currency_stability": 72,
        "labor_reliability": 75,
        "port_efficiency": 80,
        "supplier_base_depth": 95,
        "baseline_risk": 52,
        "summary": (
            "China is the world's largest manufacturer and exporter, offering unmatched "
            "supplier depth. Escalating geopolitical tensions, tariff pressures, and "
            "regulatory unpredictability raise supply chain concentration risk."
        ),
    },
    "India": {
        "region": "South Asia",
        "continent": "Asia",
        "flag": "🇮🇳",
        "continent_standing": 85,
        "world_standing": 78,
        "bargaining_power": 72,
        "economic_weight": 80,
        "trade_leverage": 68,
        "strategic_position": 74,
        "trade_war_pressure": 40,
        "security_flashpoints": 55,
        "domestic_unrest": 42,
        "strategic_rivalry": 50,
        "infrastructure_quality": 60,
        "regulatory_stability": 58,
        "currency_stability": 62,
        "labor_reliability": 70,
        "port_efficiency": 58,
        "supplier_base_depth": 72,
        "baseline_risk": 45,
        "summary": (
            "India is the fastest-growing large economy with strong IT and pharmaceutical "
            "export capabilities. Infrastructure gaps and regulatory complexity remain "
            "supply chain headwinds, though geopolitical diversification favors India."
        ),
    },
    "Bangladesh": {
        "region": "South Asia",
        "continent": "Asia",
        "flag": "🇧🇩",
        "continent_standing": 55,
        "world_standing": 48,
        "bargaining_power": 35,
        "economic_weight": 42,
        "trade_leverage": 38,
        "strategic_position": 40,
        "trade_war_pressure": 25,
        "security_flashpoints": 35,
        "domestic_unrest": 50,
        "strategic_rivalry": 20,
        "infrastructure_quality": 42,
        "regulatory_stability": 45,
        "currency_stability": 48,
        "labor_reliability": 72,
        "port_efficiency": 45,
        "supplier_base_depth": 45,
        "baseline_risk": 58,
        "summary": (
            "Bangladesh dominates global RMG (ready-made garments) with competitive "
            "labor costs and GSP trade access. Port limitations at Chittagong, "
            "political volatility, and climate vulnerability create supply chain risk."
        ),
    },
    "Vietnam": {
        "region": "Southeast Asia",
        "continent": "Asia",
        "flag": "🇻🇳",
        "continent_standing": 68,
        "world_standing": 62,
        "bargaining_power": 55,
        "economic_weight": 60,
        "trade_leverage": 60,
        "strategic_position": 65,
        "trade_war_pressure": 30,
        "security_flashpoints": 30,
        "domestic_unrest": 20,
        "strategic_rivalry": 35,
        "infrastructure_quality": 62,
        "regulatory_stability": 60,
        "currency_stability": 65,
        "labor_reliability": 78,
        "port_efficiency": 65,
        "supplier_base_depth": 60,
        "baseline_risk": 40,
        "summary": (
            "Vietnam has emerged as a top China+1 manufacturing hub for electronics "
            "and apparel. FDI inflows, young workforce, and FTA coverage are strengths. "
            "Infrastructure bottlenecks and South China Sea tensions are watch items."
        ),
    },
    "Germany": {
        "region": "Western Europe",
        "continent": "Europe",
        "flag": "🇩🇪",
        "continent_standing": 92,
        "world_standing": 88,
        "bargaining_power": 82,
        "economic_weight": 85,
        "trade_leverage": 85,
        "strategic_position": 82,
        "trade_war_pressure": 38,
        "security_flashpoints": 25,
        "domestic_unrest": 28,
        "strategic_rivalry": 40,
        "infrastructure_quality": 90,
        "regulatory_stability": 88,
        "currency_stability": 88,
        "labor_reliability": 88,
        "port_efficiency": 88,
        "supplier_base_depth": 82,
        "baseline_risk": 28,
        "summary": (
            "Germany is Europe's industrial anchor, renowned for engineering, automotive, "
            "and chemical supply chains. Energy transition costs and Russian gas dependency "
            "aftermath represent structural supply chain vulnerabilities."
        ),
    },
    "Japan": {
        "region": "East Asia",
        "continent": "Asia",
        "flag": "🇯🇵",
        "continent_standing": 88,
        "world_standing": 85,
        "bargaining_power": 80,
        "economic_weight": 82,
        "trade_leverage": 78,
        "strategic_position": 80,
        "trade_war_pressure": 30,
        "security_flashpoints": 40,
        "domestic_unrest": 12,
        "strategic_rivalry": 45,
        "infrastructure_quality": 92,
        "regulatory_stability": 85,
        "currency_stability": 70,
        "labor_reliability": 92,
        "port_efficiency": 88,
        "supplier_base_depth": 78,
        "baseline_risk": 32,
        "summary": (
            "Japan offers world-class manufacturing precision and Just-In-Time supply chain "
            "mastery. Yen depreciation, aging workforce, and North Korea-China proximity "
            "risk are ongoing concerns for global supply chain planners."
        ),
    },
    "Malaysia": {
        "region": "Southeast Asia",
        "continent": "Asia",
        "flag": "🇲🇾",
        "continent_standing": 70,
        "world_standing": 65,
        "bargaining_power": 60,
        "economic_weight": 62,
        "trade_leverage": 65,
        "strategic_position": 68,
        "trade_war_pressure": 28,
        "security_flashpoints": 28,
        "domestic_unrest": 22,
        "strategic_rivalry": 32,
        "infrastructure_quality": 72,
        "regulatory_stability": 68,
        "currency_stability": 65,
        "labor_reliability": 75,
        "port_efficiency": 75,
        "supplier_base_depth": 65,
        "baseline_risk": 38,
        "summary": (
            "Malaysia is a critical global semiconductor and electronics hub, strategically "
            "positioned in ASEAN. Port Klang is one of Asia's busiest. Ethnic political "
            "dynamics and semiconductor concentration risk are notable."
        ),
    },
    "Indonesia": {
        "region": "Southeast Asia",
        "continent": "Asia",
        "flag": "🇮🇩",
        "continent_standing": 72,
        "world_standing": 65,
        "bargaining_power": 60,
        "economic_weight": 65,
        "trade_leverage": 58,
        "strategic_position": 62,
        "trade_war_pressure": 25,
        "security_flashpoints": 32,
        "domestic_unrest": 30,
        "strategic_rivalry": 30,
        "infrastructure_quality": 60,
        "regulatory_stability": 60,
        "currency_stability": 58,
        "labor_reliability": 68,
        "port_efficiency": 58,
        "supplier_base_depth": 62,
        "baseline_risk": 45,
        "summary": (
            "Indonesia is ASEAN's largest economy and a key nickel/palm oil exporter. "
            "Resource nationalism policies and multi-island logistics complexity create "
            "supply chain friction despite strong commodity supply fundamentals."
        ),
    },
    "Singapore": {
        "region": "Southeast Asia",
        "continent": "Asia",
        "flag": "🇸🇬",
        "continent_standing": 80,
        "world_standing": 82,
        "bargaining_power": 72,
        "economic_weight": 68,
        "trade_leverage": 85,
        "strategic_position": 92,
        "trade_war_pressure": 18,
        "security_flashpoints": 12,
        "domestic_unrest": 8,
        "strategic_rivalry": 25,
        "infrastructure_quality": 98,
        "regulatory_stability": 97,
        "currency_stability": 92,
        "labor_reliability": 92,
        "port_efficiency": 98,
        "supplier_base_depth": 55,
        "baseline_risk": 18,
        "summary": (
            "Singapore is the world's premier trade and logistics hub, with AAA-rated "
            "port infrastructure, rule of law, and FTA network covering 27 agreements. "
            "Small domestic market and total trade dependency are structural constraints."
        ),
    },
}

INDICATOR_DESCRIPTIONS = {
    "continent_standing": "Regional economic and political influence rank",
    "world_standing": "Global diplomatic and economic standing",
    "bargaining_power": "Ability to negotiate favorable trade terms",
    "economic_weight": "GDP size and economic complexity",
    "trade_leverage": "Export dependency and trade relationship depth",
    "strategic_position": "Geopolitical importance to global trade routes",
    "trade_war_pressure": "Exposure to tariff escalation and trade sanctions",
    "security_flashpoints": "Proximity to active or potential conflict zones",
    "domestic_unrest": "Political stability and civil unrest risk",
    "strategic_rivalry": "Level of great-power competition affecting trade",
}

COUNTRIES = list(COUNTRY_PROFILES.keys())

INDUSTRIES = [
    "Electronics & Semiconductors",
    "Apparel & Textiles",
    "Automotive & EV",
    "Pharmaceuticals & Healthcare",
    "Food & Agriculture",
    "Oil, Gas & Energy",
    "Chemicals & Plastics",
    "Machinery & Industrial",
    "Consumer Goods & FMCG",
    "Logistics & Shipping",
]

TIME_HORIZONS = ["30 Days", "90 Days", "6 Months", "12 Months"]

INDUSTRY_RISK_MODIFIERS = {
    "Electronics & Semiconductors": {"tariff_sensitivity": 0.85, "geopolitical_sensitivity": 0.90, "freight_sensitivity": 0.75},
    "Apparel & Textiles": {"tariff_sensitivity": 0.70, "geopolitical_sensitivity": 0.50, "freight_sensitivity": 0.80},
    "Automotive & EV": {"tariff_sensitivity": 0.80, "geopolitical_sensitivity": 0.75, "freight_sensitivity": 0.70},
    "Pharmaceuticals & Healthcare": {"tariff_sensitivity": 0.55, "geopolitical_sensitivity": 0.65, "freight_sensitivity": 0.60},
    "Food & Agriculture": {"tariff_sensitivity": 0.65, "geopolitical_sensitivity": 0.60, "freight_sensitivity": 0.85},
    "Oil, Gas & Energy": {"tariff_sensitivity": 0.50, "geopolitical_sensitivity": 0.95, "freight_sensitivity": 0.60},
    "Chemicals & Plastics": {"tariff_sensitivity": 0.70, "geopolitical_sensitivity": 0.65, "freight_sensitivity": 0.75},
    "Machinery & Industrial": {"tariff_sensitivity": 0.75, "geopolitical_sensitivity": 0.60, "freight_sensitivity": 0.65},
    "Consumer Goods & FMCG": {"tariff_sensitivity": 0.60, "geopolitical_sensitivity": 0.45, "freight_sensitivity": 0.80},
    "Logistics & Shipping": {"tariff_sensitivity": 0.45, "geopolitical_sensitivity": 0.70, "freight_sensitivity": 0.95},
}
