"""
Simple Flask test to debug the issue
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

app = Flask(__name__)

@app.route('/')
def index():
    """Welcome page matching the photo graphics"""
    return render_template('welcome.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Simple test analyze endpoint"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper().strip()
        
        if not symbol:
            return jsonify({'error': 'Please enter a valid ticker symbol'}), 400
            
        if len(symbol) > 10:
            return jsonify({'error': 'Ticker symbol seems too long. Please enter a valid ticker (e.g., TSLA, AAPL).'}), 400
        
        # Simple test response
        return jsonify({
            'success': True,
            'message': f'Test analysis complete for {symbol}!',
            'symbol': symbol,
            'test_data': {
                'price': '$150.00',
                'pe_ratio': '25.5',
                'sentiment': 'Bullish'
            }
        })
            
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
