import main

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
    exitButton: None | int = None
    for index in range(len(options)):
        if options[index].lower() in ["exit", "back"]:
            exitButton = index
            continue
        print(f"{index}. {options[index]}")
    if exitButton is not None:
        print(f"{exitButton}. {options[exitButton]}")
    return int(input("Enter your choice:"))


def title(header: str) -> None:
    print(header.center(len(header) + 10, "-"))


def comma_table(data) -> str:
    table = ""
    for row in data:
        for field in row:
            table += str(field) + ","
        table = table[:-1] + "\n"
    return table


def view_transactions(conn: main.connector.Connection, id=None) -> None:
    transactions = main.load_transactions(conn)
    transactions = list(map(str, transactions))
    transactions = [transaction.split(",") for transaction in transactions]
    print("Transactions:")
    print("format:sender,receiver,value")
    print(comma_table(transactions))


def view_accounts(conn: main.connector.Connection) -> None:
    accounts = main.load_accounts(conn)
    accounts = list(map(str, accounts))
    ignore = []
    accounts = [account.split(",") for account in accounts]
    for index in range(len(accounts)):
        if int(accounts[index][-1]) == 1:
            ignore.append(index)
        else:
            _ = accounts[index].pop()
    print("Accounts:")
    print("format:id,name,balance,branch,type")
    print(comma_table(accounts))


def main_menu(conn: main.connector.Connection) -> None:
    title("Main Menu")
    options: list[str] = [
        "Exit",
        "Register New User Account",
        "Register Transaction",
        "View Accounts",
        "View Transactions",
        "Add Donation To Treasury",
    ]
    choice: int = selector(options)
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
            sender = int(("Enter sender account number:"))
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
            main.transact(conn, donation)


try:
    with open("bank.db", "rb"):
        pass
except FileNotFoundError:
    with main.connector.connect(DATABASE) as db:
        main.create_store(db)
        print(main.load_accounts(db))

while True:
    with main.connector.connect(DATABASE) as conn:
        main_menu(conn)
