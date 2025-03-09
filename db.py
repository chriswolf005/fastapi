from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"
engine = create_engine(sqlite_url, echo=True)  # 'echo=True' para ver las consultas en consola

def create_all_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Crear la aplicación y las tablas al iniciar
app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_all_tables()
