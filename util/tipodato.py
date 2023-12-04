from tkinter import ttk
import tkinter as tk
import re

def testAlphaValue(self, value):
        if value.isalpha():
            return True
        else:
            return False

def validate_entry(text):
    return text.isdecimal()

def validate_date(new_text):
    """
    Make sure `new_text` has the dd/mm/yyyy format.
    """
    # No more than ten characters.
    if len(new_text) > 10:
        return False
    checks = []
    for i, char in enumerate(new_text):
        # Indexes 2 and 5 must have the "/" character.
        if i in (2, 5):
            checks.append(char == "/")
        else:
            # The remaining characters must be numbers between 0 and 9.
            checks.append(char.isdecimal())
    # `all()` returns True if all checks are True.
    return all(checks)

root = tk.Tk()
root.config(width=300, height=200)
root.title("My App")
entry1 = ttk.Entry( validate="key", validatecommand=(root.register(validate_entry), "%S"))
entry2 = ttk.Entry( validate="key", validatecommand=(root.register(validate_date), "%P"))

entry3 = ttk.Entry( validate="key", validatecommand=(root.register(validate_entry), "%S"))
entry1.place(x=50, y=50, width=150)
entry2.place(x=50, y=100, width=150)
entry3.place(x=50, y=150, width=150)

root.mainloop()