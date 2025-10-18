"""
Telegram bot commands module
---------------------------
Defines all bot commands and their handlers
"""

from telegram import Update
from telegram.ext import ContextTypes
from utils.budget import is_token_budget_low
from utils.token_persistence import load_primary_budget
from core.data_sources import get_stock_package, get_top_volume_tickers, get_most_mentioned_tickers
from core.summarizer import summarize_stocks
from utils.tickers import clean_tickers
from config.settings import TOP_N_TRENDING, BUDGET_THRESHOLD_PERCENT

async def send_budget_reminder(update, context, remaining_percent):
    """Send budget reminder to user"""
    message = f"⚠️ Reminder: You only have {remaining_percent:.1f}% of your OpenAI token budget left!"
    await update.message.reply_text(message)

async def handle_summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle SUMMARY command - analyze top trending stocks"""
    volume = clean_tickers(get_top_volume_tickers(TOP_N_TRENDING))
    mentions = clean_tickers(get_most_mentioned_tickers(TOP_N_TRENDING))
    combined = list(dict.fromkeys(volume + mentions))

    if not combined:
        await update.message.reply_text("⚠ Could not find valid tickers right now. Try again later.")
        return

    pkgs = [get_stock_package(s) for s in combined]
    pkgs.sort(key=lambda x: (
        abs(x.get("pct_1d") if isinstance(x.get("pct_1d"), (int,float)) else 0),
        x.get("crowd", {}).get("mentions", 0)
    ), reverse=True)
    top5 = pkgs[:5]
    summary = summarize_stocks(top5, "Overall Market Summary", mode="summary", context=context)
    await update.message.reply_text(summary)

async def handle_ticker_command(update: Update, context: ContextTypes.DEFAULT_TYPE, ticker: str):
    """Handle individual ticker analysis"""
    pkg = get_stock_package(ticker)
    summary = summarize_stocks([pkg], f"Analysis for {ticker}", mode="ticker", context=context)
    await update.message.reply_text(summary)

async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🚀 Welcome to Investo Bot!

Available commands:
• Type 'SUMMARY' for market overview
• Type any ticker symbol (e.g., 'TSLA', 'AAPL') for analysis
• Type multiple tickers separated by spaces

Investo provides:
📊 Peter Lynch growth analysis
📈 Benjamin Graham value analysis  
📰 Real-time news & sentiment
🤖 AI-powered summaries

Start by typing 'SUMMARY' or a ticker symbol!
    """
    await update.message.reply_text(welcome_message)

async def handle_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
📖 Investo Bot Help

Commands:
• /start - Welcome message
• /help - This help message
• SUMMARY - Market overview with top 5 trending stocks
• [TICKER] - Analyze specific stock (e.g., TSLA, AAPL)
• [TICKER1 TICKER2] - Analyze multiple stocks

Examples:
• Type 'TSLA' for Tesla analysis
• Type 'AAPL MSFT GOOGL' for multiple stocks
• Type 'SUMMARY' for market overview

Features:
🔍 Comprehensive stock analysis
📊 Multiple investment strategies
📰 Real-time news integration
💬 Social sentiment analysis
🤖 AI-powered insights

Need more help? Contact support.
    """
    await update.message.reply_text(help_message)

async def check_budget_and_handle_message(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    startup_warnings: list
):
    """Check budget and handle incoming messages"""
    text = (update.message.text or "").strip().upper()
    if not text:
        return

    tokens_used = context.bot_data.get("tokens_used", 0)
    primary_budget = load_primary_budget()
    context.bot_data["primary_budget"] = primary_budget

    # Budget check logic, only notify ONCE!
    if is_token_budget_low(tokens_used, primary_budget, BUDGET_THRESHOLD_PERCENT):
        if not context.bot_data.get("reminder_sent"):
            remaining_percent = 100 * (primary_budget - tokens_used) / primary_budget
            await send_budget_reminder(update, context, remaining_percent)
            context.bot_data["reminder_sent"] = True
    else:
        context.bot_data["reminder_sent"] = False

    # Show warnings if any
    if startup_warnings:
        await update.message.reply_text("\n".join(startup_warnings))
        startup_warnings.clear()

    # Handle different message types
    if text == "SUMMARY":
        await handle_summary_command(update, context)
        return

    # Handle individual tickers
    tickers = [t for t in text.split() if clean_tickers([t])]
    if not tickers:
        await update.message.reply_text("❌ No valid tickers found.")
        return

    for ticker in tickers:
        await handle_ticker_command(update, context, ticker)
