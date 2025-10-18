"""
Telegram bot handler module
---------------------------
Main handler for the Telegram bot application
"""

from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters
from telegram.request import HTTPXRequest
from .commands import (
    check_budget_and_handle_message,
    handle_start_command,
    handle_help_command
)

def start_bot(
    config,
    startup_warnings,
    tokens_used,
    primary_budget
):
    """Start the Telegram bot with all handlers"""
    request = HTTPXRequest(http_version="1.1")
    app = Application.builder().token(config["TELEGRAM_BOT_TOKEN"]).request(request).build()

    # Set persistent values when the bot starts
    app.bot_data["tokens_used"] = tokens_used
    app.bot_data["primary_budget"] = primary_budget

    # Add command handlers
    app.add_handler(CommandHandler("start", handle_start_command))
    app.add_handler(CommandHandler("help", handle_help_command))

    # Add message handler for text messages (not commands)
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        lambda update, context: check_budget_and_handle_message(
            update, context, startup_warnings
        )
    ))

    print("🤖 Investo Bot ready!")
    print("📊 Type 'SUMMARY' for market overview")
    print("📈 Type any ticker symbol for analysis")
    print("❓ Type /help for more information")
    
    app.run_polling()
