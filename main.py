"""
main.py
-------
Entry point for the ASCII Art Generator.
Initialises the TkinterDnD-aware root window and launches the app.

To run:
    pip install Pillow tkinterdnd2
    python main.py
"""

from tkinterdnd2 import TkinterDnD

from app import AsciiArtApp

if __name__ == "__main__":
    # TkinterDnD.Tk() replaces the standard tk.Tk() to enable OS drag-and-drop
    root = TkinterDnD.Tk()
    app = AsciiArtApp(root)
    root.mainloop()
