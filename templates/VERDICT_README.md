# Verdict Template Documentation

## Overview

The `verdict_template.html` file contains the Combined Investment Verdict section that appears at the bottom of every combined report. This template can be edited independently to customize the verdict presentation without modifying the main combined template.

## Location

```
templates/
├── verdict_template.html  ← Edit this file to customize the verdict section
├── combined_template.html ← Main template (includes verdict via {% include %})
└── VERDICT_README.md     ← This documentation
```

## How It Works

The verdict template is included in the main combined template using Jinja2's `{% include %}` directive:

```jinja2
<!-- In combined_template.html -->
{% include 'verdict_template.html' %}
```

When the report is generated, the verdict template is automatically loaded and rendered with the same context variables as the main template.

## Available Variables

The verdict template has access to all the same variables as the main template:

### Analysis Results
- `graham_metrics` - Dictionary of Graham analysis metrics
- `lynch_metrics` - Dictionary of Lynch analysis metrics  
- `reddit_data` - Dictionary of Reddit sentiment data
- `combined_verdict` - Generated verdict text

### Stock Data
- `symbol` - Stock ticker symbol
- `company_name` - Company name
- `price` - Current stock price
- `sector` - Company sector
- `industry` - Company industry
- `market_cap` - Formatted market cap string

### Summaries
- `graham_summary` - Graham analysis summary
- `lynch_summary` - Lynch analysis summary

### Helper Functions
- `get_graham_criteria(metric)` - Get criteria for a metric
- `get_lynch_criteria(metric)` - Get criteria for a metric
- `check_graham_criteria(metric, value)` - Check if value meets criteria
- `check_lynch_criteria(metric, value)` - Check if value meets criteria

## Current Structure

```html
<div class="verdict-box">
    <h3>Combined Investment Verdict</h3>
    
    <!-- Main verdict text -->
    <div class="verdict-summary">
        {{ combined_verdict }}
    </div>
    
    <!-- Analysis breakdown badges -->
    <div style="margin-top: 1.5em;">
        <strong>Analysis Breakdown:</strong><br>
        • Graham Analysis: [BULLISH/BEARISH badge]
        • Lynch Analysis: [BULLISH/NEUTRAL badge]
        • Reddit Sentiment: [BULLISH/NEUTRAL/BEARISH badge]
    </div>
    
    <!-- Disclaimer -->
    <div style="margin-top: 1.5em; padding-top: 1em; border-top: 1px solid var(--line);">
        <p>Disclaimer text...</p>
    </div>
</div>
```

## Customization Examples

### Change the Verdict Title

```html
<!-- Before -->
<h3>Combined Investment Verdict</h3>

<!-- After -->
<h3>🎯 Investment Recommendation</h3>
```

### Add More Details

```html
<div class="verdict-summary">
    {{ combined_verdict }}
    
    <!-- Add custom section -->
    <div style="margin-top: 1em; padding: 1em; background: #0a0a0a; border-radius: 8px;">
        <strong>Key Takeaways:</strong>
        <ul style="margin: 0.5em 0; padding-left: 1.5em;">
            <li>Review fundamental metrics carefully</li>
            <li>Consider market conditions</li>
            <li>Diversify your portfolio</li>
        </ul>
    </div>
</div>
```

### Customize Disclaimer

```html
<div style="margin-top: 1.5em; padding-top: 1em; border-top: 1px solid var(--line);">
    <p style="color: var(--muted); font-size: 0.9em; margin: 0;">
        <strong>Important:</strong> This is your custom disclaimer text here.
        Add any legal or informational text you need.
    </p>
</div>
```

### Add Conditional Content

```html
{% if graham_metrics.Graham_Combined_Test and lynch_metrics.PEG < 1.0 %}
    <div style="margin-top: 1em; padding: 1em; background: rgba(0, 255, 0, 0.1); border: 1px solid #00FF00; border-radius: 8px;">
        <strong style="color: #00FF00;">⭐ Strong Buy Signal</strong>
        <p style="margin: 0.5em 0 0 0;">Both Graham and Lynch criteria are highly favorable!</p>
    </div>
{% endif %}
```

## CSS Classes Available

The verdict template can use these CSS classes from the main template:

### Layout
- `.verdict-box` - Main container (gradient background, orange border)
- `.verdict-summary` - Verdict text container

### Sentiment Indicators
- `.sentiment-indicator` - Base class for badges
- `.sentiment-bullish` - Green badge (positive)
- `.sentiment-bearish` - Red badge (negative)
- `.sentiment-neutral` - Orange badge (neutral)

### CSS Variables
- `--orange` - #FFA500 (primary brand color)
- `--green` - #00FF00 (bullish)
- `--red` - #FF3C00 (bearish)
- `--blue` - #6ad1ff (Graham accent)
- `--pink` - #FF6B6B (Reddit accent)
- `--bg` - #181818 (dark background)
- `--panel` - #222 (panel background)
- `--line` - #333 (border/line color)
- `--muted` - #aaa (muted text)

## Testing Changes

After editing `verdict_template.html`, test your changes:

```bash
# Generate a report
python main.py

# Or directly
python -c "from reports.combined_report_generator import create_combined_report; create_combined_report('AAPL')"
```

The report will automatically include your updated verdict template.

## Best Practices

1. **Keep it readable** - The verdict should be clear and easy to understand
2. **Maintain consistency** - Use the same color scheme and styling as the rest of the report
3. **Add value** - Include information that helps users make decisions
4. **Test thoroughly** - Generate reports for different stocks to ensure your changes work in all cases
5. **Use conditionals wisely** - Handle cases where data might be missing or null

## Rollback

If you need to revert changes, the original template structure is:

```html
<div class="verdict-box">
    <h3>Combined Investment Verdict</h3>
    <div class="verdict-summary">
        {{ combined_verdict }}
    </div>
    <div style="margin-top: 1.5em;">
        <strong>Analysis Breakdown:</strong><br>
        [Analysis badges]
    </div>
    <div style="margin-top: 1.5em; padding-top: 1em; border-top: 1px solid var(--line);">
        <p>Disclaimer...</p>
    </div>
</div>
```

## Support

For questions or issues:
1. Check this documentation
2. Review the main `combined_template.html` for available CSS and variables
3. Test changes incrementally
4. Keep a backup of working versions
