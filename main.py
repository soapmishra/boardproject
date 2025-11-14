from objects import Account, Transaction
import sqlite3 as connector


def create_store(conn: connector.Connection) -> None:
    cur: connector.Cursor = conn.cursor()
    tables: tuple[str, str, str] = (
        "accounts (account_number TEXT PRIMARY KEY, name TEXT, balance DOUBLE DEFAULT 0.0, branch TEXT, type TEXT, deleted TEXT)",
        "transactions (sender TEXT NOT NULL, recipient TEXT NOT NULL, value DOUBLE NOT NULL, FOREIGN KEY (sender) REFERENCES accounts(account_number), FOREIGN KEY (recipient) REFERENCES accounts(account_number))",
        "administrators (administrator_id TEXT, name TEXT, password_hash TEXT)"
    )
    for table in tables:
        try:
            _ = cur.execute(f"CREATE TABLE {table}")
        except:
            pass
    treasury: Account = Account(999, "Bank Treasury", 0.0, "Headquarters", "Official")
    write_account(conn, treasury)
    conn.commit()
    cur.close()


def load_accounts(conn: connector.Connection) -> list[Account]:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute("SELECT * from accounts")
    accounts: list[Account] = []
    account_data: tuple[int, int, str, float, int]
    for account_data in cur.fetchall():
        account = Account(*account_data)
        accounts.append(account)
    return accounts


def load_account(conn: connector.Connection, id: int) -> Account:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute(f"SELECT * from accounts where account_number = '{id}'")
    account_data = cur.fetchone()
    account: Account = Account(*account_data)
    return account


def load_transactions(conn: connector.Connection) -> list[Transaction]:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute("SELECT * from transactions")
    transactions: list[Transaction] = []
    transaction_data: tuple[int, int, float]
    for transaction_data in cur.fetchall():
        transaction = Transaction(*transaction_data)
        transactions.append(transaction)
    return transactions


def write_transaction(conn: connector.Connection, transaction: Transaction) -> None:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute(f"INSERT INTO transactions values {tuple(transaction)}")
    conn.commit()
    cur.close()


def write_account(conn: connector.Connection, account: Account) -> None:
    cur: connector.Cursor = conn.cursor()
    _ = cur.execute(f"INSERT INTO accounts values {tuple(account)} ")
    conn.commit()
    cur.close()


def delete_account(conn, data: int | str | Account):
    cur: connector.Cursor = conn.cursor()
    if isinstance(data, int):
        _ = cur.execute(f'DELETE FROM accounts WHERE account_number = "{data}"')
    elif isinstance(data, str):
        _ = cur.execute(f'DELETE FROM accounts WHERE name = "{data}"')
    elif isinstance(data, Account):
        _ = cur.execute(f'DELETE FROM accounts WHERE account_number = "{data[0]}"')
    cur.close()
    conn.commit()


def update_account(conn, id, value: float | str):
    cur: connector.Connection = conn.cursor()
    if isinstance(value, float):
        _ = cur.execute(
            f"UPDATE account SET balance = balance + {value} WHERE id = {id}"
        )
    elif isinstance(value, str):
        _ = cur.execute(f'UPDATE accounts SET name = "{value}" WHERE id = {id}')
    cur.close()
    conn.commit()


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


def donation(conn: connector.Connection, Account: Account, amount: float):
    donation = Transaction(sender=Account[0], recipient=999, value=amount)
    return donation


# TODO: implement Administrator account creation
# TODO: implement Administrator login
# TODO: implement Administrator account deletion with protection against removal of all administrators
