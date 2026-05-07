from sqlmodel import Session, select
from models.director import Director, DirectorCreate
from fastapi import HTTPException, status
from typing import List

def create_director(session: Session, director_data: DirectorCreate) -> Director:
    """Crea un nuevo director en la base de datos."""
    db_director = Director.model_validate(director_data)
    session.add(db_director)
    session.commit()
    session.refresh(db_director)
    return db_director

def get_directors(session: Session, skip: int = 0, limit: int = 10) -> List[Director]:
    """Obtiene una lista de directores con paginación."""
    statement = select(Director).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_director_by_id(session: Session, director_id: int) -> Director:
    """Busca un director por ID o lanza 404 si no existe."""
    director = session.get(Director, director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Director con id {director_id} no encontrado"
        )
    return director

def delete_director(session: Session, director_id: int):
    """Elimina un director."""
    db_director = get_director_by_id(session, director_id)
    session.delete(db_director)
    session.commit()
    return {"message": "Director eliminado exitosamente"}