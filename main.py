from objects import Account, Administrator, Transaction
import hashlib
import sqlite3 as connector


def create_store(conn: connector.Connection, passwd="") -> None:
    if passwd == "":
        passwd = input("Enter Default Administrator(id: 0) Password:")
    cur: connector.Cursor = conn.cursor()
    tables: tuple[str, str, str] = (
        "accounts (account_number TEXT PRIMARY KEY, name TEXT, balance DOUBLE DEFAULT 0.0, branch TEXT, type TEXT, deleted TEXT)",
        "transactions (sender TEXT NOT NULL, recipient TEXT NOT NULL, value DOUBLE NOT NULL, FOREIGN KEY (sender) REFERENCES accounts(account_number), FOREIGN KEY (recipient) REFERENCES accounts(account_number))",
        "administrators (administrator_id TEXT, name TEXT, password_hash TEXT)",
    )
    for table in tables:
        try:
            _ = cur.execute(f"CREATE TABLE {table}")
        except:
            pass
    treasury: Account = Account(999, "Bank Treasury", 0.0, "Headquarters", "Official")
    default_admin: Administrator = Administrator(0, "Default Administrator", passwd)
    write_admin(conn, default_admin)
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
            f"UPDATE accounts SET balance = balance + {value} WHERE account_number = {id}"
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


def write_admin(conn: connector.Connection, admin: Administrator) -> None:
    cur = conn.cursor()
    _ = cur.execute(f"INSERT INTO administrators values {tuple(admin)}")
    cur.close()
    conn.commit()


def login_admin(conn: connector.Connection, password: str) -> bool:
    cur = conn.cursor()
    bytes = password.encode("utf-8")
    hex_digest = hashlib.sha256(bytes).hexdigest()
    _ = cur.execute(
        f'SELECT password_hash FROM administrators WHERE password_hash = "{hex_digest}"'
    )
    try:
        if len(cur.fetchall()) != 0:
            return True
        return False
    finally:
        cur.close()


def get_max_admin_id(conn: connector.Connection) -> int:
    cur = conn.cursor()
    _ = cur.execute(f"SELECT max(administrator_id) from administratos")
    max_id = cur.fetchone()
    return max_id[0] if len(max_id) != 0 else -1


def remove_admin(conn: connector.Connection, password: str) -> None:
    check_cur = conn.cursor()
    _ = check_cur.execute("SELECT * FROM administrators")
    hex_digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    if len(check_cur.fetchall()) > 1:
        cur = conn.cursor()
        _ = cur.execute(
            f'DELETE FROM administrators WHERE password_hash = "{hex_digest}"'
        )
        conn.commit()
        cur.close()


def deposit(conn: connector.Connection, account_id: int, amount: float) -> bool:
    """Deposit money into an account safely."""
    if amount <= 0:
        return False

    try:
        account = load_account(conn, account_id)
    except:
        return False

    cur = conn.cursor()
    _ = cur.execute(
        f"UPDATE accounts SET balance = balance + {amount} WHERE account_number = '{account_id}'"
    )
    conn.commit()
    cur.close()
    return True
