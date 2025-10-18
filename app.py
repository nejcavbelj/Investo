"""
Investo Web Application
======================
Flask web application for Railway deployment with welcome page and stock analysis.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import load_config, startup_warnings
from core.finnhub_api import set_api_key
from reports.combined_report_generator import create_combined_report

app = Flask(__name__)

# Load configuration
config = load_config()
set_api_key(config['FINNHUB_API_KEY'])

@app.route('/')
def index():
    """Welcome page matching the photo graphics"""
    return render_template('welcome.html')

@app.route('/graham')
def graham_analysis():
    """Benjamin Graham analysis page"""
    return render_template('graham_simple.html')

@app.route('/lynch')
def lynch_analysis():
    """Peter Lynch analysis page"""
    return render_template('lynch_simple.html')

@app.route('/reddit')
def reddit_analysis():
    """Reddit sentiment analysis page"""
    return render_template('reddit_simple.html')

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
        
        # For now, return a simple success message
        # The full analysis can be implemented later
        return jsonify({
            'success': True,
            'message': f'Analysis request received for {symbol}!',
            'symbol': symbol,
            'note': 'Full analysis feature coming soon. Use the terminal version for complete analysis.'
        })
            
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/report/<path:filename>')
def serve_report(filename):
    """Serve generated reports"""
    reports_dir = PROJECT_ROOT / "reports" / "generated"
    file_path = reports_dir / filename
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        return "Report not found", 404

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = PROJECT_ROOT / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
