"""
Test script to verify the fixed report generator works
"""

from config import load_config, startup_warnings
from core.finnhub_api import set_api_key
from reports.combined_report_generator import create_combined_report

def test_report_generation():
    """Test the report generation with TSLA"""
    print("Testing Investo Combined Analysis System...")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    set_api_key(config['FINNHUB_API_KEY'])

    # Test with TSLA (the ticker that caused the error)
    symbol = "TSLA"
    print(f"Testing with {symbol}...")
    
    try:
        report_path = create_combined_report(symbol)
        
        if report_path:
            print(f"\nSUCCESS! Report generated: {report_path}")
            print("The report includes:")
            print("   • Benjamin Graham value analysis")
            print("   • Peter Lynch growth analysis") 
            print("   • Reddit sentiment analysis")
            print("   • Combined investment verdict")
            print("\nReport opened in your default browser")
            return True
        else:
            print("FAILED: Could not generate report")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_report_generation()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
