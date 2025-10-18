# Railway Deployment Guide for Investo

This guide will help you deploy your Investo investment analysis application to Railway.

## Prerequisites

1. A GitHub account with your Investo repository
2. A Railway account (sign up at [railway.app](https://railway.app))
3. All required API keys (see Environment Variables section)

## Deployment Steps

### 1. Push to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Connect to Railway

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your Investo repository
5. Railway will automatically detect it's a Python project

### 3. Configure Environment Variables

In your Railway project dashboard, go to the "Variables" tab and add these environment variables:

#### Required Variables:
```
OPENAI_API_KEY=your_openai_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here
```

#### Optional Variables (for Telegram bot):
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

#### Optional Variables (for Reddit integration):
```
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=your_reddit_user_agent_here
```

### 4. Deploy

1. Railway will automatically start building and deploying your application
2. The build process will:
   - Install Python 3.11.0 (as specified in `runtime.txt`)
   - Install dependencies from `requirements.txt`
   - Start the web application using the `Procfile`

### 5. Access Your Application

Once deployed, Railway will provide you with a URL like:
`https://your-app-name.railway.app`

You can access your Investo web interface at this URL.

## Application Features

Your deployed application includes:

- **Web Interface**: Simple form to analyze stocks
- **Report Generation**: Creates comprehensive investment analysis reports
- **File Downloads**: Users can download generated reports
- **Health Check**: `/health` endpoint for monitoring

## Monitoring

- Check the Railway dashboard for deployment logs
- Use the `/health` endpoint to verify the application is running
- Monitor resource usage in the Railway dashboard

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check that all dependencies are in `requirements.txt`
2. **Environment Variables**: Ensure all required API keys are set
3. **Port Issues**: The app automatically uses Railway's PORT environment variable
4. **File Permissions**: Reports are generated in the `reports/generated/` directory

### Logs:

View application logs in the Railway dashboard under the "Deployments" tab.

## Scaling

Railway automatically handles:
- Load balancing
- SSL certificates
- Domain management
- Auto-scaling based on traffic

## Cost

Railway offers:
- Free tier with limited usage
- Pay-as-you-go pricing for production use
- No credit card required for free tier

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
