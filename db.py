import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated, Generator
from fastapi import Depends

load_dotenv()

# 1. Asegúrate de que el driver sea psycopg2
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

# 2. Motor sincrónico estándar
engine = create_engine(database_url, echo=True, pool_pre_ping=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)