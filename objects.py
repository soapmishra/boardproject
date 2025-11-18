import hashlib


class Account:

    def __init__(self, id, name, balance, branch, type, deleted=0):
        self.id: int = int(id)
        self.name: str = str(name)
        self.branch: str = str(branch)
        self.balance: float = float(balance)
        self.type: str = str(type)
        self.deleted: int = int(deleted)

    def __str__(self) -> str:
        return f"{self.id},{self.name},{self.balance},{self.branch},{self.type},{int(self.deleted)}"

    def __repr__(self) -> str:
        return f"Acount(Acount ID: {self.id}, Account Name: {self.name}, Account Balance: {self.balance}, Bank Branch: {self.branch}, Account Type: {self.type})"

    def __iter__(self):
        return iter(
            (self.id, self.name, self.balance, self.branch, self.type, self.deleted)
        )

    def __getitem__(self, item) -> int | float:
        return tuple(self)[item]


class Transaction:

    def __init__(self, sender, recipient, value):
        self.sender: int = int(sender)
        self.recipient: int = int(recipient)
        self.value: float = float(value)

    def __str__(self) -> str:
        return f"{self.sender},{self.recipient},{self.value}"

    def __repr__(self) -> str:
        return f"Transaction(Sender Account Number:{self.sender}, Recipient Account Number: {self.recipient}, Amount: {self.value})"

    def __iter__(self):
        return iter(
            (self.sender, self.recipient, self.value)
            )

    def __getitem__(self, item) -> int | float:
        return tuple(self)[item]


class Administrator:

    def __init__(self, id, name, password):
        self.id: int = int(id)
        self.name: str = str(name)
        self.__password: str = str(password)
        self.passwordhash = self.__password.encode("utf-8")
        self.passwordhash = hashlib.sha256(self.passwordhash).hexdigest()

    def __str__(self) -> str:
        return f"{self.id},{self.name},{self.passwordhash}"

    def __repr__(self) -> str:
        return f"Administrator(ID: {self.id}, Name: {self.name}, Password: {self.__password})"

    def __iter__(self):
        return iter((self.id, self.name, self.passwordhash))

    def __getitem__(self, item):
        return tuple(self)[item]
