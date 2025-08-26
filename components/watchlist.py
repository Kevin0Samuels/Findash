import streamlit as st
import pandas as pd

def display_watchlist(portfolio_manager, fetcher):
    """Display the user's watchlist"""
    st.markdown("### ⭐ Your Watchlist")
    
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add assets to track them here.")
        return
        
    current_prices = {}
    for item in st.session_state.watchlist:
        if item['asset_type'] == 'stock':
            data = fetcher.fetch_stock_data(item['symbol'])
            if data:
                current_prices[item['symbol']] = data['current_price']
    
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.watchlist):
        with cols[i % 3]:
            with st.expander(f"{item['symbol']} ({item['asset_type']})"):
                if item['symbol'] in current_prices:
                    st.metric("Current Price", f"${current_prices[item['symbol']]:.2f}")
                
                if st.button("Remove", key=f"remove_{item['symbol']}"):
                    portfolio_manager.remove_from_watchlist(item['symbol'])
                    st.rerun()
    
    if st.button("📥 Export Watchlist to CSV"):
        watchlist_df = pd.DataFrame(st.session_state.watchlist)
        csv = watchlist_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="watchlist.csv",
            mime="text/csv"
        )