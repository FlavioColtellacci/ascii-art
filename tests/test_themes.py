"""
tests/test_themes.py
---------------------
Unit tests for themes.py.
Verifies that both DARK and LIGHT palettes are complete and well-formed.
No Tkinter — runs fully headless in CI.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import pytest

from themes import DARK, LIGHT

# Every key that app.py's _apply_theme() expects to find
REQUIRED_KEYS = [
    "bg",
    "fg",
    "entry_bg",
    "entry_fg",
    "text_bg",
    "text_fg",
    "btn_bg",
    "btn_fg",
    "panel_bg",
    "label_bg",
    "label_fg",
    "scale_bg",
    "scale_fg",
    "highlight",
]

HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


# ------------------------------------------------------------------
# Structure tests
# ------------------------------------------------------------------

@pytest.mark.parametrize("key", REQUIRED_KEYS)
def test_dark_theme_has_required_key(key):
    assert key in DARK, f"DARK theme is missing required key: '{key}'"


@pytest.mark.parametrize("key", REQUIRED_KEYS)
def test_light_theme_has_required_key(key):
    assert key in LIGHT, f"LIGHT theme is missing required key: '{key}'"


# ------------------------------------------------------------------
# Value type tests
# ------------------------------------------------------------------

def test_dark_theme_values_are_strings():
    for key, value in DARK.items():
        assert isinstance(value, str), f"DARK['{key}'] must be a string, got {type(value)}"


def test_light_theme_values_are_strings():
    for key, value in LIGHT.items():
        assert isinstance(value, str), f"LIGHT['{key}'] must be a string, got {type(value)}"


# ------------------------------------------------------------------
# Color format tests (must be valid 6-digit hex)
# ------------------------------------------------------------------

def test_dark_theme_values_are_valid_hex_colors():
    for key, value in DARK.items():
        assert HEX_COLOR_PATTERN.match(value), (
            f"DARK['{key}'] = '{value}' is not a valid #RRGGBB hex color"
        )


def test_light_theme_values_are_valid_hex_colors():
    for key, value in LIGHT.items():
        assert HEX_COLOR_PATTERN.match(value), (
            f"LIGHT['{key}'] = '{value}' is not a valid #RRGGBB hex color"
        )


# ------------------------------------------------------------------
# Contrast tests (themes must actually differ)
# ------------------------------------------------------------------

def test_dark_and_light_backgrounds_differ():
    assert DARK["bg"] != LIGHT["bg"], "DARK and LIGHT themes have the same background color"


def test_dark_and_light_text_backgrounds_differ():
    assert DARK["text_bg"] != LIGHT["text_bg"]


def test_dark_and_light_panel_backgrounds_differ():
    assert DARK["panel_bg"] != LIGHT["panel_bg"]
