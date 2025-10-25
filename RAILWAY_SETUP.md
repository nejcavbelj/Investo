# Railway Deployment Setup Guide

## 🚀 Required Environment Variables

To make Investo work on Railway, you need to configure these environment variables in your Railway project settings:

### Required for Core Functionality:
```
FINNHUB_API_KEY=your_finnhub_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Required for Reddit Sentiment Analysis:
```
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=InvestoBot/1.0
```

### Optional (for Telegram bot):
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

### Optional (for Feedback form - sends to investosystem@gmail.com):
```
GMAIL_APP_PASSWORD=your_gmail_app_password_here
FLASK_SECRET_KEY=your_random_secret_key_here
```

---

## 📝 How to Get API Keys

### 1. Finnhub API Key (Free)
1. Go to https://finnhub.io/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes: 60 API calls/minute

### 2. OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up and add payment method
3. Create an API key at https://platform.openai.com/api-keys
4. Note: This is a paid service (but very cheap for this usage)

### 3. Reddit API Credentials (Free)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - Name: Investo Bot
   - Type: Select "script"
   - Redirect URI: http://localhost:8080
4. Click "Create app"
5. Your credentials:
   - `REDDIT_CLIENT_ID`: The string under "personal use script"
   - `REDDIT_CLIENT_SECRET`: The "secret" field
   - `REDDIT_USER_AGENT`: Use "InvestoBot/1.0"

### 4. Gmail App Password (Optional - for Feedback Feature)
1. Go to your Google Account settings
2. Enable 2-Step Verification if not already enabled
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and "Other (Custom name)"
5. Enter "Investo Railway" as the name
6. Click "Generate"
7. Copy the 16-character password (without spaces)
8. Use this as `GMAIL_APP_PASSWORD` in Railway

**Note**: The feedback is sent to `investosystem@gmail.com`. You may want to update this email in `core/feedback_handler.py` to your own email.

---

## 🔧 Setting Environment Variables in Railway

1. Open your Railway project dashboard
2. Click on your deployed service
3. Go to the **Variables** tab
4. Click **+ New Variable**
5. Add each environment variable (name and value)
6. Railway will automatically redeploy with the new variables

---

## ✅ Verify Setup

After setting the environment variables:

1. Visit your Railway URL
2. Go to `/status` endpoint (e.g., `https://your-app.railway.app/status`)
3. Check that all required environment variables show as "set"
4. Check the Railway deployment logs to see initialization status

---

## 🐛 Troubleshooting

### "Analysis system is initializing" message
- **Cause**: Missing environment variables
- **Solution**: Check `/status` endpoint and add missing variables

### Report generator not available
- **Cause**: Import error or missing dependencies
- **Solution**: Check Railway logs for detailed error traceback

### Railway healthcheck failing
- **Cause**: App not binding to correct host/port
- **Solution**: Already fixed! App now binds to `0.0.0.0` and uses Railway's PORT

### Feedback form shows "Not Found" error
- **Cause**: Feedback blueprint not registered in app.py
- **Solution**: Already fixed! Feedback handler is now registered on startup

### Feedback form doesn't send email
- **Cause**: Missing `GMAIL_APP_PASSWORD` environment variable
- **Solution**: Set up Gmail App Password and add to Railway variables

---

## 📊 Testing Your Setup

1. Go to your Railway URL (e.g., `https://investo-production.up.railway.app`)
2. Enter a stock ticker (e.g., AAPL, TSLA, MSFT)
3. Click "Analyze Stock"
4. You should see a comprehensive report with:
   - Benjamin Graham value analysis
   - Peter Lynch growth analysis
   - Reddit sentiment analysis
   - Combined investment verdict

---

## 💡 Notes

- The free Finnhub tier is sufficient for personal use
- OpenAI costs are minimal (~$0.01-0.05 per analysis)
- Reddit API is completely free
- All API keys should be kept secret - never commit them to Git

