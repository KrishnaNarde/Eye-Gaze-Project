import tkinter as tk
from PIL import Image, ImageTk
import pyautogui

# Function to open voice typing
def open_voice_typing():
    # Replace this with your logic to open voice typing
    print("Opening voice typing...")

# Function to close the application
def close_application():
    root.destroy()

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Create main application window
root = tk.Tk()
root.title("Transparent Voice Typing")

# Set the window to be transparent
root.attributes('-alpha', 0.0)  # Set transparency level (0.0 to 1.0)

# Set the size of the window to cover the entire screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Capture the screen
screenshot = pyautogui.screenshot()

# Convert the screenshot to Tkinter compatible image
image = ImageTk.PhotoImage(screenshot)

# Display the screenshot as a background image
background_label = tk.Label(root, image=image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.place(relx=0.9, rely=0.1, anchor='n')

# Create buttons
button_font = ("Helvetica", 16, "bold")

open_button = tk.Button(button_frame, text="Open Voice Typing", command=open_voice_typing, font=button_font)
open_button.pack(pady=20)

close_button = tk.Button(button_frame, text="Close", command=close_application, font=button_font)
close_button.pack(pady=20)

# Run the application
root.mainloop()