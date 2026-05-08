import os
from dotenv import load_dotenv

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from fastapi import Depends
from typing import Annotated

load_dotenv()

# -----------------------------
# URLS
# -----------------------------

NEON_DATABASE_URL = os.getenv("DATABASE_URL")

LOCAL_DATABASE_URL = "sqlite:///movies.db"

# -----------------------------
# Intentar Neon
# -----------------------------

try:
    print("Intentando conectar a Neon...")

    engine = create_engine(
        NEON_DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )

    # prueba real de conexión
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("Conectado a Neon correctamente")

except Exception as e:
    print("No se pudo conectar a Neon")
    print("Usando SQLite local...")
    print(f"Error: {e}")

    engine = create_engine(
        LOCAL_DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )

# -----------------------------
# Crear tablas
# -----------------------------

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# -----------------------------
# Sesión
# -----------------------------

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
