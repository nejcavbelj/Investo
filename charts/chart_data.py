"""
Chart Data Module
================
Handles fetching and processing stock chart data from various APIs.
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def get_chart_data(symbol: str, period: str = "1y") -> Optional[Dict]:
    """
    Get historical stock price data for charting.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL')
        period (str): Period for historical data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        dict: Chart data with dates, prices, volumes, highs, and lows
        None: If data cannot be fetched
    """
    try:
        print(f"Fetching chart data for {symbol} (period: {period})...")
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            print(f"No historical data found for {symbol}")
            return None
            
        # Convert to lists for Chart.js
        dates = [date.strftime('%Y-%m-%d') for date in hist.index]
        prices = [round(float(price), 2) for price in hist['Close']]
        volumes = [int(volume) for volume in hist['Volume']]
        highs = [round(float(high), 2) for high in hist['High']]
        lows = [round(float(low), 2) for low in hist['Low']]
        
        # Calculate some basic statistics
        price_change = prices[-1] - prices[0] if len(prices) > 1 else 0
        price_change_pct = (price_change / prices[0] * 100) if prices[0] != 0 else 0
        
        chart_data = {
            'dates': dates,
            'prices': prices,
            'volumes': volumes,
            'highs': highs,
            'lows': lows,
            'period': period,
            'symbol': symbol,
            'price_change': round(price_change, 2),
            'price_change_pct': round(price_change_pct, 2),
            'current_price': prices[-1] if prices else None,
            'data_points': len(prices)
        }
        
        print(f"Successfully fetched {len(prices)} data points for {symbol}")
        return chart_data
        
    except Exception as e:
        print(f"Error fetching chart data for {symbol}: {e}")
        return None

def get_multiple_periods_data(symbol: str) -> Dict[str, Optional[Dict]]:
    """
    Get chart data for multiple periods.
    
    Args:
        symbol (str): Stock symbol
        
    Returns:
        dict: Chart data for different periods
    """
    periods = ['1mo', '3mo', '6mo', '1y', '2y', '5y']
    data = {}
    
    for period in periods:
        data[period] = get_chart_data(symbol, period)
        
    return data

def validate_chart_data(chart_data: Dict) -> bool:
    """
    Validate that chart data has all required fields.
    
    Args:
        chart_data (dict): Chart data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['dates', 'prices', 'volumes', 'highs', 'lows', 'symbol']
    
    if not chart_data:
        return False
        
    for field in required_fields:
        if field not in chart_data or not chart_data[field]:
            return False
            
    return len(chart_data['dates']) == len(chart_data['prices'])
