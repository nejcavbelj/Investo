"""
Unit tests for sentiment analysis
"""

import unittest
from unittest.mock import patch, MagicMock
from core.reddit_sentiment import get_reddit_sentiment_summary

class TestSentimentAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_ticker = "AAPL"
    
    @patch('core.reddit_sentiment.reddit')
    @patch('core.reddit_sentiment.analyzer')
    def test_reddit_sentiment_no_api(self, mock_analyzer, mock_reddit):
        """Test Reddit sentiment when API is not available"""
        mock_reddit = None
        mock_analyzer = None
        
        result = get_reddit_sentiment_summary(self.sample_ticker)
        
        self.assertEqual(result["ticker"], self.sample_ticker)
        self.assertIn("Reddit API not available", result["summary"])
    
    @patch('core.reddit_sentiment.reddit')
    @patch('core.reddit_sentiment.analyzer')
    def test_reddit_sentiment_no_posts(self, mock_analyzer, mock_reddit):
        """Test Reddit sentiment when no posts are found"""
        # Mock Reddit API
        mock_subreddit = MagicMock()
        mock_subreddit.search.return_value = []
        mock_reddit.subreddit.return_value = mock_subreddit
        
        # Mock analyzer
        mock_analyzer.polarity_scores.return_value = {"compound": 0.0}
        
        result = get_reddit_sentiment_summary(self.sample_ticker)
        
        self.assertEqual(result["ticker"], self.sample_ticker)
        self.assertIn("No relevant Reddit posts found", result["summary"])
    
    def test_sentiment_classification(self):
        """Test sentiment classification logic"""
        from core.reddit_sentiment import classify_sentiment
        
        self.assertEqual(classify_sentiment(0.3), "Bullish")
        self.assertEqual(classify_sentiment(-0.3), "Bearish")
        self.assertEqual(classify_sentiment(0.1), "Neutral")
        self.assertEqual(classify_sentiment(-0.1), "Neutral")

if __name__ == '__main__':
    unittest.main()
