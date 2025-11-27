import pandas as pd
import pandas_ta as ta

def calculate_indicators(data: list):
    """
    Calculate technical indicators for the given stock data.
    """
    if not data:
        return []

    df = pd.DataFrame(data)
    
    # Ensure numeric columns are float
    cols = ['open', 'high', 'low', 'close', 'volume']
    for col in cols:
        df[col] = df[col].astype(float)

    # 1. Moving Averages
    df['sma_5'] = ta.sma(df['close'], length=5)
    df['sma_10'] = ta.sma(df['close'], length=10)
    df['sma_20'] = ta.sma(df['close'], length=20)
    df['ema_12'] = ta.ema(df['close'], length=12)
    df['ema_26'] = ta.ema(df['close'], length=26)

    # 2. MACD
    macd = ta.macd(df['close'])
    if macd is not None:
        df = pd.concat([df, macd], axis=1)
        # Rename MACD columns for clarity if needed, pandas_ta usually names them MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        # Let's standardize column names
        df.rename(columns={
            'MACD_12_26_9': 'macd',
            'MACDh_12_26_9': 'macd_hist',
            'MACDs_12_26_9': 'macd_signal'
        }, inplace=True)

    # 3. RSI
    df['rsi'] = ta.rsi(df['close'], length=14)

    # 4. Bollinger Bands
    bb = ta.bbands(df['close'], length=20)
    if bb is not None:
        df = pd.concat([df, bb], axis=1)
        df.rename(columns={
            'BBL_20_2.0': 'bb_lower',
            'BBM_20_2.0': 'bb_middle',
            'BBU_20_2.0': 'bb_upper'
        }, inplace=True)

    # 5. Signals
    df['signal'] = 'NEUTRAL'
    
    # Simple Golden Cross / Death Cross (SMA 5 vs SMA 20)
    # We need to check the crossover. 
    # Since we are processing the whole history, we can just mark the state or specific crossover points.
    # For simplicity in this iteration, let's just mark the current trend based on the last row, 
    # but for the chart, we want the full history.
    
    # Let's add a signal column for specific events
    # 1 = Buy, -1 = Sell, 0 = Neutral
    
    # MACD Cross
    df['macd_cross'] = 0
    # Golden Cross: MACD crosses above Signal
    df.loc[(df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1)), 'macd_cross'] = 1
    # Death Cross: MACD crosses below Signal
    df.loc[(df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1)), 'macd_cross'] = -1

    # RSI Signals
    df['rsi_signal'] = 0
    df.loc[df['rsi'] < 30, 'rsi_signal'] = 1 # Oversold -> Buy
    df.loc[df['rsi'] > 70, 'rsi_signal'] = -1 # Overbought -> Sell

    # Fill NaN with None for JSON serialization
    # df = df.where(pd.notnull(df), None) # This can be flaky
    df = df.replace({np.nan: None})

    return df.to_dict(orient='records')

import numpy as np

def clean_value(val):
    """
    Convert NaN/Infinity to None for JSON serialization.
    """
    if isinstance(val, float):
        if np.isnan(val) or np.isinf(val):
            return None
    return val

def analyze_stock(symbol: str, data: list):
    """
    Perform comprehensive analysis and return a summary.
    """
    if not data:
        return {"error": "No data"}
    
    df = pd.DataFrame(data)
    # Assuming data already has indicators from calculate_indicators
    
    if df.empty:
        return {"error": "Empty data"}

    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    # Calculate change safely
    price = clean_value(last_row['close'])
    prev_close = clean_value(prev_row['close'])
    change = 0
    if price is not None and prev_close is not None:
        change = price - prev_close
    
    summary = {
        "symbol": symbol,
        "price": price,
        "change": change,
        "rsi": clean_value(last_row['rsi']),
        "macd": clean_value(last_row['macd']),
        "macd_signal": clean_value(last_row['macd_signal']),
        "recommendation": "HOLD",
        "signals": []
    }
    
    # Simple Logic for Recommendation
    score = 0
    
    rsi = summary['rsi']
    macd = summary['macd']
    macd_signal = summary['macd_signal']
    
    if rsi is not None:
        if rsi < 30:
            score += 2
            summary['signals'].append("RSI Oversold (Bullish)")
        elif rsi > 70:
            score -= 2
            summary['signals'].append("RSI Overbought (Bearish)")
            
    if macd is not None and macd_signal is not None:
        if macd > macd_signal:
            score += 1
            summary['signals'].append("MACD Bullish Trend")
        else:
            score -= 1
            summary['signals'].append("MACD Bearish Trend")
            
    # Check SMA 20
    sma_20 = clean_value(last_row.get('sma_20'))
    if price is not None and sma_20 is not None:
        if price > sma_20:
            score += 1
            summary['signals'].append("Price above SMA20")
        else:
            score -= 1
            summary['signals'].append("Price below SMA20")

    if score >= 2:
        summary['recommendation'] = "BUY"
    elif score <= -2:
        summary['recommendation'] = "SELL"
        
    return summary
