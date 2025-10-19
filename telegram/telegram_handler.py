"""
Telegram Bot Handler
===================
Main handler for the Investo Telegram bot integration.
"""

import logging
import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramHandler:
    """Handle Telegram bot operations"""
    
    def __init__(self):
        self.bot_token = None
        self.chat_id = None
        self.is_configured = False
        self.load_config()
    
    def load_config(self):
        """Load Telegram configuration from environment"""
        try:
            # Load from .env file
            env_path = Path(__file__).parent.parent / ".env"
            if env_path.exists():
                load_dotenv(env_path)
            
            self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
            
            if self.bot_token and self.chat_id:
                self.is_configured = True
                logger.info("Telegram configuration loaded successfully")
            else:
                logger.warning("Telegram configuration incomplete. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
                
        except Exception as e:
            logger.error(f"Error loading Telegram configuration: {e}")
    
    def send_message(self, message: str) -> bool:
        """Send a message via Telegram"""
        if not self.is_configured:
            logger.warning("Telegram not configured. Cannot send message.")
            return False
        
        try:
            # This would integrate with python-telegram-bot library
            # For now, just log the message
            logger.info(f"Telegram message: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_analysis_report(self, ticker: str, report_path: str) -> bool:
        """Send analysis report via Telegram"""
        message = f"""
📊 Stock Analysis Complete!

🎯 Ticker: {ticker}
📄 Report: {report_path}

The analysis includes:
• Benjamin Graham value analysis
• Peter Lynch growth analysis
• Reddit sentiment analysis

Report has been generated and saved locally.
        """
        
        return self.send_message(message)
    
    def send_error_notification(self, error_message: str) -> bool:
        """Send error notification via Telegram"""
        message = f"""
❌ Analysis Error

{error_message}

Please check the logs for more details.
        """
        
        return self.send_message(message)
    
    def is_available(self) -> bool:
        """Check if Telegram integration is available"""
        return self.is_configured

# Global instance
telegram_handler = TelegramHandler()
