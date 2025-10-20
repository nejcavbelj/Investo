"""
Charts module for Investo
========================
Handles all chart-related functionality including data fetching and rendering.
"""

from .chart_data import get_chart_data
from .chart_renderer import render_chart_html

__all__ = ['get_chart_data', 'render_chart_html']
