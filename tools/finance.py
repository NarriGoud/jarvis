import yfinance as yf

def get_market_data(symbol: str):
    """Fetches real-time stock price and market info."""
    try:
        # Normalize symbol (e.g., Apple -> AAPL, Tata Motors -> TATAMOTORS.NS)
        ticker_symbol = symbol.upper()
        if not ticker_symbol.endswith((".NS", ".BO")) and symbol.lower() not in ["aapl", "msft", "goog"]:
            # Logic to help the LLM with Indian suffixes if it forgets
            ticker_symbol += ".NS" 
            
        ticker = yf.Ticker(ticker_symbol)
        # Use fast_info for ultra-quick real-time price retrieval
        info = ticker.fast_info
        
        return {
            "symbol": ticker_symbol,
            "price": round(info['last_price'], 2),
            "currency": info['currency'],
            "market_cap": round(info['market_cap'] / 1e9, 2), # In Billions
            "day_high": round(info['day_high'], 2)
        }
    except Exception as e:
        return {"error": f"Could not find data for {symbol}. Error: {str(e)}"}