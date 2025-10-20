"""
Data sources module - Aggregates data from multiple APIs
-------------------------------------------------------
Combines Yahoo Finance, Finnhub, StockTwits, and Reddit APIs
to provide comprehensive stock data for analysis.
"""

import yfinance as yf
import requests
from datetime import datetime, timedelta
from config.settings import HTTP_TIMEOUT, MAX_NEWS_ITEMS, MAX_GLOBAL_NEWS, MAX_SENTIMENT_ITEMS

# Global API key storage
FINNHUB_API_KEY = None

def set_finnhub_api_key(key):
    """Set the Finnhub API key"""
    global FINNHUB_API_KEY
    FINNHUB_API_KEY = key

def finnhub_get(path, params):
    """Make a request to Finnhub API"""
    if not FINNHUB_API_KEY:
        return None
    try:
        url = f"https://finnhub.io/api/v1/{path}"
        p = dict(params or {})
        p["token"] = FINNHUB_API_KEY
        r = requests.get(url, params=p, timeout=HTTP_TIMEOUT)
        if r.ok:
            return r.json()
    except Exception:
        return None
    return None

def get_full_stock_data(symbol: str) -> dict:
    """
    Fetch all relevant stock data for a given symbol using yfinance.
    Returns a dictionary with fields required for fundamental analysis models.
    """
    data = {
        "symbol": symbol,
        "price": None,
        "shortName": None,
        "summary": None,
        "marketCap": None,
        "pe": None,            # trailingPE or forwardPE
        "forwardPE": None,
        "trailingPE": None,
        "eps": None,
        "epsForward": None,
        "epsTrailing": None,
        "epsGrowth": None,       # earningsQuarterlyGrowth
        "peg": None,
        "dividendYield": None,
        "volume": None,
        "avgVolume": None,
        "fiftyTwoWeekHigh": None,
        "fiftyTwoWeekLow": None,
        "debtToEquity": None,
        "currentRatio": None,
        "quickRatio": None,
        "roe": None,              # returnOnEquity
        "roa": None,              # returnOnAssets
        "profitMargin": None,
        "priceToBook": None,
        "priceToSales": None,
        "sector": None,
        "industry": None,
        "yahooUrl": f"https://finance.yahoo.com/quote/{symbol}",

        # Lynch extensions:
        "totalCash": None,
        "totalAssets": None,
        "totalCurrentAssets": None,
        "totalCurrentLiabilities": None,
        "inventory": None,
        "inventoryGrowth": None,      # Not available directly
        "salesGrowth": None,
        "revenueGrowth": None,
        "sharesPercentInsiders": None,
        "heldPercentInsiders": None,
        "earningsStdDev": None,       # Not available directly
        "freeCashflow": None,
        "fcfYield": None,

        # Graham Net-Net fields:
        "totalLiabilities": None
    }
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Basic Info
        data["shortName"] = info.get("shortName")
        data["summary"] = (info.get("longBusinessSummary") or "")[:400]
        data["price"] = info.get("currentPrice") or info.get("regularMarketPrice")
        data["marketCap"] = info.get("marketCap")

        # Earnings & Ratios
        data["pe"] = info.get("trailingPE") or info.get("forwardPE")
        data["forwardPE"] = info.get("forwardPE")
        data["trailingPE"] = info.get("trailingPE")
        data["eps"] = info.get("trailingEps") or info.get("forwardEps")
        data["epsTrailing"] = info.get("trailingEps")
        data["epsForward"] = info.get("forwardEps")
        data["epsGrowth"] = info.get("earningsQuarterlyGrowth")
        if data["pe"] and data["epsGrowth"] and data["epsGrowth"] > 0:
            data["peg"] = data["pe"] / (data["epsGrowth"] * 100 if data["epsGrowth"] < 10 else data["epsGrowth"])
        else:
            data["peg"] = None

        # Dividend
        data["dividendYield"] = (info.get("dividendYield") or 0) * 100 if info.get("dividendYield") else None

        # Volumes & Price Ranges
        data["volume"] = info.get("volume")
        data["avgVolume"] = info.get("averageVolume")
        data["fiftyTwoWeekHigh"] = info.get("fiftyTwoWeekHigh")
        data["fiftyTwoWeekLow"] = info.get("fiftyTwoWeekLow")

        # Balance Sheet & Profitability
        data["debtToEquity"] = info.get("debtToEquity")
        data["currentRatio"] = info.get("currentRatio")
        data["quickRatio"] = info.get("quickRatio")
        data["roe"] = (info.get("returnOnEquity") or 0) * 100 if info.get("returnOnEquity") else None
        data["roa"] = (info.get("returnOnAssets") or 0) * 100 if info.get("returnOnAssets") else None
        data["profitMargin"] = (info.get("profitMargins") or 0) * 100 if info.get("profitMargins") else None
        data["priceToBook"] = info.get("priceToBook")
        data["priceToSales"] = info.get("priceToSalesTrailing12Months") or info.get("priceToSales")

        # Sector/Industry
        data["sector"] = info.get("sector")
        data["industry"] = info.get("industry")

        # Lynch-specific fields
        data["totalCash"] = info.get("totalCash")
        data["totalAssets"] = info.get("totalAssets")
        data["totalCurrentAssets"] = info.get("totalCurrentAssets")
        data["totalCurrentLiabilities"] = info.get("totalCurrentLiabilities")
        data["inventory"] = info.get("inventory")
        # inventoryGrowth: Not directly available, requires custom calculation from fundamental data
        data["salesGrowth"] = info.get("salesGrowth") or info.get("revenueGrowth")
        data["revenueGrowth"] = info.get("revenueGrowth")
        data["sharesPercentInsiders"] = info.get("sharesPercentInsiders")
        data["heldPercentInsiders"] = info.get("heldPercentInsiders")
        # earningsStdDev: Not available directly
        data["freeCashflow"] = info.get("freeCashflow")
        data["fcfYield"] = (info.get("freeCashflow") / info.get("marketCap") * 100) if info.get("freeCashflow") and info.get("marketCap") else None

        # --- Graham Net-Net fields ---
        # Try to get from balance sheet if not in info
        if not data["totalCurrentAssets"] or not data["totalCurrentLiabilities"] or not data["totalLiabilities"]:
            try:
                balance = ticker.balance_sheet
                # Use the most recent column (0)
                data["totalCurrentAssets"] = balance.loc["Total Current Assets"][0] if "Total Current Assets" in balance.index else data["totalCurrentAssets"]
                data["totalCurrentLiabilities"] = balance.loc["Total Current Liabilities"][0] if "Total Current Liabilities" in balance.index else data["totalCurrentLiabilities"]
                data["totalLiabilities"] = balance.loc["Total Liabilities"][0] if "Total Liabilities" in balance.index else data["totalLiabilities"]
            except Exception as e:
                print(f"Error fetching net-net balance sheet for {symbol}: {e}")

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

    return data

