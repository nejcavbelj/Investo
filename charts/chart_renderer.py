"""
Chart Renderer Module
====================
Handles rendering stock charts using Chart.js with proper HTML and JavaScript.
"""

from typing import Dict, Optional
import json

def render_chart_html(chart_data: Dict, symbol: str) -> str:
    """
    Generate HTML and JavaScript for rendering a stock chart.
    
    Args:
        chart_data (dict): Chart data from get_chart_data()
        symbol (str): Stock symbol
        
    Returns:
        str: Complete HTML section for the chart
    """
    if not chart_data:
        return render_error_chart("No chart data available")
    
    # Convert chart data to JSON for JavaScript
    chart_data_json = json.dumps(chart_data, indent=2)
    
    html = f"""
    <!-- Stock Price Chart Section -->
    <div class="chart-section">
        <h2>Stock Price Chart</h2>
        <div class="chart-info">
            <div class="price-info">
                <span class="current-price">${chart_data.get('current_price', 'N/A')}</span>
                <span class="price-change {'positive' if chart_data.get('price_change', 0) >= 0 else 'negative'}">
                    {chart_data.get('price_change', 0):+.2f} ({chart_data.get('price_change_pct', 0):+.2f}%)
                </span>
            </div>
            <div class="period-info">
                <span>Period: {chart_data.get('period', '1y')} | Data Points: {chart_data.get('data_points', 0)}</span>
            </div>
        </div>
        <div class="chart-controls">
            <button onclick="updateChart('1mo')" class="period-btn" data-period="1mo">1 Month</button>
            <button onclick="updateChart('3mo')" class="period-btn" data-period="3mo">3 Months</button>
            <button onclick="updateChart('6mo')" class="period-btn" data-period="6mo">6 Months</button>
            <button onclick="updateChart('1y')" class="period-btn active" data-period="1y">1 Year</button>
            <button onclick="updateChart('2y')" class="period-btn" data-period="2y">2 Years</button>
            <button onclick="updateChart('5y')" class="period-btn" data-period="5y">5 Years</button>
        </div>
        <div class="chart-container">
            <canvas id="stockChart"></canvas>
            <div id="chart-error" style="display: none; color: #ff6b6b; text-align: center; padding: 20px;">
                Chart failed to load. Please refresh the page or check your internet connection.
            </div>
        </div>
    </div>
    
    <script>
        // Chart data from server
        const chartData = {chart_data_json};
        const symbol = '{symbol}';
        let stockChart = null;
        
        // Initialize chart when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, initializing chart for', symbol);
            
            if (chartData && typeof Chart !== 'undefined') {{
                console.log('Chart data available, Chart.js loaded');
                initializeChart();
            }} else {{
                console.error('Chart data or Chart.js not available');
                if (!chartData) {{
                    console.error('No chart data');
                }}
                if (typeof Chart === 'undefined') {{
                    console.error('Chart.js not loaded');
                }}
                document.getElementById('chart-error').style.display = 'block';
            }}
        }});
        
        function initializeChart() {{
            try {{
                console.log('Initializing chart for', symbol);
                
                const canvas = document.getElementById('stockChart');
                if (!canvas) {{
                    console.error('Canvas element not found!');
                    document.getElementById('chart-error').style.display = 'block';
                    return;
                }}
                
                console.log('Canvas found, creating chart...');
                const ctx = canvas.getContext('2d');
                
                // Determine chart colors based on performance
                const firstPrice = chartData.prices[0];
                const lastPrice = chartData.prices[chartData.prices.length - 1];
                const isPositive = lastPrice >= firstPrice;
                const lineColor = isPositive ? '#00FF00' : '#FF3C00';
                const fillColor = isPositive ? 'rgba(0, 255, 0, 0.1)' : 'rgba(255, 60, 0, 0.1)';
                
                console.log('Chart colors:', lineColor, fillColor);
                
                stockChart = new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: chartData.dates,
                        datasets: [{{
                            label: `${{symbol}} Price`,
                            data: chartData.prices,
                            borderColor: lineColor,
                            backgroundColor: fillColor,
                            borderWidth: 2,
                            fill: true,
                            tension: 0.1,
                            pointRadius: 0,
                            pointHoverRadius: 6,
                            pointHoverBackgroundColor: lineColor,
                            pointHoverBorderColor: '#fff',
                            pointHoverBorderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: true,
                                labels: {{
                                    color: '#fff',
                                    font: {{
                                        size: 14
                                    }}
                                }}
                            }},
                            tooltip: {{
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleColor: '#FFA500',
                                bodyColor: '#fff',
                                borderColor: '#FFA500',
                                borderWidth: 1,
                                callbacks: {{
                                    label: function(context) {{
                                        return `${{symbol}}: ${{context.parsed.y.toFixed(2)}}`;
                                    }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{
                                grid: {{
                                    color: '#333',
                                    drawBorder: false
                                }},
                                ticks: {{
                                    color: '#aaa',
                                    maxTicksLimit: 8
                                }}
                            }},
                            y: {{
                                grid: {{
                                    color: '#333',
                                    drawBorder: false
                                }},
                                ticks: {{
                                    color: '#aaa',
                                    callback: function(value) {{
                                        return '$' + value.toFixed(2);
                                    }}
                                }}
                            }}
                        }},
                        interaction: {{
                            intersect: false,
                            mode: 'index'
                        }}
                    }}
                }});
                
                console.log('Chart created successfully:', stockChart);
                
            }} catch (error) {{
                console.error('Error creating chart:', error);
                document.getElementById('chart-error').style.display = 'block';
            }}
        }}
        
        async function updateChart(period) {{
            console.log('Updating chart to period:', period);
            
            // Update button states
            document.querySelectorAll('.period-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.querySelector(`[data-period="${{period}}"]`).classList.add('active');
            
            // For now, show a message that this requires backend implementation
            alert(`Chart period update to ${{period}} requires backend API implementation. Currently showing ${{chartData.period}} data.`);
        }}
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
    Get CSS styles for the chart.
    
    Returns:
        str: CSS styles for chart components
    """
    return """
    /* Chart styling */
    .chart-section {
        background: #1b1b1b; border: 1px solid var(--line); border-radius: 8px; padding: 1.5em; margin: 2em 0;
    }
    .chart-section h2 { margin-top: 0; color: var(--orange); }
    .chart-info {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 1em; flex-wrap: wrap;
    }
    .price-info {
        display: flex; align-items: center; gap: 10px;
    }
    .current-price {
        font-size: 1.5em; font-weight: bold; color: var(--orange);
    }
    .price-change {
        font-size: 1em; font-weight: bold;
    }
    .price-change.positive { color: var(--green); }
    .price-change.negative { color: var(--red); }
    .period-info {
        color: var(--muted); font-size: 0.9em;
    }
    .chart-container {
        position: relative; height: 400px; width: 100%; margin: 1em 0; 
        background: #0a0a0a; border: 1px solid #333; border-radius: 8px; padding: 10px;
    }
    .chart-controls {
        display: flex; gap: 10px; margin-bottom: 1em; flex-wrap: wrap;
    }
    .chart-controls button {
        background: var(--panel); border: 1px solid var(--line); color: var(--ink); 
        padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: all 0.2s;
    }
    .chart-controls button:hover { background: var(--orange); color: var(--bg); }
    .chart-controls button.active { background: var(--orange); color: var(--bg); }
    """
