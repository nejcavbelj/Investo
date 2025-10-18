"""
Investo - Interactive Report Generator
=====================================
Interactive version that allows users to input their own ticker symbols.
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

    # Safety counter to prevent infinite reports
    reports_generated = 0
    max_reports = 5  # Maximum reports per session
    
    while True:
        print("\nOptions:")
        print("1. Analyze a stock (enter ticker symbol)")
        print("2. Analyze AAPL (example)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            if reports_generated >= max_reports:
                print(f"\nMaximum reports per session reached ({max_reports}). Please restart the program.")
                break
                
            symbol = input("Enter stock symbol (e.g., AAPL, MSFT, GOOGL): ").upper().strip()
            if symbol:
                print(f"\nGenerating combined analysis report for {symbol}...")
                report_path = create_combined_report(symbol)
                
                if report_path:
                    reports_generated += 1
                    print(f"\nAnalysis complete! Report saved to: {report_path}")
                    print("The report includes:")
                    print("   • Benjamin Graham value analysis")
                    print("   • Peter Lynch growth analysis") 
                    print("   • Reddit sentiment analysis")
                    print("   • Combined investment verdict")
                    print("\nReport opened in your default browser")
                    print(f"Reports generated this session: {reports_generated}/{max_reports}")
                else:
                    print("Failed to generate report")
            else:
                print("Please enter a valid ticker symbol")
                
        elif choice == "2":
            if reports_generated >= max_reports:
                print(f"\nMaximum reports per session reached ({max_reports}). Please restart the program.")
                break
                
            symbol = "AAPL"
            print(f"\nGenerating combined analysis report for {symbol}...")
            report_path = create_combined_report(symbol)
            
            if report_path:
                reports_generated += 1
                print(f"\nAnalysis complete! Report saved to: {report_path}")
                print("The report includes:")
                print("   • Benjamin Graham value analysis")
                print("   • Peter Lynch growth analysis") 
                print("   • Reddit sentiment analysis")
                print("   • Combined investment verdict")
                print("\nReport opened in your default browser")
                print(f"Reports generated this session: {reports_generated}/{max_reports}")
            else:
                print("Failed to generate report")
                
        elif choice == "3":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
