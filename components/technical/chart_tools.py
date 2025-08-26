import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_advanced_chart(price_data, chart_type='line', indicators=None):
    """Create advanced chart with multiple options"""
    
    if indicators is None:
        indicators = {}
    
    fig = go.Figure()
    
    if chart_type == 'line':
        fig.add_trace(go.Scatter(
            x=price_data.index, 
            y=price_data['Close'], 
            name='Price',
            line=dict(color='#1f77b4', width=2)
        ))
    
    elif chart_type == 'candlestick':
        fig.add_trace(go.Candlestick(
            x=price_data.index,
            open=price_data['Open'],
            high=price_data['High'],
            low=price_data['Low'],
            close=price_data['Close'],
            name='OHLC'
        ))
    
    elif chart_type == 'area':
        fig.add_trace(go.Scatter(
            x=price_data.index,
            y=price_data['Close'],
            name='Price',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=2)
        ))
    
    elif chart_type == 'heikin-ashi':
        # Calculate Heikin-Ashi values
        ha_close = (price_data['Open'] + price_data['High'] + price_data['Low'] + price_data['Close']) / 4
        ha_open = (price_data['Open'].shift(1) + price_data['Close'].shift(1)) / 2
        ha_open.iloc[0] = (price_data['Open'].iloc[0] + price_data['Close'].iloc[0]) / 2
        ha_high = price_data[['High', 'Open', 'Close']].max(axis=1)
        ha_low = price_data[['Low', 'Open', 'Close']].min(axis=1)
        
        fig.add_trace(go.Candlestick(
            x=price_data.index,
            open=ha_open,
            high=ha_high,
            low=ha_low,
            close=ha_close,
            name='Heikin-Ashi'
        ))
    
    # Add indicators
    for indicator_name, indicator_data in indicators.items():
        if indicator_data is not None and len(indicator_data) == len(price_data):
            fig.add_trace(go.Scatter(
                x=price_data.index,
                y=indicator_data,
                name=indicator_name,
                line=dict(dash='dash' if 'MA' in indicator_name else 'solid')
            ))
    
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=500,
        showlegend=True
    )
    
    return fig

