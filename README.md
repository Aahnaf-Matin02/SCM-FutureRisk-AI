# 🌐 SCM FutureRisk AI

> **AI-Powered Supply Chain Risk Intelligence Platform**
> Combining Machine Learning forecasting, real-time news signals, and Claude AI strategic recommendations.

---

## 🚀 Live Demo

> **Demo works fully without API keys.** All pages use curated demo data when APIs are not connected.

---

## 📋 Features

| Feature | Description |
|---------|-------------|
| 🌍 **Country Intelligence** | Structured risk profiles for 10 countries with 10+ indicators |
| 📡 **Global Risk Monitor** | Real-time news signals via Google Search API (or demo data) |
| 🤖 **ML Forecast Engine** | Gradient Boosting model with 17 features + 180-day forecast |
| 🧠 **Claude Decision Room** | Claude AI strategic recommendations with 5-step action plans |
| ✅ **Evidence Verification** | Cross-check AI claims against news evidence with support scores |
| 🎛️ **Scenario Simulator** | 9-lever interactive simulation with tornado sensitivity chart |
| 📊 **Premium Dashboard** | Plotly gauges, radars, heatmaps, and line charts |

---

## 🏗️ Project Structure

```
scm-futurerisk-ai/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # API key template
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
└── modules/
    ├── __init__.py
    ├── country_data.py             # Country intelligence profiles (10 countries)
    ├── ml_engine.py                # Gradient Boosting ML model + forecasting
    ├── search_intelligence.py      # Google Search API + demo fallback
    ├── decision_ai.py              # Claude API + rule-based fallback
    ├── scenario_simulator.py       # 9-lever scenario simulation engine
    └── visualizations.py           # Plotly chart factories
```

---

## ⚡ Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/scm-futurerisk-ai.git
cd scm-futurerisk-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API keys (optional)
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 5. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🔑 API Keys

The app works in **Demo Mode** without any keys. Connect APIs for live intelligence:

| Key | Where to Get | Used For |
|-----|-------------|----------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | Claude AI strategic recommendations |
| `SEARCH_API_KEY` | [Google Custom Search](https://developers.google.com/custom-search/v1/introduction) | Real-time news signals |
| `SEARCH_ENGINE_ID` | [Programmable Search Engine](https://programmablesearchengine.google.com) | Search engine configuration |

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set **Main file path**: `app.py`
5. Add secrets in **Settings → Secrets**:
   ```toml
   ANTHROPIC_API_KEY = "your_key_here"
   SEARCH_API_KEY = "your_key_here"
   SEARCH_ENGINE_ID = "your_engine_id"
   ```
6. Deploy!

---

## 🚂 Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add environment variables in Railway dashboard under **Variables**.

---

## 🐳 Deploy with Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t scm-futurerisk-ai .
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  -e SEARCH_API_KEY=your_key \
  -e SEARCH_ENGINE_ID=your_id \
  scm-futurerisk-ai
```

---

## 🌍 Supported Countries

| Country | Region | Baseline Risk |
|---------|--------|--------------|
| 🇺🇸 United States | North America | 38/100 |
| 🇨🇳 China | East Asia | 52/100 |
| 🇮🇳 India | South Asia | 45/100 |
| 🇧🇩 Bangladesh | South Asia | 58/100 |
| 🇻🇳 Vietnam | Southeast Asia | 40/100 |
| 🇩🇪 Germany | Western Europe | 28/100 |
| 🇯🇵 Japan | East Asia | 32/100 |
| 🇲🇾 Malaysia | Southeast Asia | 38/100 |
| 🇮🇩 Indonesia | Southeast Asia | 45/100 |
| 🇸🇬 Singapore | Southeast Asia | 18/100 |

---

## 🏭 Supported Industries

- Electronics & Semiconductors
- Apparel & Textiles
- Automotive & EV
- Pharmaceuticals & Healthcare
- Food & Agriculture
- Oil, Gas & Energy
- Chemicals & Plastics
- Machinery & Industrial
- Consumer Goods & FMCG
- Logistics & Shipping

---

## 🤖 Sample Output

```
Country: United States
Industry: Electronics & Semiconductors
Time Horizon: 90 Days

Predicted Supply Chain Risk: 67/100
Risk Direction: Deteriorating ↑
Confidence: Medium-High (72%)

Main Risks:
  🔺 Tariff escalation risk (68% intensity) on Electronics & Semiconductors inputs
  🔺 Geopolitical conflict disrupting trade routes (45%)
  🔺 Freight cost surge (55%) extending lead times
  🔺 Risk trajectory is deteriorating — proactive action window is narrowing

Recommended Decision: Diversify suppliers

Action Plan:
  1. Audit current US-based supplier contracts for risk concentration
  2. Map Electronics sub-tier supplier exposure
  3. Set up real-time monitoring dashboard
  4. Identify and pre-qualify backup supplier candidates
  5. Review safety stock levels for critical components

Evidence Quality: Medium-High
Final Confidence: 72%
```

---

## 🔧 ML Model Details

| Component | Specification |
|-----------|--------------|
| Algorithm | GradientBoostingRegressor |
| Training Samples | 800 synthetic country-risk samples |
| Features | 17 (country + global signals) |
| Scaler | StandardScaler |
| Forecasting | Quadratic Bezier interpolation |
| Feature Importance | Permutation-based (+15% perturbation) |

---

## 📊 Pages Reference

| Page | Description |
|------|-------------|
| 🏠 Executive Summary | KPI cards, gauge, forecast chart, signal cards, key drivers |
| 🌍 Country Intelligence | Indicator bars, radar chart, country comparison |
| 📡 Global Risk Monitor | Heatmap, signal cards, news articles |
| 🤖 ML Forecast | Feature importance, 180-day forecast, multi-horizon bar |
| 🧠 Claude Decision Room | AI recommendation, action plan, risk/opportunity cards |
| ✅ Evidence Verification | Evidence support score, verified vs. unverified claims |
| 🎛️ Scenario Simulator | 9-lever simulation, tornado chart, live KPI updates |
| 📚 Data Sources | Methodology, limitations, technical stack |

---

## 🛡️ Security Notes

- ✅ API keys stored in environment variables only
- ✅ `.env` excluded from git via `.gitignore`
- ✅ No keys hardcoded anywhere in source
- ✅ Search results cached 30 minutes (saves API quota)
- ✅ Decision results cached 1 hour (saves API credits)

---

## 📄 License

MIT License — Free to use, modify, and deploy.

---

## 👨‍💻 Built for

Supply chain analysts, procurement teams, risk managers, and business strategists who need fast, evidence-backed supply chain intelligence without building a full data infrastructure.

---

*SCM FutureRisk AI · v1.0 · 2025*
