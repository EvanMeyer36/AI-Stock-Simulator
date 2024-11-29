import openai
import os
import yfinance as yf

# Load API keys
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_market_overview(gainers):
    """
    Generate a comprehensive market overview for investment suggestions.
    
    Args:
        gainers (list): List of top gaining stock tickers
    
    Returns:
        dict: Detailed market data for each gainer and major indices
    """
    market_data = {}
    
    # Collect detailed information for top gainers
    for ticker in gainers:
        try:
            stock = yf.Ticker(ticker)
            market_data[ticker] = {
                'Current Price': stock.history(period="1d")['Close'].iloc[-1],
                'Company Name': stock.info.get('longName', 'N/A'),
                'Sector': stock.info.get('sector', 'N/A'),
                'Market Cap': stock.info.get('marketCap', 'N/A'),
                'PE Ratio': stock.info.get('trailingPE', 'N/A'),
                'Dividend Yield': stock.info.get('dividendYield', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching details for {ticker}: {e}")
    
    # Add major indices
    indices = {
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones',
        '^IXIC': 'Nasdaq'
    }
    
    for symbol, name in indices.items():
        try:
            index = yf.Ticker(symbol)
            market_data[name] = {
                'Current Price': index.history(period="1d")['Close'].iloc[-1],
                'Daily Change': index.info.get('regularMarketChangePercent', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching {name} data: {e}")
    
    return market_data

def suggest_investments(market_data, portfolio):
    """
    Generate AI-powered investment suggestions.
    
    Args:
        market_data (dict): Comprehensive market overview
        portfolio (dict): Current portfolio holdings and balance
    
    Returns:
        str: AI-generated investment recommendations
    """
    holdings = portfolio.get('holdings', {})
    balance = portfolio.get('balance', 0)

    # Format holdings into a readable string
    holdings_str = "\n".join(
        [f"{ticker}: {quantity}" for ticker, quantity in holdings.items()]
    ) if holdings else "No current holdings."

    # Format market data for the prompt
    market_overview_str = "Market Overview:\n"
    for key, data in market_data.items():
        market_overview_str += f"{key}:\n"
        for metric, value in data.items():
            market_overview_str += f"- {metric}: {value}\n"
        market_overview_str += "\n"

    prompt = f"""
    Current Portfolio:
    Balance: ${balance:.2f}
    Holdings:
    {holdings_str}

    {market_overview_str}

    Provide strategic investment recommendations:
    1. Evaluate potential buy/sell/hold decisions
    2. Consider portfolio diversification
    3. Highlight potential opportunities based on market trends
    4. Provide concise rationale for each recommendation
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a sophisticated financial advisor AI analyzing market data and portfolio composition."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating investment suggestions: {e}"