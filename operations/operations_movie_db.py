from sqlmodel import Session, select
from models.movie import Movie, MovieCreate, MovieUpdate
from fastapi import HTTPException, status

def create_movie(session: Session, movie_data: MovieCreate, poster_path: str = None) -> Movie:
    db_movie = Movie.model_validate(movie_data)
    if poster_path:
        db_movie.poster_url = poster_path
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

def get_movies(session: Session, skip: int = 0, limit: int = 10):
    # Solo seleccionamos las películas activas
    statement = select(Movie).where(Movie.is_active == True).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_movie_by_id(session: Session, movie_id: int):
    movie = session.get(Movie, movie_id)
    # Si no existe O está desactivada, lanzamos 404
    if not movie or not movie.is_active:
        raise HTTPException(status_code=404, detail="Movie not found or inactive")
    return movie

def delete_movie(session: Session, movie_id: int):
    # Buscamos la película (usamos session.get para incluir las inactivas si quisieras restaurarlas)
    db_movie = session.get(Movie, movie_id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Borrado lógico
    db_movie.is_active = False
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return {"message": "Película movida al historial (desactivada)"}