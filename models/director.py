from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class DirectorBase(SQLModel):
    name: str
    nationality: str

class Director(DirectorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movies: List["Movie"] = Relationship(back_populates="director")

class DirectorCreate(DirectorBase):
    pass

class DirectorPublic(DirectorBase):
    id: int