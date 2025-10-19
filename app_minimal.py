"""
Minimal Investo Web Application for Railway
==========================================
Simplified version that will definitely work on Railway.
"""

from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    """Welcome page matching the photo graphics"""
    try:
        return render_template('welcome.html')
    except Exception as e:
        return f"Welcome to Investo! (Template error: {e})", 200

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'message': 'Investo web app is running'}), 200

@app.route('/graham')
def graham_analysis():
    """Benjamin Graham analysis page"""
    try:
        return render_template('graham_simple.html')
    except Exception as e:
        return f"Graham Analysis Page (Template error: {e})", 200

@app.route('/lynch')
def lynch_analysis():
    """Peter Lynch analysis page"""
    try:
        return render_template('lynch_simple.html')
    except Exception as e:
        return f"Lynch Analysis Page (Template error: {e})", 200

@app.route('/reddit')
def reddit_analysis():
    """Reddit sentiment analysis page"""
    try:
        return render_template('reddit_simple.html')
    except Exception as e:
        return f"Reddit Analysis Page (Template error: {e})", 200

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze stock and return results"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper().strip()
        
        if not symbol:
            return jsonify({'error': 'Please enter a valid ticker symbol'}), 400
            
        if len(symbol) > 10:
            return jsonify({'error': 'Ticker symbol seems too long. Please enter a valid ticker (e.g., TSLA, AAPL).'}), 400
        
        return jsonify({
            'success': True,
            'message': f'Analysis request received for {symbol}!',
            'symbol': symbol,
            'note': 'Web interface is working! Full analysis feature coming soon.'
        })
            
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
