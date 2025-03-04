from pydantic import BaseModel
class CustomerBase(BaseModel):
    name: str
    description: str |None
    email:str
    age:int

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None = None

class Transaction(BaseModel):
    id: int
    amount: int
    description: str 

class Invoice(BaseModel):
    id: int
    customer: Customer
    transaction: list[Transaction]
    date: str
    total: int
    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transaction)