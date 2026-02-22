"""
tests/test_converter.py
-----------------------
Unit tests for converter.py.
No Tkinter, no UI — runs fully headless in CI.
"""

import sys
import os

# Allow importing from the project root regardless of where pytest is run from
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PIL import Image

from converter import DEFAULT_CHARSET, load_image, map_to_ascii, resize_image


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def make_gray_image(width=10, height=10, brightness=128):
    """Create a solid grayscale image for testing."""
    return Image.new("L", (width, height), color=brightness)


def make_image_file(tmp_path, width=10, height=10, brightness=128):
    """Write a real PNG to a temp file and return its path."""
    img = make_gray_image(width, height, brightness)
    filepath = str(tmp_path / "test_image.png")
    img.save(filepath)
    return filepath


# ------------------------------------------------------------------
# DEFAULT_CHARSET
# ------------------------------------------------------------------

def test_default_charset_not_empty():
    assert len(DEFAULT_CHARSET) > 0


def test_default_charset_is_string():
    assert isinstance(DEFAULT_CHARSET, str)


# ------------------------------------------------------------------
# load_image
# ------------------------------------------------------------------

def test_load_image_returns_grayscale_image(tmp_path):
    filepath = make_image_file(tmp_path)
    img = load_image(filepath)
    assert img.mode == "L"


def test_load_image_raises_on_invalid_file(tmp_path):
    bad_file = str(tmp_path / "not_an_image.txt")
    with open(bad_file, "w") as f:
        f.write("this is not an image")
    with pytest.raises(Exception):
        load_image(bad_file)


def test_load_image_raises_on_missing_file():
    with pytest.raises(Exception):
        load_image("/nonexistent/path/image.png")


# ------------------------------------------------------------------
# resize_image
# ------------------------------------------------------------------

def test_resize_image_output_width():
    img = make_gray_image(100, 100)
    resized = resize_image(img, 50)
    assert resized.width == 50


def test_resize_image_height_uses_aspect_ratio_and_factor():
    img = make_gray_image(100, 100)
    resized = resize_image(img, 50)
    expected_height = int(50 * (100 / 100) * 0.55)
    assert resized.height == expected_height


def test_resize_image_minimum_height_is_one():
    """Very small width should not produce a zero-height image."""
    img = make_gray_image(1000, 10)
    resized = resize_image(img, 1)
    assert resized.height >= 1


def test_resize_image_preserves_grayscale_mode():
    img = make_gray_image(50, 50)
    resized = resize_image(img, 20)
    assert resized.mode == "L"


# ------------------------------------------------------------------
# map_to_ascii
# ------------------------------------------------------------------

def test_map_to_ascii_returns_string():
    img = make_gray_image(5, 5)
    result = map_to_ascii(img, DEFAULT_CHARSET)
    assert isinstance(result, str)


def test_map_to_ascii_correct_line_count():
    img = make_gray_image(5, 3)
    result = map_to_ascii(img, DEFAULT_CHARSET)
    lines = result.split("\n")
    assert len(lines) == 3


def test_map_to_ascii_correct_line_width():
    img = make_gray_image(7, 4)
    result = map_to_ascii(img, DEFAULT_CHARSET)
    lines = result.split("\n")
    for line in lines:
        assert len(line) == 7


def test_map_to_ascii_black_image_uses_first_char():
    """Pixel brightness 0 → index 0 → first char in charset."""
    img = make_gray_image(3, 1, brightness=0)
    result = map_to_ascii(img, DEFAULT_CHARSET)
    assert result == DEFAULT_CHARSET[0] * 3


def test_map_to_ascii_white_image_uses_last_char():
    """Pixel brightness 255 → index len-1 → last char in charset."""
    img = make_gray_image(3, 1, brightness=255)
    result = map_to_ascii(img, DEFAULT_CHARSET)
    assert result == DEFAULT_CHARSET[-1] * 3


def test_map_to_ascii_custom_charset_only_produces_those_chars():
    custom = "AB"
    img = make_gray_image(5, 5)
    result = map_to_ascii(img, custom)
    for char in result:
        assert char in custom or char == "\n", f"Unexpected char: {repr(char)}"


def test_map_to_ascii_single_char_charset():
    """A one-character charset should fill every cell with that character."""
    img = make_gray_image(4, 2)
    result = map_to_ascii(img, "X")
    for char in result:
        assert char in ("X", "\n")