def get_company_news(symbol, days=7, max_items=MAX_NEWS_ITEMS):
    """Get company-specific news from Finnhub"""
    end = datetime.now().date()
    start = end - timedelta(days=days)
    js = finnhub_get("company-news", {"symbol": symbol, "from": str(start), "to": str(end)})
    if not js: return []
    seen = set()
    out = []
    for item in sorted(js, key=lambda x: x.get("datetime", 0), reverse=True):
        h = item.get("headline", "").strip()
        if not h or h in seen: continue
        seen.add(h)
        out.append(h[:150])
        if len(out) >= max_items: break
    return out

def get_global_news(max_items=MAX_GLOBAL_NEWS):
    """Get global market news from Finnhub"""
    js = finnhub_get("news", {"category": "general"})
    if not js: return []
    seen, out = set(), []
    for item in js:
        h = item.get("headline", "").strip()
        if not h or h in seen: continue
        seen.add(h)
        out.append(h[:150])
        if len(out) >= max_items: break
    return out

def get_crowd_sentiment(symbol, max_items=MAX_SENTIMENT_ITEMS):
    """Get crowd sentiment from StockTwits"""
    try:
        url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
        r = requests.get(url, timeout=HTTP_TIMEOUT)
        if not r.ok: return {"mentions": 0, "bull": 0, "bear": 0}
        msgs = r.json().get("messages", [])[:max_items]
        bull = bear = 0
        for m in msgs:
            s = (m.get("entities") or {}).get("sentiment") or {}
            if s.get("basic") == "Bullish": bull += 1
            if s.get("basic") == "Bearish": bear += 1
        return {"mentions": len(msgs), "bull": bull, "bear": bear}
    except Exception:
        return {"mentions": 0, "bull": 0, "bear": 0}

def get_historical_data(symbol, period="1y"):
    """
    Get historical stock price data for charting.
    
    Args:
        symbol (str): Stock symbol
        period (str): Period for historical data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        dict: Chart data with dates, prices, and volumes
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
            
        # Convert to lists for Chart.js
        dates = [date.strftime('%Y-%m-%d') for date in hist.index]
        prices = [round(float(price), 2) for price in hist['Close']]
        volumes = [int(volume) for volume in hist['Volume']]
        highs = [round(float(high), 2) for high in hist['High']]
        lows = [round(float(low), 2) for low in hist['Low']]
        
        return {
            'dates': dates,
            'prices': prices,
            'volumes': volumes,
            'highs': highs,
            'lows': lows,
            'period': period
        }
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return None

def get_stock_package(symbol):
    """Get complete stock data package including fundamentals, news, and sentiment"""
    d = get_full_stock_data(symbol)
    d["news"] = get_company_news(symbol)
    d["crowd"] = get_crowd_sentiment(symbol)
    d["chart_data"] = get_historical_data(symbol, "1y")  # Default to 1 year
    return d

def get_top_volume_tickers(n=10):
    """Get top volume tickers from Yahoo Finance"""
    try:
        tickers = yf.Tickers("^GSPC ^DJI ^IXIC")
        # This is a simplified implementation - in practice you'd want to get actual top volume data
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "AMD", "INTC"][:n]
    except Exception:
        return []

def get_most_mentioned_tickers(n=10):
    """Get most mentioned tickers - simplified implementation"""
    # In practice, this would analyze social media mentions
    return ["TSLA", "AAPL", "NVDA", "AMZN", "MSFT", "GOOGL", "META", "AMD", "NFLX", "INTC"][:n]
