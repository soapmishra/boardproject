from objects import Account, Transaction
import sqlite3

def create_store(conn: sqlite3.Connection) -> None:
    cur: sqlite3.Cursor = conn.cursor()
    tables: tuple[str, str] = ("accounts (account_number VARCAHR(20) PRIMARY KEY, name VARCHAR(100), balance DOUBLE DEFAULT 0.0, branch VARCHAR(20))",
                                                   "transactions (sender VARCHAR(20) NOT NULL, recipient VARCHAR(20) NOT NULL, value DOUBLE NOT NULL, FOREIGN KEY (sender) REFERENCES accounts(account_number), FOREIGN KEY (recipient) REFERENCES accounts(account_number))")
    for table in tables:
        try:
            _ = cur.execute(f'CREATE TABLE {table}')
        except:
            pass

def load_accounts(conn: sqlite3.Connection) -> list[Account]:
    cur: sqlite3.Cursor = conn.cursor()
    _ = cur.execute('SELECT * from accounts')
    accounts: list[Account] = []
    account: list[int | str | float]
    for account in cur.fetchall():
        (id, name, balance, branch) = (value for value in account)
        accounts.append(Account(id=id, name=name, balance=balance, branch=branch))
    return accounts

def load_transactions(conn: sqlite3.Connection) -> list[Transaction]:
    cur: sqlite3.Cursor = conn.cursor()
    _ = cur.execute('SELECT * from transactions')
    transactions: list[Transaction] = []
    transaction: list[int | float]
    for transaction in cur.fetchall():
        (sender, recipient, value) = (value for value in transaction)
        transactions.append(Transaction(sender=sender,recipient=recipient,value=value))
    return transactions