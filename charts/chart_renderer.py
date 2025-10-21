"""
Chart Renderer Module
====================
Handles rendering stock charts using TradingView widget with Investo styling.
"""

from typing import Dict, Optional
import json

def render_chart_html(chart_data: Dict, symbol: str) -> str:
    """
    Generate HTML and JavaScript for rendering a TradingView stock chart.
    
    Args:
        chart_data (dict): Chart data from get_chart_data() (used for price info)
        symbol (str): Stock symbol
        
    Returns:
        str: Complete HTML section for the TradingView chart
    """
    if not chart_data:
        return render_error_chart("No chart data available")
    
    # Extract price information
    current_price = chart_data.get('current_price', 'N/A')
    price_change = chart_data.get('price_change', 0)
    price_change_pct = chart_data.get('price_change_pct', 0)
    period = chart_data.get('period', '1y')
    
    # Map period to TradingView range format
    period_map = {
        '1mo': '1M',
        '3mo': '3M',
        '6mo': '6M',
        '1y': '12M',
        '2y': '24M',
        '5y': '60M',
        'ytd': 'YTD',
        'max': 'ALL'
    }
    tv_range = period_map.get(period, '12M')
    
    html = f"""
    <!-- Stock Price Chart Section - TradingView Widget -->
    <div class="chart-section">
        <h2>Stock Price Chart</h2>
        <div class="chart-info">
            <div class="price-info">
                <span class="current-price">${current_price}</span>
                <span class="price-change {'positive' if price_change >= 0 else 'negative'}">
                    {price_change:+.2f} ({price_change_pct:+.2f}%)
                </span>
            </div>
            <div class="period-info">
                <span class="chart-symbol">Symbol: {symbol}</span>
            </div>
        </div>
        
        <!-- TradingView Widget Container -->
        <div class="tradingview-widget-container">
            <div id="tradingview_chart"></div>
            <div id="chart-loading" class="chart-loading">
                <div class="loading-spinner"></div>
                <p>Loading TradingView chart...</p>
            </div>
        </div>
    </div>
    
    <!-- TradingView Widget Script -->
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        // Initialize TradingView widget when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Initializing TradingView chart for {symbol}');
            
            try {{
                // Hide loading spinner after a delay
                setTimeout(function() {{
                    const loading = document.getElementById('chart-loading');
                    if (loading) {{
                        loading.style.display = 'none';
                    }}
                }}, 2000);
                
                // Initialize TradingView widget
                new TradingView.widget({{
                    "container_id": "tradingview_chart",
                    "width": "100%",
                    "height": 480,
                    "symbol": "NASDAQ:{symbol}",
                    "interval": "D",
                    "timezone": "Etc/UTC",
                    "theme": "dark",
                    "style": "1",
                    "locale": "en",
                    "toolbar_bg": "#181818",
                    "enable_publishing": false,
                    "range": "{tv_range}",
                    "hide_top_toolbar": false,
                    "hide_legend": false,
                    "save_image": false,
                    "backgroundColor": "#181818",
                    "gridColor": "#333333",
                    "hide_side_toolbar": false,
                    "allow_symbol_change": true,
                    "studies": [],
                    "show_popup_button": false,
                    "popup_width": "1000",
                    "popup_height": "650",
                    "support_host": "https://www.tradingview.com"
                }});
                
                console.log('TradingView widget initialized successfully');
                
            }} catch (error) {{
                console.error('Error initializing TradingView widget:', error);
                const loading = document.getElementById('chart-loading');
                if (loading) {{
                    loading.innerHTML = '<p style="color: #ff6b6b;">Failed to load chart. Please refresh the page.</p>';
                }}
            }}
        }});
    </script>
    """
    
    return html

def render_error_chart(error_message: str = "Chart data unavailable") -> str:
    """
    Render an error state for the chart.
    
    Args:
        error_message (str): Error message to display
        
    Returns:
        str: HTML for error state
    """
    return f"""
    <!-- Stock Price Chart Section - Error State -->
    <div class="chart-section">
        <h2>Stock Price Chart</h2>
        <div class="chart-container">
            <div style="color: #ff6b6b; text-align: center; padding: 40px; background: #1a1a1a; border-radius: 8px;">
                <h3>Chart Unavailable</h3>
                <p>{error_message}</p>
            </div>
        </div>
    </div>
    """

def get_chart_css() -> str:
    """
    Get CSS styles for the TradingView chart.
    
    Returns:
        str: CSS styles for chart components with Investo styling
    """
    return """
    /* Chart styling - Investo Style */
    .chart-section {
        background: #1b1b1b; 
        border: 2px solid #FFA500; 
        border-radius: 12px; 
        padding: 1.5em; 
        margin: 2em 0;
        box-shadow: 0 4px 16px rgba(255, 165, 0, 0.1);
    }
    .chart-section h2 { 
        margin-top: 0; 
        color: #FFA500; 
        font-size: 1.8em;
        margin-bottom: 1em;
    }
    .chart-info {
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 1.5em; 
        flex-wrap: wrap;
        padding: 1em;
        background: #0a0a0a;
        border-radius: 8px;
        border: 1px solid #333;
    }
    .price-info {
        display: flex; 
        align-items: center; 
        gap: 15px;
    }
    .current-price {
        font-size: 2em; 
        font-weight: bold; 
        color: #FFA500;
        text-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
    }
    .price-change {
        font-size: 1.2em; 
        font-weight: bold;
        padding: 0.3em 0.8em;
        border-radius: 6px;
    }
    .price-change.positive { 
        color: #00FF00; 
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid #00FF00;
    }
    .price-change.negative { 
        color: #FF3C00; 
        background: rgba(255, 60, 0, 0.1);
        border: 1px solid #FF3C00;
    }
    .period-info {
        color: #aaa; 
        font-size: 0.95em;
    }
    .chart-symbol {
        color: #6ad1ff;
        font-weight: 600;
    }
    
    /* TradingView Widget Container */
    .tradingview-widget-container {
        position: relative; 
        height: 480px; 
        width: 100%; 
        margin: 1em 0; 
        background: #181818; 
        border: 1px solid #333; 
        border-radius: 8px; 
        overflow: hidden;
    }
    #tradingview_chart {
        width: 100%;
        height: 100%;
    }
    
    /* Loading State */
    .chart-loading {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #181818;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    .chart-loading p {
        color: #FFA500;
        font-size: 1.1em;
        margin-top: 1em;
    }
    
    /* Loading Spinner */
    .loading-spinner {
        border: 4px solid #333;
        border-top: 4px solid #FFA500;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    """