def render_chart_tools(price_data, symbol):
    """Main function to render chart tools"""
    st.header(f"📊 Advanced Charting: {symbol}")
    
    if price_data is None:
        st.warning("No price data available")
        return
    
    # Chart type selection
    chart_type = st.selectbox(
        "Chart Type",
        ["Line", "Candlestick", "Area", "Heikin-Ashi"],
        key="chart_type"
    ).lower().replace(' ', '-')
    
    # Technical indicators to show
    st.subheader("Chart Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_volume = st.checkbox("Show Volume", value=True)
        log_scale = st.checkbox("Logarithmic Scale", value=False)
    
    with col2:
        show_grid = st.checkbox("Show Grid", value=True)
        # Add more chart settings here
    
    # Create the chart
    chart = create_advanced_chart(price_data, chart_type)
    
    # Add volume if requested
    if show_volume and 'Volume' in price_data.columns:
        # Create subplot with volume
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Price', 'Volume'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Add price chart
        if chart_type == 'candlestick' or chart_type == 'heikin-ashi':
            fig.add_trace(go.Candlestick(
                x=price_data.index,
                open=price_data['Open'],
                high=price_data['High'],
                low=price_data['Low'],
                close=price_data['Close'],
                name='Price'
            ), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(
                x=price_data.index, 
                y=price_data['Close'], 
                name='Price',
                line=dict(color='#1f77b4', width=2)
            ), row=1, col=1)
        
        # Add volume
        colors = ['red' if price_data['Close'].iloc[i] < price_data['Open'].iloc[i] 
                 else 'green' for i in range(len(price_data))]
        
        fig.add_trace(go.Bar(
            x=price_data.index,
            y=price_data['Volume'],
            name='Volume',
            marker_color=colors
        ), row=2, col=1)
        
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            height=600,
            showlegend=False
        )
        
        if log_scale:
            fig.update_yaxes(type="log", row=1, col=1)
        
        if show_grid:
            fig.update_xaxes(showgrid=True)
            fig.update_yaxes(showgrid=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Just show price chart
        if log_scale:
            chart.update_yaxes(type="log")
        
        if show_grid:
            chart.update_xaxes(showgrid=True)
            chart.update_yaxes(showgrid=True)
        
        st.plotly_chart(chart, use_container_width=True)
    
    # Chart analysis tools
    st.subheader("Chart Analysis")
    
    if st.button("📏 Show Support/Resistance Levels"):
        # Simple support/resistance detection
        st.info("Support/Resistance Levels:")
        
        # Simple algorithm to find potential levels
        closes = price_data['Close'].values
        levels = []
        
        for i in range(2, len(closes) - 2):
            if (closes[i] > closes[i-1] and closes[i] > closes[i-2] and 
                closes[i] > closes[i+1] and closes[i] > closes[i+2]):
                levels.append(("Resistance", closes[i]))
            elif (closes[i] < closes[i-1] and closes[i] < closes[i-2] and 
                  closes[i] < closes[i+1] and closes[i] < closes[i+2]):
                levels.append(("Support", closes[i]))
        
        # Group similar levels and display
        if levels:
            level_df = pd.DataFrame(levels, columns=['Type', 'Price'])
            level_df = level_df.groupby('Type')['Price'].agg(['mean', 'count']).round(2)
            st.dataframe(level_df)
        else:
            st.write("No clear support/resistance levels detected.")
    
    # Trend analysis - FIXED: Add bounds checking
    if st.button("📈 Trend Analysis"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Get the length of the data
            data_length = len(price_data)
            
            # Short-term trend (20 days) - only if we have enough data
            if data_length >= 20:
                short_trend = "🟢 Bullish" if price_data['Close'].iloc[-1] > price_data['Close'].iloc[-20] else "🔴 Bearish"
                st.metric("Short-term (20d)", short_trend)
            else:
                st.metric("Short-term (20d)", "📊 Need more data", f"Only {data_length} days available")
            
            # Medium-term trend (50 days) - only if we have enough data
            if data_length >= 50:
                medium_trend = "🟢 Bullish" if price_data['Close'].iloc[-1] > price_data['Close'].iloc[-50] else "🔴 Bearish"
                st.metric("Medium-term (50d)", medium_trend)
            else:
                st.metric("Medium-term (50d)", "📊 Need more data", f"Only {data_length} days available")
            
            # Long-term trend (200 days) - only if we have enough data
            if data_length >= 200:
                long_trend = "🟢 Bullish" if price_data['Close'].iloc[-1] > price_data['Close'].iloc[-200] else "🔴 Bearish"
                st.metric("Long-term (200d)", long_trend)
            else:
                st.metric("Long-term (200d)", "📊 Need more data", f"Only {data_length} days available")
        
        with col2:
            # Volatility analysis - only if we have enough data
            if data_length >= 20:
                volatility_20d = price_data['Close'].pct_change().std() * np.sqrt(252) * 100
                st.metric("Annualized Volatility (20d)", f"{volatility_20d:.1f}%")
            else:
                st.metric("Annualized Volatility (20d)", "📊 Need more data")
            
            if data_length >= 50:
                volatility_50d = price_data['Close'].pct_change().std() * np.sqrt(252) * 100
                st.metric("Annualized Volatility (50d)", f"{volatility_50d:.1f}%")
            else:
                st.metric("Annualized Volatility (50d)", "📊 Need more data")
    
    # Pattern recognition (simplified)
    if st.button("🔍 Pattern Recognition"):
        st.info("Common Chart Patterns:")
        
        patterns = []
        closes = price_data['Close'].values
        
        # Simple pattern detection
        if len(closes) >= 10:
            recent = closes[-10:]
            # Check for upward trend
            if all(recent[i] < recent[i+1] for i in range(len(recent)-1)):
                patterns.append(("Strong Uptrend", "🟢", "Continuing bullish momentum"))
            
            # Check for downward trend
            if all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
                patterns.append(("Strong Downtrend", "🔴", "Continuing bearish momentum"))
            
            # Check for consolidation
            if max(recent) / min(recent) < 1.05:  # Less than 5% range
                patterns.append(("Consolidation", "🟡", "Price is consolidating, watch for breakout"))
        
        if patterns:
            for pattern, icon, description in patterns:
                st.write(f"{icon} **{pattern}**: {description}")
        else:
            st.write("No clear patterns detected in recent price action.")
    
    # Export chart data
    if st.button("💾 Export Chart Data"):
        csv = price_data.to_csv()
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{symbol}_chart_data.csv",
            mime="text/csv"
        )

def add_drawing_tools(fig):
    """Add drawing tools to the chart (conceptual)"""
    st.sidebar.subheader("Drawing Tools")
    
    drawing_tool = st.sidebar.selectbox(
        "Select Drawing Tool",
        ["None", "Trendline", "Horizontal Line", "Vertical Line", "Fibonacci Retracement"]
    )
    
    if drawing_tool != "None":
        st.info(f"Selected: {drawing_tool}. Click on the chart to place points.")
        # In a real implementation, you would use Plotly's drawing tools
        # or create custom interactivity
    
    return fig