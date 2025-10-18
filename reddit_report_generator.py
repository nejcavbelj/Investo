"""
Reddit Sentiment Report Generator
===============================
Generates standalone Reddit sentiment reports like the one shown in the image.
"""

from config import load_config, startup_warnings
from core.finnhub_api import set_api_key
from core.reddit_sentiment import get_reddit_sentiment_summary, render_html_report

def main():
    """Generate Reddit sentiment report"""
    print("Reddit Sentiment Report Generator")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    set_api_key(config['FINNHUB_API_KEY'])

    # Use TSLA as example
    symbol = "TSLA"
    print(f"Generating Reddit sentiment report for {symbol}...")
    
    try:
        # Get Reddit sentiment data
        reddit_data = get_reddit_sentiment_summary(symbol)
        
        # Generate detailed HTML report
        render_html_report(reddit_data)
        
        print(f"\nReddit sentiment report generated successfully!")
        print("The report includes:")
        print("   • Comprehensive sentiment metrics")
        print("   • Visual charts (donut charts, buzz meter)")
        print("   • Subreddit weight analysis")
        print("   • Top Reddit posts with links")
        print("   • Reliability and confidence scores")
        print("\nReport opened in your default browser")
        
    except Exception as e:
        print(f"Error generating Reddit report: {e}")

if __name__ == "__main__":
    main()
