"""
Combined Report Generator
========================
Generates comprehensive HTML reports combining Graham, Lynch, and Reddit analyses.
"""

import os
import webbrowser
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from config.settings import PROJECT_ROOT

from core.data_sources import get_stock_package
from core.graham_analysis import graham_metrics
from core.lynch_analysis import lynch_metrics
from core.reddit_sentiment import get_reddit_sentiment_summary
from reports.report_builder import get_graham_interpretation, get_lynch_interpretation, generate_graham_summary, generate_lynch_summary

def get_graham_criteria(metric):
    """Get Graham criteria for a metric"""
    criteria = {
        'P/E': 'Should be < 15',
        'P/B': 'Should be < 1.5',
        'Debt/Equity': 'Should be < 0.5',
        'Current_Ratio': 'Should be > 2.0',
        'Dividend_Record_Years': 'Should be ≥ 20',
        'Earnings_Stability_10Y': 'Should be True',
        'Margin_of_Safety_%': 'Should be > 30%',
        'NetNet_Buy_Candidate': 'Should be True for deep value'
    }
    return criteria.get(metric, 'See analysis')

def get_lynch_criteria(metric):
    """Get Lynch criteria for a metric"""
    criteria = {
        'P/E': 'Good if < 15, concerning if > 25',
        'PEG': 'Ideal around 1.0, < 0.5 is very attractive',
        'EPS_Growth_%': 'Higher growth is better, > 15% is excellent',
        'ROE_%': '> 15% is good, > 20% is excellent',
        'Debt/Equity': 'Lower is better, < 0.5 is conservative',
        'Current_Ratio': '> 2.0 indicates good liquidity',
        'Price/Book': 'Lower is better for value, < 1.5 is attractive',
        'Price/Sales': 'Lower is better, < 1.0 is very attractive'
    }
    return criteria.get(metric, 'See analysis')

def check_graham_criteria(metric, value):
    """Check if a metric meets Graham criteria"""
    if value is None:
        return False
    
    checks = {
        'P/E': lambda v: v < 15,
        'P/B': lambda v: v < 1.5,
        'Debt/Equity': lambda v: v < 0.5,
        'Current_Ratio': lambda v: v > 2.0,
        'Dividend_Record_Years': lambda v: v >= 20,
        'Earnings_Stability_10Y': lambda v: v is True,
        'Margin_of_Safety_%': lambda v: v > 30,
        'NetNet_Buy_Candidate': lambda v: v is True
    }
    
    check_func = checks.get(metric)
    if check_func:
        try:
            return check_func(value)
        except (TypeError, ValueError):
            return False
    return False

def check_lynch_criteria(metric, value):
    """Check if a metric meets Lynch criteria"""
    if value is None:
        return False
    
    checks = {
        'P/E': lambda v: v < 15,
        'PEG': lambda v: v < 1.0,
        'EPS_Growth_%': lambda v: v > 15,
        'ROE_%': lambda v: v > 15,
        'Debt/Equity': lambda v: v < 0.5,
        'Current_Ratio': lambda v: v > 2.0,
        'Price/Book': lambda v: v < 1.5,
        'Price/Sales': lambda v: v < 1.0
    }
    
    check_func = checks.get(metric)
    if check_func:
        try:
            return check_func(value)
        except (TypeError, ValueError):
            return False
    return False

def generate_combined_verdict(graham_metrics, lynch_metrics, reddit_data):
    """Generate a combined investment verdict"""
    verdicts = []
    
    # Graham verdict
    if graham_metrics.get('Graham_Combined_Test'):
        verdicts.append("Graham analysis suggests this is a defensive investment opportunity")
    else:
        verdicts.append("Graham analysis indicates this stock doesn't meet conservative criteria")
    
    # Lynch verdict
    peg = lynch_metrics.get('PEG')
    growth = lynch_metrics.get('EPS_Growth_%')
    if peg and peg < 1.0:
        verdicts.append("Lynch analysis shows excellent value relative to growth")
    elif peg and peg < 1.5:
        verdicts.append("Lynch analysis indicates reasonable value")
    else:
        verdicts.append("Lynch analysis suggests potential overvaluation")
    
    # Reddit verdict
    reddit_verdict = reddit_data.get('verdict', 'Neutral')
    reddit_score = reddit_data.get('reddit_score', 50)
    if reddit_verdict == 'Bullish' and reddit_score > 70:
        verdicts.append("Reddit sentiment is strongly positive with high reliability")
    elif reddit_verdict == 'Bearish' and reddit_score < 30:
        verdicts.append("Reddit sentiment is negative with concerning reliability")
    else:
        verdicts.append("Reddit sentiment is mixed or neutral")
    
    # Overall recommendation
    graham_pass = graham_metrics.get('Graham_Combined_Test', False)
    lynch_good = peg and peg < 1.5
    reddit_positive = reddit_verdict == 'Bullish' and reddit_score > 60
    
    # Convert to integers to avoid NoneType errors
    positive_signals = sum([
        int(graham_pass) if graham_pass is not None else 0,
        int(lynch_good) if lynch_good is not None else 0,
        int(reddit_positive) if reddit_positive is not None else 0
    ])
    
    if positive_signals >= 2:
        recommendation = "BUY - Multiple analysis methods suggest positive outlook"
    elif positive_signals == 1:
        recommendation = "HOLD - Mixed signals, requires careful consideration"
    else:
        recommendation = "SELL/AVOID - Multiple red flags across analysis methods"
    
    verdict_text = f"{recommendation}. " + " ".join(verdicts)
    return verdict_text

