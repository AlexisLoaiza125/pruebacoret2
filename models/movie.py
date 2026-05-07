from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class MovieBase(SQLModel):
    id: int = Field(primary_key=True, index=True)
    title: str
    description: str
    year: int
    poster_url: Optional[str] = None
    director_id: int = Field(foreign_key="director.id")
    is_active: bool = Field(default=True)  # <-- Nueva columna

class Movie(MovieBase, table=True):
    director: "Director" = Relationship(back_populates="movies")
    reviews: List["Review"] = Relationship(back_populates="movie")

class MovieCreate(MovieBase):
    pass

class MovieUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    director_id: Optional[int] = None

class MoviePublic(MovieBase):
    id: int