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

def get_yahoo_news(symbol, max_items=10):
    """Get latest news from Yahoo Finance for a stock"""
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        
        if not news or len(news) == 0:
            print(f"No Yahoo Finance news found for {symbol}")
            return []
        
        formatted_news = []
        for item in news[:max_items]:
            try:
                # News items now have 'content' key with nested data
                if 'content' in item and item['content']:
                    content = item['content']
                    
                    # Extract data from content
                    title = content.get('title', 'No title available')
                    
                    # Try different URL keys
                    link = content.get('clickThroughUrl', {}).get('url', '') if content.get('clickThroughUrl') else ''
                    if not link:
                        link = content.get('canonicalUrl', {}).get('url', '#') if content.get('canonicalUrl') else '#'
                    
                    # Get provider info
                    provider = content.get('provider', {})
                    publisher = provider.get('displayName', 'Unknown') if provider else 'Unknown'
                    
                    # Handle timestamp
                    timestamp = content.get('pubDate', 0)
                    if timestamp:
                        try:
                            publish_time = datetime.fromtimestamp(timestamp).strftime('%B %d, %Y at %I:%M %p')
                        except:
                            publish_time = 'Recently'
                    else:
                        publish_time = 'Recently'
                    
                    news_item = {
                        'title': title,
                        'link': link,
                        'publisher': publisher,
                        'publish_time': publish_time,
                        'source': 'Yahoo Finance',
                        'timestamp': timestamp  # For sorting
                    }
                    formatted_news.append(news_item)
            except Exception as e:
                print(f"Error processing Yahoo news item: {e}")
                continue
        
        print(f"Successfully fetched {len(formatted_news)} Yahoo Finance news items for {symbol}")
        return formatted_news
        
    except Exception as e:
        print(f"Error fetching Yahoo news for {symbol}: {e}")
        return []

def get_finnhub_news(symbol, max_items=10):
    """Get latest news from Finnhub for a stock"""
    try:
        end = datetime.now().date()
        start = end - timedelta(days=30)  # Get news from last 30 days
        
        news_data = finnhub_get("company-news", {
            "symbol": symbol, 
            "from": str(start), 
            "to": str(end)
        })
        
        if not news_data:
            print(f"No Finnhub news found for {symbol}")
            return []
        
        formatted_news = []
        for item in sorted(news_data, key=lambda x: x.get("datetime", 0), reverse=True)[:max_items]:
            title = item.get('headline', 'No title available')
            link = item.get('url', '#')
            publisher = item.get('source', 'Unknown')
            timestamp = item.get('datetime', 0)
            
            if timestamp:
                try:
                    publish_time = datetime.fromtimestamp(timestamp).strftime('%B %d, %Y at %I:%M %p')
                except:
                    publish_time = 'Recently'
            else:
                publish_time = 'Recently'
            
            news_item = {
                'title': title,
                'link': link,
                'publisher': publisher,
                'publish_time': publish_time,
                'source': 'Finnhub',
                'timestamp': timestamp
            }
            formatted_news.append(news_item)
        
        print(f"Successfully fetched {len(formatted_news)} Finnhub news items for {symbol}")
        return formatted_news
        
    except Exception as e:
        print(f"Error fetching Finnhub news for {symbol}: {e}")
        return []

def get_tradingview_news(symbol, max_items=10):
    """
    Get news from TradingView-compatible sources
    Note: TradingView doesn't have a public API, so we'll use alternative news sources
    """
    # TradingView doesn't have a public news API
    # This is a placeholder for future implementation
    print(f"TradingView news API not available (no public API)")
    return []

def get_aggregated_news(symbol, max_items=3):
    """
    Aggregate news from multiple sources, remove duplicates, and return top 3 latest
    """
    print(f"Fetching aggregated news for {symbol} from multiple sources...")
    
    all_news = []
    
    # Fetch from all sources
    yahoo_news = get_yahoo_news(symbol, max_items=10)
    finnhub_news = get_finnhub_news(symbol, max_items=10)
    tradingview_news = get_tradingview_news(symbol, max_items=10)
    
    # Combine all news
    all_news.extend(yahoo_news)
    all_news.extend(finnhub_news)
    all_news.extend(tradingview_news)
    
    if not all_news:
        print(f"No news found from any source for {symbol}")
        return []
    
    # Remove duplicates based on similar titles
    unique_news = []
    seen_titles = set()
    
    # Sort by timestamp (most recent first)
    all_news.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    
    for news_item in all_news:
        title = news_item['title'].lower().strip()
        
        # Create a simplified version of the title for comparison
        # Remove common words and punctuation
        title_words = set(title.split())
        
        # Check if this title is too similar to any existing title
        is_duplicate = False
        for seen_title in seen_titles:
            seen_words = set(seen_title.split())
            # If more than 70% of words match, consider it a duplicate
            common_words = title_words & seen_words
            if len(common_words) > 0 and len(common_words) / max(len(title_words), len(seen_words)) > 0.7:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_news.append(news_item)
            seen_titles.add(title)
            
            if len(unique_news) >= max_items:
                break
    
    print(f"Aggregated {len(unique_news)} unique news items from {len(all_news)} total articles")
    return unique_news

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
    This function is deprecated - use charts.chart_data.get_chart_data() instead.
    """
    from charts.chart_data import get_chart_data
    return get_chart_data(symbol, period)

def get_stock_package(symbol):
    """Get complete stock data package including fundamentals, news, and sentiment"""
    from charts.chart_data import get_chart_data
    d = get_full_stock_data(symbol)
    d["news"] = get_company_news(symbol)  # Keep old Finnhub news for compatibility
    d["yahoo_news"] = get_aggregated_news(symbol, max_items=3)  # Aggregated news from all sources
    d["crowd"] = get_crowd_sentiment(symbol)
    d["chart_data"] = get_chart_data(symbol, "1y")  # Default to 1 year
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
