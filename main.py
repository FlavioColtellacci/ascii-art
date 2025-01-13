import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

# Default ASCII character set
DEFAULT_CHARSET = "@%#*+=-:. "

# Function to load and process the image
def load_image(filepath):
    try:
        image = Image.open(filepath).convert("L")  # Convert to grayscale
        return image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        return None

# Function to resize the image for ASCII conversion
def resize_image(image, width):
    aspect_ratio = image.height / image.width
    new_height = int(width * aspect_ratio * 0.55)  # Adjust height for ASCII proportions
    return image.resize((width, new_height))

# Function to map brightness to ASCII characters
def map_to_ascii(image, charset):
    pixels = image.getdata()
    ascii_chars = [charset[int((pixel / 255) * (len(charset) - 1))] for pixel in pixels]
    ascii_art = "\n".join(
        ["".join(ascii_chars[i:i + image.width]) for i in range(0, len(ascii_chars), image.width)]
    )
    return ascii_art

# Function to display ASCII art in the text area
def display_ascii(ascii_art):
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, ascii_art)

# Function to save ASCII art to a .txt file
def save_ascii_art(ascii_art):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
    if filepath:
        try:
            with open(filepath, "w") as file:
                file.write(ascii_art)
            messagebox.showinfo("Success", f"ASCII art saved as {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save ASCII art: {e}")

# Function triggered by the "Generate ASCII" button
def on_generate_click():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
    if not filepath:
        return
    image = load_image(filepath)
    if image is None:
        return

    # Resize and generate ASCII art
    resized_image = resize_image(image, resolution_scale.get())
    ascii_art = map_to_ascii(resized_image, charset_entry.get() or DEFAULT_CHARSET)
    display_ascii(ascii_art)
    global current_ascii_art
    current_ascii_art = ascii_art

# Function triggered by the "Save As" button
def on_save_click():
    if current_ascii_art:
        save_ascii_art(current_ascii_art)
    else:
        messagebox.showerror("Error", "No ASCII art to save!")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("ASCII Art Generator")
root.geometry("800x600")
root.resizable(False, False)

# Left panel for controls
control_frame = tk.Frame(root)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# ASCII charset input
tk.Label(control_frame, text="Custom Charset:", font=("Arial", 12)).pack(pady=5)
charset_entry = tk.Entry(control_frame, font=("Arial", 12))
charset_entry.insert(0, DEFAULT_CHARSET)
charset_entry.pack(pady=5)

# Resolution scale
tk.Label(control_frame, text="Resolution:", font=("Arial", 12)).pack(pady=5)
resolution_scale = tk.Scale(control_frame, from_=10, to_=150, orient=tk.HORIZONTAL, font=("Arial", 10))
resolution_scale.set(50)
resolution_scale.pack(pady=5)

# Generate and Save buttons
generate_button = tk.Button(control_frame, text="Generate ASCII", font=("Arial", 12), command=on_generate_click)
generate_button.pack(pady=10)

save_button = tk.Button(control_frame, text="Save As", font=("Arial", 12), command=on_save_click)
save_button.pack(pady=10)

# Right panel for ASCII art display
text_area = tk.Text(root, wrap=tk.WORD, font=("Courier", 10), bg="black", fg="white")
text_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Variable to store the current ASCII art
current_ascii_art = None

# Start the Tkinter event loop
root.mainloop()
