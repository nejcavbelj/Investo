# Investo Web Application Deployment

## Overview
This document explains how to deploy and use the Investo web application on Railway.

## Features
- **Interactive Welcome Page**: Matches the design from the provided photo with dark theme and orange accents
- **Real-time Stock Analysis**: Enter any ticker symbol to get comprehensive analysis
- **Terminal Integration**: The original `main.py` now includes interactive terminal input
- **Railway Deployment**: Ready for deployment on Railway platform

## Local Development

### Running the Web App Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The web app will be available at `http://localhost:5000`

### Running the Terminal Version
```bash
# Run the interactive terminal version
python main.py
```

## Railway Deployment

### Prerequisites
1. Railway account
2. GitHub repository with your code
3. Environment variables configured

### Deployment Steps

1. **Connect to Railway**:
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select this project

2. **Configure Environment Variables**:
   Add these variables in Railway dashboard:
   ```
   OPENAI_API_KEY=your_openai_key
   FINNHUB_API_KEY=your_finnhub_key
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_secret
   REDDIT_USER_AGENT=your_user_agent
   ```

3. **Deploy**:
   - Railway will automatically detect the `Procfile` and `railway.json`
   - The app will be deployed using Gunicorn
   - Your app will be available at the provided Railway URL

### Files for Railway Deployment
- `app.py` - Main Flask application
- `Procfile` - Tells Railway how to run the app
- `railway.json` - Railway-specific configuration
- `requirements.txt` - Python dependencies (updated with Flask)
- `templates/welcome.html` - Welcome page template

## Usage

### Web Interface
1. Visit your Railway app URL
2. Enter a stock ticker symbol (e.g., TSLA, AAPL, MSFT)
3. Click "Analyze Stock"
4. Wait for analysis to complete
5. View the comprehensive report

### Terminal Interface
1. Run `python main.py`
2. Enter ticker symbol when prompted
3. View the generated HTML report
4. Option to analyze additional stocks

## Architecture

### Web Application Structure
```
app.py                 # Flask web application
templates/
  └── welcome.html     # Welcome page matching photo design
Procfile              # Railway deployment configuration
railway.json          # Railway-specific settings
requirements.txt      # Updated with Flask dependencies
```

### Key Features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Analysis**: AJAX-based stock analysis
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during analysis
- **Report Integration**: Seamless report viewing

## API Endpoints

### GET /
- **Purpose**: Welcome page
- **Response**: HTML welcome page

### POST /analyze
- **Purpose**: Analyze stock
- **Body**: `{"symbol": "TSLA"}`
- **Response**: Analysis results or error message

### GET /report/<filename>
- **Purpose**: Serve generated reports
- **Response**: HTML report content

## Troubleshooting

### Common Issues

1. **App won't start on Railway**:
   - Check environment variables are set
   - Verify `Procfile` exists
   - Check logs in Railway dashboard

2. **Analysis fails**:
   - Verify API keys are correct
   - Check ticker symbol is valid
   - Review error messages in browser console

3. **Reports not loading**:
   - Check file permissions
   - Verify report generation completed
   - Check Railway logs for errors

### Environment Variables Required
- `OPENAI_API_KEY`: For AI summaries
- `FINNHUB_API_KEY`: For financial data
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`: For Reddit sentiment (optional)

## Development Notes

### Design Matching
The welcome page has been designed to match the provided photo:
- Dark background (#0a0a0a)
- Orange accent color (#ffa500)
- "Smart Stock Analysis" header tag
- Large "Investo" title
- Descriptive tagline
- Input form with "Stock Ticker Symbol" label
- "Analyze Stock" button

### Integration
Both the terminal (`main.py`) and web (`app.py`) versions use the same core analysis functions:
- `create_combined_report()` from `reports.combined_report_generator`
- Same configuration and API setup
- Identical report generation and styling

This ensures consistent results whether using the terminal or web interface.
