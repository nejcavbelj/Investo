# Investo Combined Analysis Report

## Overview
Investo now generates comprehensive HTML reports that combine three different investment analysis methods:

1. **Benjamin Graham Analysis** - Value investing principles
2. **Peter Lynch Analysis** - Growth investing principles  
3. **Reddit Sentiment Analysis** - Social media sentiment and buzz

## How to Use

### Quick Start (Default Ticker)
```bash
python main.py
```
This will analyze TSLA and generate:
- A combined report with all three analyses
- A detailed Reddit sentiment report (like the image shown)

### Interactive Mode
```bash
python interactive_main.py
```
This provides a menu-driven interface where you can:
- Enter any ticker symbol for analysis
- Run the TSLA example
- Exit the program

### Standalone Reddit Report
```bash
python reddit_report_generator.py
```
This generates only the detailed Reddit sentiment report with charts and visualizations.

## Report Features

### Combined Report
The generated HTML report includes:

#### Company Information
- Company name, current price, sector, industry, market cap

#### Benjamin Graham Analysis
- P/E ratio, P/B ratio, debt-to-equity
- Current ratio, dividend record
- Net-Net analysis (NCAV)
- Graham Combined Test results
- Margin of safety calculations

#### Peter Lynch Analysis  
- PEG ratio, EPS growth
- ROE, ROA, profit margins
- Price-to-sales, price-to-book ratios
- Cash position, insider ownership
- Free cash flow yield

#### Reddit Sentiment Analysis
- Overall sentiment (Bullish/Neutral/Bearish)
- Reddit score (0-100)
- Mentions count, sentiment confidence
- Buzz ratio, sentiment momentum
- **Link to detailed Reddit report**

#### Combined Investment Verdict
- Overall BUY/HOLD/SELL recommendation
- Analysis breakdown from all three methods
- Comprehensive investment summary

### Detailed Reddit Report
The standalone Reddit report includes all the features shown in the image:

#### Comprehensive Metrics Table
- Mentions (last 14 days)
- Average Sentiment with verdict
- Sentiment Standard Deviation
- Sentiment Confidence percentage
- Sentiment Momentum
- Buzz Ratio
- Reliability Weight
- DD Quality Ratio
- Weighted Sentiment Bias
- Reliability Index (with color-coded badge)
- Composite Reddit Score

#### Visual Charts
- **Sentiment Confidence Donut Chart** - Shows agreement level
- **Buzz Meter** - Horizontal bar with color zones (Fading/Healthy/Hype)
- **Analytical vs Emotional Donut Chart** - Shows quality of posts
- **Subreddit Weights** - Visual bars showing credibility of each subreddit

#### Investo Verdict Section
- Overall sentiment verdict with color coding
- Sentiment trend analysis
- Buzz level assessment
- Discussion quality metrics
- Reliability factors

#### Top Reddit Posts
- Direct links to relevant Reddit discussions
- Quality indicators for analytical posts
- Sentiment scores for each post
- Subreddit source and engagement metrics

## Requirements

Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

## Configuration

You'll need to set up your API keys in a `.env` file:
- `FINNHUB_API_KEY` - For financial data
- `REDDIT_CLIENT_ID` - For Reddit sentiment analysis
- `REDDIT_CLIENT_SECRET` - For Reddit API access
- `REDDIT_USER_AGENT` - For Reddit API identification

## Output

Reports are saved in different locations:
- **Combined reports**: `reports/generated/combined_report_[TICKER]_[TIMESTAMP].html`
- **Reddit reports**: `reddit_report_[TICKER].html` (in project root)

Both reports automatically open in your default web browser for immediate viewing.

## Example Output

The system now provides:
1. **Professional combined report** with dark-themed HTML interface
2. **Detailed Reddit sentiment report** matching the style shown in the image
3. **Color-coded sentiment indicators** and interactive elements
4. **Direct links to Reddit posts** for further research
5. **Comprehensive investment recommendations** based on multiple analysis methods

This gives you a complete 360-degree view of any stock using multiple analysis methodologies combined with real-time social sentiment data, exactly like the Reddit report shown in the image.
