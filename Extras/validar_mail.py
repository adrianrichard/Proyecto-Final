from tkinter import *
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter Validation Demo')

        self.create_widgets()
    
    def on_validate_input(self,P):
        # Example validation function
        return P.isdigit() or P == ""
    
    def on_invalid_input(self, msg):
        # Example function to handle invalid input
        self.invalid_label.config(text=msg)
        
    def create_widgets(self):
        # label
        ttk.Label(text='Email:').grid(row=0, column=0, padx=5, pady=5)

        # email entry
        vcmd = (self.register(self.validate), '%P')
        ivcmd = (self.register(self.on_invalid),)

        self.email_entry = Entry(self, width=50, bg="sky blue")
        self.email_entry.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)
        self.email_entry.grid(row=0, column=1, columnspan=2, padx=5)

        self.label_error = ttk.Label(self, foreground='red')
        self.label_error.grid(row=1, column=1, sticky=tk.W, padx=5)
        self.validated_entry = Entry(self, validatecommand=self.on_validate_input, invalidcommand=self.on_invalid_input)
        self.validated_entry.grid(row=2, column=1, sticky=tk.W, padx=5)

        self.invalid_label = tk.Label(self, fg="red")
        self.invalid_label.grid(row=3, column=1, sticky=tk.W, padx=5)
        # button
        self.send_button = tk.Button(text='Send', state="normal", disabledforeground="red", command=self.show_message).grid(row=0, column=4, padx=5)
    
    
    def show_message(self, error='Tkinter Validation Demo', color='black'):
        self.label_error['text'] = error
        self.email_entry['foreground'] = color

    def validate(self, value):
        """
        Validat the email entry
        :param value:
        :return:
        """
        pattern = r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(pattern, value) is None:
            
            return False
        self.email_entry.configure(bg="white")
        self.show_message()
        return True

    def on_invalid(self):
        """
        Show the error message if the data is not valid
        :return:
        """
        #self.show_message('Please enter a valid email', 'red')
        #self.email_entry['background'] = 'red'
        self.email_entry.focus()
        #messagebox.showwarning("Invalid", "Invalid email format.")


if __name__ == '__main__':
    app = App()
    app.mainloop()

'''def __init__(self, master=None, **kwargs):
        self.valid_command = kwargs.pop("validatecommand", None)
        self.invalid_command = kwargs.pop("invalidcommand", None)
        super().__init__(master, **kwargs)
        self.config(validate="key")
        self.config(validatecommand=(self.register(self.validate_input), '%P'))

    def validate_input(self, new_value):
        is_valid = self.valid_command(new_value)
        if is_valid:
            if self.invalid_command:
                self.invalid_command("")
        else:
            if self.invalid_command:
                self.invalid_command("Invalid input")
        return True  # Always return True to allow the validation to continue

def main():
    def on_validate_input(P):
        # Example validation function
        return P.isdigit() or P == ""

    def on_invalid_input(msg):
        # Example function to handle invalid input
        invalid_label.config(text=msg)

    root = tk.Tk()
    root.title("Validated Entry Example")

    validated_entry = ValidatedEntry(root, validatecommand=on_validate_input, invalidcommand=on_invalid_input)
    validated_entry.pack(padx=10, pady=10)

    invalid_label = tk.Label(root, fg="red")
    invalid_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
'''