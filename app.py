"""
app.py
------
Main application class for the ASCII Art Generator.
Handles all UI construction, theming, drag-and-drop, image preview,
and ASCII generation/saving logic.

Dependencies:
    pip install Pillow tkinterdnd2
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES

from converter import DEFAULT_CHARSET, load_image, map_to_ascii, resize_image
from themes import DARK, LIGHT


class AsciiArtApp:
    """
    Main application window for the ASCII Art Generator.
    Instantiate this class with a TkinterDnD.Tk() root window.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("1100x700")
        self.root.minsize(800, 500)

        # State
        self.current_ascii_art = None
        self.current_theme = "dark"
        # Keep a reference to the preview PhotoImage to prevent garbage collection
        self.preview_photo = None

        self._build_ui()
        self._apply_theme(DARK)

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        """Build and arrange all widgets."""

        # ── Top-level layout: left control panel | right content area ──
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_control_panel()
        self._build_content_area()

        # ── Register the entire window as a drag-and-drop target ──
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop)

    def _build_control_panel(self):
        """Left panel: theme toggle, charset, resolution, buttons, DnD hint."""
        self.control_frame = tk.Frame(self.main_frame, width=190)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        # Prevent the frame from shrinking to fit its contents
        self.control_frame.pack_propagate(False)

        # Theme toggle — sits at the very top for easy access
        self.theme_btn = tk.Button(
            self.control_frame,
            text="☀  Light Mode",
            font=("Arial", 11),
            command=self.toggle_theme,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.theme_btn.pack(fill=tk.X, pady=(0, 20))

        # Custom charset input
        self.charset_label = tk.Label(
            self.control_frame, text="Custom Charset:", font=("Arial", 12)
        )
        self.charset_label.pack(anchor=tk.W, pady=(0, 2))

        self.charset_entry = tk.Entry(self.control_frame, font=("Arial", 12))
        self.charset_entry.insert(0, DEFAULT_CHARSET)
        self.charset_entry.pack(fill=tk.X, pady=(0, 15))

        # Resolution slider
        self.resolution_label = tk.Label(
            self.control_frame, text="Resolution:", font=("Arial", 12)
        )
        self.resolution_label.pack(anchor=tk.W, pady=(0, 2))

        self.resolution_scale = tk.Scale(
            self.control_frame,
            from_=10,
            to=150,
            orient=tk.HORIZONTAL,
            font=("Arial", 10),
        )
        self.resolution_scale.set(50)
        self.resolution_scale.pack(fill=tk.X, pady=(0, 20))

        # Action buttons
        self.generate_btn = tk.Button(
            self.control_frame,
            text="📂  Open Image",
            font=("Arial", 12),
            command=self.on_generate_click,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.generate_btn.pack(fill=tk.X, pady=(0, 8))

        self.save_btn = tk.Button(
            self.control_frame,
            text="💾  Save As .txt",
            font=("Arial", 12),
            command=self.on_save_click,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.save_btn.pack(fill=tk.X)

        # Drag-and-drop hint at the bottom of the panel
        self.dnd_label = tk.Label(
            self.control_frame,
            text="——————————\n💡 Drag & drop an\nimage anywhere\non the window",
            font=("Arial", 10),
            justify=tk.CENTER,
        )
        self.dnd_label.pack(pady=(30, 0))

    def _build_content_area(self):
        """Right area: image preview panel on top, ASCII text area below."""
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ── Image preview panel (fixed 200px height) ──
        self.preview_frame = tk.Frame(self.right_frame, height=200)
        self.preview_frame.pack(fill=tk.X, pady=(0, 6))
        self.preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(
            self.preview_frame,
            text="Image preview will appear here\nafter you open or drop an image",
            font=("Arial", 11),
            justify=tk.CENTER,
        )
        self.preview_label.pack(expand=True)

        # ── ASCII text area with scrollbars ──
        # Scrollbars must be packed before the text widget
        self.v_scroll = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.h_scroll = tk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_area = tk.Text(
            self.right_frame,
            wrap=tk.NONE,           # No word wrap — ASCII art must stay aligned
            font=("Courier", 8),
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.v_scroll.config(command=self.text_area.yview)
        self.h_scroll.config(command=self.text_area.xview)

    # ------------------------------------------------------------------
    # Theming
    # ------------------------------------------------------------------

    def _apply_theme(self, theme):
        """Apply a color palette dict to every widget in the app."""
        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])

        # Control panel
        self.control_frame.configure(bg=theme["panel_bg"])
        self.charset_label.configure(bg=theme["label_bg"], fg=theme["label_fg"])
        self.resolution_label.configure(bg=theme["label_bg"], fg=theme["label_fg"])
        self.dnd_label.configure(bg=theme["panel_bg"], fg=theme["label_fg"])
        self.charset_entry.configure(
            bg=theme["entry_bg"],
            fg=theme["entry_fg"],
            insertbackground=theme["fg"],   # Cursor color inside entry
        )
        self.resolution_scale.configure(
            bg=theme["scale_bg"],
            fg=theme["scale_fg"],
            troughcolor=theme["highlight"],
            highlightbackground=theme["panel_bg"],
        )
        for btn in (self.theme_btn, self.generate_btn, self.save_btn):
            btn.configure(
                bg=theme["btn_bg"],
                fg=theme["btn_fg"],
                activebackground=theme["highlight"],
                activeforeground=theme["fg"],
            )

        # Content area
        self.right_frame.configure(bg=theme["bg"])
        self.preview_frame.configure(bg=theme["panel_bg"])
        self.preview_label.configure(bg=theme["panel_bg"], fg=theme["label_fg"])
        self.text_area.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["fg"],
        )
        self.v_scroll.configure(bg=theme["panel_bg"])
        self.h_scroll.configure(bg=theme["panel_bg"])

    def toggle_theme(self):
        """Switch between dark and light themes."""
        if self.current_theme == "dark":
            self._apply_theme(LIGHT)
            self.theme_btn.configure(text="🌙  Dark Mode")
            self.current_theme = "light"
        else:
            self._apply_theme(DARK)
            self.theme_btn.configure(text="☀  Light Mode")
            self.current_theme = "dark"

    # ------------------------------------------------------------------
    # Image Processing
    # ------------------------------------------------------------------

    def _process_image(self, filepath):
        """
        Core pipeline: load → preview → convert to ASCII → display.
        Called by both the file picker and the drag-and-drop handler.
        """
        filepath = filepath.strip()

        # macOS tkinterdnd2 wraps paths that contain spaces in curly braces.
        # Example: "{/Users/name/My File.png}" → "/Users/name/My File.png"
        if filepath.startswith("{") and filepath.endswith("}"):
            filepath = filepath[1:-1]

        try:
            image = load_image(filepath)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")
            return

        self._show_preview(filepath)

        charset = self.charset_entry.get() or DEFAULT_CHARSET
        width = self.resolution_scale.get()
        resized = resize_image(image, width)
        ascii_art = map_to_ascii(resized, charset)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, ascii_art)
        self.current_ascii_art = ascii_art

    def _show_preview(self, filepath):
        """
        Display a thumbnail of the original image in the preview panel.
        Fits within the panel width × 180px while keeping aspect ratio.
        """
        try:
            img = Image.open(filepath)
            # winfo_width() may return 1 before the widget has been rendered
            panel_width = max(self.preview_frame.winfo_width(), 600)
            img.thumbnail((panel_width, 180))
            self.preview_photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=self.preview_photo, text="")
        except Exception as e:
            self.preview_label.configure(
                image="", text=f"Preview unavailable: {e}"
            )

    # ------------------------------------------------------------------
    # Event Handlers
    # ------------------------------------------------------------------

    def on_generate_click(self):
        """Open a file picker dialog and process the selected image."""
        filepath = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("All files", "*.*"),
            ],
        )
        if filepath:
            self._process_image(filepath)

    def on_drop(self, event):
        """
        Handle a file dropped onto the application window.
        event.data contains the dropped filepath (string).
        """
        self._process_image(event.data)

    def on_save_click(self):
        """Save the current ASCII art output to a .txt file."""
        if not self.current_ascii_art:
            messagebox.showerror("Nothing to save", "Generate ASCII art first!")
            return

        filepath = filedialog.asksaveasfilename(
            title="Save ASCII art",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(self.current_ascii_art)
                messagebox.showinfo(
                    "Saved", f"ASCII art saved as:\n{os.path.basename(filepath)}"
                )
            except Exception as e:
                messagebox.showerror("Save failed", f"Could not save file:\n{e}")
