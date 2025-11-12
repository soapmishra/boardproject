import random

class Account:

    def __init__(self, id, name, balance, branch):
        self.id: int = random.randint(1000, 9999) if id not in range(1000, 10000) else id
        self.name: str = name
        self.branch: str = branch
        self.balance: float = balance

    def get(self, what: str) -> str | None:
        match what:
            case 'id':
                return str(self.id)
            case 'name':
                return str(self.name)
            case 'balance':
                return str(self.balance)
            case 'branch':
                return str(self.branch)
            case _:
                pass


class Transaction:

    def __init__(self, sender, recipient, value):
        self.sender: int = sender
        self.recipient: int = recipient
        self.value: float = value

    def get(self, what: str) -> str|None:
        match what:
            case 'sender':
                return str(self.sender)
            case 'recipient':
                return str(self.recipient)
            case 'value':
                return str(self.value)
            case _:
                pass