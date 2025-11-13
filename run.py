import main

DATABASE = 'bank.db'

def selector(options:list[str]) -> int:
    exitButton: None | int = None
    for index in range(len(options)):
        if options[index].lower() in ['exit','back']:
            exitButton = index
            continue
        print(f"{index}. {options[index]}")
    if exitButton is not None:
        print(f"{exitButton}. {options[exitButton]}")
    return int(input('Enter your choice:'))

def title(header: str) -> None:
    print(header.center(len(header)+10, '-'))

def comma_table(data: list[list[object]|tuple[object]]) -> str:
    table=''
    for row in data:
        for field in row:
            table+=str(field)+'\n'
        table+='\n'
    return table
    return table

def view_transactions(transactions: str) -> None:
    print('Transactions:')
    print('format:sender,receiver,value')
    print(transactions)



def main_menu() -> None:
    title("Main Menu")
    options: list[str] = ['Exit', 'Create new account','Send money', 'View transactions', 'Request Loan']
    choice: int = selector(options)
    match choice:
        case 0:
            exit()
        case 1:
            pass #TODO: implement account creation
        case 2:
            pass #TODO: implement transaction send
        case 3:
            pass #TODO: implement loans

try:
    with open('bank.db','rb'):
        pass
except FileNotFoundError:
    with main.connector.connect(DATABASE) as db:
        main.create_store(db)
        print(main.load_accounts(db))

while True:
    main_menu()