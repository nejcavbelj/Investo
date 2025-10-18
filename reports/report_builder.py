"""
Report builder module for generating PDF/HTML reports
"""

import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from config.settings import GENERATED_REPORTS_DIR

def create_lynch_report(symbol, data, metrics):
    """Create a Peter Lynch analysis report"""
    filename = f"lynch_{symbol}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    filepath = GENERATED_REPORTS_DIR / filename
    
    # Ensure directory exists
    GENERATED_REPORTS_DIR.mkdir(exist_ok=True)
    
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#FFA500')
    )
    story.append(Paragraph(f"Peter Lynch Analysis: {symbol}", title_style))
    story.append(Spacer(1, 12))
    
    # Basic info
    story.append(Paragraph(f"Company: {data.get('shortName', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"Price: ${data.get('price', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"Sector: {data.get('sector', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Metrics table
    metrics_data = [['Metric', 'Value', 'Interpretation']]
    for key, value in metrics.items():
        if key not in ['sector', 'industry']:
            interpretation = get_lynch_interpretation(key, value)
            metrics_data.append([key.replace('_', ' '), str(value), interpretation])
    
    metrics_table = Table(metrics_data)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFA500')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("Analysis Metrics", styles['Heading2']))
    story.append(metrics_table)
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Summary", styles['Heading2']))
    summary = generate_lynch_summary(metrics)
    story.append(Paragraph(summary, styles['Normal']))
    
    doc.build(story)
    return str(filepath)

def create_graham_report(symbol, data, metrics):
    """Create a Benjamin Graham analysis report"""
    filename = f"graham_{symbol}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    filepath = GENERATED_REPORTS_DIR / filename
    
    # Ensure directory exists
    GENERATED_REPORTS_DIR.mkdir(exist_ok=True)
    
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.HexColor('#6ad1ff')
    )
    story.append(Paragraph(f"Benjamin Graham Analysis: {symbol}", title_style))
    story.append(Spacer(1, 12))
    
    # Basic info
    story.append(Paragraph(f"Company: {data.get('shortName', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"Price: ${data.get('price', 'N/A')}", styles['Normal']))
    story.append(Paragraph(f"Sector: {data.get('sector', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Metrics table
    metrics_data = [['Metric', 'Value', 'Interpretation']]
    for key, value in metrics.items():
        if key not in ['sector', 'industry', 'price', 'marketCap']:
            interpretation = get_graham_interpretation(key, value)
            metrics_data.append([key.replace('_', ' '), str(value), interpretation])
    
    metrics_table = Table(metrics_data)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6ad1ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("Analysis Metrics", styles['Heading2']))
    story.append(metrics_table)
    story.append(Spacer(1, 20))
    
    # Net-Net Commentary
    if 'NetNet_Comment' in metrics:
        story.append(Paragraph("Net-Net Analysis", styles['Heading2']))
        story.append(Paragraph(metrics['NetNet_Comment'], styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Summary", styles['Heading2']))
    summary = generate_graham_summary(metrics)
    story.append(Paragraph(summary, styles['Normal']))
    
    doc.build(story)
    return str(filepath)

def get_lynch_interpretation(metric, value):
    """Get interpretation for Lynch metrics"""
    interpretations = {
        'P/E': 'Good if < 15, concerning if > 25',
        'PEG': 'Ideal around 1.0, < 0.5 is very attractive',
        'EPS_Growth_%': 'Higher growth is better, > 15% is excellent',
        'ROE_%': '> 15% is good, > 20% is excellent',
        'Debt/Equity': 'Lower is better, < 0.5 is conservative',
        'Current_Ratio': '> 2.0 indicates good liquidity',
        'Price/Book': 'Lower is better for value, < 1.5 is attractive'
    }
    return interpretations.get(metric, 'See analysis for interpretation')

def get_graham_interpretation(metric, value):
    """Get interpretation for Graham metrics"""
    interpretations = {
        'P/E': 'Should be < 15 for defensive investors',
        'P/B': 'Should be < 1.5, ideally < 1.0',
        'Debt/Equity': 'Should be < 0.5 for safety',
        'Current_Ratio': 'Should be > 2.0 for liquidity',
        'Dividend_Yield_%': 'Higher yield is better if sustainable',
        'Margin_of_Safety_%': 'Should be > 30% for safety',
        'Graham_Combined_Test': 'True means passes all Graham criteria'
    }
    return interpretations.get(metric, 'See analysis for interpretation')

def generate_lynch_summary(metrics):
    """Generate Lynch-style summary"""
    pe = metrics.get('P/E')
    peg = metrics.get('PEG')
    growth = metrics.get('EPS_Growth_%')
    
    summary = f"This analysis uses Peter Lynch's growth investing principles. "
    
    if pe and pe < 15:
        summary += f"The P/E ratio of {pe} is attractive. "
    elif pe and pe > 25:
        summary += f"The P/E ratio of {pe} is high and requires strong growth justification. "
    
    if peg and peg < 1.0:
        summary += f"The PEG ratio of {peg} suggests good value relative to growth. "
    
    if growth and growth > 15:
        summary += f"Strong earnings growth of {growth}% supports the investment thesis. "
    
    summary += "Consider the company's competitive position and industry trends."
    return summary

def generate_graham_summary(metrics):
    """Generate Graham-style summary"""
    pe = metrics.get('P/E')
    pb = metrics.get('P/B')
    mos = metrics.get('Margin_of_Safety_%')
    combined_test = metrics.get('Graham_Combined_Test')
    
    summary = f"This analysis uses Benjamin Graham's value investing principles. "
    
    if combined_test:
        summary += "This stock passes all Graham defensive investor criteria. "
    else:
        summary += "This stock does not meet all Graham criteria. "
    
    if mos and mos > 30:
        summary += f"The margin of safety of {mos}% provides good downside protection. "
    
    if pe and pe < 15:
        summary += f"The P/E ratio of {pe} is within Graham's conservative range. "
    
    if pb and pb < 1.5:
        summary += f"The P/B ratio of {pb} suggests reasonable valuation. "
    
    summary += "Consider this as a defensive investment with focus on capital preservation."
    return summary
