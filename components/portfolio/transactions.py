import streamlit as st
import pandas as pd
from datetime import datetime

def render_transactions():
    st.header("💼 Transaction History")
    
    if 'transactions' not in st.session_state:
        st.session_state.transactions = []
    
    with st.expander("➕ Record New Transaction", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.selectbox("Type", ["Buy", "Sell"])
            symbol = st.text_input("Symbol", placeholder="AAPL")
            asset_type = st.selectbox("Asset Type", ["Stock", "Crypto"])
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0.0, value=10.0, step=1.0)
            price = st.number_input("Price per share", min_value=0.0, value=150.0, step=0.01)
            date = st.date_input("Date", datetime.now())
        
        if st.button("Record Transaction"):
            if symbol and quantity > 0 and price > 0:
                total_amount = quantity * price
                
                transaction = {
                    'date': date.strftime("%Y-%m-%d"),
                    'type': transaction_type,
                    'symbol': symbol.upper(),
                    'asset_type': asset_type,
                    'quantity': quantity,
                    'price': price,
                    'total_amount': total_amount,
                    'timestamp': datetime.now().isoformat()
                }
                
                st.session_state.transactions.append(transaction)
                st.success(f"Recorded {transaction_type} of {quantity} {symbol} @ ${price:.2f}")
                st.rerun()
            else:
                st.error("Please fill all fields correctly.")
    
    if st.session_state.transactions:
        transactions_df = pd.DataFrame(st.session_state.transactions)
        transactions_df = transactions_df.sort_values('date', ascending=False)
        
        st.dataframe(transactions_df[['date', 'type', 'symbol', 'quantity', 'price', 'total_amount']], 
                    use_container_width=True)
        
        st.subheader("Transaction Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_buys = len(transactions_df[transactions_df['type'] == 'Buy'])
            st.metric("Total Buys", total_buys)
        
        with col2:
            total_sells = len(transactions_df[transactions_df['type'] == 'Sell'])
            st.metric("Total Sells", total_sells)
        
        with col3:
            total_volume = transactions_df['total_amount'].sum()
            st.metric("Total Volume", f"${total_volume:,.2f}")
        
        if st.button("📥 Export Transactions to CSV"):
            csv = transactions_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "transactions.csv", "text/csv")
    
    else:
        st.info("No transactions recorded yet. Add your first transaction above.")