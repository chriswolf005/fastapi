from fastapi import APIRouter, status, HTTPException, Query
from sqlmodel import select

from models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from db import SessionDep

router = APIRouter()

# Endpoint para crear clientes
@router.post(
    "/customers",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"]
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# Endpoint para listar todos los clientes
@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

# Endpoint para obtener un cliente por ID
@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def get_customer(session: SessionDep, customer_id: int):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    return customer_db

# Endpoint para eliminar un cliente por ID
@router.delete("/customers/{customer_id}", status_code=status.HTTP_200_OK, tags=["customers"])
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
@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"]
)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

# Endpoint para suscribir un cliente a un plan
@router.post("/customers/{customer_id}/plans/{plan_id}")
async def subscribe_customer_to_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The customer or plan doesn't exist"
        )
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

# Endpoint para obtener los planes de un cliente
@router.get("/customers/{customer_id}/plans")
async def get_customer_plans(customer_id: int, session: SessionDep
,plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer doesn't exist"
        )
    query=(select(CustomerPlan)
           .where(CustomerPlan.customer_id==customer_id)
           .where(CustomerPlan.status==plan_status)
           )
    plans=session.exec(query).all()
    return plans