from typing import Iterator


import random

class Account:

    def __init__(self, id, name, balance, branch):
        self.id: int = random.randint(1000, 9999) if id not in range(1000, 10000) else id
        self.name: str = name
        self.branch: str = branch
        self.balance: float = balance

    def __str__(self) -> str:
        return f"'{self.id}','{self.name}',{self.balance},'{self.branch}'"

    def __repr__(self) -> str:
        return f"Acount({self.id}, {self.name}, {self.balance}, {self.branch})"
    
    def __iter__(self) -> Iterator[int | str | float]:
        return iter((self.id, self.name, self.balance, self.branch))

    def __getitem__(self, item) -> int | float:
        return tuple(self)[item]


class Transaction:

    def __init__(self, sender, recipient, value):
        self.sender: int = sender
        self.recipient: int = recipient
        self.value: float = value

    def __str__(self) -> str:
        return f"'{self.sender}','{self.recipient}',{self.value}"

    def __repr__(self) -> str:
        return f"Transaction(Sender Account Number:{self.sender}, Recipient Account Number: {self.recipient}, Amount: {self.value})"

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

    def __iter__(self) -> Iterator[int | float]:
        return iter((self.sender, self.recipient, self.value))

    def __getitem__(self, item) -> int | float:
        return tuple(self)[item]