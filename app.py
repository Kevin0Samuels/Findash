import streamlit as st
import yfinance as yf
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="FinDash - Personal Finance Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
from core.data_fetcher import StreamlitDataFetcher
from core.calculators import SIPCalculator, PortfolioManager
from components.charts import create_price_chart, create_sip_chart
from components.news import display_news
from components.watchlist import display_watchlist
from components.alerts import display_price_alerts
from components.performance import display_portfolio_performance
from components.portfolio.overview import render_portfolio_overview
from components.portfolio.holdings import render_holdings
from components.portfolio.transactions import render_transactions
from components.technical.indicators import render_technical_indicators
from components.technical.chart_tools import render_chart_tools

def main():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
      
    st.markdown('<h1 class="main-header">📊 FinDash - Personal Finance Tracker</h1>', unsafe_allow_html=True)
    st.markdown("### Track your investments and plan your SIPs with real-time data")    
    fetcher = StreamlitDataFetcher()
    sip_calc = SIPCalculator()
    portfolio_manager = PortfolioManager()    
    st.sidebar.markdown("## 🎛️ Control Panel")    
    st.sidebar.markdown("### 📈 Select Assets")    
    asset_type = st.sidebar.selectbox(
    "Choose Asset Type",
    [
        "Stocks", 
        "Cryptocurrency", 
        "SIP Calculator", 
        "Portfolio Overview",
        "Portfolio Holdings", 
        "Transactions",
        "Technical Analysis",
        "Chart Tools"
    ]
) 
    news_api_key = st.sidebar.text_input("News API Key (optional)", type="password") 

    if asset_type == "Stocks":
        stock_symbol = st.sidebar.selectbox(
            "Select Stock",
            ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX", "NVDA", "BRK-B", "JPM", "JNJ", "V"],
            key="stock_selector"
        )
        if st.sidebar.button("⭐ Add to Watchlist"):
            if portfolio_manager.add_to_watchlist(stock_symbol, "stock"):
                st.sidebar.success(f"Added {stock_symbol} to watchlist")
            else:
                st.sidebar.info(f"{stock_symbol} is already in your watchlist")
        
        with st.spinner(f"Fetching data for {stock_symbol}..."):
            stock_data = fetcher.fetch_stock_data(stock_symbol)
            
            if stock_data:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Price",
                        f"${stock_data['current_price']:.2f}",
                        f"{stock_data['change_1d']:.2f}% (1D)"
                    )
                
                with col2:
                    st.metric(
                        "30D Change",
                        f"{stock_data['change_30d']:.2f}%",
                        delta_color="normal"
                    )
                
                with col3:
                    st.metric(
                        "Volume",
                        f"{stock_data['volume']:,.0f}",
                    )
                
                with col4:
                    st.metric(
                        "52W Range",
                        f"${stock_data['low_52w']:.0f} - ${stock_data['high_52w']:.0f}"
                    )
                
                st.markdown(f"### 🏢 {stock_data['company_name']} ({stock_data['symbol']})")
                
                chart = create_price_chart(stock_data, stock_data['company_name'])
                st.plotly_chart(chart, use_container_width=True)
                
                news = fetcher.fetch_news(stock_symbol, news_api_key)
                display_news(news, stock_symbol)
                
                st.markdown("### 📋 Recent Price Data")
                recent_data = stock_data['history'].tail(7)[['Open', 'High', 'Low', 'Close', 'Volume']].round(2)
                st.dataframe(recent_data, use_container_width=True)
                
                if st.button("📥 Export Data to CSV"):
                    csv = recent_data.to_csv()
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{stock_symbol}_data.csv",
                        mime="text/csv"
                    )
            else:
                st.error(f"❌ Failed to fetch data for {stock_symbol}. Please try again.")
    
    elif asset_type == "Cryptocurrency":
        crypto_symbol = st.sidebar.selectbox(
            "Select Cryptocurrency",
            ["bitcoin", "ethereum", "binancecoin", "cardano", "solana", "polkadot", "dogecoin", "avalanche-2"],
            key="crypto_selector"
        )
        
        crypto_names = {
            "bitcoin": "Bitcoin", "ethereum": "Ethereum", "binancecoin": "BNB",
            "cardano": "Cardano", "solana": "Solana", "polkadot": "Polkadot",
            "dogecoin": "Dogecoin", "avalanche-2": "Avalanche"
        }
        
        if st.sidebar.button("⭐ Add to Watchlist"):
            if portfolio_manager.add_to_watchlist(crypto_symbol.upper(), "crypto"):
                st.sidebar.success(f"Added {crypto_symbol.upper()} to watchlist")
            else:
                st.sidebar.info(f"{crypto_symbol.upper()} is already in your watchlist")
        
        with st.spinner(f"Fetching data for {crypto_names.get(crypto_symbol, crypto_symbol)}..."):
            crypto_data = fetcher.fetch_crypto_data(crypto_symbol)
            
            if crypto_data:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Current Price",
                        f"${crypto_data['current_price']:,.2f}",
                        f"{crypto_data['24h_change']:.2f}% (24H)"
                    )
                
                with col2:
                    st.metric(
                        "30D Change",
                        f"{crypto_data['change_30d']:.2f}%"
                    )
                
                with col3:
                    if crypto_data.get('market_cap'):
                        st.metric(
                            "Market Cap",
                            f"${crypto_data['market_cap']/1e9:.1f}B"
                        )
                
                with col4:
                    if crypto_data.get('volume_24h'):
                        st.metric(
                            "24H Volume",
                            f"${crypto_data['volume_24h']/1e9:.1f}B"
                        )
                
                st.markdown(f"### 🪙 {crypto_names.get(crypto_symbol, crypto_symbol)} ({crypto_data['symbol']})")
                
                chart = create_price_chart(crypto_data, crypto_names.get(crypto_symbol, crypto_symbol))
                st.plotly_chart(chart, use_container_width=True)
                
                news = fetcher.fetch_news(crypto_symbol, news_api_key)
                display_news(news, crypto_symbol)
                
                st.markdown("### 📋 Recent Price Data")
                recent_data = crypto_data['history'].tail(7).round(2)
                st.dataframe(recent_data, use_container_width=True)
                
                if st.button("📥 Export Data to CSV"):
                    csv = recent_data.to_csv()
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{crypto_symbol}_data.csv",
                        mime="text/csv"
                    )
            else:
                st.error(f"❌ Failed to fetch data for {crypto_names.get(crypto_symbol, crypto_symbol)}. Please try again.")
    
    elif asset_type == "SIP Calculator":
        st.sidebar.markdown("### 💰 SIP Parameters")
        
        monthly_investment = st.sidebar.number_input(
            "Monthly Investment (₹)",
            min_value=500,
            max_value=100000,
            value=15000,
            step=1000
        )
        
        annual_return = st.sidebar.slider(
            "Expected Annual Return (%)",
            min_value=1.0,
            max_value=30.0,
            value=12.0,
            step=0.5
        )
        
        investment_years = st.sidebar.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=40,
            value=15
        )
        
        result = sip_calc.calculate_sip_future_value(monthly_investment, annual_return, investment_years)
        timeline = sip_calc.generate_sip_timeline(monthly_investment, annual_return, investment_years)
        
        st.markdown("### 💰 SIP Investment Calculator")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Monthly Investment",
                f"₹{monthly_investment:,}"
            )
        
        with col2:
            st.metric(
                "Total Invested",
                f"₹{result['total_invested']:,.0f}"
            )
        
        with col3:
            st.metric(
                "Future Value",
                f"₹{result['future_value']:,.0f}",
                f"₹{result['profit']:,.0f} profit"
            )
        
        with col4:
            st.metric(
                "Total Returns",
                f"{result['return_percentage']:.1f}%"
            )
        
        st.markdown("### 📊 Investment Summary")
        summary_data = {
            "Parameter": ["Monthly Investment", "Investment Period", "Expected Return", 
                         "Total Invested", "Maturity Value", "Total Profit", "Returns"],
            "Value": [f"₹{monthly_investment:,}", f"{investment_years} years", f"{annual_return}%",
                     f"₹{result['total_invested']:,}", f"₹{result['future_value']:,.0f}",
                     f"₹{result['profit']:,.0f}", f"{result['return_percentage']:.1f}%"]
        }
        st.table(pd.DataFrame(summary_data))
        
        if st.button("📈 Generate Detailed Analysis"):
            chart = create_sip_chart(timeline)
            st.plotly_chart(chart, use_container_width=True)
            
        if st.button("📥 Export SIP Results"):
            timeline_df = pd.DataFrame(timeline)
            csv = timeline_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="sip_calculator_results.csv",
                mime="text/csv"
            )
    
    elif asset_type == "Portfolio Overview":
        display_watchlist(portfolio_manager, fetcher)
        current_prices = {}
        display_price_alerts(portfolio_manager, current_prices)
        display_portfolio_performance()
    

    elif asset_type == "Portfolio Holdings":
        render_holdings()

    elif asset_type == "Transactions":
        render_transactions()

    elif asset_type == "Technical Analysis":
        stock_symbol = st.sidebar.selectbox("Select Symbol", ["AAPL", "GOOGL", "MSFT"])
        stock_data = fetcher.fetch_stock_data(stock_symbol)
        if stock_data:
            render_technical_indicators(stock_data['history'], stock_symbol)

    elif asset_type == "Chart Tools":
        stock_symbol = st.sidebar.selectbox("Select Symbol", ["AAPL", "GOOGL", "MSFT"])
        stock_data = fetcher.fetch_stock_data(stock_symbol)
        if stock_data:
            render_chart_tools(stock_data['history'], stock_symbol)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "**FinDash** is a comprehensive personal finance tracker built with Streamlit. "
        "Track stocks, crypto, and plan your SIP investments with real-time data and interactive visualizations."
    )
    
    st.sidebar.markdown("### 🔧 Features")
    st.sidebar.markdown("""
    - 📊 Real-time stock prices
    - 🪙 Cryptocurrency tracking  
    - 💰 SIP calculator with projections
    - 📈 Interactive charts
    - 📱 Mobile-responsive design
    - ⭐ Watchlist functionality
    - 🔔 Price alerts
    - 📰 News integration
    - 📥 Data export capabilities
    """)

if __name__ == "__main__":
    main()