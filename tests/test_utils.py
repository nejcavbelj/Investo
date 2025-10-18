"""
Unit tests for utility functions
"""

import unittest
from utils.helpers import is_valid_ticker, clean_tickers, normalize_ticker, validate_ticker_list
from utils.budget import is_token_budget_low, calculate_remaining_tokens, get_budget_status

class TestHelpers(unittest.TestCase):
    
    def test_is_valid_ticker(self):
        """Test ticker validation"""
        self.assertTrue(is_valid_ticker("AAPL"))
        self.assertTrue(is_valid_ticker("TSLA"))
        self.assertTrue(is_valid_ticker("MSFT"))
        self.assertFalse(is_valid_ticker("CEO"))
        self.assertFalse(is_valid_ticker("ETF"))
        self.assertFalse(is_valid_ticker(""))
        self.assertFalse(is_valid_ticker("INVALID"))
        self.assertFalse(is_valid_ticker("123"))
    
    def test_clean_tickers(self):
        """Test ticker cleaning"""
        tickers = ["AAPL", "CEO", "TSLA", "ETF", "MSFT"]
        cleaned = clean_tickers(tickers)
        self.assertEqual(cleaned, ["AAPL", "TSLA", "MSFT"])
    
    def test_normalize_ticker(self):
        """Test ticker normalization"""
        self.assertEqual(normalize_ticker("aapl"), "AAPL")
        self.assertEqual(normalize_ticker("  tsla  "), "TSLA")
        self.assertEqual(normalize_ticker(""), "")
    
    def test_validate_ticker_list(self):
        """Test ticker list validation"""
        tickers = ["AAPL", "CEO", "TSLA", "invalid"]
        valid, invalid = validate_ticker_list(tickers)
        self.assertEqual(valid, ["AAPL", "TSLA"])
        self.assertEqual(invalid, ["CEO", "invalid"])

class TestBudget(unittest.TestCase):
    
    def test_is_token_budget_low(self):
        """Test budget low detection"""
        self.assertTrue(is_token_budget_low(950, 1000, 10))  # 5% remaining
        self.assertFalse(is_token_budget_low(800, 1000, 10))  # 20% remaining
        self.assertTrue(is_token_budget_low(1000, 1000, 10))  # 0% remaining
        self.assertTrue(is_token_budget_low(100, 0, 10))  # Zero budget
    
    def test_calculate_remaining_tokens(self):
        """Test remaining tokens calculation"""
        self.assertEqual(calculate_remaining_tokens(300, 1000), 700)
        self.assertEqual(calculate_remaining_tokens(1000, 1000), 0)
        self.assertEqual(calculate_remaining_tokens(1200, 1000), 0)
    
    def test_get_budget_status(self):
        """Test budget status classification"""
        self.assertEqual(get_budget_status(950, 1000), "CRITICAL")
        self.assertEqual(get_budget_status(800, 1000), "LOW")
        self.assertEqual(get_budget_status(500, 1000), "MODERATE")
        self.assertEqual(get_budget_status(200, 1000), "HEALTHY")

if __name__ == '__main__':
    unittest.main()
