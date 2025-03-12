from datetime import datetime
from fastapi import FastAPI, status, Depends, HTTPException
from zoneinfo import ZoneInfo
from models import Customer, Transaction, Invoice, CustomerCreate,CustomerUpdate
from db import get_session, SessionDep, create_all_tables
from sqlmodel import Session, select
from .routers import customer
# Inicializar la aplicación FastAPI y crear las tablas
app = FastAPI(lifespan=create_all_tables())
app.include_router(customer.router)
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

