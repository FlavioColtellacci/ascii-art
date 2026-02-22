"""
themes.py
---------
Color palette definitions for the ASCII Art Generator UI.
Each theme is a plain dict — keys map directly to widget config properties
in app.py's _apply_theme() method.

No Tkinter imports here — keeping this module headless-safe for testing.
"""

DARK = {
    "bg":          "#1e1e1e",   # Main window background
    "fg":          "#e0e0e0",   # General foreground text
    "entry_bg":    "#2d2d2d",   # Text entry field background
    "entry_fg":    "#e0e0e0",   # Text entry field text
    "text_bg":     "#0d0d0d",   # ASCII output area background
    "text_fg":     "#00ff41",   # ASCII output text (classic matrix green)
    "btn_bg":      "#3a3a3a",   # Button background
    "btn_fg":      "#e0e0e0",   # Button label text
    "panel_bg":    "#252525",   # Side panel and preview frame background
    "label_bg":    "#252525",   # Label widget background
    "label_fg":    "#e0e0e0",   # Label widget text
    "scale_bg":    "#252525",   # Slider background
    "scale_fg":    "#e0e0e0",   # Slider text/tick color
    "highlight":   "#555555",   # Button active/hover highlight
}

LIGHT = {
    "bg":          "#f5f5f5",
    "fg":          "#1a1a1a",
    "entry_bg":    "#ffffff",
    "entry_fg":    "#1a1a1a",
    "text_bg":     "#ffffff",
    "text_fg":     "#1a1a1a",
    "btn_bg":      "#dcdcdc",
    "btn_fg":      "#1a1a1a",
    "panel_bg":    "#e8e8e8",
    "label_bg":    "#e8e8e8",
    "label_fg":    "#1a1a1a",
    "scale_bg":    "#e8e8e8",
    "scale_fg":    "#1a1a1a",
    "highlight":   "#c0c0c0",
}
