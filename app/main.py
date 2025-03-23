from typing import Annotated
from fastapi import Depends, FastAPI, Request, status, HTTPException
from datetime import datetime
import time
from zoneinfo import ZoneInfo

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Customer, Transaction, Invoice, CustomerCreate, CustomerUpdate
from db import create_all_tables
from .routers import customer, transactions, plans

# Inicializar la aplicación FastAPI y crear las tablas
app = FastAPI(lifespan=create_all_tables())
app.include_router(customer.router)
app.include_router(transactions.router)
app.include_router(plans.router)

# Middleware para imprimir headers y tiempos de respuesta
@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    start_time = time.time()
    
    # Imprimir todos los headers
    print("\n---- Incoming Request Headers ----")
    for key, value in request.headers.items():
        print(f"{key}: {value}")
    print("----------------------------------\n")

    response = await call_next(request)

    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    print(f"Request {request.url} completed in {process_time:.4f} seconds")

    return response
security = HTTPBasic()
@app.get("/")
async def root(credentials:Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username=="admin" and credentials.password=="admin":
        return {"message":"Welcome Admin"}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Unauthorized")
       

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
