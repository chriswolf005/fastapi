from fastapi import  APIRouter
from models import Transaction

router=APIRouter()
# Endpoint para crear transacciones
@router.post("/transactions", response_model=Transaction ,tags=["transactions"])
async def create_transaction(transaction_data: Transaction):
    return transaction_data