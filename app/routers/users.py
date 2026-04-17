from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.users import get_user, get_user_by_email, create_user, update_user, delete_user
from .. import schemas
from ..database import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserCreate)
def router_create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=list[schemas.User])
def router_read_users(id: int, db: Session = Depends(get_db)):
    return get_user(db, id)

@router.get("/by_email/", response_model=schemas.User)
def router_read_user_by_email(email: str, db: Session = Depends(get_db)):
    return get_user_by_email(db, email)

@router.put("/{user_id}", response_model=schemas.UserUpdate )
def router_update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    if not update_user(db, user_id, user):
        raise HTTPException(status_code=404, detail="User not found")
    return get_user(db, user_id)        

@router.delete("/{user_id}")
def router_delete_user(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}