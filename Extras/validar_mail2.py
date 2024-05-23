import re
import tkinter as tk
from tkinter import messagebox
def valid_email(email):
    basic_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(basic_pattern, email):
        messagebox.showwarning("Invalid", "Invalid email format.")
    
def is_valid_email(email):
    # Regular expression pattern for basic email validation
    basic_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Regular expression patterns for popular email services
    gmail_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    outlook_pattern = r"^[a-zA-Z0-9._%+-]+@(outlook|hotmail)\.(com|live)$"
    yahoo_pattern = r"^[a-zA-Z0-9._%+-]+@yahoo\.com$"

    # Perform basic email validation
    if not re.match(basic_pattern, email):
        return False, "Invalid email format."

    # Check for popular email services
    if re.match(gmail_pattern, email):
        return True, "Valid Gmail address."
    elif re.match(outlook_pattern, email):
        return True, "Valid Outlook/Hotmail address."
    elif re.match(yahoo_pattern, email):
        return True, "Valid Yahoo address."

    # No specific email service found, return basic validation result
    return True, "Valid email address."

def on_validate_click():
    email = entry_email.get().lower()

    if not email:
        messagebox.showwarning("Error", "Please enter an email address.")
        return

    is_valid, message = is_valid_email(email)

    if is_valid:
        messagebox.showinfo("Valid", message)
    else:
        messagebox.showwarning("Invalid", message)

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Email Validator")

    app.window_width = 400
    app.window_height = 200

    # Set the window size
    app.geometry(f"{app.window_width}x{app.window_height}")

    label = tk.Label(app, text="Enter email address:")
    label.grid(padx=10, pady=10, column=0, row=0)

    entry_email = tk.Entry(app, width=30)
    entry_email.grid(padx=10,pady=5, column=0, row=1)

    validate_button = tk.Button(app, text="Validate Email", command=on_validate_click)
    validate_button.grid(pady=10, column=0, row=2)
    label2 = tk.Label(app, text="Enter email address:")
    label2.grid(pady=10, column=1, row=0)

    entry_email2 = tk.Entry(app, width=30, validate="key", validatecommand=(app.register(valid_email), "%S"))
    entry_email2.grid(padx=10,pady=5, column=1, row=1)

    validate_button2 = tk.Button(app, text="Validate Email", command=on_validate_click)
    validate_button2.grid(pady=10, column=1, row=2)
    app.mainloop()