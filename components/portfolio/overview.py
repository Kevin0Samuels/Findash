import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def render_portfolio_overview():
    st.header("📊 Portfolio Overview")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {
            'total_value': 125430,
            'cash_balance': 15000,
            'initial_investment': 100000,
            'holdings': {}
        }
    
    portfolio = st.session_state.portfolio
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_gain = portfolio['total_value'] - portfolio['initial_investment']
        gain_percentage = (total_gain / portfolio['initial_investment']) * 100
        st.metric("Total Value", f"${portfolio['total_value']:,.2f}", 
                 f"{gain_percentage:.1f}%")
    
    with col2:
        st.metric("Cash Balance", f"${portfolio['cash_balance']:,.2f}")
    
    with col3:
        st.metric("Total Gain", f"${total_gain:,.2f}", 
                 f"{gain_percentage:.1f}%")
    
    with col4:
        daily_change = 2850
        daily_percentage = 2.3
        st.metric("Today's Change", f"${daily_change:,.2f}", 
                 f"{daily_percentage:.1f}%")
    
    st.subheader("Performance Over Time")
    dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
    portfolio_values = [100000 + i*100 + np.random.normal(0, 500) for i in range(len(dates))]
    spy_values = [100000 + i*80 + np.random.normal(0, 400) for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=portfolio_values, name='Your Portfolio', 
                           line=dict(color='#1f77b4', width=3)))
    fig.add_trace(go.Scatter(x=dates, y=spy_values, name='S&P 500', 
                           line=dict(color='#888888', width=2)))
    
    fig.update_layout(
        title="Portfolio Performance vs Benchmark",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Portfolio Allocation")
    
    if portfolio['holdings']:
        allocation_data = []
        for symbol, holding in portfolio['holdings'].items():
            allocation_data.append({
                'Asset': symbol,
                'Value': holding['current_value'],
                'Percentage': (holding['current_value'] / portfolio['total_value']) * 100
            })
        
        allocation_data.append({
            'Asset': 'CASH',
            'Value': portfolio['cash_balance'],
            'Percentage': (portfolio['cash_balance'] / portfolio['total_value']) * 100
        })
        
        allocation_df = pd.DataFrame(allocation_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(allocation_df, values='Value', names='Asset', 
                        title='Asset Allocation')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(allocation_df, x='Asset', y='Value', 
                        title='Value by Asset', color='Asset')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No holdings yet. Add some stocks or crypto to see allocation charts.")
    
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Update Prices", help="Refresh all holding prices"):
            st.success("Prices updated!")
    
    with col2:
        if st.button("📊 Export Report", help="Export portfolio report to CSV"):
            export_data = {
                'Date': [datetime.now().strftime("%Y-%m-%d")],
                'Total_Value': [portfolio['total_value']],
                'Cash_Balance': [portfolio['cash_balance']],
                'Total_Gain': [total_gain]
            }
            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "portfolio_overview.csv", "text/csv")
    
    with col3:
        if st.button("📈 View Detailed Analysis", help="View advanced analytics"):
            st.session_state.show_advanced_analytics = True
            st.rerun()