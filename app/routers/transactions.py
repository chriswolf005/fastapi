from fastapi import APIRouter, status, HTTPException, Depends, Query
from models import Transaction, Customer, TransactionCreate
from db import SessionDep
from sqlmodel import select

router = APIRouter()

# Endpoint para crear transacciones
@router.post("/transactions", tags=["transactions"])
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    
    return transaction_db

# Endpoint para listar transacciones con paginación
@router.get("/transactions", tags=["transactions"])
async def list_transaction(
    session: SessionDep, 
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(10, description="Número máximo de registros a devolver")
):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions
