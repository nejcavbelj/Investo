"""
Unit tests for Lynch analysis module
"""

import unittest
from unittest.mock import patch
from core.lynch_analysis import lynch_metrics, calc_pe, calc_peg, calc_roe

class TestLynchAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = {
            "symbol": "AAPL",
            "price": 150.0,
            "forwardPE": 25.0,
            "trailingPE": 23.0,
            "earningsQuarterlyGrowth": 0.15,
            "dividendYield": 0.02,
            "returnOnEquity": 0.20,
            "returnOnAssets": 0.15,
            "profitMargins": 0.25,
            "priceToBook": 5.0,
            "priceToSales": 3.0,
            "totalCash": 1000000000,
            "totalAssets": 5000000000,
            "totalCurrentAssets": 2000000000,
            "totalCurrentLiabilities": 1000000000,
            "inventory": 500000000,
            "sector": "Technology",
            "industry": "Consumer Electronics"
        }
    
    def test_calc_pe(self):
        """Test P/E calculation"""
        pe = calc_pe(self.sample_data)
        self.assertEqual(pe, 25.0)  # Should prefer forwardPE
        
        # Test with only trailing PE
        data_no_forward = self.sample_data.copy()
        del data_no_forward["forwardPE"]
        pe = calc_pe(data_no_forward)
        self.assertEqual(pe, 23.0)
    
    def test_calc_peg(self):
        """Test PEG calculation"""
        pe = calc_pe(self.sample_data)
        peg = calc_peg(pe, 15.0)  # 15% growth
        self.assertAlmostEqual(peg, 1.67, places=2)
    
    def test_calc_roe(self):
        """Test ROE calculation"""
        roe = calc_roe(self.sample_data)
        self.assertEqual(roe, 20.0)
    
    def test_lynch_metrics(self):
        """Test complete Lynch metrics calculation"""
        metrics = lynch_metrics(self.sample_data)
        
        # Check that all expected metrics are present
        expected_metrics = [
            "P/E", "EPS_Growth_%", "PEG", "Debt/Equity", "Dividend_Yield_%",
            "Cash/Assets_%", "Inventory/Sales_Growth_%", "Insider_Ownership_%",
            "ROE_%", "ROA_%", "Profit_Margin_%", "Price/Book", "Price/Sales",
            "Current_Ratio", "Quick_Ratio", "Earnings_Yield_%", "FCF_Yield_%"
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
        
        # Check specific values
        self.assertEqual(metrics["P/E"], 25.0)
        self.assertEqual(metrics["ROE_%"], 20.0)
        self.assertEqual(metrics["sector"], "Technology")

if __name__ == '__main__':
    unittest.main()
