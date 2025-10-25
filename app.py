"""
Investo Web Application
======================
Flask web application for Railway deployment with welcome page and stock analysis.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

app = Flask(__name__, template_folder=str(PROJECT_ROOT / 'templates'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Register feedback blueprint
from core.feedback_handler import feedback_bp
app.register_blueprint(feedback_bp)


# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Register feedback blueprint
try:
    from core.feedback_handler import feedback_bp
    app.register_blueprint(feedback_bp)
    print("✓ Feedback handler registered")
except Exception as e:
    print(f"✗ Warning: Could not register feedback handler: {e}")

# Try to load configuration, but don't fail if it's not available
config = {}
create_combined_report = None

print("=" * 60)
print("Initializing Investo Flask App...")
print("=" * 60)

try:
    from config import load_config, startup_warnings
    config = load_config()
    print("✓ Configuration loaded successfully")
except Exception as e:
    print(f"✗ Warning: Could not load config: {e}")
    import traceback
    traceback.print_exc()

try:
    from core.finnhub_api import set_api_key
    if config.get('FINNHUB_API_KEY'):
        set_api_key(config['FINNHUB_API_KEY'])
        print("✓ Finnhub API key configured")
    else:
        print("✗ Warning: FINNHUB_API_KEY not found in config")
except Exception as e:
    print(f"✗ Warning: Could not set API key: {e}")
    import traceback
    traceback.print_exc()

try:
    from reports.combined_report_generator import create_combined_report
    print("✓ Report generator imported successfully")
except Exception as e:
    print(f"✗ ERROR: Could not import report generator: {e}")
    import traceback
    traceback.print_exc()
    create_combined_report = None

print("=" * 60)
if create_combined_report:
    print("STATUS: Report generator is READY")
else:
    print("STATUS: Report generator is NOT AVAILABLE")
print("=" * 60)

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
    return {"status": "ok"}, 200

@app.route('/status')
def status_check():
    """Diagnostic endpoint to check system status"""
    status = {
        "app": "running",
        "config_loaded": bool(config),
        "report_generator": "available" if create_combined_report else "unavailable",
        "required_env_vars": {
            "FINNHUB_API_KEY": "set" if os.getenv("FINNHUB_API_KEY") else "missing",
            "OPENAI_API_KEY": "set" if os.getenv("OPENAI_API_KEY") else "missing",
            "REDDIT_CLIENT_ID": "set" if os.getenv("REDDIT_CLIENT_ID") else "missing",
            "REDDIT_CLIENT_SECRET": "set" if os.getenv("REDDIT_CLIENT_SECRET") else "missing",
            "REDDIT_USER_AGENT": "set" if os.getenv("REDDIT_USER_AGENT") else "missing",
        },
        "optional_features": {
            "feedback_email": "enabled" if os.getenv("GMAIL_APP_PASSWORD") else "disabled (saves to file only)",
            "flask_sessions": "enabled" if os.getenv("FLASK_SECRET_KEY") else "using default key"
        }
    }
    return status, 200

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
    print(f"\n{'='*60}")
    print(f"Received analysis request")
    print(f"{'='*60}")
    try:
        data = request.get_json()
        print(f"Request data: {data}")
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({'error': 'Invalid request. Please send JSON data.'}), 400
            
        symbol = data.get('symbol', '').upper().strip()
        print(f"Analyzing symbol: {symbol}")
        
        if not symbol:
            return jsonify({'error': 'Please enter a valid ticker symbol'}), 400
            
        if len(symbol) > 10:
            return jsonify({'error': 'Ticker symbol seems too long. Please enter a valid ticker (e.g., TSLA, AAPL).'}), 400
        
        # Try to run full analysis if available
        if create_combined_report is not None:
            try:
                report_path = create_combined_report(symbol)
                if report_path:
                    return jsonify({
                        'success': True,
                        'message': f'Analysis complete for {symbol}!',
                        'symbol': symbol,
                        'report_path': str(report_path)
                    }), 200
                else:
                    return jsonify({
                        'error': f'Could not generate report for {symbol}. The ticker may not exist or data may be unavailable.'
                    }), 400
            except Exception as analysis_error:
                print(f"Analysis failed for {symbol}: {analysis_error}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'error': f'Analysis failed: {str(analysis_error)}'
                }), 500
        else:
            # Fallback when report generator is not available
            return jsonify({
                'success': True,
                'message': f'Analysis system is initializing for {symbol}. Please check back in a moment.',
                'symbol': symbol
            }), 200
            
    except Exception as e:
        print(f"Unexpected error in /analyze: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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
