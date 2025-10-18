"""
Budget management utilities
"""

from config.settings import DEFAULT_BUDGET, BUDGET_THRESHOLD_PERCENT

def is_token_budget_low(tokens_used, primary_budget, threshold_percent=BUDGET_THRESHOLD_PERCENT):
    """
    Returns True if the remaining token budget is less than or equal to the threshold percentage.
    """
    if primary_budget == 0:
        return True  # Avoid division by zero; treat as low budget.
    remaining_percent = 100 * (primary_budget - tokens_used) / primary_budget
    return remaining_percent <= threshold_percent

def calculate_remaining_tokens(tokens_used, primary_budget):
    """Calculate remaining tokens"""
    return max(0, primary_budget - tokens_used)

def calculate_remaining_percentage(tokens_used, primary_budget):
    """Calculate remaining percentage of budget"""
    if primary_budget == 0:
        return 0
    return max(0, 100 * (primary_budget - tokens_used) / primary_budget)

def get_budget_status(tokens_used, primary_budget):
    """Get budget status string"""
    remaining_percent = calculate_remaining_percentage(tokens_used, primary_budget)
    
    if remaining_percent <= 10:
        return "CRITICAL"
    elif remaining_percent <= 25:
        return "LOW"
    elif remaining_percent <= 50:
        return "MODERATE"
    else:
        return "HEALTHY"

def format_budget_info(tokens_used, primary_budget):
    """Format budget information for display"""
    remaining = calculate_remaining_tokens(tokens_used, primary_budget)
    remaining_percent = calculate_remaining_percentage(tokens_used, primary_budget)
    status = get_budget_status(tokens_used, primary_budget)
    
    return {
        "tokens_used": tokens_used,
        "primary_budget": primary_budget,
        "remaining_tokens": remaining,
        "remaining_percent": remaining_percent,
        "status": status
    }
