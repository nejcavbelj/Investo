"""
Global settings and configuration constants for Investo
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
CORE_DIR = PROJECT_ROOT / "core"
REPORTS_DIR = PROJECT_ROOT / "reports"
TELEGRAM_DIR = PROJECT_ROOT / "telegram"
UTILS_DIR = PROJECT_ROOT / "utils"
TESTS_DIR = PROJECT_ROOT / "tests"

# API timeouts
HTTP_TIMEOUT = 12
REQUEST_TIMEOUT = 15

# Analysis settings
TOP_N_TRENDING = 10
MAX_NEWS_ITEMS = 5
MAX_GLOBAL_NEWS = 6
MAX_SENTIMENT_ITEMS = 100

# Token budget settings
DEFAULT_BUDGET = 1000
BUDGET_THRESHOLD_PERCENT = 10

# File paths
TOKEN_DATA_PATH = os.path.expanduser("~/investment_news_bot/token_data.json")
ENV_FILE_PATH = PROJECT_ROOT / ".env"

# Report settings
REPORT_TEMPLATES_DIR = REPORTS_DIR / "templates"
GENERATED_REPORTS_DIR = REPORTS_DIR / "generated"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
