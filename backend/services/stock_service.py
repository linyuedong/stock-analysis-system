import yfinance as yf
import pandas as pd
import json

def fetch_stock_data(symbol: str, period: str = "2y", interval: str = "1d"):
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        symbol (str): Stock ticker symbol (e.g., "AAPL", "NVDA").
        period (str): Data period to download (e.g., "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max").
        interval (str): Data interval (e.g., "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo").
        
    Returns:
        list: List of dictionaries containing stock data.
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return []
        
        # Reset index to make Date a column
        df.reset_index(inplace=True)
        
        # Rename columns to lowercase for consistency
        df.columns = [c.lower() for c in df.columns]
        
        # Convert Date to string (YYYY-MM-DD)
        if 'date' in df.columns:
            df['time'] = df['date'].dt.strftime('%Y-%m-%d')
        elif 'datetime' in df.columns: # For intraday data
             df['time'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Select relevant columns
        result_df = df[['time', 'open', 'high', 'low', 'close', 'volume']]
        
        # Convert to list of dicts
        data = result_df.to_dict(orient='records')
        
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return []

def get_stock_info(symbol: str):
    """
    Get basic stock info.
    """
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {e}")
        return {}
