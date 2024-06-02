import tkinter as tk
from tkinter import messagebox

# Define User class
class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposited {amount}")
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            self.history.append(f"Withdrew {amount}")
            return True

    def transfer(self, amount, other_user):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            other_user.balance += amount
            self.history.append(f"Transferred {amount} to {other_user.user_id}")
            other_user.history.append(f"Received {amount} from {self.user_id}")
            return True

    def get_history(self):
        return "\n".join(self.history)

    def get_balance(self):
        return self.balance

# Define ATM class
class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            self.current_user = user
            return True
        return False

# Define ATM GUI
class ATMGUI(tk.Tk):
    def __init__(self, atm):
        super().__init__()
        self.atm = atm
        self.title("ATM System")
        self.geometry("400x300")
        self.user_id = tk.StringVar()
        self.pin = tk.StringVar()
        self.balance_var = tk.StringVar()
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self, text="User ID").pack()
        tk.Entry(self, textvariable=self.user_id).pack()
        tk.Label(self, text="PIN").pack()
        tk.Entry(self, textvariable=self.pin, show="*").pack()
        tk.Button(self, text="Login", command=self.login).pack()

    def create_main_screen(self):
        self.clear_screen()
        self.balance_var.set(f"Balance: {self.atm.current_user.get_balance()}")
        tk.Label(self, textvariable=self.balance_var).pack()
        tk.Button(self, text="Transaction History", command=self.show_history).pack()
        tk.Button(self, text="Withdraw", command=self.withdraw).pack()
        tk.Button(self, text="Deposit", command=self.deposit).pack()
        tk.Button(self, text="Transfer", command=self.transfer).pack()
        tk.Button(self, text="Quit", command=self.quit_app).pack()

    def update_balance(self):
        self.balance_var.set(f"Balance: {self.atm.current_user.get_balance()}")

    def login(self):
        user_id = self.user_id.get()
        pin = self.pin.get()
        if self.atm.authenticate(user_id, pin):
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid User ID or PIN")

    def show_history(self):
        history = self.atm.current_user.get_history()
        messagebox.showinfo("Transaction History", history)

    def withdraw(self):
        amount = self.simple_input_dialog("Withdraw Amount")
        if amount and amount.isdigit():
            amount = int(amount)
            if self.atm.current_user.withdraw(amount):
                messagebox.showinfo("Success", f"Withdrew {amount}")
                self.update_balance()
            else:
                messagebox.showerror("Error", "Insufficient funds")

    def deposit(self):
        amount = self.simple_input_dialog("Deposit Amount")
        if amount and amount.isdigit():
            amount = int(amount)
            self.atm.current_user.deposit(amount)
            messagebox.showinfo("Success", f"Deposited {amount}")
            self.update_balance()

    def transfer(self):
        recipient_id = self.simple_input_dialog("Recipient User ID")
        amount = self.simple_input_dialog("Transfer Amount")
        if recipient_id and amount and amount.isdigit():
            amount = int(amount)
            recipient = self.atm.users.get(recipient_id)
            if recipient:
                if self.atm.current_user.transfer(amount, recipient):
                    messagebox.showinfo("Success", f"Transferred {amount} to {recipient_id}")
                    self.update_balance()
                else:
                    messagebox.showerror("Error", "Insufficient funds")
            else:
                messagebox.showerror("Error", "Recipient not found")

    def quit_app(self):
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def simple_input_dialog(self, prompt):
        input_var = tk.StringVar()
        dialog = tk.Toplevel(self)
        dialog.title(prompt)
        tk.Label(dialog, text=prompt).pack()
        tk.Entry(dialog, textvariable=input_var).pack()
        tk.Button(dialog, text="OK", command=dialog.destroy).pack()
        dialog.wait_window()
        return input_var.get()

# Create ATM instance and add some users
atm = ATM()
atm.add_user(User("user1", "1234", 1000))
atm.add_user(User("user2", "5678", 500))

# Start the GUI application
app = ATMGUI(atm)
app.mainloop()
