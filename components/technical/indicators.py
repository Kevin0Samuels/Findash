import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    
    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up_val = delta
            down_val = 0.
        else:
            up_val = 0.
            down_val = -delta
        
        up = (up * (period - 1) + up_val) / period
        down = (down * (period - 1) + down_val) / period
        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    ema_fast = pd.Series(prices).ewm(span=fast).mean()
    ema_slow = pd.Series(prices).ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    
    return macd, signal_line, histogram

def calculate_moving_averages(prices, windows=[20, 50, 200]):
    """Calculate multiple moving averages"""
    ma_data = {}
    for window in windows:
        ma_data[f'MA{window}'] = pd.Series(prices).rolling(window=window).mean()
    return ma_data

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    rolling_mean = pd.Series(prices).rolling(window=window).mean()
    rolling_std = pd.Series(prices).rolling(window=window).std()
    
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    return upper_band, rolling_mean, lower_band

def render_technical_indicators(price_data, symbol):
    """Main function to render technical indicators"""
    st.header(f"📈 Technical Analysis: {symbol}")
    
    if price_data is None or len(price_data) < 50:
        st.warning("Need at least 50 data points for technical analysis")
        return
    
    prices = price_data['Close'].values
    
    # Indicator selection
    st.subheader("Select Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        show_rsi = st.checkbox("RSI", value=True)
    with col2:
        show_macd = st.checkbox("MACD", value=True)
    with col3:
        show_ma = st.checkbox("Moving Averages", value=True)
    with col4:
        show_bb = st.checkbox("Bollinger Bands", value=False)
    
    # Calculate indicators
    indicators = {}
    
    if show_rsi:
        indicators['RSI'] = calculate_rsi(prices)
    
    if show_macd:
        macd, signal, histogram = calculate_macd(prices)
        indicators['MACD'] = macd
        indicators['Signal'] = signal
        indicators['Histogram'] = histogram
    
    if show_ma:
        ma_data = calculate_moving_averages(prices)
        indicators.update(ma_data)
    
    if show_bb:
        upper, middle, lower = calculate_bollinger_bands(prices)
        indicators['BB_Upper'] = upper
        indicators['BB_Middle'] = middle
        indicators['BB_Lower'] = lower
    
    # Create charts
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Price with Indicators', 'Oscillators'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Price chart
    fig.add_trace(
        go.Scatter(x=price_data.index, y=price_data['Close'], name='Price'),
        row=1, col=1
    )
    
    # Add indicators to price chart
    for name, values in indicators.items():
        if name.startswith('MA') or name.startswith('BB'):
            fig.add_trace(
                go.Scatter(x=price_data.index, y=values, name=name),
                row=1, col=1
            )
    
    # Add oscillators to second chart
    if show_rsi:
        fig.add_trace(
            go.Scatter(x=price_data.index, y=indicators['RSI'], name='RSI'),
            row=2, col=1
        )
        # Add RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    if show_macd:
        fig.add_trace(
            go.Scatter(x=price_data.index, y=indicators['MACD'], name='MACD'),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=price_data.index, y=indicators['Signal'], name='Signal'),
            row=2, col=1
        )
        # Add histogram as bars
        fig.add_trace(
            go.Bar(x=price_data.index, y=indicators['Histogram'], name='Histogram'),
            row=2, col=1
        )
    
    fig.update_layout(height=800, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Trading signals based on indicators
    if st.checkbox("Show Trading Signals"):
        st.subheader("Trading Signals")
        
        signals = []
        
        # RSI signals
        if show_rsi and len(indicators['RSI']) > 0:
            current_rsi = indicators['RSI'][-1]
            if current_rsi > 70:
                signals.append(("RSI Overbought", "Consider selling", "🔴"))
            elif current_rsi < 30:
                signals.append(("RSI Oversold", "Consider buying", "🟢"))
        
        # MACD signals
        if show_macd and len(indicators['MACD']) > 1:
            current_macd = indicators['MACD'][-1]
            previous_macd = indicators['MACD'][-2]
            current_signal = indicators['Signal'][-1]
            
            if current_macd > current_signal and previous_macd <= indicators['Signal'][-2]:
                signals.append(("MACD Bullish Crossover", "Buy signal", "🟢"))
            elif current_macd < current_signal and previous_macd >= indicators['Signal'][-2]:
                signals.append(("MACD Bearish Crossover", "Sell signal", "🔴"))
        
        if signals:
            for signal, description, icon in signals:
                st.write(f"{icon} **{signal}**: {description}")
        else:
            st.info("No strong trading signals detected.")