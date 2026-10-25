"""
Design tokens and typography specifications for Pip Learn.
An editorial learning studio where classical artistic warmth meets modern software craftsmanship.
"""
from app.config import COLORS

FONT_SERIF = "'Instrument Serif', Georgia, serif"
FONT_SANS = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Fira Code', Menlo, Monaco, Consolas, monospace"

HEADLINE_HERO = f"font-family: {FONT_SERIF}; font-size: 3.5rem; line-height: 1.1; font-weight: 400; letter-spacing: -0.02em;"
HEADLINE_SECTION = f"font-family: {FONT_SERIF}; font-size: 2.5rem; line-height: 1.15; font-weight: 400; letter-spacing: -0.015em;"
HEADLINE_CARD = f"font-family: {FONT_SERIF}; font-size: 1.75rem; line-height: 1.25; font-weight: 400;"

BODY_TEXT = f"font-family: {FONT_SANS}; font-size: 1rem; line-height: 1.6; color: {COLORS['secondary_text']};"
BODY_SMALL = f"font-family: {FONT_SANS}; font-size: 0.875rem; line-height: 1.5; color: {COLORS['muted_text']};"
LABEL_TAG = f"font-family: {FONT_SANS}; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;"

CARD_STYLE = f"background-color: {COLORS['primary_surface']}; border: 1px solid {COLORS['border']}; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);"
BUTTON_PRIMARY = f"background-color: {COLORS['forest']}; color: #FFFFFF; font-family: {FONT_SANS}; font-weight: 500; border-radius: 6px; padding: 8px 18px; transition: all 200ms ease;"
BUTTON_SECONDARY = f"background-color: {COLORS['secondary_surface']}; color: {COLORS['primary_text']}; border: 1px solid {COLORS['border']}; font-family: {FONT_SANS}; font-weight: 500; border-radius: 6px; padding: 8px 18px; transition: all 200ms ease;"
