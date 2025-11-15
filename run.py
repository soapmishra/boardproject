import main
import os
import time
import sys


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text: str, delay: float = 0.01) -> None:
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def header(text: str) -> None:
    width = max(len(text) + 10, 50)
    print(Color.OKCYAN + ("=" * width) + Color.ENDC)
    print(Color.BOLD + text.center(width) + Color.ENDC)
    print(Color.OKCYAN + ("=" * width) + Color.ENDC)


def pause(message="Press Enter to continue..."):
    input(Color.OKBLUE + message + Color.ENDC)


def paginated_view(rows: list[list[str]], page_size: int = 10, columns="") -> None:
    """Display lists in paginated form."""
    if not rows:
        print("No data available.")
        return

    index = 0
    while index < len(rows):
        clear_screen()
        if columns != "":
            print(columns)
        print(
            Color.BOLD
            + f"Showing rows {index+1} to {min(index+page_size, len(rows))}"
            + Color.ENDC
        )
        print("-" * 50)

        for row in rows[index : index + page_size]:
            print(" | ".join(str(x) for x in row))

        print("-" * 50)

        if index + page_size >= len(rows):
            break

        choice = input("Next page? (Y/n): ")
        if choice.lower() not in ("", "y"):
            break

        index += page_size


DATABASE = "bank.db"
BRANCHES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
]
AC_TYPES = ["Checking Acount", "Savings Account", "Salary Account"]


def selector(options: list[str]) -> int:
    print()
    for i, option in enumerate(options):
        print(f"{Color.OKGREEN}{i}{Color.ENDC}. {option}")
    print()
    return int(input("Enter your choice: "))


def title(header_text: str):
    header(header_text)


def comma_table(data) -> str:
    table = ""
    for row in data:
        for field in row:
            table += str(field) + ","
        table = table[:-1] + "\n"
    return table


def view_transactions(conn):
    transactions = main.load_transactions(conn)
    rows = [str(x).split(",") for x in transactions]

    header("Transactions")
    columns = "Columns: Sender | Receiver | Value"
    paginated_view(rows, page_size=10, columns=columns)
    pause()


def view_accounts(conn):
    accounts = main.load_accounts(conn)
    rows = []
    for acc in accounts:
        if acc.deleted == 0:
            rows.append([acc.id, acc.name, acc.balance, acc.branch, acc.type])

    header("Accounts")
    columns = "Columns: ID | Name | Balance | Branch | Type"
    paginated_view(rows, page_size=10, columns=columns)
    pause()


def view_statement(conn):
    clear_screen()
    header("Account Statement Generator")

    try:
        account_id = int(input("Enter account number: "))
    except ValueError:
        print(Color.FAIL + "Invalid account number." + Color.ENDC)
        pause()
        return

    # Try to load the account
    try:
        account = main.load_account(conn, account_id)
    except:
        print(Color.FAIL + "Account does not exist." + Color.ENDC)
        pause()
        return

    # Fetch all transactions
    transactions = main.load_transactions(conn)

    incoming = []
    outgoing = []

    # Categorize transactions
    for t in transactions:
        if t.recipient == account_id:
            incoming.append([t.sender, t.recipient, t.value])
        elif t.sender == account_id:
            outgoing.append([t.sender, t.recipient, t.value])

    clear_screen()
    header(f"Statement for Account {account_id}")

    # Show account info
    print(Color.BOLD + f"Name: {account.name}" + Color.ENDC)
    print(f"Branch: {account.branch}")
    print(f"Type: {account.type}")
    print(Color.OKGREEN + f"Current Balance: {account.balance}" + Color.ENDC)
    print("\n")

    # Display incoming
    print(Color.OKCYAN + "Incoming Transactions" + Color.ENDC)
    if incoming:
        paginated_view(incoming)
    else:
        print("No incoming transactions.\n")

    # Display outgoing
    print(Color.OKCYAN + "Outgoing Transactions" + Color.ENDC)
    if outgoing:
        paginated_view(outgoing)
    else:
        print("No outgoing transactions.\n")

    pause("End of statement. Press Enter to return...")


def main_menu(conn: main.connector.Connection) -> None:
    clear_screen()
    title("Main Menu")
    options: list[str] = [
        "Log out",
        "Register New Bank Account",
        "Register Transaction",
        "View Accounts",
        "View Transactions",
        "Add Donation To Treasury",
        "Create Administrator Account",
        "Delete Administrator Account",
        "Add Money Deposit",
        "View Account Statement",
    ]
    choice: int = selector(options)
    clear_screen()
    match choice:
        case 0:
            exit()
        case 1:
            # Register New User Account
            name = input("Enter account holder name:")
            title("Select a branch:")
            branch = BRANCHES[selector(BRANCHES)]
            title("Select account type:")
            ac_type = AC_TYPES[selector(AC_TYPES)]
            existing_acnumber = map(tuple, main.load_accounts(conn))
            existing_acnumber = max(int(x[0]) for x in existing_acnumber)
            account = main.Account(
                id=existing_acnumber + 1,
                name=name,
                balance=0.0,
                branch=branch,
                type=ac_type,
            )
            print(repr(account))
            if input("Confirm (y/N): ") in "Yy":
                main.write_account(conn, account)
        case 2:
            # Register Transaction
            sender = int(input("Enter sender account number:"))
            reciever = int(input("Enter receiver account number:"))
            value = abs(int(input("Enter amount to send:")))
            transaction = main.Transaction(sender, reciever, value)
            print(repr(transaction))
            if input("Confirm (y/N): ") in "Yy":
                main.transact(conn, transaction)
        case 3:
            # View Accounts
            view_accounts(conn)
        case 4:
            # View Transactions
            view_transactions(conn)
        case 5:
            # Add Donation To Treasury
            donor = int(input("Enter donor account number:"))
            amount = abs(int(input("Enter amount to donate:")))
            donor = main.load_account(conn, donor)
            donation = main.donation(conn, donor, amount)
            print(repr(donation))
            if input("Confirm (y/N)") in "Yy":
                main.transact(conn, donation)
        case 6:
            # Add new administrator account
            username = input("Enter Username:")
            password = input("Set Password")
            id = main.get_max_admin_id(conn) + 1
            administrator = main.Administrator(id, username, password)
            print(repr(administrator))
            if input("Confirm (y/N)") in "Yy":
                main.write_admin(conn, administrator)
        case 7:
            password = input("Enter password for account to remove:")
            main.remove_admin(conn, password)
        case 8:
            # Add Money Deposit
            account_id = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit: "))

            if amount <= 0:
                print("Invalid amount.")
            else:
                print(f"Deposit {amount} into Account {account_id}?")
                if input("Confirm (y/N): ") in "Yy":
                    try:
                        main.update_account(conn, account_id, amount)
                        print("Deposit successful.")
                    except:
                        print("Deposit failed. Account may not exist.")
        case 9:
            # View Account Statement
            view_statement(conn)


try:
    with open("bank.db", "rb"):
        pass
except FileNotFoundError:
    with main.connector.connect(DATABASE) as db:
        main.create_store(db)


def main_activity():
    # Login ONCE
    with main.connector.connect(DATABASE) as conn:
        while True:
            password = input("Enter your password: ")
            if main.login_admin(conn, password=password):
                print("Login successful.\n")
                break
            else:
                print("Try again, wrong password.\n")

    # After login, stay in the menu forever
    while True:
        with main.connector.connect(DATABASE) as conn:
            main_menu(conn)


if __name__ == "__main__":
    main_activity()
