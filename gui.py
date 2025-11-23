import tkinter as tk
from tkinter import ttk, messagebox
import main
import run

DATABASE = run.DATABASE


class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Bank Login")

        tk.Label(root, text="Administrator Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        with main.connector.connect(DATABASE) as conn:
            pw = self.password_entry.get()
            if main.login_admin(conn, pw):
                self.root.destroy()
                MainMenu()
            else:
                messagebox.showerror("Error", "Wrong password.")


class MainMenu:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Bank Management System")

        tk.Label(self.win, text="Main Menu", font=("Arial", 18)).pack(pady=10)

        buttons = [
            ("View Accounts", self.show_accounts),
            ("View Transactions", self.show_transactions),
            ("Deposit Money", self.deposit),
            ("View Account Statement", self.statement),
            ("Exit", self.win.destroy),
        ]

        for text, cmd in buttons:
            tk.Button(self.win, text=text, width=30, command=cmd).pack(pady=5)

        self.win.mainloop()

    def show_accounts(self):
        AccountsWindow()

    def show_transactions(self):
        TransactionsWindow()

    def deposit(self):
        DepositWindow()

    def statement(self):
        StatementWindow()


class AccountsWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Accounts")

        tk.Label(self.win, text="Accounts", font=("Arial", 16)).pack(pady=10)

        table = ttk.Treeview(self.win, columns=("id", "name", "balance", "branch", "type"))
        table.heading("id", text="ID")
        table.heading("name", text="Name")
        table.heading("balance", text="Balance")
        table.heading("branch", text="Branch")
        table.heading("type", text="Type")
        table.pack(fill="both", expand=True)

        with main.connector.connect(DATABASE) as conn:
            for acc in main.load_accounts(conn):
                if acc.deleted == 0:
                    table.insert("", "end", values=(acc.id, acc.name, acc.balance, acc.branch, acc.type))


class TransactionsWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Transactions")

        tk.Label(self.win, text="Transactions", font=("Arial", 16)).pack(pady=10)

        table = ttk.Treeview(self.win, columns=("sender", "receiver", "amount"))
        for col in ("sender", "receiver", "amount"):
            table.heading(col, text=col.capitalize())
        table.pack(fill="both", expand=True)

        with main.connector.connect(DATABASE) as conn:
            for t in main.load_transactions(conn):
                table.insert("", "end", values=(t.sender, t.recipient, t.value))


class DepositWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Deposit Money")

        tk.Label(self.win, text="Deposit Money", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.win, text="Account Number:").pack()
        self.acc_entry = tk.Entry(self.win)
        self.acc_entry.pack()

        tk.Label(self.win, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.win)
        self.amount_entry.pack()

        tk.Button(self.win, text="Deposit", command=self.deposit_money).pack(pady=10)

    def deposit_money(self):
        try:
            account_id = int(self.acc_entry.get())
            amount = float(self.amount_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input.")
            return

        with main.connector.connect(DATABASE) as conn:
            main.update_account(conn, account_id, amount)

        messagebox.showinfo("Success", "Deposit completed.")


class StatementWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Account Statement")

        tk.Label(self.win, text="Account Statement", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.win, text="Account Number:").pack()
        self.acc_entry = tk.Entry(self.win)
        self.acc_entry.pack()

        tk.Button(self.win, text="Generate Statement", command=self.generate).pack(pady=10)

    def generate(self):
        try:
            account_id = int(self.acc_entry.get())
        except:
            messagebox.showerror("Error", "Invalid account number.")
            return

        with main.connector.connect(DATABASE) as conn:
            acc = main.load_account(conn, account_id)
            transactions = main.load_transactions(conn)

        win = tk.Toplevel()
        win.title(f"Statement for Account {account_id}")

        tk.Label(win, text=f"Name: {acc.name}", font=("Arial", 12)).pack()
        tk.Label(win, text=f"Balance: {acc.balance}").pack()
        tk.Label(win, text="Transactions:", font=("Arial", 14)).pack(pady=10)

        table = ttk.Treeview(win, columns=("sender", "receiver", "amount"))
        for col in ("sender", "receiver", "amount"):
            table.heading(col, text=col.capitalize())
        table.pack(fill="both", expand=True)

        for t in transactions:
            if t.sender == account_id or t.recipient == account_id:
                table.insert("", "end", values=(t.sender, t.recipient, t.value))


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
