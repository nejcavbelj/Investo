# Investo - Investment Analysis Bot

🚀 **Investo** is a comprehensive investment analysis bot that combines multiple legendary investment strategies with real-time market data, AI-powered insights, and social sentiment analysis.

## 🌟 Features

### 📊 **Investment Analysis**
- **Peter Lynch Growth Analysis** - PEG ratios, earnings growth, ROE/ROA analysis
- **Benjamin Graham Value Analysis** - Net-Net (NCAV), intrinsic value, margin of safety
- **Multi-factor Analysis** - Combines quantitative metrics with qualitative factors

### 📰 **Real-time Data**
- **Yahoo Finance Integration** - Comprehensive financial data and ratios
- **Finnhub API** - Company news and global market updates
- **StockTwits Sentiment** - Crowd sentiment and social buzz
- **Reddit Analysis** - Multi-factor sentiment with reliability scoring

### 🤖 **AI-Powered Insights**
- **OpenAI GPT Integration** - Intelligent market summaries
- **Token Budget Management** - Smart API usage tracking
- **Context-Aware Analysis** - Different modes for single stocks vs market overview

### 💬 **Telegram Bot Interface**
- **Easy Commands** - Type tickers or "SUMMARY" for analysis
- **Budget Alerts** - Automatic notifications when approaching limits
- **Error Handling** - Graceful fallbacks and user-friendly messages

## 🏗️ Architecture

```
Investo/
│
├── main.py                        # Entry point – orchestrates data collection, analysis & reporting
│
├── config/
│   ├── settings.py                # Global variables (paths, timeouts, constants)
│   ├── credentials_example.env    # Example .env for users
│   └── __init__.py
│
├── core/
│   ├── lynch_analysis.py          # Peter Lynch-style valuation logic
│   ├── graham_analysis.py         # Benjamin Graham / value investor module
│   ├── reddit_sentiment.py        # Reddit sentiment collector
│   ├── finnhub_api.py             # Handles Finnhub API requests
│   ├── data_sources.py            # Data aggregator from APIs
│   ├── summarizer.py              # AI summary generator (GPT)
│   └── __init__.py
│
├── reports/
│   ├── report_builder.py          # PDF/HTML report generation using ReportLab
│   ├── templates/
│   │   ├── lynch_template.html
│   │   ├── graham_template.html
│   │   └── base_style.css
│   └── generated/
│       └── TSLA_2025-10-14.pdf    # Example of generated output
│
├── telegram/
│   ├── telegram_handler.py        # Handles bot commands, responses, user input
│   ├── commands.py                # Defines /start, /help, /summary, ticker handlers
│   └── __init__.py
│
├── utils/
│   ├── logger.py                  # Unified logging setup
│   ├── helpers.py                 # Common helper functions
│   ├── cache_manager.py           # Simple JSON or SQLite caching
│   └── __init__.py
│
├── tests/
│   ├── test_lynch.py              # Unit tests for analysis
│   ├── test_sentiment.py
│   └── __init__.py
│
├── venv/                          # Virtual environment (ignored in Git)
│
├── .env                           # Your private API keys
├── .env.example                   # Template for other users
├── .gitignore                     # Ensures venv & secrets aren't pushed to Git
├── requirements.txt               # Dependencies (praw, yfinance, vaderSentiment, reportlab, etc.)
└── README.md                      # Setup guide & usage instructions
```

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/investo.git
cd investo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**

```bash
# Copy example environment file
cp config/credentials_example.env .env

# Edit .env with your API keys
nano .env
```

**Required API Keys:**
- `OPENAI_API_KEY` - For AI summaries
- `TELEGRAM_BOT_TOKEN` - For bot functionality
- `FINNHUB_API_KEY` - For financial data and news
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` - For Reddit sentiment (optional)

### 3. **Run the Bot**

```bash
python main.py
```

## 📱 Usage

### **Telegram Commands**

- `/start` - Welcome message and instructions
- `/help` - Detailed help information
- `SUMMARY` - Market overview with top 5 trending stocks
- `TSLA` - Analyze specific stock (Tesla)
- `AAPL MSFT GOOGL` - Analyze multiple stocks

### **Example Interactions**

```
User: SUMMARY
Bot: 📊 Overall Market Summary
     Top 5 trending stocks with AI analysis...

User: TSLA
Bot: 🚗 Analysis for TSLA
     Peter Lynch: Growth stock with strong PEG...
     Benjamin Graham: High P/E, not a value play...
```

## 🔧 Development

### **Running Tests**

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_lynch.py

# Run with coverage
python -m pytest --cov=core tests/
```

### **Code Quality**

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 📊 Analysis Methods

### **Peter Lynch Analysis**
- **P/E Ratio** - Price-to-earnings evaluation
- **PEG Ratio** - Price/earnings to growth ratio
- **ROE/ROA** - Return on equity/assets
- **Cash Position** - Financial strength indicators
- **Insider Ownership** - Management confidence

### **Benjamin Graham Analysis**
- **Net-Net Value** - Deep value screening (NCAV)
- **Intrinsic Value** - Graham's formula: IV = EPS × (8.5 + 2g)
- **Margin of Safety** - Downside protection calculation
- **Debt-to-Equity** - Financial stability metrics
- **Dividend Record** - Consistent income history

### **Sentiment Analysis**
- **Reddit Sentiment** - Multi-factor analysis with reliability scoring
- **StockTwits Buzz** - Social media sentiment tracking
- **News Integration** - Real-time company and market news

## 🛠️ Customization

### **Adding New Analysis Methods**

1. Create new analysis module in `core/`
2. Implement calculation functions
3. Add to `core/__init__.py`
4. Update report templates if needed

### **Extending Data Sources**

1. Add new API module in `core/`
2. Implement data fetching functions
3. Integrate with `data_sources.py`
4. Update tests

## 📈 Performance

- **Caching** - JSON-based caching for API responses
- **Budget Management** - Smart token usage tracking
- **Error Handling** - Graceful fallbacks for API failures
- **Async Support** - Non-blocking Telegram bot operations

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Peter Lynch** - For growth investing principles
- **Benjamin Graham** - For value investing methodology
- **OpenAI** - For AI-powered analysis capabilities
- **Yahoo Finance** - For comprehensive financial data
- **Finnhub** - For real-time market news

## 📞 Support

- 📧 Email: support@investo.com
- 💬 Telegram: @InvestoSupport
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/investo/issues)

---

**⚠️ Disclaimer**: This bot is for educational and informational purposes only. Not financial advice. Always do your own research before making investment decisions.
