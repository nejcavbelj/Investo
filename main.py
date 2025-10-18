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
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    set_api_key(config['FINNHUB_API_KEY'])

    # Interactive ticker input
    print("\nWelcome to Investo - Smart Stock Analysis")
    print("Enter any stock ticker to receive an instant, comprehensive analysis")
    print("powered by advanced algorithms.\n")
    
    while True:
        symbol = input("Enter stock ticker symbol (e.g., TSLA, AAPL, MSFT): ").upper().strip()
        
        if not symbol:
            print("Please enter a valid ticker symbol.")
            continue
            
        if len(symbol) > 10:  # Basic validation
            print("Ticker symbol seems too long. Please enter a valid ticker (e.g., TSLA, AAPL).")
            continue
            
        print(f"\nAnalyzing {symbol}...")
        print("This may take a few moments as we gather comprehensive data...")
        
        # Generate combined report
        report_path = create_combined_report(symbol)
        
        if report_path:
            print(f"\nAnalysis complete! Report saved to: {report_path}")
            print("The report includes:")
            print("   - Benjamin Graham value analysis")
            print("   - Peter Lynch growth analysis") 
            print("   - Reddit sentiment analysis")
            print("   - Combined investment verdict")
            print("\nReport opened in your default browser")
            
            # Ask if user wants to analyze another stock
            another = input("\nWould you like to analyze another stock? (y/n): ").lower().strip()
            if another in ['y', 'yes']:
                print("\n" + "="*50)
                continue
            else:
                print("\nThank you for using Investo! Goodbye!")
                break
        else:
            print("Failed to generate report. Please check the ticker symbol and try again.")
            
            retry = input("Would you like to try another ticker? (y/n): ").lower().strip()
            if retry in ['y', 'yes']:
                continue
            else:
                print("Goodbye!")
                break

if __name__ == "__main__":
    main()
