import random

class Account:
    def __init__(self, name: str, branch: str, balance: float = 0, id: int = 0):
        self.id: int = random.randint(1000, 9999) if id not in range(1000, 10000) else id
        self.name: str = name
        self.branch: str = branch
        self.balance: float = balance


class Transaction:
    pass