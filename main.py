from datetime import datetime
from fastapi import FastAPI, status, Depends, HTTPException
from zoneinfo import ZoneInfo
from models import Customer, Transaction, Invoice, CustomerCreate,CustomerUpdate
from db import get_session, SessionDep, create_all_tables
from sqlmodel import Session, select

# Inicializar la aplicación FastAPI y crear las tablas
app = FastAPI(lifespan=create_all_tables())

# Diccionario de zonas horarias por país
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

@app.get("/time/{iso_code}")
async def get_time(iso_code: str):
    iso = iso_code.upper()
    time_zone_str = country_timezone.get(iso)

    if not time_zone_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid country code"
        )

    tz = ZoneInfo(time_zone_str)
    return {"time": datetime.now(tz).isoformat()}

# Endpoint para crear clientes
@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# Endpoint para listar todos los clientes
@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

# Endpoint para obtener un cliente por ID
@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(session: SessionDep, customer_id: int):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    return customer_db

# Endpoint para eliminar un cliente por ID
@app.delete("/customers/{customer_id}", status_code=status.HTTP_200_OK)
async def delete_customer(session: SessionDep, customer_id: int):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    session.delete(customer_db)
    session.commit()
    return {"message": "Customer deleted successfully"}

# Endpoint para actualizar un cliente por ID
@app.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
async def read_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

# Endpoint para crear transacciones
@app.post("/transactions", response_model=Transaction)
async def create_transaction(transaction_data: Transaction):
    return transaction_data

# Endpoint para crear facturas
@app.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: Invoice):
    return invoice_data
