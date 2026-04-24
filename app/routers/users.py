from app import routers
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.users import get_user, get_user_by_email, create_user, update_user, delete_user
from schemas import UserCreate, UserUpdate, User
from database import SessionLocal

users_router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post("/", response_model=UserCreate)
def router_create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@users_router.get("/", response_model=list[User])
def router_read_users(id: int, db: Session = Depends(get_db)):
    return get_user(db, id)

@users_router.get("/by_email/", response_model=User)
def router_read_user_by_email(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(db, email)

@users_router.put("/{user_id}", response_model=UserUpdate )
def router_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    if not update_user(db, user_id, user):
        raise HTTPException(status_code=404, detail="User not found")
    return get_user(db, user_id)        

@users_router.delete("/{user_id}")
def router_delete_user(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}