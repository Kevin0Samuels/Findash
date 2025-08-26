import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

def render_holdings():
    st.header("📦 Your Holdings")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {
            'holdings': {},
            'cash_balance': 15000
        }
    
    portfolio = st.session_state.portfolio
    
    with st.expander("➕ Add New Holding", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            symbol = st.text_input("Symbol", placeholder="AAPL")
        
        with col2:
            asset_type = st.selectbox("Type", ["Stock", "Crypto"])
        
        with col3:
            quantity = st.number_input("Quantity", min_value=0.0, value=10.0, step=1.0)
        
        with col4:
            purchase_price = st.number_input("Purchase Price", min_value=0.0, value=150.0, step=1.0)
        
        if st.button("Add to Portfolio"):
            if symbol and quantity > 0 and purchase_price > 0:
                if symbol in portfolio['holdings']:
                    holding = portfolio['holdings'][symbol]
                    total_quantity = holding['quantity'] + quantity
                    avg_price = ((holding['quantity'] * holding['purchase_price']) + 
                                (quantity * purchase_price)) / total_quantity
                    
                    portfolio['holdings'][symbol] = {
                        'quantity': total_quantity,
                        'purchase_price': avg_price,
                        'total_invested': total_quantity * avg_price,
                        'current_price': holding['current_price'],
                        'current_value': total_quantity * holding['current_price'],
                        'asset_type': asset_type,
                        'last_updated': datetime.now().strftime("%Y-%m-%d")
                    }
                else:
                    current_price = purchase_price * (1 + np.random.uniform(-0.1, 0.3))
                    portfolio['holdings'][symbol] = {
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'total_invested': quantity * purchase_price,
                        'current_price': current_price,
                        'current_value': quantity * current_price,
                        'asset_type': asset_type,
                        'last_updated': datetime.now().strftime("%Y-%m-%d")
                    }
                
                st.success(f"Added {quantity} shares of {symbol} to portfolio!")
                st.rerun()
            else:
                st.error("Please fill all fields correctly.")
    
    if portfolio['holdings']:
        holdings_data = []
        total_invested = 0
        total_current = 0
        
        for symbol, holding in portfolio['holdings'].items():
            gain_loss = holding['current_value'] - holding['total_invested']
            gain_loss_pct = (gain_loss / holding['total_invested']) * 100
            
            holdings_data.append({
                'Symbol': symbol,
                'Type': holding['asset_type'],
                'Quantity': holding['quantity'],
                'Avg Price': f"${holding['purchase_price']:.2f}",
                'Current Price': f"${holding['current_price']:.2f}",
                'Invested': f"${holding['total_invested']:,.2f}",
                'Current Value': f"${holding['current_value']:,.2f}",
                'P&L': f"${gain_loss:,.2f}",
                'P&L %': f"{gain_loss_pct:.1f}%",
                'P&L Color': 'green' if gain_loss >= 0 else 'red'
            })
            
            total_invested += holding['total_invested']
            total_current += holding['current_value']
        
        total_gain_loss = total_current - total_invested
        total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0
        
        holdings_data.append({
            'Symbol': 'TOTAL',
            'Type': '',
            'Quantity': '',
            'Avg Price': '',
            'Current Price': '',
            'Invested': f"${total_invested:,.2f}",
            'Current Value': f"${total_current:,.2f}",
            'P&L': f"${total_gain_loss:,.2f}",
            'P&L %': f"{total_gain_loss_pct:.1f}%",
            'P&L Color': 'green' if total_gain_loss >= 0 else 'red'
        })
        
        df = pd.DataFrame(holdings_data)
        
        def color_pl(val):
            color = 'green' if float(val.replace('$', '').replace(',', '').replace('%', '')) >= 0 else 'red'
            return f'color: {color}'
        
        styled_df = df.style.applymap(color_pl, subset=['P&L', 'P&L %'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        if st.button("📥 Export Holdings to CSV"):
            export_df = df.drop(columns=['P&L Color'])
            csv = export_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "portfolio_holdings.csv", "text/csv")
    
    else:
        st.info("No holdings yet. Add some stocks or crypto to your portfolio.")