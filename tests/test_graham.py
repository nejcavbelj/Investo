"""
Unit tests for Graham analysis module
"""

import unittest
from core.graham_analysis import graham_metrics, calc_pe, calc_pb, calc_intrinsic_value

class TestGrahamAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_data = {
            "symbol": "AAPL",
            "price": 150.0,
            "forwardPE": 25.0,
            "trailingPE": 23.0,
            "priceToBook": 5.0,
            "earningsQuarterlyGrowth": 0.15,
            "trailingEps": 6.0,
            "dividendYield": 0.02,
            "debtToEquity": 0.3,
            "totalCurrentAssets": 2000000000,
            "totalCurrentLiabilities": 1000000000,
            "totalLiabilities": 1500000000,
            "marketCap": 2500000000000,
            "sector": "Technology",
            "industry": "Consumer Electronics"
        }
    
    def test_calc_pe(self):
        """Test P/E calculation"""
        pe = calc_pe(self.sample_data)
        self.assertEqual(pe, 25.0)  # Should prefer forwardPE
    
    def test_calc_pb(self):
        """Test P/B calculation"""
        pb = calc_pb(self.sample_data)
        self.assertEqual(pb, 5.0)
    
    def test_calc_intrinsic_value(self):
        """Test intrinsic value calculation"""
        iv = calc_intrinsic_value(self.sample_data)
        # IV = EPS * (8.5 + 2 * growth)
        # IV = 6.0 * (8.5 + 2 * 15) = 6.0 * 38.5 = 231.0
        self.assertEqual(iv, 231.0)
    
    def test_graham_metrics(self):
        """Test complete Graham metrics calculation"""
        metrics = graham_metrics(self.sample_data)
        
        # Check that all expected metrics are present
        expected_metrics = [
            "P/E", "P/B", "EPS_Growth_10Y_%", "Earnings_Stability_10Y",
            "Debt/Equity", "Current_Ratio", "Dividend_Record_Years",
            "Dividend_Yield_%", "Intrinsic_Value", "Margin_of_Safety_%",
            "Net_Net_Value", "NetNet_Buy_Candidate", "NetNet_Comment",
            "Graham_Combined_Test", "Expected_Return_%"
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
        
        # Check specific values
        self.assertEqual(metrics["P/E"], 25.0)
        self.assertEqual(metrics["P/B"], 5.0)
        self.assertEqual(metrics["Intrinsic_Value"], 231.0)
        self.assertEqual(metrics["sector"], "Technology")

if __name__ == '__main__':
    unittest.main()
