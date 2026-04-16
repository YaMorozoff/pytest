
from fastapi import APIRouter

from app.database import SessionLocal


router = APIRouter(prefix="/posts", tags=["posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)

@router.get("/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.list_posts(db, skip=skip, limit=limit)

@router.update("/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.list_posts(db, skip=skip, limit=limit)

@router.delete("/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.list_posts(db, skip=skip, limit=limit)