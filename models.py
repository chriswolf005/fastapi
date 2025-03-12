from pydantic import BaseModel
from sqlmodel import SQLModel,Field
class CustomerBase(SQLModel):
    name: str= Field(default=None)
    description: str |None = Field(default=None)
    email:str = Field(default=None)
    age:int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase,table=True):
    id: int | None = Field(default=None, primary_key=True)

class Transaction(BaseModel):
    id: int= Field(default=None)
    amount: int= Field(default=None)
    description: str = Field(default=None)

class Invoice(BaseModel):
    id: int
    customer: Customer
    transaction: list[Transaction]
    date: str
    total: int
    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transaction)