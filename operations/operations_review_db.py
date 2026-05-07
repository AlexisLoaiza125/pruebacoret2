from sqlmodel import Session, select
from models.review import Review, ReviewCreate
from models.movie import Movie
from fastapi import HTTPException, status
from typing import List

def create_review(session: Session, review_data: ReviewCreate) -> Review:
    """
    Crea una reseña validando primero que la película asociada exista.
    """
    # Verificación de integridad manual para manejo de errores limpio
    movie = session.get(Movie, review_data.movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede crear reseña: La película {review_data.movie_id} no existe"
        )
    
    db_review = Review.model_validate(review_data)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

def get_reviews_by_movie(session: Session, movie_id: int) -> List[Review]:
    """Obtiene todas las reseñas de una película específica."""
    statement = select(Review).where(Review.movie_id == movie_id)
    return session.exec(statement).all()

def get_review_by_id(session: Session, review_id: int) -> Review:
    """Busca una reseña por ID."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada"
        )
    return review

def delete_review(session: Session, review_id: int):
    """Elimina una reseña."""
    db_review = get_review_by_id(session, review_id)
    session.delete(db_review)
    session.commit()
    return {"message": "Reseña eliminada"}