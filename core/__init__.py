"""
Core analysis modules for Investo
"""

from .lynch_analysis import lynch_metrics
from .graham_analysis import graham_metrics
from .data_sources import get_stock_package, get_top_volume_tickers, get_most_mentioned_tickers
from .finnhub_api import set_api_key as set_finnhub_api_key, get_company_news, get_global_news
from .reddit_sentiment import get_reddit_sentiment_summary
from .summarizer import summarize_stocks

__all__ = [
    'lynch_metrics',
    'graham_metrics', 
    'get_stock_package',
    'get_top_volume_tickers',
    'get_most_mentioned_tickers',
    'set_finnhub_api_key',
    'get_company_news',
    'get_global_news',
    'get_reddit_sentiment_summary',
    'summarize_stocks'
]
