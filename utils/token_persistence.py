"""
Token persistence utilities
"""

import json
import os
from pathlib import Path
from config.settings import DEFAULT_BUDGET, PROJECT_ROOT

# Use project directory for token data
DATA_PATH = PROJECT_ROOT / "token_data.json"

def load_token_data():
    """Load token usage data from file"""
    if DATA_PATH.exists():
        try:
            with open(DATA_PATH, "r") as f:
                data = json.load(f)
                return data.get("tokens_used", 0), data.get("primary_budget", DEFAULT_BUDGET)
        except Exception as e:
            print(f"Error loading token data: {e}")
            return 0, DEFAULT_BUDGET
    return 0, DEFAULT_BUDGET

def save_token_data(tokens_used, primary_budget):
    """Save token usage data to file"""
    try:
        # Ensure directory exists
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(DATA_PATH, "w") as f:
            json.dump({
                "tokens_used": tokens_used,
                "primary_budget": primary_budget,
                "last_updated": str(Path().cwd())
            }, f, indent=2)
    except Exception as e:
        print(f"Error saving token data: {e}")

def load_primary_budget():
    """Load only the primary budget from file"""
    if DATA_PATH.exists():
        try:
            with open(DATA_PATH, "r") as f:
                data = json.load(f)
                return data.get("primary_budget", DEFAULT_BUDGET)
        except Exception as e:
            print(f"Error loading primary budget: {e}")
            return DEFAULT_BUDGET
    return DEFAULT_BUDGET

def reset_token_data():
    """Reset token data to default values"""
    save_token_data(0, DEFAULT_BUDGET)

def get_token_data_info():
    """Get comprehensive token data information"""
    tokens_used, primary_budget = load_token_data()
    remaining = max(0, primary_budget - tokens_used)
    remaining_percent = max(0, 100 * remaining / primary_budget) if primary_budget > 0 else 0
    
    return {
        "tokens_used": tokens_used,
        "primary_budget": primary_budget,
        "remaining_tokens": remaining,
        "remaining_percent": remaining_percent,
        "data_file": str(DATA_PATH),
        "file_exists": DATA_PATH.exists()
    }