def create_combined_report(symbol):
    """Create a combined HTML report for a stock symbol"""
    print(f"Analyzing {symbol}...")
    
    # Get stock data
    stock_data = get_stock_package(symbol)
    if not stock_data.get('price'):
        print(f"Could not fetch data for {symbol}")
        return None
    
    print("Running Graham analysis...")
    graham_results = graham_metrics(stock_data)
    
    print("Running Lynch analysis...")
    lynch_results = lynch_metrics(stock_data)
    
    print("Analyzing Reddit sentiment...")
    reddit_results = get_reddit_sentiment_summary(symbol)
    
    # ✅ SAFETY FIX: Handle missing Reddit data keys
    required_keys = [
        "sentiment_confidence", "buzz_ratio", "reliability_index",
        "reddit_score", "verdict", "mentions", "avg_sentiment",
        "dd_quality_ratio", "weighted_bias", "sentiment_momentum",
        "std_dev", "reliability_weight"
    ]
    for key in required_keys:
        reddit_results.setdefault(key, 0)

    reddit_results.setdefault("ticker", symbol)
    reddit_results.setdefault("subreddit_breakdown", {})
    reddit_results.setdefault("top_posts", [])

    # Optional: friendly note for report
    if "summary" in reddit_results:
        reddit_results["verdict"] = "Neutral"
        reddit_results["reddit_score"] = 50
        reddit_results["note"] = reddit_results["summary"]
    else:
        reddit_results["note"] = "Reddit sentiment analysis completed successfully."
    
    # Reddit sentiment analysis complete (no standalone report needed)
    print("Reddit sentiment analysis complete")
    
    # Generate summaries
    graham_summary = generate_graham_summary(graham_results)
    lynch_summary = generate_lynch_summary(lynch_results)
    combined_verdict = generate_combined_verdict(graham_results, lynch_results, reddit_results)
    
    # Load template
    template_path = PROJECT_ROOT / "templates" / "combined_template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Format market cap
    market_cap = stock_data.get('marketCap')
    if market_cap:
        if market_cap >= 1e12:
            market_cap_str = f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            market_cap_str = f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = f"${market_cap:,.0f}"
    else:
        market_cap_str = "N/A"
    
    # Render HTML
    html_content = template.render(
        symbol=symbol,
        company_name=stock_data.get('shortName', 'N/A'),
        price=stock_data.get('price', 'N/A'),
        sector=stock_data.get('sector', 'N/A'),
        industry=stock_data.get('industry', 'N/A'),
        market_cap=market_cap_str,
        graham_metrics=graham_results,
        lynch_metrics=lynch_results,
        reddit_data=reddit_results,
        graham_summary=graham_summary,
        lynch_summary=lynch_summary,
        combined_verdict=combined_verdict,
        generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        get_graham_criteria=get_graham_criteria,
        get_lynch_criteria=get_lynch_criteria,
        check_graham_criteria=check_graham_criteria,
        check_lynch_criteria=check_lynch_criteria
    )
    
    # Save report
    reports_dir = PROJECT_ROOT / "reports" / "generated"
    reports_dir.mkdir(exist_ok=True)

    # Always overwrite the latest report for each symbol
    filename = f"combined_report_{symbol}.html"
    filepath = reports_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Report saved as {filepath}")
    
    # Open in browser only once
    try:
        webbrowser.open(f"file://{filepath.absolute()}")
        print(f"Report opened in browser")
    except Exception as e:
        print(f"Could not open browser: {e}")
        print(f"Please manually open: {filepath}")
    
    return str(filepath)

def main():
    """Main function to generate combined report"""
    print("Starting Investo Combined Analysis...")
    
    # Get ticker from user
    symbol = input("Enter stock symbol (e.g., AAPL): ").upper().strip()
    if not symbol:
        symbol = "AAPL"  # Default example
    
    # Generate report
    report_path = create_combined_report(symbol)
    
    if report_path:
        print(f"\nAnalysis complete! Report saved to: {report_path}")
        print("The report includes:")
        print("   • Benjamin Graham value analysis")
        print("   • Peter Lynch growth analysis") 
        print("   • Reddit sentiment analysis")
        print("   • Combined investment verdict")
    else:
        print("Failed to generate report")

if __name__ == "__main__":
    main()
