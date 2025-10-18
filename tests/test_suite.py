"""
Test suite for Investo
"""

import unittest
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import test modules
from tests.test_lynch import TestLynchAnalysis
from tests.test_graham import TestGrahamAnalysis
from tests.test_sentiment import TestSentimentAnalysis
from tests.test_utils import TestHelpers, TestBudget

def create_test_suite():
    """Create comprehensive test suite"""
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestLynchAnalysis))
    suite.addTest(unittest.makeSuite(TestGrahamAnalysis))
    suite.addTest(unittest.makeSuite(TestSentimentAnalysis))
    suite.addTest(unittest.makeSuite(TestHelpers))
    suite.addTest(unittest.makeSuite(TestBudget))
    
    return suite

def run_tests():
    """Run all tests"""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
