import yfinance as yf
import requests
import pandas as pd
from io import StringIO

def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        return current_price
    except Exception as e:
        print(f"Error fetching price for {ticker}: {e}")
        return None

def get_top_gainers():
    url = "https://finance.yahoo.com/gainers"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Use StringIO to wrap the response text
        df = pd.read_html(StringIO(response.text))[0]
        
        top_gainers = df['Symbol'].head(5).tolist()
        return top_gainers
    
    except Exception as e:
        print(f"Error scraping top gainers: {e}")
        return []

def analyze_top_gainers():
    top_gainers = get_top_gainers()
    
    gainers_info = []
    for ticker in top_gainers:
        price = get_stock_price(ticker)
        if price:
            stock = yf.Ticker(ticker)
            info = {
                'Ticker': ticker,
                'Current Price': price,
                'Company Name': stock.info.get('longName', 'N/A'),
                'Percent Change': stock.info.get('regularMarketChangePercent', 0)
            }
            gainers_info.append(info)
    
    return gainers_info