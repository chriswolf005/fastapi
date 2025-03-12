from fastapi import  APIRouter
from models import Invoice

# Endpoint para crear facturas
router=APIRouter()
@router.post("/invoices", response_model=Invoice,tags=["invoice"])
async def create_invoice(invoice_data: Invoice):
    return invoice_data