"""
converter.py
------------
Pure ASCII conversion logic. No UI imports — this module is intentionally
decoupled from Tkinter so it can be tested headlessly in CI.
"""

from PIL import Image

# Default brightness-to-character mapping (dark → light)
DEFAULT_CHARSET = "@%#*+=-:. "


def load_image(filepath):
    """
    Open an image file and convert it to grayscale.
    Raises IOError if the file cannot be opened or is not a valid image.
    The caller (app.py) is responsible for showing error dialogs.
    """
    image = Image.open(filepath).convert("L")
    return image


def resize_image(image, width):
    """
    Resize image to the target width while preserving aspect ratio.
    The 0.55 factor compensates for ASCII characters being taller than wide.
    """
    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)
    # Ensure at least 1 pixel height to avoid empty output
    new_height = max(1, new_height)
    return image.resize((width, new_height))


def map_to_ascii(image, charset):
    """
    Map each pixel's brightness to a character in the charset.
    Bright pixels → characters at the end of charset (lighter).
    Dark pixels  → characters at the start of charset (heavier).
    Returns a multi-line string of ASCII art.
    """
    pixels = image.getdata()
    charset_len = len(charset)
    ascii_chars = [
        charset[int((pixel / 255) * (charset_len - 1))]
        for pixel in pixels
    ]
    ascii_art = "\n".join(
        ["".join(ascii_chars[i : i + image.width])
         for i in range(0, len(ascii_chars), image.width)]
    )
    return ascii_art
