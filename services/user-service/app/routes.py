# Interface layer — HTTP endpoints.
#
# This file defines the FastAPI router and maps HTTP verbs + paths to
# service function calls. It is the only layer that knows about HTTP.
#
# Rules:
# - Never call repository functions directly — always go through service
# - Catch ValueError from the service layer and raise HTTPException instead
# - Use Depends(get_db) to inject the database session
#
# This file should expose:
# - POST   /v1/users/          -> create a user
# - GET    /v1/users/          -> list users (with limit/offset pagination)
# - GET    /v1/users/{user_id} -> get one user by ID (404 if not found)
#
# See the README for the full implementation.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserOut, UserList
from app import service

router = APIRouter(prefix="/v1/users")

@router.post("/", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return service.add_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=UserList)
def list_users(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return service.fetch_all_users(db, limit, offset)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return service.fetch_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
