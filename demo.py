#!/usr/bin/env python3
"""
Example script demonstrating Investo's new structure
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.data_sources import get_stock_package
from core.lynch_analysis import lynch_metrics
from core.graham_analysis import graham_metrics
from core.summarizer import summarize_stocks
from utils.helpers import clean_tickers

def demo_analysis(symbol):
    """Demonstrate analysis capabilities"""
    print(f"🔍 Analyzing {symbol}...")
    
    # Get stock data package
    data = get_stock_package(symbol)
    
    if not data.get('shortName'):
        print(f"❌ Could not fetch data for {symbol}")
        return
    
    print(f"📊 Company: {data['shortName']}")
    print(f"💰 Price: ${data.get('price', 'N/A')}")
    print(f"🏢 Sector: {data.get('sector', 'N/A')}")
    
    # Lynch Analysis
    print("\n📈 Peter Lynch Analysis:")
    lynch_results = lynch_metrics(data)
    print(f"   P/E Ratio: {lynch_results.get('P/E', 'N/A')}")
    print(f"   PEG Ratio: {lynch_results.get('PEG', 'N/A')}")
    print(f"   ROE: {lynch_results.get('ROE_%', 'N/A')}%")
    
    # Graham Analysis
    print("\n📉 Benjamin Graham Analysis:")
    graham_results = graham_metrics(data)
    print(f"   P/E Ratio: {graham_results.get('P/E', 'N/A')}")
    print(f"   P/B Ratio: {graham_results.get('P/B', 'N/A')}")
    print(f"   Margin of Safety: {graham_results.get('Margin_of_Safety_%', 'N/A')}%")
    
    # AI Summary
    print("\n🤖 AI Summary:")
    summary = summarize_stocks([data], f"Analysis for {symbol}", mode="ticker")
    print(summary)

def main():
    """Main demo function"""
    print("🚀 Investo Demo - New Structure")
    print("=" * 40)
    
    # Demo with popular stocks
    symbols = ["AAPL", "TSLA", "MSFT"]
    
    for symbol in symbols:
        try:
            demo_analysis(symbol)
            print("\n" + "=" * 40)
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            print("\n" + "=" * 40)

if __name__ == "__main__":
    main()
