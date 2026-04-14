from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app import models
from app.scemas import UserBase


def get_user(db: Session, user_id: int):
    return db.get(models.User, user_id)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user:UserBase)->UserBase:
    db_user = models.User(name=user.name, email=user.emal)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise


def update_user(db: Session, user_id: int, user)->bool:
    user = db.get(models.User, user_id)
    if not user:
        return False

    data = user.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(user, k, v)

    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return True

    except IntegrityError:
        db.rollback()
        raise


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(models.User, user_id)
    if not user:
        return False
    try:
        db.delete(user_id)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
