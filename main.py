from objects import Account, Transaction
import sqlite3 as connector


def create_store(conn: connector.Connection) -> None:
    cur: connector.Cursor = conn.cursor()
    tables: tuple[str, str] = ("accounts (account_number VARCHAR(20) PRIMARY KEY, name VARCHAR(100), balance DOUBLE DEFAULT 0.0, branch VARCHAR(20))",
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
        accounts.append(Account(id=int(id), name=name, balance=float(balance), branch=branch))
    cur.close()
    return accounts

def load_transactions(conn: connector.Connection) -> list[Transaction]:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute('SELECT * from transactions')
    transactions: list[Transaction] = []
    transaction: list[int | float]
    for transaction in cur.fetchall():
        (sender, recipient, value) = (value for value in transaction)
        transactions.append(Transaction(sender=int(sender),recipient=int(recipient),value=value))
    return transactions

def write_transaction(conn: connector.Connection, transaction: Transaction) -> None:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute(f'INSERT INTO transactions values {tuple(transaction)}')
    conn.commit()
    cur.close()

def write_account(conn: connector.Connection, account: Account) -> None:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute(f'INSERT INTO accounts values {tuple(account)} ')
    conn.commit()
    cur.close()

def remove_account(conn, account: int | str | Account):
    cur: connector.Cursor = conn.cursor()
    if isinstance(account, int):
        _ = cur.execute(f'DELETE FROM accounts WHERE account_number = "{account}"')
        cur.close()
    elif isinstance(account, str):
        _ = cur.execute(f'DELETE FROM accounts WHERE name = "{account}"')
        cur.close()
    elif isinstance(account, Account):
        _ = cur.execute(f'DELETE FROM accounts WHERE "{account[0]}"')
        cur.close()

def update_account(conn, id, value: float | str ):
    cur: connector.Connection = conn.cursor()
    if isinstance(value, float):
        _ = cur.execute(f'UPDATE account SET balance = balance + {value}')
    elif isinstance(value, str):
        _ = cur.execute(f'UPDATE accounts SET name = "{value}"')

def transact(conn: connector.Connection, transaction: Transaction):
    (sender, receiver, amount) = transaction
    update_account(conn, sender, -amount)
    update_account(conn, receiver, amount)
    write_transaction(conn, transaction)
    
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
    #TODO: WIP

def request_loan() -> None:
    pass
    #TODO: implement