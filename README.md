# 📊 Marketing Intelligence Dashboard with AI Insights

Interactive BI dashboard with AI-powered analysis of marketing campaign performance and business outcomes.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python run_dashboard.py
# OR
streamlit run src/dashboard.py
```

## 📈 Features

- **🤖 AI Chat Assistant**: Ask any questions about your marketing data
- **📊 Key Metrics**: Spend, Revenue, ROAS, Orders overview
- **📈 Channel Performance**: ROAS comparison across platforms
- **🗺️ Geographic Analysis**: State-wise performance metrics
- **📈 Trend Analysis**: Time series charts
- **🔍 Interactive Filters**: Date range and platform filtering

## 🤖 AI Setup

1. **Get Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Add to config.py**: Replace `your_gemini_api_key_here` with your actual API key
3. **Chat with AI**: Ask any questions about your marketing data

*Note: Dashboard works without AI key - shows basic charts only*

## 🎯 Key Metrics

- **ROAS** (Return on Ad Spend)
- **CTR** (Click-Through Rate)
- **CPC** (Cost Per Click)
- **CPM** (Cost Per Mille)
- **Customer Acquisition Rate**
- **Average Order Value**

## 📊 Data Sources

- **Facebook.csv**: Campaign data (ASC, Prospecting tactics)
- **Google.csv**: Campaign data (Search, Display tactics)
- **TikTok.csv**: Campaign data (Retargeting, Spark Ads)
- **business.csv**: Daily business metrics (orders, revenue, customers)

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Connect repository to share.streamlit.io
3. Deploy with one click

### Local Development
```bash
streamlit run src/marketing_dashboard.py
```

## 📋 Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy

---
