import main

DATABASE = 'bank.db'

def selector(options:list[str]) -> int:
    for index in range(len(options)):
        print(index+1, options[index])
    return int(input('Enter your choice:'))


with main.sqlite3.connect(DATABASE) as db:
    main.create_store(db)
    print(main.load_accounts(db))