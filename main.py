from objects import Account, Transaction

import sqlite3
DATABASE = 'bank.db'
def create_store(conn: sqlite3.Connection) -> None:
    cur: sqlite3.Cursor = conn.cursor()
    tables: tuple[str, str] = ("accounts (account_number VARCAHR(20) PRIMARY KEY, name VARCHAR(100), balance DOUBLE DEFAULT 0.0)",
                                                   "transactions (sender VARCHAR(20) NOT NULL, recipient VARCHAR(20) NOT NULL, value DOUBLE NOT NULL, FOREIGN KEY (sender) REFERENCES accounts(account_number), FOREIGN KEY (recipient) REFERENCES accounts(account_number))")
    for table in tables:
        try:
            _ = cur.execute(f'CREATE TABLE {table}')
        except:
            pass

def load_accounts(conn) -> list[Account]:
    return []

def load_transactions(conn) -> list[Transaction]:
    return []
with sqlite3.connect(DATABASE) as db:
    create_store(db)