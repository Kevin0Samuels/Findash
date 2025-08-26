import streamlit as st
from datetime import datetime

def display_news(news_articles, symbol):
    """Display news articles in a formatted way"""
    if not news_articles:
        st.info(f"No news available for {symbol}")
        return
        
    st.markdown(f"### 📰 Latest News about {symbol}")
    
    for article in news_articles:
        with st.container():
            st.markdown(f"#### {article['title']}")
            st.markdown(f"*Source: {article['source']['name']} - {datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00')).strftime('%B %d, %Y')}*")
            st.markdown(f"{article['description']}")
            st.markdown(f"[Read more]({article['url']})")
            st.markdown("---")