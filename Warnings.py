from tkinter import messagebox


def invalid_entry_amount_msg():
    messagebox.showwarning("Invalid Entry Amount",
                           "Entry amount was over $500.00 limit!")


def prompt_high_entry(amount):
    result = messagebox.askquestion(f"Entry Confirmation",
                           f"Are you sure you want to enter {amount}?",
                           icon="question")

    return result
