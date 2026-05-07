from contextlib import asynccontextmanager
from typing import List, Annotated
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from db import create_db_and_tables, SessionDep
from utils import save_poster
from models.movie import Movie, MoviePublic, MovieCreate, MovieUpdate
from models.director import DirectorPublic, DirectorCreate, Director
from models.review import ReviewPublic, ReviewCreate, Review
from operations import operations_movie_db as movie_ops
from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# --- ENDPOINTS MOVIE (CRUD Completo) ---

@app.post("/movies/", response_model=MoviePublic)
async def create_movie(
    session: SessionDep,
    id: Annotated[int, Form()],
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    year: Annotated[int, Form()],
    director_id: Annotated[int, Form()],
    file: UploadFile = File(...)
):
    poster_path = save_poster(file)
    movie_in = MovieCreate(id=id,title=title, description=description, year=year, director_id=director_id)
    return movie_ops.create_movie(session, movie_in, poster_path)

@app.get("/movies/", response_model=List[MoviePublic])
def read_movies(session: SessionDep, skip: int = 0, limit: int = 10):
    return movie_ops.get_movies(session, skip, limit)

@app.patch("/movies/{movie_id}", response_model=MoviePublic)
def update_movie(session: SessionDep, movie_id: int, movie_data: MovieUpdate):
    return movie_ops.update_movie(session, movie_id, movie_data)

@app.delete("/movies/{movie_id}")
def delete_movie(session: SessionDep, movie_id: int):
    return movie_ops.delete_movie(session, movie_id)

# --- ENDPOINTS DIRECTOR & REVIEW (CRUD Básico) ---

@app.post("/directors/", response_model=DirectorPublic)
def create_director(session: SessionDep, director: DirectorCreate):
    db_director = Director.model_validate(director)
    session.add(db_director)
    session.commit()
    session.refresh(db_director)
    return db_director

@app.post("/reviews/", response_model=ReviewPublic)
def create_review(session: SessionDep, review: ReviewCreate):
    db_review = Review.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review




@app.get("/movies/history/", response_model=List[MoviePublic])
def read_deleted_movies(session: SessionDep):
    # Trae solo las que tienen is_active en False
    statement = select(Movie).where(Movie.is_active == False)
    return session.exec(statement).all()