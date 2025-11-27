from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://frontend-lflkxhdn7-linyds-projects.vercel.app"  # 替换为您的 Vercel域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Stock Analysis API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from services.stock_service import fetch_stock_data, get_stock_info
from services.analysis_service import calculate_indicators, analyze_stock

@app.get("/api/stock/{symbol}")
def get_stock_history(symbol: str, period: str = "2y", interval: str = "1d"):
    raw_data = fetch_stock_data(symbol, period, interval)
    analyzed_data = calculate_indicators(raw_data)
    return {"symbol": symbol, "data": analyzed_data}

@app.get("/api/stock/{symbol}/analyze")
def get_stock_analysis(symbol: str):
    # Get enough data for indicators
    raw_data = fetch_stock_data(symbol, period="6mo", interval="1d")
    analyzed_data = calculate_indicators(raw_data)
    summary = analyze_stock(symbol, analyzed_data)
    return summary

@app.get("/api/stock/{symbol}/info")
def get_stock_details(symbol: str):
    info = get_stock_info(symbol)
    return {"symbol": symbol, "info": info}

@app.get("/api/scanner")
def scan_market():
    # Expanded list: US tech stocks + HK stocks + A-shares
    symbols = [
        # US Tech
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD',
        # Hong Kong Stocks
        '0700.HK',   # Tencent
        '9988.HK',   # Alibaba
        '3690.HK',   # Meituan
        '1810.HK',   # Xiaomi
        '9618.HK',   # JD.com
        '1211.HK',   # BYD (HK)
        '2318.HK',   # Ping An Insurance
        # A-shares (Shanghai)
        '600519.SS', # Kweichow Moutai
        '600036.SS', # China Merchants Bank
        '601318.SS', # Ping An Insurance (A)
        # A-shares (Shenzhen)
        '000858.SZ', # Wuliangye
        '002594.SZ', # BYD (A)
        '300750.SZ', # CATL (Ningde Shidai)
    ]
    results = []
    
    for symbol in symbols:
        try:
            # Fetch less data for speed
            raw_data = fetch_stock_data(symbol, period="6mo", interval="1d")
            if not raw_data:
                continue
            analyzed_data = calculate_indicators(raw_data)
            summary = analyze_stock(symbol, analyzed_data)
            
            if summary['recommendation'] == 'BUY':
                results.append(summary)
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")
            continue
            
    return {"results": results}
