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

app = Flask(__name__, template_folder='templates')

# Try to load configuration, but don't fail if it's not available
config = {}
create_combined_report = None

try:
    from config import load_config, startup_warnings
    config = load_config()
except Exception as e:
    print(f"Warning: Could not load config: {e}")

try:
    from core.finnhub_api import set_api_key
    if config.get('FINNHUB_API_KEY'):
        set_api_key(config['FINNHUB_API_KEY'])
except Exception as e:
    print(f"Warning: Could not set API key: {e}")

try:
    from reports.combined_report_generator import create_combined_report
except Exception as e:
    print(f"Warning: Could not import report generator: {e}")
    create_combined_report = None

@app.route('/')
def index():
    """Welcome page matching the photo graphics"""
    try:
        # Check if template exists
        template_path = PROJECT_ROOT / "templates" / "welcome.html"
        if not template_path.exists():
            return f"Welcome to Investo! (Template file not found: {template_path})", 200
        
        return render_template('welcome.html')
    except Exception as e:
        # Return a simple HTML page instead of just text
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Investo - Smart Stock Analysis</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: white; padding: 50px; text-align: center; }}
                h1 {{ color: #ffa500; font-size: 3rem; margin-bottom: 20px; }}
                p {{ font-size: 1.2rem; margin-bottom: 10px; }}
                .error {{ color: #ff6b6b; background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 20px; }}
                a {{ color: #6ad1ff; text-decoration: none; margin: 0 15px; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>Investo</h1>
            <p>Smart Stock Analysis Platform</p>
            <div class="error">
                <p>Template Error: {e}</p>
                <p>But the app is working! You can still use the analysis features:</p>
            </div>
            <div>
                <a href="/health">Health Check</a>
                <a href="/graham">Graham Analysis</a>
                <a href="/lynch">Lynch Analysis</a>
                <a href="/reddit">Reddit Analysis</a>
            </div>
        </body>
        </html>
        """, 200

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'message': 'Investo web app is running'}), 200

@app.route('/graham')
def graham_analysis():
    """Benjamin Graham analysis page"""
    try:
        return render_template('graham_analysis.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graham Analysis - Investo</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: white; padding: 50px; text-align: center; }}
                h1 {{ color: #6ad1ff; font-size: 2.5rem; margin-bottom: 20px; }}
                .error {{ color: #ff6b6b; background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 20px; }}
                a {{ color: #ffa500; text-decoration: none; margin: 0 15px; }}
            </style>
        </head>
        <body>
            <h1>Benjamin Graham Analysis</h1>
            <div class="error">
                <p>Template Error: {e}</p>
                <p>Graham analysis feature coming soon!</p>
            </div>
            <div>
                <a href="/">Home</a>
                <a href="/lynch">Lynch Analysis</a>
                <a href="/reddit">Reddit Analysis</a>
            </div>
        </body>
        </html>
        """, 200

@app.route('/lynch')
def lynch_analysis():
    """Peter Lynch analysis page"""
    try:
        return render_template('lynch_analysis.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lynch Analysis - Investo</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: white; padding: 50px; text-align: center; }}
                h1 {{ color: #ffa500; font-size: 2.5rem; margin-bottom: 20px; }}
                .error {{ color: #ff6b6b; background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 20px; }}
                a {{ color: #6ad1ff; text-decoration: none; margin: 0 15px; }}
            </style>
        </head>
        <body>
            <h1>Peter Lynch Analysis</h1>
            <div class="error">
                <p>Template Error: {e}</p>
                <p>Lynch analysis feature coming soon!</p>
            </div>
            <div>
                <a href="/">Home</a>
                <a href="/graham">Graham Analysis</a>
                <a href="/reddit">Reddit Analysis</a>
            </div>
        </body>
        </html>
        """, 200

@app.route('/reddit')
def reddit_analysis():
    """Reddit sentiment analysis page"""
    try:
        return render_template('reddit_analysis.html')
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reddit Analysis - Investo</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #0a0a0a; color: white; padding: 50px; text-align: center; }}
                h1 {{ color: #FF6B6B; font-size: 2.5rem; margin-bottom: 20px; }}
                .error {{ color: #ff6b6b; background: #2a2a2a; padding: 20px; border-radius: 10px; margin: 20px; }}
                a {{ color: #6ad1ff; text-decoration: none; margin: 0 15px; }}
            </style>
        </head>
        <body>
            <h1>Reddit Sentiment Analysis</h1>
            <div class="error">
                <p>Template Error: {e}</p>
                <p>Reddit analysis feature coming soon!</p>
            </div>
            <div>
                <a href="/">Home</a>
                <a href="/graham">Graham Analysis</a>
                <a href="/lynch">Lynch Analysis</a>
            </div>
        </body>
        </html>
        """, 200

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
        
        # Try to run full analysis if available
        try:
            if create_combined_report is not None:
                report_path = create_combined_report(symbol)
                if report_path:
                    return jsonify({
                        'success': True,
                        'message': f'Analysis complete for {symbol}!',
                        'symbol': symbol,
                        'report_path': report_path
                    })
        except Exception as analysis_error:
            print(f"Analysis failed: {analysis_error}")
        
        # Fallback to simple response
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
