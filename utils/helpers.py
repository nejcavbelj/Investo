"""
Ticker validation and cleaning utilities
"""

import re

def is_valid_ticker(ticker: str) -> bool:
    """Check if a ticker symbol is valid"""
    return bool(re.fullmatch(r"[A-Z]{1,5}", ticker)) and ticker not in {"CEO", "ETF", "US", "I"}

def clean_tickers(tickers):
    """Filter list of tickers to only include valid ones"""
    return [t for t in tickers if is_valid_ticker(t)]

def normalize_ticker(ticker: str) -> str:
    """Normalize ticker symbol to uppercase"""
    return ticker.upper().strip() if ticker else ""

def validate_ticker_list(tickers):
    """Validate a list of tickers and return valid ones with errors"""
    valid_tickers = []
    invalid_tickers = []
    
    for ticker in tickers:
        normalized = normalize_ticker(ticker)
        if is_valid_ticker(normalized):
            valid_tickers.append(normalized)
        else:
            invalid_tickers.append(ticker)
    
    return valid_tickers, invalid_tickers
