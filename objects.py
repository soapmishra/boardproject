import random

class Account:

    def __init__(self, id, name, balance, branch):
        self.id: int = random.randint(1000, 9999) if id not in range(1000, 10000) else id
        self.name: str = name
        self.branch: str = branch
        self.balance: float = balance

    def get(self, what: str) -> str|int|float|None:
        match what:
            case 'id':
                return self.id
            case 'name':
                return self.name
            case 'balance':
                return self.balance
            case 'branch':
                return self.balance
            case _:
                pass


class Transaction:
    pass