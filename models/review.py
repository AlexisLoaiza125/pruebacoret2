from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class ReviewBase(SQLModel):
    rating: int
    comment: str
    movie_id: int = Field(foreign_key="movie.id")

class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie: "Movie" = Relationship(back_populates="reviews")

class ReviewCreate(ReviewBase):
    pass

class ReviewPublic(ReviewBase):
    id: int