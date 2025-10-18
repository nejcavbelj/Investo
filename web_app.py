"""
Investo Web Application for Railway Deployment
=============================================
Simple Flask web interface for the Investo investment analysis system.
"""

import os
import webbrowser
from flask import Flask, render_template_string, request, jsonify, send_file
from pathlib import Path
import threading
import time

from config import load_config, startup_warnings
from core.finnhub_api import set_api_key
from reports.combined_report_generator import create_combined_report

app = Flask(__name__)

# Global variables for configuration
config = None
api_configured = False

def initialize_app():
    """Initialize the application with configuration"""
    global config, api_configured
    
    try:
        config = load_config()
        set_api_key(config['FINNHUB_API_KEY'])
        api_configured = True
        print("✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        api_configured = False

# Initialize on startup
initialize_app()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Investo - Investment Analysis</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #bdc3c7;
            cursor: not-allowed;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            display: none;
        }
        .status.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .features {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .features h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        .features ul {
            color: #34495e;
        }
        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Investo Investment Analysis</h1>
        
        <form id="analysisForm">
            <div class="form-group">
                <label for="symbol">Stock Symbol:</label>
                <input type="text" id="symbol" name="symbol" placeholder="e.g., AAPL, MSFT, GOOGL, TSLA" required>
            </div>
            <button type="submit" id="analyzeBtn">Analyze Stock</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating analysis report...</p>
        </div>
        
        <div class="status" id="status"></div>
        
        <div class="features">
            <h3>📈 What you'll get:</h3>
            <ul>
                <li><strong>Benjamin Graham Value Analysis</strong> - Fundamental value assessment</li>
                <li><strong>Peter Lynch Growth Analysis</strong> - Growth potential evaluation</li>
                <li><strong>Reddit Sentiment Analysis</strong> - Social media sentiment insights</li>
                <li><strong>Combined Investment Verdict</strong> - Comprehensive recommendation</li>
            </ul>
        </div>
    </div>

    <script>
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const symbol = document.getElementById('symbol').value.toUpperCase();
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const status = document.getElementById('status');
            
            // Show loading state
            analyzeBtn.disabled = true;
            loading.style.display = 'block';
            status.style.display = 'none';
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symbol: symbol })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    status.className = 'status success';
                    status.innerHTML = `
                        <strong>✅ Analysis Complete!</strong><br>
                        Report generated for ${symbol}. 
                        <a href="/download/${result.report_filename}" target="_blank">Download Report</a>
                    `;
                } else {
                    status.className = 'status error';
                    status.innerHTML = `<strong>❌ Error:</strong> ${result.error}`;
                }
            } catch (error) {
                status.className = 'status error';
                status.innerHTML = `<strong>❌ Error:</strong> Failed to analyze stock. Please try again.`;
            } finally {
                analyzeBtn.disabled = false;
                loading.style.display = 'none';
                status.style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    """Analyze a stock and generate report"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper().strip()
        
        if not symbol:
            return jsonify({'success': False, 'error': 'Please provide a stock symbol'})
        
        if not api_configured:
            return jsonify({'success': False, 'error': 'API configuration not available'})
        
        # Generate the report
        report_path = create_combined_report(symbol)
        
        if report_path and Path(report_path).exists():
            report_filename = Path(report_path).name
            return jsonify({
                'success': True, 
                'report_filename': report_filename,
                'message': f'Analysis complete for {symbol}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to generate report'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download_report(filename):
    """Download generated report"""
    try:
        reports_dir = Path('reports/generated')
        file_path = reports_dir / filename
        
        if file_path.exists():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'api_configured': api_configured,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
