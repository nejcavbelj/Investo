# Charts Module

Professional stock chart integration for Investo using TradingView widgets.

## Overview

This module provides TradingView-powered interactive stock charts with Investo's custom styling and branding.

## Structure

```
charts/
├── __init__.py          # Module initialization
├── chart_data.py        # Stock data fetching and processing
├── chart_renderer.py    # TradingView widget HTML/CSS generation
└── README.md           # This file
```

## Features

### TradingView Integration
- **Professional Charts**: Industry-standard TradingView widgets
- **Interactive**: Full charting tools, indicators, and drawing tools
- **Real-time Data**: Live market data from TradingView
- **Dark Theme**: Matches Investo's dark color scheme

### Investo Styling
- **Orange Accent**: Primary color #FFA500 (Investo brand)
- **Dark Background**: #181818 (matches Investo theme)
- **Custom Borders**: 2px orange borders with glow effects
- **Price Display**: Large, prominent price with change indicators
- **Loading Animation**: Branded spinner with orange accent

### Data Processing
- **yfinance Integration**: Fetches historical data for price calculations
- **Price Changes**: Calculates 1-year price change and percentage
- **Multi-Period Support**: 1M, 3M, 6M, 1Y, 2Y, 5Y, YTD, ALL
- **Error Handling**: Graceful fallbacks for data issues

## Usage

### Basic Usage

```python
from charts.chart_data import get_chart_data
from charts.chart_renderer import render_chart_html, get_chart_css

# Fetch chart data
chart_data = get_chart_data('AAPL', '1y')

# Generate chart HTML
chart_html = render_chart_html(chart_data, 'AAPL')
chart_css = get_chart_css()

# Use in template
template.render(
    chart_html=chart_html,
    chart_css=chart_css
)
```

### In Reports

The chart module is automatically integrated into combined reports:

```python
from reports.combined_report_generator import create_combined_report

# Chart is automatically included at the top
create_combined_report('AAPL')
```

## API Reference

### `chart_data.py`

#### `get_chart_data(symbol: str, period: str = "1y") -> Optional[Dict]`
Fetches historical stock data from yfinance.

**Parameters:**
- `symbol`: Stock ticker symbol (e.g., 'AAPL')
- `period`: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max')

**Returns:**
```python
{
    'dates': [...],              # List of date strings
    'prices': [...],             # List of closing prices
    'volumes': [...],            # List of volumes
    'highs': [...],              # List of daily highs
    'lows': [...],               # List of daily lows
    'period': '1y',              # Selected period
    'symbol': 'AAPL',            # Stock symbol
    'price_change': 26.86,       # Price change in dollars
    'price_change_pct': 11.41,   # Price change in percentage
    'current_price': 262.24,     # Most recent price
    'data_points': 250           # Number of data points
}
```

### `chart_renderer.py`

#### `render_chart_html(chart_data: Dict, symbol: str) -> str`
Generates TradingView widget HTML with Investo styling.

**Parameters:**
- `chart_data`: Data from `get_chart_data()`
- `symbol`: Stock ticker symbol

**Returns:**
- Complete HTML with TradingView widget and initialization script

#### `get_chart_css() -> str`
Returns CSS styles for the chart section.

**Returns:**
- CSS string with Investo-branded styling

#### `render_error_chart(error_message: str) -> str`
Renders an error state when chart data is unavailable.

## TradingView Widget Configuration

The widget is configured with these settings:

```javascript
{
    "container_id": "tradingview_chart",
    "width": "100%",
    "height": 480,
    "symbol": "NASDAQ:AAPL",       // Auto-prefixed with exchange
    "interval": "D",               // Daily candles
    "timezone": "Etc/UTC",
    "theme": "dark",               // Dark theme
    "style": "1",                  // Candle style
    "toolbar_bg": "#181818",       // Investo background
    "backgroundColor": "#181818",   // Chart background
    "gridColor": "#333333",        // Grid lines
    "range": "12M",                // Default 1 year
    "allow_symbol_change": true    // User can search stocks
}
```

## Styling

### Colors
- **Primary (Orange)**: `#FFA500` - Headers, price, accents
- **Green**: `#00FF00` - Positive changes
- **Red**: `#FF3C00` - Negative changes
- **Background**: `#181818` - Main background
- **Panel**: `#1b1b1b` - Section background
- **Border**: `#333` - Subtle borders

### Components
- **Chart Section**: Orange border with glow effect
- **Price Display**: Large, bold orange text
- **Change Badge**: Green/red with matching background
- **Loading Spinner**: Rotating orange spinner
- **TradingView Container**: 480px height, rounded corners

## Error Handling

The module handles errors gracefully:

1. **Data Fetch Errors**: Returns `None`, triggers error chart
2. **Widget Load Errors**: Shows error message in chart container
3. **Invalid Symbols**: TradingView shows search interface
4. **Network Issues**: Loading state with error feedback

## Dependencies

- `yfinance`: Stock data fetching
- `typing`: Type hints
- `json`: Data serialization
- TradingView: External widget library (CDN)

## Integration

Charts are automatically integrated into the combined report template:

1. Data fetched in `get_stock_package()`
2. HTML generated in `create_combined_report()`
3. Rendered at top of report (after company info)
4. CSS injected into template styles
5. TradingView script loads on page load

## Future Enhancements

- [ ] Period selection buttons (requires backend API)
- [ ] Multiple timeframe tabs
- [ ] Technical indicators presets
- [ ] Save chart preferences
- [ ] Export chart images
- [ ] Compare multiple stocks

## Troubleshooting

**Chart not loading?**
- Check browser console for errors
- Verify internet connection (TradingView CDN required)
- Check if symbol is valid on NASDAQ/NYSE

**Wrong exchange?**
- Update symbol prefix in `chart_renderer.py`
- Example: `NYSE:`, `NASDAQ:`, `AMEX:`

**Styling issues?**
- Ensure `chart_css` is injected into template
- Check CSS variable definitions in main template
- Verify no CSS conflicts with other styles

## License

Part of the Investo project.
