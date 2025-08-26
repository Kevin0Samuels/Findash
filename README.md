# 📊 FinDash - Personal Finance & Investment Tracker

A comprehensive dashboard to track SIPs, stock/crypto prices, and visualize investment growth with real-time data and interactive charts.

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Overview

**FinDash** is a personal finance tracker for monitoring and analyzing investments.

### Key Features
- API Integration: Yahoo Finance, CoinGecko, Alpha Vantage
- Interactive Data Visualization: Plotly, Matplotlib
- Modern Dashboard Interface: Streamlit
- SIP Calculator with projections
- Real-time market data for stocks and cryptocurrencies

---

## 🎯 Live Demo: https://findash-hmwahhqzaajhjzddy6s8qs.streamlit.app/

---
## 🚀 Features

- **Stock Tracking:** Real-time prices, 30-day history, key metrics
- **Cryptocurrency Tracking:** Live prices, 24H/30D changes, market cap
- **SIP Calculator:** Compound interest, projections, scenario analysis
- **Interactive Dashboard:** Real-time updates, mobile-responsive, export charts/tables

---

## 🛠️ Tech Stack

| Component         | Technology                          |
|-------------------|-------------------------------------|
| Backend           | Python 3.8+                         |
| Frontend          | Streamlit                           |
| Data Sources      | Yahoo Finance, CoinGecko, Alpha Vantage |
| Visualization     | Plotly, Matplotlib                  |
| Data Processing   | Pandas, NumPy                       |
| Caching           | Streamlit caching                   |
| Deployment        | Streamlit Cloud Ready               |

---

## 📦 Installation

**Prerequisites:** Python 3.8+, pip

```sh
git clone https://github.com/yourusername/findash.git
cd findash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
```
Dashboard opens at [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
findash/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   ├── sample_data.csv
│   └── cache/
├── utils/
│   ├── data_fetcher.py
│   ├── calculator.py
│   └── visualizations.py
├── assets/
│   ├── images/
│   └── styles/
└── screenshots/
```

---

## 🎮 Usage

- **Stocks:** Select symbol, fetch data, view metrics/charts
- **Cryptocurrency:** Select coin, fetch data, review prices
- **SIP Calculator:** Set parameters, generate analysis

---

## 📊 Sample SIP Projections
|--------------------|--------------|----------|----------------|---------------|-------------|
| Monthly Investment | Annual Return | Period   | Total Invested | Maturity Value | Profit    |
|--------------------|--------------|----------|----------------|---------------|-------------|
| ₹15,000            | 12%          | 15 years | ₹27,00,000     | ₹100,27,601   | ₹73,27,601  |
| ₹10,000            | 15%          | 20 years | ₹24,00,000     | ₹1,23,14,000  | ₹99,14,000  |
| ₹5,000             | 10%          | 25 years | ₹15,00,000     | ₹65,92,000    | ₹50,92,000  |
|--------------------|--------------|----------|----------------|---------------|-------------|

## 🔧 API Configuration

- **Yahoo Finance:** `yfinance` (no API key)
- **CoinGecko:** Free, no API key
- **Alpha Vantage:** [Get free API key](https://www.alphavantage.co/support/#api-key)

---

## 🚀 Deployment

- **Streamlit Cloud:** Push to GitHub, deploy at [streamlit.io/cloud](https://streamlit.io/cloud)
- **Local:**  
    ```sh
    pip install streamlit plotly pandas yfinance
    streamlit run app.py --server.runOnSave true
    ```
- **Other:** Heroku, AWS, DigitalOcean, Google Cloud Run

---

## 📈 Roadmap

- Portfolio Management: Multiple holdings
- Custom Alerts & Notifications
- Advanced Technical Analysis: RSI, MACD, Bollinger Bands
- Export: PDF, CSV/Excel
- User Authentication
- More Asset Classes: Mutual funds, bonds, ETFs
- Goal-based Planning
- Tax Calculations
- International Markets
- Social Features

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Make changes & test
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

**Dev Setup:**
```sh
pip install -r requirements-dev.txt
python -m pytest tests/
flake8 .
```

---

## 📄 License

MIT License. See LICENSE file.

---

## 🎉 Acknowledgments

- Yahoo Finance
- CoinGecko
- Alpha Vantage
- Streamlit
- Plotly
- Pandas & NumPy

---

## 📞 Contact

- GitHub Issues
- Discussions
- Email: ikkevinsamuels@gmail.com

---

## 🏆 Use Cases

- Internship Applications (Fintech, Quantitative Analysis, Data Science)
- Hackathons
- Portfolio Projects
- Personal Finance Management

---

## ⚡ Performance

- Data caching minimizes API calls
- Fallback mechanisms for reliability
- Responsive design

---

⭐ **If you find this project useful, please give it a star on GitHub!**
