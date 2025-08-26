import streamlit as st
from datetime import datetime, timedelta
import time
class SIPCalculator:
    """SIP Calculator for Streamlit"""
    
    def calculate_sip_future_value(self, monthly_investment, annual_return, years):
        """Calculate SIP future value"""
        monthly_rate = annual_return / 12 / 100
        total_months = int(years * 12)
        
        if monthly_rate == 0:
            future_value = monthly_investment * total_months
        else:
            future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
        
        total_invested = monthly_investment * total_months
        profit = future_value - total_invested
        
        return {
            'future_value': future_value,
            'total_invested': total_invested,
            'profit': profit,
            'return_percentage': (profit / total_invested) * 100 if total_invested > 0 else 0
        }
    def generate_sip_timeline(self, monthly_investment, annual_return, years):
        """Generate SIP timeline"""
        monthly_rate = annual_return / 12 / 100
        timeline = []
        total_months = int(years * 12)
        
        for month in range(1, total_months + 1):
            if monthly_rate == 0:
                value = monthly_investment * month
            else:
                value = monthly_investment * (((1 + monthly_rate) ** month - 1) / monthly_rate)
            
            timeline.append({
                'month': month,
                'year': round(month / 12, 1),
                'invested': monthly_investment * month,
                'value': value,
                'profit': value - (monthly_investment * month)
            })
        
        return timeline

class PortfolioManager:
    """Manage user portfolio and watchlist"""
    
    def __init__(self):
        if 'watchlist' not in st.session_state:
            st.session_state.watchlist = []
        
        if 'price_alerts' not in st.session_state:
            st.session_state.price_alerts = []
    
    def add_to_watchlist(self, symbol, asset_type):
        """Add a symbol to the watchlist"""
        if symbol not in [item['symbol'] for item in st.session_state.watchlist]:
            st.session_state.watchlist.append({
                'symbol': symbol,
                'asset_type': asset_type,
                'added_date': datetime.now().strftime("%Y-%m-%d")
            })
            return True
        return False
    
    def remove_from_watchlist(self, symbol):
        """Remove a symbol from the watchlist"""
        st.session_state.watchlist = [item for item in st.session_state.watchlist if item['symbol'] != symbol]
    
    def add_price_alert(self, symbol, target_price, condition):
        """Add a price alert"""
        alert_id = f"{symbol}_{target_price}_{condition}_{int(time.time())}"
        st.session_state.price_alerts.append({
            'id': alert_id,
            'symbol': symbol,
            'target_price': target_price,
            'condition': condition,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'triggered': False
        })
    
    def remove_price_alert(self, alert_id):
        """Remove a price alert"""
        st.session_state.price_alerts = [alert for alert in st.session_state.price_alerts if alert['id'] != alert_id]
    
    def check_price_alerts(self, current_prices):
        """Check if any price alerts should be triggered"""
        triggered_alerts = []
        for alert in st.session_state.price_alerts:
            if alert['triggered']:
                continue
                
            symbol = alert['symbol']
            if symbol not in current_prices:
                continue
                
            current_price = current_prices[symbol]
            target_price = alert['target_price']
            condition = alert['condition']
            
            if ((condition == 'above' and current_price >= target_price) or
                (condition == 'below' and current_price <= target_price)):
                alert['triggered'] = True
                alert['triggered_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                triggered_alerts.append(alert)
        
        return triggered_alerts