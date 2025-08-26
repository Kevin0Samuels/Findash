import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

def display_portfolio_performance():
    st.markdown("### 📊 Portfolio Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Value", "$125,430", "+2.3%")
    with col2:
        st.metric("Today's Change", "+$2,850", "+1.8%")
    with col3:
        st.metric("Total Gain", "$25,430", "+25.4%")
    with col4:
        st.metric("YTD Return", "+15.2%", "vs. SPY +12.1%")
    
    dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
    portfolio_values = [100000 + i*100 + np.random.normal(0, 500) for i in range(len(dates))]
    spy_values = [100000 + i*80 + np.random.normal(0, 400) for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=portfolio_values, name='Your Portfolio', line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=dates, y=spy_values, name='S&P 500', line=dict(color='#888888')))
    
    fig.update_layout(
        title="Portfolio Performance vs Benchmark",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("📊 Export Performance Data"):
        perf_df = pd.DataFrame({
            'Date': dates,
            'Portfolio_Value': portfolio_values,
            'SPY_Value': spy_values
        })
        csv = perf_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="portfolio_performance.csv",
            mime="text/csv"
        )