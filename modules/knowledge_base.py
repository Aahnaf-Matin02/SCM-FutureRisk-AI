"""
modules/knowledge_base.py
==========================
Deep supply chain management knowledge base for SCM FutureRisk AI.
This module provides the AI analyst with structured, expert-level knowledge across:
  - SCM theory and frameworks
  - Country-specific trade intelligence
  - Industry supply chain dynamics
  - Risk quantification methodologies
  - Disruption pattern library
  - Regulatory intelligence
  - Strategic decision playbooks
"""

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: SCM THEORETICAL FRAMEWORKS
# ═══════════════════════════════════════════════════════════════════════════════

SCM_FRAMEWORKS = {
    "SCOR_MODEL": {
        "name": "Supply Chain Operations Reference (SCOR) Model",
        "version": "12.0",
        "processes": {
            "Plan": "Demand/supply planning, inventory planning, production scheduling, distribution planning",
            "Source": "Procurement, supplier qualification, purchasing, inbound logistics",
            "Make": "Manufacturing, assembly, testing, packaging, quality control",
            "Deliver": "Order management, warehousing, outbound logistics, transportation",
            "Return": "Reverse logistics, warranty management, excess/obsolete handling",
            "Enable": "Data management, process management, risk management, compliance",
        },
        "performance_metrics": {
            "Reliability": ["Perfect Order Fulfillment", "Order Fill Rate", "Delivery Performance to Commit Date"],
            "Responsiveness": ["Order Fulfillment Cycle Time", "Upside Flexibility", "Downside Adaptability"],
            "Agility": ["Overall Value at Risk", "Total Supply Chain Risk"],
            "Cost": ["COGS", "Supply Chain Management Cost", "Cost to Serve"],
            "Assets": ["Cash-to-Cash Cycle Time", "Return on Supply Chain Fixed Assets", "Inventory Days of Supply"],
        },
        "risk_relevance": "SCOR enables risk mapping across each process. Disruption in Source processes (e.g., supplier failure) cascades to Make (production stoppage) and Deliver (customer service failure) within 2–8 weeks.",
    },

    "VUCA_FRAMEWORK": {
        "name": "VUCA Supply Chain Risk Framework",
        "components": {
            "Volatility": {
                "definition": "Rate and magnitude of change in supply/demand signals",
                "scm_examples": ["Demand spikes >30% in <30 days", "Commodity price swings >20%/quarter", "Currency moves >5% in a week"],
                "mitigation": "Safety stock buffers, flexible contracts, dynamic safety stock formulas (sigma * z * LT^0.5)",
            },
            "Uncertainty": {
                "definition": "Lack of predictability in causal relationships",
                "scm_examples": ["Unknown tariff trajectory", "Unpredictable regulatory changes", "Supplier financial stability unknowns"],
                "mitigation": "Scenario planning, dual sourcing, supply chain mapping (N-tier visibility)",
            },
            "Complexity": {
                "definition": "Number of interacting variables and non-linear relationships",
                "scm_examples": ["Multi-tier supplier networks", "Multi-modal transport", "Multi-currency pricing"],
                "mitigation": "Supply chain digitization, control towers, DDMRP (Demand-Driven MRP)",
            },
            "Ambiguity": {
                "definition": "Unclear meaning of information; multiple valid interpretations",
                "scm_examples": ["Conflicting geopolitical signals", "Mixed PMI data", "Ambiguous trade negotiation outcomes"],
                "mitigation": "Structured scenario playbooks, pre-defined escalation triggers, war-gaming exercises",
            },
        },
    },

    "DDMRP": {
        "name": "Demand-Driven Material Requirements Planning",
        "description": "Modern planning approach replacing traditional MRP push with pull-based buffers",
        "buffer_zones": {
            "Red": "Emergency buffer — replenishment triggers below this level",
            "Yellow": "Working stock — normal consumption zone",
            "Green": "Order generation zone — reorder point range",
        },
        "key_equations": {
            "Buffer_Size": "Average Daily Usage × Decoupled Lead Time × Buffer Factor",
            "Red_Base": "Minimum Order Quantity OR Average Daily Usage × Decoupled Lead Time × Lead Time Factor",
            "Reorder_Point": "Top of Red = Full Red + Yellow",
        },
        "scm_relevance": "DDMRP reduces supply chain nervousness by 40–60% vs traditional MRP. Critical for high-disruption environments.",
    },

    "RESILIENCE_FRAMEWORKS": {
        "4Rs": {
            "Redundancy": "Backup capacity, dual sourcing, safety stock beyond cycle stock",
            "Flexibility": "Multi-sourcing, postponement, flexible capacity contracts",
            "Velocity": "Speed of detection, response, and recovery from disruption",
            "Visibility": "N-tier supply chain mapping, real-time tracking, early warning systems",
        },
        "Recovery_Sequence": [
            "T+0: Disruption detected via early warning system",
            "T+1-3d: Activate emergency response team and assess impact scope",
            "T+4-7d: Deploy emergency inventory allocation and alternative sourcing",
            "T+2-4wk: Qualify and onboard backup suppliers",
            "T+1-3mo: Redesign network to prevent recurrence",
            "T+3-6mo: Embed systemic resilience capabilities",
        ],
    },

    "PORTER_SUPPLY_CHAIN": {
        "name": "Porter's Value Chain for SCM Risk Analysis",
        "primary_activities": {
            "Inbound_Logistics": "Receiving, warehousing, inventory control — disruption source: supplier delays, port congestion",
            "Operations": "Manufacturing, assembly — disruption source: labor unrest, energy shortage, equipment failure",
            "Outbound_Logistics": "Distribution, delivery — disruption source: freight rate spikes, route disruptions",
            "Marketing_Sales": "Order management — disruption source: demand volatility",
            "Service": "After-sales — disruption source: parts availability",
        },
        "support_activities": {
            "Procurement": "Supplier selection and management — risk: single-source dependency",
            "Technology": "Systems and digitization — risk: cyber disruption",
            "HR": "Workforce management — risk: labor market tightness",
            "Infrastructure": "Finance, legal, quality — risk: regulatory non-compliance",
        },
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: COUNTRY DEEP INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════

COUNTRY_DEEP_INTEL = {
    "United States": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 5800,
            "top_exports": ["Refined petroleum", "Crude oil", "Semiconductors", "Civilian aircraft", "Pharmaceuticals"],
            "top_imports": ["Consumer electronics", "Vehicles", "Machinery", "Pharmaceuticals", "Oil"],
            "top_trading_partners": ["Mexico (16%)", "Canada (15%)", "China (12%)", "Germany (5%)", "Japan (5%)"],
            "trade_deficit_2024_USD_bn": -773,
            "key_ftas": ["USMCA", "KORUS", "Japan Trade Agreement", "CAFTA-DR"],
        },
        "supply_chain_strengths": [
            "World's deepest capital markets enabling supplier financing",
            "Unmatched R&D ecosystem driving supply chain innovation",
            "USMCA creates tightly integrated North American production platform",
            "Reserve currency status eliminates FX transaction costs domestically",
            "Advanced logistics infrastructure: 45,000+ miles of interstate highway",
            "Top-ranked airports and 300+ seaports handling 95% of overseas trade",
        ],
        "supply_chain_vulnerabilities": [
            "China dependency for electronics/rare earths despite reshoring push",
            "Aging port infrastructure vs. Asian competitors (LA/LB congestion chronic)",
            "Truck driver shortage: 80,000 driver deficit as of 2024",
            "Section 232 / Section 301 tariffs creating retaliatory uncertainty",
            "Political polarization creating regulatory volatility every 4 years",
            "Concentration risk: 70% of US generic drug APIs sourced from China/India",
        ],
        "regulatory_environment": {
            "tariff_regime": "Section 301 (China tariffs 7.5–100%), Section 232 (steel/aluminum 25%), IEEPA emergency powers",
            "key_regulations": ["UFLPA (Xinjiang forced labor)", "CHIPS Act domestic semiconductor incentives", "IRA EV supply chain rules", "FTC supply chain disclosure requirements"],
            "sanctions": "OFAC sanctions on Russia, Iran, North Korea, Venezuela heavily restrict sourcing",
            "esg_requirements": "SEC climate disclosure rules, forced labor import ban expanding",
        },
        "freight_intelligence": {
            "major_ports": ["LA/Long Beach (40% of US imports)", "NY/NJ", "Savannah", "Houston", "Seattle/Tacoma"],
            "la_lb_baseline_dwell_days": 4.2,
            "us_intermodal_network": "BNSF + UP duopoly covering 90% of western US rail freight",
            "air_freight_hubs": ["Memphis (FedEx)", "Louisville (UPS)", "Anchorage (Asia bridge)", "Cincinnati"],
            "freight_trends_2025": "Nearshoring to Mexico adds +15% cross-border truck volume; port investments in Savannah/Houston shifting east coast share",
        },
        "geopolitical_watchpoints": [
            "US-China tech decoupling accelerating: TSMC, ASML export restrictions",
            "CHIPS Act driving $280B+ semiconductor domestic investment through 2030",
            "IRA forcing EV battery supply chain to North America/FTA partners by 2027",
            "NATO obligations creating supply chain alignment requirements with allies",
            "2024-2026: Tariff policy most unpredictable in 90 years — scenario plan quarterly",
        ],
        "industry_risks": {
            "Electronics": "CRITICAL — 90% of consumer electronics imported; China alternatives nascent",
            "Pharma": "HIGH — API dependency on China/India; FDA approval adds 18-month qualification time",
            "Auto": "HIGH — USMCA rules of origin compliance requiring rapid North American reshoring",
            "FMCG": "MODERATE — Diverse sourcing but freight cost sensitivity high",
            "Energy": "LOW-MODERATE — Net energy exporter reduces import risk",
        },
    },

    "China": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 6300,
            "top_exports": ["Consumer electronics", "Machinery", "Steel", "Textiles", "EVs/batteries"],
            "top_imports": ["Integrated circuits", "Iron ore", "Crude oil", "Soybeans", "LNG"],
            "top_trading_partners": ["ASEAN (15%)", "EU (13%)", "US (12%)", "South Korea (6%)", "Japan (5%)"],
            "trade_surplus_2024_USD_bn": 823,
            "key_ftas": ["RCEP", "ASEAN FTA", "BRI bilateral agreements (140+ countries)"],
        },
        "supply_chain_strengths": [
            "World's largest manufacturing ecosystem with unparalleled supplier density",
            "Complete electronics supply chain vertical integration (rare earths → finished goods)",
            "RCEP gives duty-free access to 30% of global GDP",
            "Belt & Road infrastructure investments create captive supply chain corridors",
            "$500B+ annual infrastructure investment sustaining manufacturing advantage",
            "14 of world's 20 busiest container ports are Chinese",
        ],
        "supply_chain_vulnerabilities": [
            "US/EU tech export controls severing access to advanced semiconductors",
            "Geopolitical risk premium rising: multinationals accelerating China+1 strategies",
            "Demographic decline: working-age population peaked 2011, labor costs tripling since 2010",
            "Property sector crisis affecting supplier liquidity and factory investment",
            "Zero-COVID legacy: supply chain managers now embed political-lockdown risk scenarios",
            "Taiwan Strait scenarios could halt $500B+/yr of global semiconductor supply",
        ],
        "regulatory_environment": {
            "tariff_regime": "RCEP preferential rates; retaliatory tariffs on US/EU goods 6.5–125%",
            "key_regulations": ["Cross-border Data Transfer rules", "Dual Circulation policy (domestic priority)", "Data Security Law restricting data export", "List System controlling rare earth exports"],
            "export_controls": "China controls 90%+ of rare earth processing; uses as strategic leverage",
            "esg_requirements": "Carbon neutrality pledge 2060; Green Finance taxonomy reshaping supply chain",
        },
        "freight_intelligence": {
            "major_ports": ["Shanghai (world #1)", "Ningbo-Zhoushan (#3)", "Shenzhen (#4)", "Guangzhou (#5)", "Qingdao (#6)"],
            "rail": "China-Europe Railway Express (CR Express): 60+ routes, 100,000+ trips annually vs. 45-day sea route",
            "air_freight_hubs": ["Zhengzhou (Foxconn air hub)", "Shanghai Pudong", "Guangzhou Baiyun"],
            "freight_trends_2025": "Vessel blank sailings increasing due to demand uncertainty; Cosco/CSCL state support maintaining capacity during downturns",
        },
        "geopolitical_watchpoints": [
            "Taiwan Strait: PLA military exercises increasing; scenario planning mandatory for electronics SC",
            "South China Sea: Hague ruling ignored; territorial claims affect shipping insurance premiums",
            "CATL/BYD battery dominance: 60% of global EV battery supply; Western alternatives lag by 5+ years",
            "Rare earth processing monopoly: China controls 85% of global REE refining — critical for EV, defense, electronics",
            "Digital yuan/CIPS: Gradual dollar-payment system bypass reduces SWIFT leverage",
        ],
        "industry_risks": {
            "Electronics": "HIGH (geopolitical) / LOW (availability) — unmatched capacity but risk concentration",
            "Pharma": "MODERATE — API dominant exporter; US/EU dual-sourcing mandates emerging",
            "Auto": "MODERATE — BYD/CATL exports rising but tariff barriers limiting",
            "Textiles": "LOW-MODERATE — UFLPA restricting Xinjiang cotton; Vietnam/Bangladesh alternative growth",
            "Energy": "MODERATE — major coal/LNG importer; price spikes affect manufacturing cost base",
        },
    },

    "Bangladesh": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 92,
            "top_exports": ["RMG (85% of exports)", "Knitwear", "Woven garments", "Jute products", "Frozen fish"],
            "top_imports": ["Cotton", "Machinery", "Petroleum", "Iron/steel", "Edible oil"],
            "top_trading_partners": ["EU (55% of exports)", "US (18%)", "UK (8%)", "Germany (specific)"],
            "trade_balance_2024_USD_bn": -18,
            "key_ftas": ["GSP (EU, UK)", "SAFTA", "APTA", "LDC zero-tariff access to 48 developed economies"],
        },
        "supply_chain_strengths": [
            "World's 2nd largest RMG exporter ($46B+ annually) — highly competitive",
            "LDC GSP access gives 0% duty to EU vs. competitors' 12% (ends 2026 with EBA graduation)",
            "Low labor costs: $95/month minimum wage vs. Vietnam $180, China $350+",
            "Established global buyer relationships: H&M, Zara, Gap, Walmart, Primark",
            "Growing compliance infrastructure: 200+ LEED-certified factories (world's most)",
            "Young demographic dividend: 100M working-age population",
        ],
        "supply_chain_vulnerabilities": [
            "CRITICAL: 85% export concentration in RMG — single-sector catastrophic risk",
            "Chittagong Port bottleneck: handles 92% of trade, chronic congestion (7-10 day vessel wait)",
            "Forex reserve crisis: $19B reserves (2024) vs. $46B peak — import coverage <4 months",
            "Political instability: 2024 political transition creating regulatory uncertainty",
            "Climate vulnerability: 70% of country at <1m elevation; cyclone risk to factory districts",
            "LDC graduation 2026: losing EU GSP preference could cost $2B/yr in export revenue",
            "Energy crisis: load-shedding 8-12 hrs/day in 2022-23; ongoing power reliability issues",
            "Banking sector stress: NPL ratio 11%+ affecting supplier payment reliability",
        ],
        "regulatory_environment": {
            "tariff_regime": "Average bound tariff 167%; applied tariff 14%; LDC preferences critical",
            "key_regulations": ["Export Processing Zones (EPZ) rules", "Bangladesh Bank FX controls", "Labor Act compliance for buyer audits"],
            "upcoming_changes": "GSP+ application to EU for post-LDC status; CPTPP consideration",
            "esg_requirements": "EU CSDD directive affecting supply chain due diligence requirements for exporters",
        },
        "freight_intelligence": {
            "major_ports": ["Chittagong (Chattogram) — 92% of trade", "Mongla (secondary, limited capacity)"],
            "chittagong_issues": "Single-entry port; Karnaphuli River siltation limits vessel size to <75,000 DWT; feeder service to Singapore/Colombo adds 7-10 days vs. direct",
            "inland_transport": "Dhaka-Chittagong corridor chronically congested; truck dwell time avg 3-4 days",
            "air_freight": "Hazrat Shahjalal Airport limited air cargo capacity; Sylhet secondary",
            "freight_trends_2025": "Bay of Bengal Industrial Growth Belt initiative; Matarbari deep-sea port development (2026 target)",
        },
        "geopolitical_watchpoints": [
            "India-Bangladesh economic integration deepening via Teesta water treaty and rail corridors",
            "China BRI investments: $38B committed; Padma Bridge, power plants create dependency",
            "Rohingya refugee crisis: 1M+ in Cox's Bazar; regional stability risk",
            "US Indo-Pacific strategy: Bangladesh positioning between India-China rivalry",
            "LDC graduation 2026: most critical trade policy event in Bangladesh's history",
        ],
        "industry_risks": {
            "Apparel": "MODERATE — competitive but GSP sunset, compliance cost inflation, labor unrest",
            "Pharma": "LOW — growing domestic generic pharma; API import dependency",
            "FMCG": "MODERATE — import-dependent; currency risk high",
            "Electronics": "HIGH — minimal domestic capability; pure import dependency",
            "Food": "MODERATE — food security risk; import-dependent for wheat/edible oil",
        },
    },

    "Vietnam": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 790,
            "top_exports": ["Electronics/phones (35%)", "Machinery", "Textiles", "Footwear", "Seafood"],
            "top_imports": ["Electronics components", "Machinery", "Fabrics", "Steel", "Petroleum"],
            "top_trading_partners": ["US (28% of exports)", "China (largest import source)", "EU (12%)", "South Korea (8%)"],
            "trade_surplus_2024_USD_bn": 28,
            "key_ftas": ["CPTPP", "EVFTA", "RCEP", "VKFTA", "UKVFTA"],
        },
        "supply_chain_strengths": [
            "Top China+1 beneficiary: $38B FDI in 2023, Samsung alone exports $65B/yr from Vietnam",
            "CPTPP + EVFTA dual access covers 40% of global GDP with preferential rates",
            "Competitive labor: $190-220/month — above Bangladesh but below China; rapidly growing skills",
            "Strategic location: South China Sea hub connecting NE and SE Asian supply chains",
            "Young workforce: 60% under 35; literacy 95%",
            "Rapidly improving infrastructure: Tan Cang-Cai Mep port expansion, Hanoi-HCMC expressway",
        ],
        "supply_chain_vulnerabilities": [
            "Input dependency: 65% of electronics components imported from China — disruption multiplier",
            "Shallow supplier ecosystem: FDI-led growth without domestic Tier 2/3 supplier development",
            "Infrastructure bottleneck: road/rail capacity lagging FDI inflow pace",
            "Power grid reliability: electricity shortages in 2023 impacted Samsung/LG production",
            "US trade scrutiny: 'transshipment' concerns; currency manipulation watch list",
            "South China Sea tensions: territorial disputes with China create shipping risk premium",
            "Wage inflation: 8-12% annually — competitiveness window narrowing vs. India/Bangladesh",
        ],
        "freight_intelligence": {
            "major_ports": ["Ho Chi Minh City / Cai Mep (world top 25)", "Haiphong (north)", "Da Nang (central)"],
            "cai_mep_advantage": "First deep-water port in SE Asia accepting mega-vessels (>20,000 TEU) directly",
            "connectivity": "Feeder services to Singapore (2 days), direct to US West Coast (16 days), Europe (25 days)",
            "freight_trends_2025": "North-south rail corridor development accelerating; air cargo capacity expanding at Noi Bai (Hanoi) and Long Thanh (new HCMC airport 2026)",
        },
        "geopolitical_watchpoints": [
            "Bamboo diplomacy: Vietnam maintains balanced relations between US and China — strategic advantage",
            "IPEF membership: gaining digital trade and supply chain resilience frameworks",
            "South China Sea: China's maritime claims overlap Vietnam EEZ; periodic standoffs",
            "Samsung 60% of phone exports: extreme concentration risk in single company",
            "US GSP considerations: Vietnam could gain enhanced status as strategic partner",
        ],
    },

    "Germany": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 2850,
            "top_exports": ["Vehicles/parts", "Machinery", "Chemicals", "Pharmaceuticals", "Electronics"],
            "top_imports": ["Energy (gas, oil)", "Electronics", "Vehicles", "Chemicals", "Metals"],
            "top_trading_partners": ["US (10%)", "China (8%)", "Netherlands (7%)", "France (7%)", "UK (5%)"],
            "trade_surplus_2024_USD_bn": 185,
            "key_ftas": ["EU Single Market (27 countries)", "CETA (Canada)", "EU-Japan EPA", "EU-South Korea FTA"],
        },
        "supply_chain_strengths": [
            "EU Single Market: frictionless trade with 26 countries covering 450M consumers",
            "Mittelstand ecosystem: 3.5M SMEs creating deepest industrial supplier base in Europe",
            "Hamburg/Rotterdam gateway: direct access to 800M EU consumers within 24-48hr truck",
            "Deutsche Bahn rail network: 33,000km track connecting to all EU capitals",
            "Engineering excellence: ISO/DIN standards drive global quality benchmarking",
            "Fraunhofer Institutes: 72 applied research centers accelerating Industry 4.0 adoption",
        ],
        "supply_chain_vulnerabilities": [
            "Russia energy dependency legacy: gas-price spike added €200B+ energy costs in 2022-23",
            "Auto sector disruption: combustion engine sunset (EU 2035) threatening 770,000 jobs",
            "China export dependency: German auto/machinery exports 30% to China — retaliatory tariff risk",
            "Labor shortage: 2M unfilled positions in 2024; skilled worker immigration reform lagging",
            "Bureaucratic/permitting delays: average 4+ years for major infrastructure projects",
            "Rhine river drought: 2018 and 2022 disrupted inland waterway transport critical for chemicals",
        ],
        "freight_intelligence": {
            "major_ports": ["Hamburg (#3 Europe)", "Bremen/Bremerhaven", "Rotterdam access (100km west)"],
            "rail": "Hamburg-Duisburg: world's busiest rail freight corridor; connection to China CR Express",
            "road": "Autobahn network; truck toll system (Maut); driver shortage impacting last-mile",
            "freight_trends_2025": "H2 hydrogen corridor development; digitization of customs (ATLAS system); Rhine barge expansion",
        },
        "geopolitical_watchpoints": [
            "Economic security: Germany-China decoupling pressure from EU and US allies",
            "Defense spending: NATO 2% GDP target driving procurement supply chain changes",
            "EU CBAM: Carbon Border Adjustment Mechanism affecting import prices from high-carbon producers",
            "Volkswagen/BASF Chinese JV decisions: bellwether for German corporate China strategy",
        ],
    },

    "Japan": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 1580,
            "top_exports": ["Vehicles", "Semiconductors/components", "Machinery", "Steel", "Chemicals"],
            "top_imports": ["Energy (LNG, oil, coal)", "Electronics", "Food", "Pharmaceuticals"],
            "top_trading_partners": ["China (20%)", "US (15%)", "South Korea (7%)", "Taiwan (7%)", "Australia (6%)"],
            "trade_deficit_2024_USD_bn": -68,
            "key_ftas": ["CPTPP", "EU-Japan EPA", "RCEP", "US-Japan Trade Agreement"],
        },
        "supply_chain_strengths": [
            "Toyota Production System (TPS/JIT) — gold standard for lean manufacturing globally",
            "Keiretsu networks: cross-ownership supply chain loyalty creates extreme stability",
            "Kaizen culture: continuous improvement embedded across entire supply chain",
            "World-class port infrastructure: Yokohama, Kobe, Nagoya among Asia's most efficient",
            "Precision manufacturing: TSMC-level semiconductor equipment (TEL, Shin-Etsu, JSR)",
            "CPTPP leadership: negotiating enhanced market access for Japanese exporters",
        ],
        "supply_chain_vulnerabilities": [
            "2011 legacy: Tohoku earthquake exposed JIT fragility — single-source semiconductor dependencies still persist",
            "Yen depreciation: JPY at 30-year lows raises import costs 20-30%; energy import bill surging",
            "North Korea missile risk: DPRK tests disrupt Japanese airspace; port security costs rising",
            "Demographic crisis: world's most aged workforce; robot adoption offsetting but not matching",
            "China territorial disputes: Senkaku/Diaoyu Islands; export control retaliation risks",
            "100% energy import dependency: LNG from Australia/Qatar; oil from Middle East",
        ],
        "freight_intelligence": {
            "major_ports": ["Nagoya (#1 Japan, auto)", "Yokohama (#2)", "Kobe (#3)", "Osaka", "Tokyo"],
            "logistics_strength": "Japan holds LPI score 3.9/4.0 — among world's top 5 logistics performers",
            "freight_trends_2025": "Osaka-Kansai Expo 2025 infrastructure boost; hydrogen supply chain development",
        },
    },

    "Singapore": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 980,
            "top_exports": ["Refined petroleum", "Electronics", "Chemicals", "Machinery"],
            "top_imports": ["Crude oil", "Electronics", "Machinery", "Chemicals"],
            "top_trading_partners": ["China (14%)", "Malaysia (11%)", "US (8%)", "Indonesia (6%)", "Australia (5%)"],
            "trade_surplus_2024_USD_bn": 58,
            "key_ftas": ["27 FTAs covering 90+ countries", "CPTPP", "ASEAN", "EU-Singapore FTA (EUSFTA)", "US-Singapore FTA"],
        },
        "supply_chain_strengths": [
            "PSA Singapore: world's #2 container port; 37M TEU annual capacity with highest efficiency",
            "Changi Airport: world's best airport 6+ years; 1.8M tonnes air cargo annually",
            "27 FTAs: most comprehensive FTA network in Asia; 0% tariff on 99% of trade",
            "AAA sovereign credit rating: cheapest supply chain financing cost in region",
            "Legal system: English common law, world's #1 ranked for rule of law",
            "Digital trade hub: TradeTrust, Networked Trade Platform eliminating paper documentation",
            "Strategic neutrality: trades freely with US, China, India simultaneously",
        ],
        "supply_chain_vulnerabilities": [
            "Zero domestic production: 100% food and energy import dependent",
            "Water dependency: 40% from Malaysia under treaty expiring 2061",
            "Small land mass: no industrial hinterland; pure services/logistics economy",
            "Salary costs: $4,500-6,000/month for logistics manager vs. regional peers",
            "Real estate: land scarcity means warehouse costs among world's highest",
        ],
        "freight_intelligence": {
            "port_stats": "PSA handles 37M TEU; 600 shipping lines; 200+ countries connected; 5 container terminals",
            "jurongport": "Bulk and liquid cargo; chemicals hub",
            "air_cargo": "Changi Airport Air Cargo: top 5 globally; Singapore Airlines World Cargo",
            "freight_trends_2025": "Tuas megaport development (65M TEU capacity by 2040); hydrogen bunkering pioneer",
        },
        "geopolitical_watchpoints": [
            "US-China rivalry: Singapore's neutrality increasingly tested; 40% exports to each",
            "South China Sea: Singapore depends on safe passage; UNCLOS champion",
            "Malaysia relations: water, airspace, HSR project periodic tensions",
        ],
    },

    "India": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 1300,
            "top_exports": ["Petroleum products", "Pharmaceuticals", "Gems/jewelry", "Machinery", "IT services"],
            "top_imports": ["Crude oil", "Gold", "Electronics", "Coal", "Machinery"],
            "top_trading_partners": ["US (18% of exports)", "UAE (7%)", "Netherlands (5%)", "China (largest import source 15%)"],
            "trade_deficit_2024_USD_bn": -247,
            "key_ftas": ["ASEAN-India FTA", "India-UAE CEPA", "India-Australia ECTA", "SAARC"],
        },
        "supply_chain_strengths": [
            "PLI schemes: $26B production-linked incentives across 14 sectors driving manufacturing",
            "Generic pharma superpower: 20% of global generic export volume; FDA-approved capacity",
            "IT/ITES: 50%+ of global IT outsourcing; digital supply chain capability",
            "Demographic dividend: 900M working-age population by 2030; English-speaking workforce",
            "China+1 prime beneficiary: Apple, Samsung, Tesla shifting manufacturing",
            "Natural resources: 4th largest coal, significant iron ore; reducing import dependency",
        ],
        "supply_chain_vulnerabilities": [
            "Infrastructure gap: logistics cost = 14% of GDP vs. 8% in China; poor last-mile connectivity",
            "Regulatory complexity: GST implementation improving but state-level variations persist",
            "Power reliability: 8-10% average transmission loss; rural grid gaps affecting factories",
            "Port congestion: JNPT handling 60% of containerized trade — chronic overcapacity issues",
            "China input dependency: electronics components, chemicals, APIs — $100B+ annual imports",
            "Land acquisition: 5-7 year process for greenfield industrial projects",
            "Labor law complexity: 29 central labor laws being consolidated into 4 codes (slow implementation)",
        ],
        "freight_intelligence": {
            "major_ports": ["JNPT/Nhava Sheva (60% of containers)", "Mundra (ADANI, largest private)", "Chennai", "Vizag", "Kochi"],
            "rail": "Indian Railways: 68,000km network; Dedicated Freight Corridors (Eastern+Western) operational",
            "road": "NH network expanding to 200,000km; last-mile connectivity challenge in rural areas",
            "freight_trends_2025": "PM GatiShakti infrastructure push; multimodal logistics parks development; DPIIT supply chain reforms",
        },
    },

    "Malaysia": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 590,
            "top_exports": ["Electronics/semiconductors (40%)", "Palm oil", "LNG", "Petroleum products", "Rubber gloves"],
            "top_imports": ["Electronics components", "Machinery", "Petroleum", "Chemicals", "Vehicles"],
            "top_trading_partners": ["Singapore (14%)", "China (13%)", "US (11%)", "Japan (7%)", "EU (9%)"],
            "trade_surplus_2024_USD_bn": 36,
            "key_ftas": ["ASEAN FTA", "CPTPP", "RCEP", "Malaysia-Australia FTA"],
        },
        "supply_chain_strengths": [
            "Semiconductor packaging hub: Intel, Texas Instruments, Infineon, NXP — 13% of global IC packaging",
            "Port Klang + Tanjung Pelepas: top 15 global container ports; ASEAN strategic gateway",
            "Petronas oil/gas: LNG exporter supporting energy supply chain",
            "Halal hub: world's top halal food/pharma certification — $2.3T global halal market access",
            "English-speaking, multicultural workforce",
            "Data center boom: Microsoft, Google, AWS investing $10B+ in Malaysian capacity",
        ],
        "supply_chain_vulnerabilities": [
            "US semiconductor scrutiny: Malaysia investigated for China chip transshipment (2023-24)",
            "Single-commodity concentration: 40% exports in electronics creates cyclical risk",
            "Political instability: 5 governments in 5 years (2018-2023); policy continuity risk",
            "Skilled worker shortage: brain drain to Singapore reducing engineering pool",
            "Palm oil ESG pressure: EU deforestation regulation restricting palm oil imports",
        ],
    },

    "Indonesia": {
        "trade_profile": {
            "total_trade_2024_USD_bn": 540,
            "top_exports": ["Coal", "Palm oil", "Nickel/ore", "Petroleum", "Rubber"],
            "top_imports": ["Machinery", "Electronics", "Steel", "Chemicals", "Petroleum"],
            "top_trading_partners": ["China (22%)", "US (9%)", "Japan (8%)", "India (7%)", "Malaysia (5%)"],
            "trade_surplus_2024_USD_bn": 31,
            "key_ftas": ["ASEAN FTA", "RCEP", "Indonesia-Australia CEPA (IA-CEPA)"],
        },
        "supply_chain_strengths": [
            "World #1 nickel producer (50% of global supply) — critical for EV batteries",
            "World's #2 coal exporter — critical for Asian power generation supply chains",
            "Palm oil: 55% of global supply — food, oleochemicals, biodiesel",
            "ASEAN's largest economy: 278M population domestic market",
            "Young median age 30: growing middle class driving domestic consumption",
            "Batam/Bintan FTZ: special economic zones adjacent to Singapore",
        ],
        "supply_chain_vulnerabilities": [
            "Resource nationalism: nickel ore export ban (2020) forcing downstream processing — affects EV SC",
            "Archipelago logistics: 17,000+ islands creating extreme domestic distribution complexity",
            "Infrastructure deficit: logistics costs 24% of GDP — highest in region",
            "Corruption index: Transparency International #110 — supply chain compliance risk",
            "Java concentration: 60% of GDP, 55% of population on single island — disaster risk",
            "Port inefficiency: Tanjung Priok (Jakarta) handling 60% of trade with chronic congestion",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: INDUSTRY DEEP INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════

INDUSTRY_DEEP_INTEL = {
    "Electronics & Semiconductors": {
        "global_market_size_2024_USD_bn": 595,
        "supply_chain_structure": {
            "tier_1": "OEMs (Apple, Samsung, TSMC, Intel) — design and final assembly",
            "tier_2": "Contract manufacturers (Foxconn, Pegatron, Flex) — component assembly",
            "tier_3": "Component makers (NAND, DRAM, analog ICs) — specialized components",
            "tier_4": "Materials/chemicals (ASML lithography, silicon wafers, photoresist)",
        },
        "concentration_risks": {
            "TSMC": "92% of world's most advanced chips (≤5nm) — single-point-of-failure for tech sector",
            "ASML": "100% monopoly on EUV lithography — no second source exists; Dutch export controls key",
            "Samsung": "30% of NAND flash, 40% of DRAM — Korean geopolitical risk multiplier",
            "China_rare_earths": "85-90% of rare earth processing including neodymium (motors), dysprosium (magnets)",
        },
        "disruption_scenarios": {
            "Taiwan_Strait": {
                "probability_5yr": "15-25%",
                "impact": "CATASTROPHIC — $1.6T annual revenue disruption; 3-5 year recovery",
                "contingency": "CHIPS Act subsidies; TSMC Arizona fab (2nm by 2028); Intel recovery play",
            },
            "Chip_Export_Controls": {
                "probability_12mo": "HIGH — ongoing escalation",
                "impact": "HIGH — Chinese IDMs capacity gap 3-4 node generations behind TSMC",
                "contingency": "Chinese domestic substitution accelerating (SMIC, Hua Hong) but 3-5yr gap",
            },
        },
        "lead_times": {
            "advanced_semiconductors": "52-104 weeks (TSMC advanced node)",
            "memory_chips": "16-26 weeks",
            "passive_components": "8-16 weeks",
            "PCB_assemblies": "4-12 weeks",
        },
        "risk_mitigation_best_practices": [
            "Maintain 90-day safety stock for allocation-risk components (semiconductors)",
            "Dual-qualify all single-source ICs with >$500K annual spend",
            "Join industry semiconductor allocation consortia",
            "Embed supply chain risk scoring in supplier KPI dashboards",
            "Negotiate Last-Time-Buy clauses for EOL components",
        ],
    },

    "Apparel & Textiles": {
        "global_market_size_2024_USD_bn": 1800,
        "supply_chain_structure": {
            "tier_1": "Retailers/brands (H&M, Zara, Gap, Nike) — design and retail",
            "tier_2": "CMT/FOB garment manufacturers (Bangladesh, Vietnam, India, Turkey)",
            "tier_3": "Fabric mills and dye houses (China, India, Vietnam, Korea)",
            "tier_4": "Fiber producers (cotton: US/India/China; synthetics: chemical companies)",
        },
        "sourcing_concentration": {
            "China": "35% of global apparel exports (declining from 50% in 2010)",
            "Bangladesh": "7% global, #2 — RMG focused",
            "Vietnam": "6.5% global, #3 — fast growing",
            "India": "5% global, #4",
            "Turkey": "4% global — nearshore for EU brands",
        },
        "season_lead_times": {
            "traditional": "6-9 months (Bangladesh, South Asia)",
            "fast_fashion_south_asia": "4-6 months",
            "nearshore_Turkey_Morocco": "4-6 weeks (for EU buyers)",
            "onshore_trend": "2-4 weeks (emerging; 3D knitting, automated cut/sew)",
        },
        "key_risks_2025": {
            "GSP_Bangladesh": "Bangladesh LDC graduation 2026 removes 12% EU duty advantage — cost competitive alert",
            "UFLPA_Xinjiang": "US cotton import ban from Xinjiang; burden of proof on importer",
            "EU_CSDD": "Mandatory supply chain due diligence; factory audit requirements expanding to Tier 3",
            "Labor_wages": "Bangladesh, Vietnam minimum wages up 30-50% since 2020; margin compression",
            "Freight_normalization": "Container rates normalized post-COVID but Red Sea diversion adding 8-12 days Europe routes",
        },
    },

    "Automotive & EV": {
        "global_market_size_2024_USD_bn": 2900,
        "supply_chain_structure": {
            "tier_1": "OEMs (Toyota, VW, GM, Tesla, BYD) + Tier 1 systems (Bosch, Denso, Magna)",
            "tier_2": "Component makers (brakes, seats, HVAC, electronics)",
            "tier_3": "Sub-components (metal stampings, plastics, bearings, fasteners)",
            "tier_4": "Raw materials (steel, aluminum, copper, lithium, cobalt, nickel)",
        },
        "ev_battery_supply_chain": {
            "cathode_materials": "Lithium (Chile 50%, Australia 35%), Cobalt (DRC 75%), Nickel (Indonesia 50%)",
            "cell_manufacturers": "CATL (37% global), LG Energy (14%), Panasonic (11%), Samsung SDI (7%)",
            "pack_assembly": "Increasingly in-house by OEMs",
            "recycling_loop": "Li-cycle, Redwood Materials — closed-loop critical minerals emerging",
        },
        "ira_impact": {
            "battery_content": "50% of battery components must be from North America or FTA partners by 2024",
            "critical_minerals": "40% of critical minerals from North America or FTA partners (escalating to 80% by 2027)",
            "implication": "Forces OEMs to build North American battery gigafactories; reshapes Asian battery SC",
        },
        "disruption_history": {
            "2011_Japan": "Toyota 60-day production halt from Tohoku earthquake; exposed JIT vulnerability",
            "2021_chip": "$200B industry revenue loss from semiconductor shortage; 12M vehicles unproduced",
            "2022_Russia": "Palladium (40% from Russia) supply disruption affecting catalytic converters",
        },
    },

    "Pharmaceuticals & Healthcare": {
        "global_market_size_2024_USD_bn": 1620,
        "api_concentration": {
            "China": "40% of global API production by volume; 80% of US penicillin supply",
            "India": "20% of global generics export value; 200+ FDA-approved facilities",
            "EU": "30% of innovative drug production",
        },
        "lead_times": {
            "API_procurement": "3-6 months typical; 6-18 months for controlled substances",
            "drug_qualification": "18-24 months for FDA site change approval",
            "cold_chain": "2-8°C: complex logistics; -60 to -80°C (mRNA): ultra-cold chain",
        },
        "regulatory_risk": {
            "FDA_Warning_Letters": "~200 per year to API/finished dose facilities; import alerts can halt supply",
            "data_integrity": "#1 FDA 483 observation — affects 30-40% of inspections in India/China",
            "EMA_GMP": "European compliance increasing divergence from FDA — dual compliance cost",
        },
        "pandemic_lessons": {
            "PPE": "95% US import dependency from China revealed; Strategic National Stockpile gaps",
            "vaccines": "IP waiver debate vs. tech transfer; COVAX supply chain failures",
            "reshoring": "BARDA BioPreparedness now requiring US manufacturing capability for critical drugs",
        },
    },

    "Food & Agriculture": {
        "global_market_size_2024_USD_bn": 9500,
        "choke_points": {
            "Grain": "Ukraine/Russia: 30% of global wheat/corn exports pre-2022; Black Sea Initiative collapse",
            "Soybeans": "US + Brazil + Argentina = 85% of global soybean trade",
            "Palm_oil": "Indonesia + Malaysia = 85% of global palm oil",
            "Shipping_routes": "Bab el-Mandeb, Strait of Hormuz, Malacca Strait — food shipment vulnerabilities",
        },
        "climate_risk": {
            "El_Nino_2023": "Reduced cocoa, coffee, palm oil, rice yields 10-25%; price spikes immediate",
            "water_scarcity": "Murray-Darling (Australia), Colorado River (US), North China Plain — production at risk",
            "carbon_regulation": "EU Deforestation Regulation: coffee, cocoa, soy, palm oil compliance mandatory 2025",
        },
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: GLOBAL DISRUPTION PATTERN LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

DISRUPTION_PATTERNS = {
    "Port_Congestion": {
        "triggers": ["Vessel bunching from weather delays", "Labor strikes (ILWU, longshoremen)", "Equipment failures", "Pandemic protocols"],
        "typical_duration": "2-8 weeks",
        "industries_most_affected": ["Electronics", "FMCG", "Apparel"],
        "leading_indicators": ["Vessel waiting times > 3 days", "Blank sailings >15%", "Port congestion index > 7/10"],
        "mitigation": ["Air freight surge capacity", "Inland depot diversification", "Pre-positioning safety stock"],
    },
    "Supplier_Financial_Distress": {
        "triggers": ["Interest rate spikes", "Revenue decline >20% YoY", "Currency depreciation", "Commodity price spike"],
        "early_warning_signals": ["Payment term extension requests", "Reduction in capex", "Key personnel departures", "Auditor qualifications"],
        "typical_impact": "4-16 weeks supply disruption post-failure",
        "mitigation": ["Financial health monitoring (Dun & Bradstreet, CreditSafe)", "Dual sourcing", "Advance inventory builds"],
    },
    "Geopolitical_Trade_Restriction": {
        "triggers": ["Tariff escalation", "Export controls", "Sanctions", "Investment screening"],
        "warning_period": "1-6 months (legislation visible before implementation)",
        "mitigation": ["Tariff engineering (rules of origin optimization)", "FTZ/bonded warehouse strategies", "Country of origin diversification"],
        "case_studies": ["US Section 301 China tariffs 2018", "UFLPA 2022", "CHIPS Act export controls 2022-23"],
    },
    "Natural_Disaster": {
        "types": ["Earthquake (Japan, Turkey)", "Hurricane (US Gulf, Caribbean)", "Flood (Thailand 2011, Pakistan 2022)", "Drought (Rhine, Yangtze, Panama Canal)"],
        "recovery_timeline": {
            "minor": "1-4 weeks",
            "moderate": "1-3 months",
            "major": "3-12 months",
            "catastrophic": "1-5 years",
        },
        "mitigation": ["Geographic supplier diversification", "Business continuity planning", "Catastrophic loss insurance", "Inventory pre-positioning"],
    },
    "Labor_Disruption": {
        "types": ["Strike", "Shortage", "Safety incident closure", "Wage dispute"],
        "high_risk_sectors": ["Ports (ILWU, longshoremen unions)", "Automotive (UAW)", "Airlines", "Logistics"],
        "indicators": ["Contract expiry + 6 months", "Union filing notices", "Wage inflation gap >5%"],
        "mitigation": ["Multi-port routing agreements", "Labor dispute early warning tracking", "Automation investment"],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: STRATEGIC DECISION PLAYBOOKS
# ═══════════════════════════════════════════════════════════════════════════════

DECISION_PLAYBOOKS = {
    "Diversify suppliers": {
        "when_to_use": "Risk score >55 OR single-source dependency with tariff/geopolitical exposure",
        "timeline": "3-18 months depending on qualification requirements",
        "steps": [
            "Map current supplier concentration by country, region, and tier",
            "Define target state: no single country >40%, no single supplier >25% for critical inputs",
            "Issue RFQ to 3-5 alternative suppliers per critical category",
            "Run parallel production trials for 90 days with backup supplier",
            "Negotiate dual-award contracts splitting volume 70/30 (primary/backup)",
            "Build supplier scorecard tracking quality, delivery, financial health quarterly",
        ],
        "cost_impact": "2-8% cost increase typical; offset by reduced disruption cost over 3-5yr horizon",
        "kpis": ["Supplier concentration index (HHI)", "Countries per critical category", "Dual-qualified SKU %"],
        "pitfalls": ["Splitting volume too small for backup supplier to maintain interest", "Qualification timeline underestimated", "Hidden costs of parallel validation"],
    },
    "Increase safety stock": {
        "when_to_use": "Lead time extension >2 weeks OR demand volatility >15% OR freight unreliability",
        "formula": "Safety Stock = Z × σ_demand × √(Lead_Time) where Z=1.65 (95% service level)",
        "target_calculation": {
            "current_lead_time": "X days",
            "safety_stock_formula": "For 95% service: Z=1.65; For 99%: Z=2.33",
            "cost_of_inventory": "Typical 15-25% of inventory value per year (holding cost)",
        },
        "steps": [
            "Calculate current safety stock vs. statistically optimal levels by SKU",
            "Prioritize ABC analysis: A items = high safety stock, C items = lean",
            "Negotiate vendor-managed inventory (VMI) or consignment for high-risk inputs",
            "Review warehouse capacity and financing availability",
            "Set reorder point triggers and escalation protocols",
        ],
        "cost_impact": "Each week of additional safety stock = 0.3-0.5% of annual COGS in carrying cost",
        "pitfalls": ["Overstocking creates cash flow drain", "Obsolescence risk for fast-moving tech categories"],
    },
    "Hedge freight/currency exposure": {
        "when_to_use": "Freight cost >8% of COGS OR currency exposure >30% of cost base",
        "instruments": {
            "freight_hedging": "Forward Freight Agreements (FFAs), container rate derivatives (Freightos FBX futures)",
            "currency_hedging": "Forward contracts (3-12 months), options (flexibility with premium cost), natural hedging (USD billing)",
        },
        "steps": [
            "Quantify total freight and FX exposure in annual COGS",
            "Determine hedge ratio: typically 50-80% of forecasted volume",
            "Select instruments based on cost, liquidity, and basis risk",
            "Establish hedge policy with CFO approval and board oversight",
            "Monitor mark-to-market and rebalance quarterly",
        ],
        "cost_impact": "Hedging cost = 0.5-2% of notional; provides certainty vs. spot market volatility",
        "pitfalls": ["Over-hedging when volumes fall creates mark-to-market losses", "Basis risk if actual routes differ from hedged routes"],
    },
    "Nearshore production": {
        "when_to_use": "Geopolitical risk score >70 OR lead time >60 days with demand volatility >20%",
        "analysis_framework": {
            "TCO": "Total Cost of Ownership = Unit cost + Freight + Duty + Inventory carrying + Disruption risk premium",
            "breakeven": "Nearshoring justified when TCO saving > factory setup amortization over 5 years",
            "decision_matrix": ["Labor cost delta", "Lead time improvement", "Tariff savings", "Logistics cost", "Geopolitical risk reduction"],
        },
        "steps": [
            "Calculate full TCO for current offshore vs. nearshore location",
            "Identify top 3 nearshore candidate locations with supplier ecosystem assessment",
            "Evaluate labor availability, infrastructure, FTA access, special economic zones",
            "Develop phased migration plan: pilot line → partial transfer → full transfer",
            "Parallel run offshore and nearshore for 6 months before full cutover",
        ],
        "timeline": "18-36 months for full implementation",
        "pitfalls": ["Underestimating technology transfer time", "Supplier ecosystem immaturity in target location", "Hidden costs of parallel operations"],
    },
    "Avoid new sourcing contracts": {
        "when_to_use": "Risk score >70 AND deteriorating direction AND no near-term catalyst for improvement",
        "actions": [
            "Place sourcing moratorium on new long-term contracts (>6 months) from affected country",
            "Activate force majeure review in existing contracts",
            "Pre-qualify alternative sources before existing contracts expire",
            "Communicate risk rationale to senior procurement leadership",
            "Set monthly risk threshold review with clear reinstatement criteria",
        ],
        "communication": "Frame as risk management pause, not permanent exit — preserves supplier relationships",
        "pitfalls": ["Market share loss if competitors continue sourcing at lower cost during pause", "Supplier relationships deteriorate without communication"],
    },
    "Monitor only": {
        "when_to_use": "Risk score <35 AND stable/improving direction AND no acute signal threats",
        "monitoring_cadence": {
            "daily": "Freight rate index, major port disruption alerts, geopolitical news",
            "weekly": "Supplier communication health check, inventory vs. safety stock levels",
            "monthly": "Country risk score re-assessment, supplier financial health review",
            "quarterly": "Full supply chain risk audit, scenario plan refresh",
        },
        "escalation_triggers": [
            "Risk score increases >10 pts in 30 days",
            "Single supplier represents >40% of category volume",
            "Freight rates spike >30% in 2 weeks",
            "Country political event (election, coup, major policy change)",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 6: GLOBAL MACRO CONTEXT (2025)
# ═══════════════════════════════════════════════════════════════════════════════

GLOBAL_MACRO_2025 = {
    "freight_markets": {
        "container_rates": "Shanghai Containerized Freight Index (SCFI) at $2,200-2,800/FEU Asia-Europe (up 60% from 2024 trough due to Red Sea diversion)",
        "red_sea_impact": "Houthi attacks forcing 90% of Asia-Europe traffic around Cape of Good Hope, adding 10-14 days and $500-800/FEU",
        "airfreight": "Air cargo rates at $3.50-4.50/kg Asia-Europe; belly capacity constraints from passenger fleet management",
        "outlook": "Container rates expected to normalize H2 2025 if Red Sea resolves; 2026 overcapacity risk as newbuild orders deliver",
    },
    "oil_energy": {
        "brent_range_2025": "$75-95/barrel — OPEC+ production cuts offsetting demand slowdown",
        "lng_market": "European LNG spot prices €35-45/MWh; Japan/Korea term contracts at discount",
        "impact_on_scm": "Every $10/barrel oil increase adds 0.3-0.5% to freight cost as bunker fuel surcharge",
    },
    "trade_policy_2025": {
        "us_tariffs": "Trump administration 2025 tariffs: 10-20% universal baseline, 60%+ on China electronics, 25% on Canada/Mexico non-USMCA goods",
        "eu_cbam": "Carbon Border Adjustment Mechanism (CBAM) fully operative; steel, aluminum, cement, fertilizers affected",
        "wto_disputes": "WTO appellate body still non-functional; bilateral dispute resolution dominant",
        "critical_minerals": "US, EU, Japan competing to secure Li, Co, Ni, REE supply chains from Africa/South America",
    },
    "geopolitical_flashpoints": {
        "ukraine": "Conflict ongoing; Black Sea grain corridor impacted; Russian sanctions maintained",
        "taiwan": "PLA military exercises increasing frequency; insurance premiums for Taiwan Strait up 40%",
        "red_sea": "Houthi attacks ongoing; US/UK naval escort operations; insurance war-risk premiums +300%",
        "south_china_sea": "Philippines-China maritime standoffs at Scarborough Shoal and Second Thomas Shoal",
        "iran": "IRGC drone program threatening Middle East shipping; Hormuz Strait risk elevated",
    },
    "technology_disruptions": {
        "ai_supply_chain": "Generative AI adoption for demand forecasting improving accuracy by 15-30%",
        "ev_transition": "ICE-to-EV transition displacing $200B of auto parts suppliers globally",
        "reshoring_tech": "Advanced robotics enabling viable nearshoring for labor-intensive categories",
        "blockchain_traceability": "EU Digital Product Passport regulation driving supply chain traceability mandates",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PART 7: RISK QUANTIFICATION FORMULAS
# ═══════════════════════════════════════════════════════════════════════════════

RISK_FORMULAS = {
    "Value_at_Risk": {
        "formula": "VaR = Annual_Revenue × Disruption_Probability × Average_Revenue_Loss_%",
        "example": "$500M revenue × 15% probability × 20% revenue impact = $15M VaR",
    },
    "Safety_Stock": {
        "formula": "SS = Z_score × σ_demand × √(Lead_Time_days / 365)",
        "z_scores": {"90%": 1.28, "95%": 1.65, "98%": 2.05, "99%": 2.33, "99.9%": 3.09},
        "example": "95% service level: 1.65 × 500_units_std × √(30/365) = 243 units",
    },
    "Dual_Sourcing_Breakeven": {
        "formula": "Breakeven = (Primary_Cost - Backup_Cost) / (Disruption_Probability × Disruption_Duration_days × Daily_Revenue)",
        "insight": "If breakeven < 2 years, dual sourcing is almost always economically justified",
    },
    "Total_Cost_Ownership": {
        "components": [
            "Unit cost (COGS)",
            "Freight cost (typically 2-15% of product value)",
            "Import duty (0-100%+ depending on country/product)",
            "Inventory carrying cost (15-25% of inventory value/year)",
            "Quality cost (rework, returns, recalls)",
            "Supply chain risk premium (VaR amortized over planning horizon)",
            "Carbon/compliance cost (emerging 2-5% for EU-destined goods)",
        ],
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# PART 8: KNOWLEDGE RETRIEVAL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_country_deep_intel(country: str) -> dict:
    """Return deep intelligence for a given country."""
    return COUNTRY_DEEP_INTEL.get(country, {})


def get_industry_deep_intel(industry: str) -> dict:
    """Return deep intelligence for a given industry."""
    # Normalize industry name to key
    for key in INDUSTRY_DEEP_INTEL:
        if industry.lower().startswith(key.split()[0].lower()):
            return INDUSTRY_DEEP_INTEL[key]
    return {}


def get_decision_playbook(decision: str) -> dict:
    """Return the playbook for a given decision."""
    return DECISION_PLAYBOOKS.get(decision, {})


def get_framework_context(framework_name: str) -> dict:
    """Return a specific SCM framework."""
    return SCM_FRAMEWORKS.get(framework_name, {})


def build_analyst_context(country: str, industry: str) -> str:
    """
    Build a comprehensive context string for the AI analyst,
    combining country intel, industry intel, frameworks, and macro context.
    Returns a structured text block for inclusion in Claude prompts.
    """
    country_intel = COUNTRY_DEEP_INTEL.get(country, {})
    industry_intel = get_industry_deep_intel(industry)

    sections = []

    # Country section
    if country_intel:
        tp = country_intel.get("trade_profile", {})
        strengths = "\n".join(f"  + {s}" for s in country_intel.get("supply_chain_strengths", [])[:5])
        vulns = "\n".join(f"  - {v}" for v in country_intel.get("supply_chain_vulnerabilities", [])[:5])
        geo = "\n".join(f"  • {g}" for g in country_intel.get("geopolitical_watchpoints", [])[:4])
        reg = country_intel.get("regulatory_environment", {})

        sections.append(f"""
=== COUNTRY INTELLIGENCE: {country} ===
Trade Volume: ${tp.get('total_trade_2024_USD_bn', 'N/A')}B (2024)
Top Exports: {', '.join(tp.get('top_exports', [])[:4])}
Top Partners: {', '.join(tp.get('top_trading_partners', [])[:4])}
Key FTAs: {', '.join(tp.get('key_ftas', [])[:4])}

SUPPLY CHAIN STRENGTHS:
{strengths}

SUPPLY CHAIN VULNERABILITIES:
{vulns}

REGULATORY ENVIRONMENT:
  Tariff Regime: {reg.get('tariff_regime', 'N/A')}
  Key Regulations: {', '.join(reg.get('key_regulations', [])[:3])}

GEOPOLITICAL WATCHPOINTS:
{geo}
""")

    # Industry section
    if industry_intel:
        sc = industry_intel.get("supply_chain_structure", {})
        risks = industry_intel.get("key_risks_2025", {})
        lead_times = industry_intel.get("lead_times", {})

        risk_text = "\n".join(f"  ! {k}: {v}" for k, v in list(risks.items())[:4])
        lt_text = "\n".join(f"  • {k}: {v}" for k, v in list(lead_times.items())[:4])

        sections.append(f"""
=== INDUSTRY INTELLIGENCE: {industry} ===
Global Market Size: ${industry_intel.get('global_market_size_2024_USD_bn', 'N/A')}B
Tier 1: {sc.get('tier_1', 'N/A')}
Tier 2: {sc.get('tier_2', 'N/A')}
Tier 3: {sc.get('tier_3', 'N/A')}

KEY RISKS 2025:
{risk_text}

LEAD TIMES:
{lt_text}
""")

    # Global macro
    macro = GLOBAL_MACRO_2025
    sections.append(f"""
=== GLOBAL MACRO CONTEXT 2025 ===
Container Freight: {macro['freight_markets']['container_rates']}
Red Sea Impact: {macro['freight_markets']['red_sea_impact']}
Oil Market: {macro['oil_energy']['brent_range_2025']}
US Trade Policy: {macro['trade_policy_2025']['us_tariffs']}
Active Flashpoints: {', '.join(macro['geopolitical_flashpoints'].keys())}
""")

    # SCOR framework reference
    sections.append("""
=== SCM FRAMEWORK REFERENCE ===
SCOR Model: Plan → Source → Make → Deliver → Return → Enable
4R Resilience: Redundancy + Flexibility + Velocity + Visibility
VUCA Risk: Volatility (buffers) → Uncertainty (dual source) → Complexity (digitize) → Ambiguity (scenarios)
""")

    return "\n".join(sections)
