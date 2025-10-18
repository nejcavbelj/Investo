"""
Investo - Investment Analysis Bot
===============================
Entry point for the Investo investment analysis system.
Generates combined reports with Graham, Lynch, and Reddit analyses.
"""

from config import load_config, startup_warnings
from core.finnhub_api import set_api_key
from reports.combined_report_generator import create_combined_report

def main():
    """Main entry point for Investo"""
    print("Starting Investo Combined Analysis System...")
    
    # Load configuration
    config = load_config()
    set_api_key(config['FINNHUB_API_KEY'])

    # Use TSLA as test ticker (the one that was causing issues)
    symbol = "TSLA"
    print(f"Using test ticker: {symbol}")
    
    print(f"\nGenerating combined analysis report for {symbol}...")
    
    # Generate combined report
    report_path = create_combined_report(symbol)
    
    if report_path:
        print(f"\nAnalysis complete! Report saved to: {report_path}")
        print("The report includes:")
        print("   • Benjamin Graham value analysis")
        print("   • Peter Lynch growth analysis") 
        print("   • Reddit sentiment analysis")
        print("   • Combined investment verdict")
        print("\nReport opened in your default browser")
        print("\nTo analyze other stocks, use: python interactive_main.py")
    else:
        print("Failed to generate report")

if __name__ == "__main__":
    main()
