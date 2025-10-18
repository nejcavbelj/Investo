# Investo Web Interface - Separate Analysis Sections

## Overview
The web interface has been reorganized into separate HTML files for each analysis section, allowing you to edit and inspect each section individually in Cursor.

## Available Routes

### 1. Welcome Page
- **URL**: `http://localhost:5000/`
- **File**: `templates/welcome.html`
- **Description**: Main welcome page matching the photo design with ticker input form

### 2. Benjamin Graham Analysis
- **URL**: `http://localhost:5000/graham`
- **File**: `templates/graham_simple.html`
- **Description**: Value investing analysis with P/E, P/B, debt ratios, and Graham criteria

### 3. Peter Lynch Analysis
- **URL**: `http://localhost:5000/lynch`
- **File**: `templates/lynch_simple.html`
- **Description**: Growth investing analysis with PEG ratios, ROE, ROA, and growth metrics

### 4. Reddit Sentiment Analysis
- **URL**: `http://localhost:5000/reddit`
- **File**: `templates/reddit_simple.html`
- **Description**: Social sentiment analysis with Reddit metrics, buzz ratio, and sentiment indicators

## How to Use

### Running the Web Interface
```bash
python app.py
```

### Accessing Individual Sections
1. **Welcome Page**: Open `http://localhost:5000/` in your browser
2. **Graham Analysis**: Open `http://localhost:5000/graham` in a new tab
3. **Lynch Analysis**: Open `http://localhost:5000/lynch` in a new tab
4. **Reddit Analysis**: Open `http://localhost:5000/reddit` in a new tab

### Navigation
Each page includes navigation links at the top to easily switch between sections:
- **Welcome** (orange) - Main page
- **Graham Analysis** (blue) - Value investing metrics
- **Lynch Analysis** (orange) - Growth investing metrics
- **Reddit Analysis** (pink) - Social sentiment metrics

## File Structure

```
templates/
├── welcome.html          # Main welcome page (matches photo design)
├── graham_simple.html    # Benjamin Graham analysis section
├── lynch_simple.html     # Peter Lynch analysis section
├── reddit_simple.html    # Reddit sentiment analysis section
└── base_styles.html      # Shared CSS styles (not used in simple versions)
```

## Editing Interface

### In Cursor
1. **Open each HTML file** in Cursor for editing
2. **Preview changes** by refreshing the corresponding URL in your browser
3. **Test navigation** between sections using the links

### Visual Inspection
- Each section can be opened in a **separate browser tab**
- **Real-time editing** - changes are visible immediately after refresh
- **Independent styling** - each section has its own complete CSS

## Features

### Graham Analysis (`/graham`)
- P/E Ratio analysis with Graham criteria
- P/B Ratio evaluation
- Debt-to-Equity assessment
- Current Ratio analysis
- Dividend record tracking
- Graham Combined Test visualization
- Margin of Safety calculations

### Lynch Analysis (`/lynch`)
- P/E Ratio for growth stocks
- PEG Ratio analysis (key Lynch metric)
- EPS Growth percentage
- ROE and ROA metrics
- Profit Margin analysis
- Growth visualization charts

### Reddit Analysis (`/reddit`)
- Reddit mentions count
- Sentiment analysis with confidence
- Buzz ratio meter
- Reliability index
- Composite Reddit score
- Sample Reddit discussions
- Sentiment visualization charts

## Styling

### Color Scheme
- **Background**: Dark (#181818)
- **Panels**: Dark gray (#222)
- **Orange**: #FFA500 (primary accent)
- **Blue**: #6ad1ff (Graham section)
- **Pink**: #FF6B6B (Reddit section)
- **Green**: #00FF00 (positive indicators)
- **Red**: #FF3C00 (negative indicators)

### Components
- **Donut charts** for visual metrics
- **Progress bars** for ratios
- **Status indicators** with color coding
- **Responsive grid** layout
- **Navigation links** for easy switching

## Development Workflow

1. **Edit HTML files** in Cursor
2. **Save changes**
3. **Refresh browser** to see updates
4. **Test navigation** between sections
5. **Iterate** on design and content

## Next Steps

- **Customize styling** for each section
- **Add real data** integration
- **Enhance visualizations**
- **Improve responsive design**
- **Add interactive features**

## Notes

- All templates use **static sample data** for demonstration
- **Navigation links** are included on each page
- **Consistent styling** across all sections
- **Ready for Railway deployment** with the existing `app.py`
