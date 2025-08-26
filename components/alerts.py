import streamlit as st
import time
from datetime import datetime

def display_price_alerts(portfolio_manager, current_prices):
    st.markdown("### 🔔 Price Alerts")
    
    with st.form("add_alert_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            alert_symbol = st.text_input("Symbol", key="alert_symbol")
        with col2:
            target_price = st.number_input("Target Price", min_value=0.01, value=100.0, step=1.0)
        with col3:
            condition = st.selectbox("Condition", ["above", "below"])
        
        if st.form_submit_button("Add Alert"):
            if alert_symbol:
                portfolio_manager.add_price_alert(alert_symbol.upper(), target_price, condition)
                st.success(f"Alert added for {alert_symbol} {condition} ${target_price}")
            else:
                st.error("Please enter a symbol")
    
    if not st.session_state.price_alerts:
        st.info("No price alerts set up yet.")
    else:
        for alert in st.session_state.price_alerts:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**{alert['symbol']}**")
            with col2:
                status = "✅ Triggered" if alert['triggered'] else "🟡 Active"
                st.write(status)
            with col3:
                st.write(f"{alert['condition']} ${alert['target_price']}")
            with col4:
                if st.button("Delete", key=f"delete_{alert['id']}"):
                    portfolio_manager.remove_price_alert(alert['id'])
                    st.rerun()
        
        triggered = portfolio_manager.check_price_alerts(current_prices)
        for alert in triggered:
            st.success(f"Alert! {alert['symbol']} is {alert['condition']} ${alert['target_price']}")