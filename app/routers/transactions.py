from fastapi import  APIRouter,status,HTTPException
from models import Transaction,Customer
from models import TransactionCreate
from db import SessionDep
from sqlmodel import select

router=APIRouter()
# Endpoint para crear transacciones
@router.post("/transactions" ,tags=["transactions"])
async def create_transaction(transaction_data: TransactionCreate,session:SessionDep):
    transaction_data_dict=transaction_data.model_dump()
    Customer=session.get(Customer,transaction_data_dict.get('customer_id'))
    if not Customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    Transaction_db=Transaction.model_validate(transaction_data_dict)
    session.add(Transaction_db)
    session.commit()
    session.refresh(Transaction_db)
    return transaction_data

@router.get("/transactions",tags=["transactions"])
async def list_transaction(session: SessionDep):
    query=select(Transaction)
    Transaction=session.exec(query.all())
    return Transaction