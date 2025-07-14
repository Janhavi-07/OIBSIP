import tkinter as tk
import random
import string
import pyperclip

# Function to generate random password
def generate_password(length, use_uppercase, use_digits, use_symbols):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    char_pool = lowercase
    if use_uppercase:
        char_pool += uppercase
    if use_digits:
        char_pool += digits
    if use_symbols:
        char_pool += symbols
    
    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password

# Function to determine password strength
def check_strength(password):
    if len(password) >= 12 and any(char.isdigit() for char in password) and any(char.isupper() for char in password) and any(char in string.punctuation for char in password):
        return "Strong"
    elif len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password):
        return "Moderate"
    else:
        return "Weak"

# Function to handle the password generation and display
def on_generate():
    length = int(length_entry.get())
    use_uppercase = uppercase_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    
    password = generate_password(length, use_uppercase, use_digits, use_symbols)
    strength = check_strength(password)
    
    password_text.config(state=tk.NORMAL)  # Enable editing to update text
    password_text.delete(1.0, tk.END)  # Clear previous text
    password_text.insert(tk.END, password)  # Insert new password
    password_text.config(state=tk.DISABLED)  # Disable editing
    
    # Set the password strength label text
    strength_label.config(text="Password Strength: ")
    
    # Create a colored box to show the password strength
    strength_box.config(text=strength)
    
    # Change the font color of the password based on strength
    if strength == "Strong":
        password_text.config(fg="black")  # Password in black
        strength_box.config(bg="green", fg="white")
    elif strength == "Moderate":
        password_text.config(fg="black")  # Password in black
        strength_box.config(bg="yellow", fg="black")
    else:
        password_text.config(fg="black")  # Password in black
        strength_box.config(bg="red", fg="white")

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_text.get(1.0, tk.END).strip()
    pyperclip.copy(password)

# Create main window
window = tk.Tk()
window.title("Random Password Generator")

# Title label (make the title size bigger)
title_label = tk.Label(window, text="Random Password Generator", bg="#2e2e2e", fg="white", font=("Arial", 30, "bold"))
title_label.pack(pady=20)  # Reduced padding

# Maximize the window
window.state('zoomed')

window.configure(bg="#2e2e2e")
font = ("Arial", 16)

# Create a frame for the input section
input_frame = tk.Frame(window, bg="#2e2e2e")
input_frame.pack(pady=10)  # Reduced padding

# Place the "Enter Password Length" label on the left and the input textbox on the right
tk.Label(input_frame, text="Enter password length:", bg="#2e2e2e", fg="white", font=("Arial", 16, "bold")).pack(side=tk.LEFT, padx=5)
length_entry = tk.Entry(input_frame, font=font)
length_entry.pack(side=tk.RIGHT, padx=5)

# Create a frame for the options (checkboxes, generate button, etc.)
options_frame = tk.Frame(window, bg="#2e2e2e")
options_frame.pack(pady=5)  # Reduced padding

# Checkboxes for password options (Adjust font and size)
uppercase_var = tk.BooleanVar()
tk.Checkbutton(options_frame, text="Include uppercase letters", variable=uppercase_var, bg="#2e2e2e", fg="white", font=("Arial", 14), selectcolor="black").pack(pady=3)

digits_var = tk.BooleanVar()
tk.Checkbutton(options_frame, text="Include digits", variable=digits_var, bg="#2e2e2e", fg="white", font=("Arial", 14), selectcolor="black").pack(pady=3)

symbols_var = tk.BooleanVar()
tk.Checkbutton(options_frame, text="Include symbols", variable=symbols_var, bg="#2e2e2e", fg="white", font=("Arial", 14), selectcolor="black").pack(pady=5)

# Button to generate password (Make the button a bit smaller)
generate_button = tk.Button(options_frame, text="Generate Password", command=on_generate, bg="#4CAF50", fg="white", font=("Arial", 15, "bold"), relief="raised", bd=3)
generate_button.pack(pady=5)

# Frame to display generated password and strength
result_frame = tk.Frame(window, bg="#2e2e2e")
result_frame.pack(pady=10)  # Reduced padding

# Label for generated password
password_label = tk.Label(result_frame, text="Generated Password: ", bg="#2e2e2e", fg="white", font=("Arial", 16))
password_label.pack(pady=5)  # Reduced padding

# Textbox for displaying generated password (fix the small size issue)
password_text = tk.Text(result_frame, height=2, width=45, font=("Arial", 14), wrap=tk.WORD, bd=2, relief="solid")
password_text.pack(pady=5)  # Reduced padding
password_text.config(state=tk.DISABLED)  # Disable editing
password_text.config(fg="black")  # Set default text color to black

# Password strength label (unchanged)
strength_label = tk.Label(result_frame, text="Password Strength: ", bg="#2e2e2e", fg="white", font=("Arial", 16))
strength_label.pack(pady=5)  # Reduced padding

# Box to display password strength
strength_box = tk.Label(result_frame, text="Weak", bg="red", fg="white", font=("Arial", 16), height=1, width=20, anchor="center")
strength_box.pack(pady=5)  # Reduced padding

# Button to copy password to clipboard
copy_button = tk.Button(result_frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#FFC107", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=3)
copy_button.pack(pady=5)  # Reduced padding

# Start the GUI loop
window.mainloop()
