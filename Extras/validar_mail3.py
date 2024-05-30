import tkinter as tk

class ValidatedEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        self.valid_command = kwargs.pop("validatecommand", None)
        self.invalid_command = kwargs.pop("invalidcommand", None)
        super().__init__(master, **kwargs)
        self.config(validate="key")
        self.config(validatecommand=(self.register(self.validate_input), '%P'))



def main():

    def __init__( master=None, **kwargs):
        valid_command = kwargs.pop("validatecommand", None)
        invalid_command = kwargs.pop("invalidcommand", None)
        super().__init__(master, **kwargs)

    def validate_input(new_value):
        is_valid = valid_command(new_value)
        if is_valid:
            if invalid_command:
                invalid_command("")
        else:
            if invalid_command:
                invalid_command("Invalid input")
        return True  # Always return True to allow the validation to continue

    def on_validate_input(P):
        # Example validation function
        invalid_label.config(text="correcto", fg='blue')
        return P.isdigit() or P == ""


    def on_invalid_input():
        # Example function to handle invalid input
        invalid_label.config(text="Error", fg='red')

    root = tk.Tk()
    root.title("Validated Entry Example")

    validated_entry = tk.Entry(root)
    validated_entry.config(validate="key")
    validated_entry.config(validatecommand=(root.register(on_validate_input), '%P'))
    validated_entry.config(invalidcommand=(root.register(on_invalid_input), ))
    validated_entry.pack(padx=10, pady=10)

    invalid_label = tk.Label(root, fg="red")
    invalid_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
