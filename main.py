from datetime import datetime
from fastapi import FastAPI
from zoneinfo import ZoneInfo
from models import Customer
from models import Transaction
from models import Invoice,CustomerCreate
from db import get_session,SessionDep


app = FastAPI()

country_timezone = {
    "CO": "America/Bogota",
    "US": "America/New_York",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "ES": "Europe/Madrid",
    "FR": "Europe/Paris",
    "DE": "Europe/Berlin",
    "IT": "Europe/Rome",
    "PE": "America/Lima",
    "RD": "America/Santo_Domingo",
}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/time/{iso_code}")  # Agregué la barra '/'
async def time(iso_code: str):
    iso = iso_code.upper()
    timeZone_str = country_timezone.get(iso)

    if not timeZone_str:
        return {"error": "Invalid country code"}

    tz = ZoneInfo(timeZone_str)
    return {"time": datetime.now(tz).isoformat()}

db_customers :list[Customer]= []


@app.post("/customers",response_model=Customer)
async def create_customer(customer_data:CustomerCreate,session:SessionDep):
    customer=Customer.model_validate(customer_data.model_dump())
    #Asumiendo que se hace en la base de datos
    customer.id=len(db_customers)+1
    db_customers.append(customer)
    
    return customer

@app.get("/customers",response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get("/customers/{customer_id}",response_model=Customer)
async def list_customerid(customer_id:int):
    customer=next(c for c in db_customers if c.id==customer_id)
    return customer



@app.post("/transactions")
async def create_transactions(transaction_data:Transaction):
    
    return transaction_data

@app.post("/invoices")
async def create_invoices(invoices_data:Invoice):
    
    return invoices_data
