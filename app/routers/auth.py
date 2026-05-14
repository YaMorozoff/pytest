from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import create_access_token, verify_password, hash_password

from models import User as UserModel 
from schemas import User, UserCreate, Token
from database import SessionLocal

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(
        name=user_data.name,
        email=user_data.email,
        telephone=user_data.telephone,
        hashed_password=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    if not user:
        print(f"DEBUG: User with email {form_data.username} not found")
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    is_valid = verify_password(form_data.password, user.hashed_password)
    print(f"DEBUG: Password valid: {is_valid}")

    if not is_valid:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}