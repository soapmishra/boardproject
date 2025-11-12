from objects import Account, Transaction
import sqlite3

DATABASE = 'bank.db'
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
    accounts: list[Account] =[]
    for account in cur.fetchall():
        accountData = {
            "id" : str(int(account[0])),
            "name" : str(account[1]),
            "balance" : float(account[2]),
            "branch" : str(account[3])
            }
        accounts.append(Account(**accountData))
    return accounts

def load_transactions(conn: sqlite3.Connection) -> list[Transaction]:
    return []

with sqlite3.connect(DATABASE) as db:
    create_store(db)