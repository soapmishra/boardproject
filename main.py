from multiprocessing import Value
from objects import Account, Transaction
import sqlite3 as connector

def create_store(conn: connector.Connection) -> None:
    cur: connector.Cursor = conn.cursor()
    tables: tuple[str, str] = ("accounts (account_number VARCAHR(20) PRIMARY KEY, name VARCHAR(100), balance DOUBLE DEFAULT 0.0, branch VARCHAR(20))",
                                                   "transactions (sender VARCHAR(20) NOT NULL, recipient VARCHAR(20) NOT NULL, value DOUBLE NOT NULL, FOREIGN KEY (sender) REFERENCES accounts(account_number), FOREIGN KEY (recipient) REFERENCES accounts(account_number))")
    for table in tables:
        try:
            _ = cur.execute(f'CREATE TABLE {table}')
        except:
            pass
    conn.commit()
    cur.close()

def load_accounts(conn: connector.Connection) -> list[Account]:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute('SELECT * from accounts')
    accounts: list[Account] = []
    account: list[int | str | float]
    for account in cur.fetchall():
        (id, name, balance, branch) = (value for value in account)
        accounts.append(Account(id=id, name=name, balance=balance, branch=branch))
    cur.close()
    return accounts

def load_transactions(conn: connector.Connection) -> list[Transaction]:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute('SELECT * from transactions')
    transactions: list[Transaction] = []
    transaction: list[int | float]
    for transaction in cur.fetchall():
        (sender, recipient, value) = (value for value in transaction)
        transactions.append(Transaction(sender=sender,recipient=recipient,value=value))
    return transactions

def write_transaction(conn: connector.Connection, transaction: Transaction) -> None:
    cur: connector.Cursor = conn.cursor()
    (sender, recipient, value) = (data for data in transaction.getAll)
    _ = cur.execute(f'INSERT INTO transactions ({sender},{recipient},{value})')
    conn.commit()
    cur.close()
    
def bank_funds(connection: connector.Connection) -> float:
    transactions: list[Transaction] = load_transactions(connection)
    balance: float = 0
    for transaction in transactions:
        balance += transaction.value
    return balance

def is_loanable(connection: connector.Connection, amount: float | int) -> bool:
    if bank_funds(connection) < amount:
        return False
    return True

def request_loan() -> None:
    pass