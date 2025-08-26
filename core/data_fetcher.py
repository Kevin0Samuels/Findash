import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class StreamlitDataFetcher:
    """Data fetcher optimized for Streamlit with caching"""
    
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_stock_data(_self, symbol, period="1mo"):
        """Fetch stock data with Streamlit caching"""
        # Mock realistic data for demo
        mock_prices = {
            'AAPL': 220.50, 'GOOGL': 175.25, 'MSFT': 415.80, 'TSLA': 185.30,
            'AMZN': 180.75, 'META': 520.40, 'NFLX': 485.90, 'NVDA': 920.15,
            'BRK-B': 425.30, 'JPM': 210.45, 'JNJ': 155.80, 'V': 280.90
        }
        
        company_names = {
            'AAPL': 'Apple Inc.', 'GOOGL': 'Alphabet Inc.', 'MSFT': 'Microsoft Corporation',
            'TSLA': 'Tesla Inc.', 'AMZN': 'Amazon.com Inc.', 'META': 'Meta Platforms Inc.',
            'NFLX': 'Netflix Inc.', 'NVDA': 'NVIDIA Corporation', 'BRK-B': 'Berkshire Hathaway',
            'JPM': 'JPMorgan Chase & Co.', 'JNJ': 'Johnson & Johnson', 'V': 'Visa Inc.'
        }
        
        base_price = mock_prices.get(symbol, 100.0)
        
        # Generate realistic historical data
        np.random.seed(hash(symbol) % 1000)  # Consistent random data per symbol
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        prices = []
        
        current = base_price
        for i in range(30):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            current = max(current * (1 + change), base_price * 0.7)  # Prevent unrealistic drops
            prices.append(current)
        
        hist = pd.DataFrame({
            'Close': prices,
            'Open': [p * (1 + np.random.normal(0, 0.005)) for p in prices],
            'High': [p * (1 + abs(np.random.normal(0, 0.01))) for p in prices],
            'Low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in prices],
            'Volume': [np.random.randint(50000000, 200000000) for _ in prices]
        }, index=dates)
        
        current_price = prices[-1]
        change_30d = ((current_price - prices[0]) / prices[0]) * 100
        change_1d = ((prices[-1] - prices[-2]) / prices[-2]) * 100
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'currency': 'USD',
            'company_name': company_names.get(symbol, f"{symbol} Corporation"),
            'history': hist,
            'change_30d': change_30d,
            'change_1d': change_1d,
            'volume': hist['Volume'].iloc[-1],
            'high_52w': max(prices) * 1.1,
            'low_52w': min(prices) * 0.9
        }

    @st.cache_data(ttl=300)
    def fetch_crypto_data(_self, crypto_id, days=30):
        """Fetch crypto data with caching"""
        try:
            # Get current price
            price_url = f"{_self.coingecko_url}/simple/price"
            price_params = {
                'ids': crypto_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true'
            }
            
            price_response = requests.get(price_url, params=price_params, headers=_self.headers)
            price_data = price_response.json()
            
            # Get historical data
            history_url = f"{_self.coingecko_url}/coins/{crypto_id}/market_chart"
            history_params = {'vs_currency': 'usd', 'days': days}
            
            history_response = requests.get(history_url, params=history_params, headers=_self.headers)
            history_data = history_response.json()
            
            prices = history_data['prices']
            dates = [datetime.fromtimestamp(price[0]/1000) for price in prices]
            price_values = [price[1] for price in prices]
            
            hist_df = pd.DataFrame({'Date': dates, 'Close': price_values}).set_index('Date')
            
            current_price = price_data[crypto_id]['usd']
            change_30d = ((current_price - price_values[0]) / price_values[0]) * 100
            
            return {
                'symbol': crypto_id.upper(),
                'current_price': current_price,
                'currency': 'USD',
                'history': hist_df,
                'change_30d': change_30d,
                '24h_change': price_data[crypto_id].get('usd_24h_change', 0),
                'market_cap': price_data[crypto_id].get('usd_market_cap', 0),
                'volume_24h': price_data[crypto_id].get('usd_24h_vol', 0)
            }
        except Exception as e:
            st.error(f"Error fetching crypto data: {e}")
            return None

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def fetch_news(_self, query, api_key=None):
        """Fetch news articles related to a query"""
        try:
            # If no API key, return mock data for demo
            if not api_key:
                return _self.generate_mock_news(query)
                
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': api_key,
                'pageSize': 5
            }
            
            response = requests.get(_self.news_api_url, params=params, headers=_self.headers)
            data = response.json()
            
            if data['status'] == 'ok':
                return data['articles']
            else:
                st.warning("News API limit reached. Using demo data.")
                return _self.generate_mock_news(query)
                
        except Exception as e:
            st.warning(f"Could not fetch news: {e}. Using demo data.")
            return _self.generate_mock_news(query)
    
    def generate_mock_news(_self, query):
        """Generate mock news data for demo purposes"""
        mock_titles = {
            'AAPL': [
                "Apple Announces New iPhone with Revolutionary Features",
                "Apple Stock Hits All-Time High Amid Strong Earnings",
                "Analysts Upgrade Apple Price Target to $250"
            ],
            'GOOGL': [
                "Google's AI Breakthrough Could Transform Search",
                "Alphabet Announces Stock Split Plan",
                "Google Cloud Continues Strong Growth Trajectory"
            ],
            'MSFT': [
                "Microsoft Azure Gains Market Share in Cloud Computing",
                "New Windows Update Addresses Security Vulnerabilities",
                "Microsoft Teams Adds New Collaboration Features"
            ],
            'bitcoin': [
                "Bitcoin Surges Past $60,000 Amid Institutional Adoption",
                "Regulatory Concerns Weigh on Cryptocurrency Markets",
                "El Salvador Adopts Bitcoin as Legal Tender"
            ],
            'ethereum': [
                "Ethereum 2.0 Upgrade Nears Completion",
                "NFT Market Continues to Drive Ethereum Demand",
                "Ethereum Foundation Announces Grants for Developers"
            ]
        }
        
        default_titles = [
            f"{query} Stock Shows Strong Performance in Q3",
            f"Analysts Bullish on {query} Despite Market Volatility",
            f"New Product Launch Could Boost {query} Revenue",
            f"{query} Expands into New Markets",
            f"CEO of {query} Company Announces Strategic Initiatives"
        ]
        
        titles = mock_titles.get(query, default_titles)
        
        articles = []
        for i, title in enumerate(titles[:5]):
            articles.append({
                'title': title,
                'url': f"https://example.com/news/{query.lower()}-{i}",
                'publishedAt': (datetime.now() - timedelta(days=i)).isoformat(),
                'source': {'name': 'Financial News'},
                'description': f"This is a demo description for {title}. In a real application, this would be fetched from NewsAPI."
            })
        
        return articles