from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models


def get_posts(db: Session, post_id: int):
    return db.get(models.Post, post_id)


def create_post(db: Session, post):
    post = models.Post(
        title=post.title,
        body=post.body,
        author_id=post.author_id,
        author=post.author,
        tags=post.tags,
    )
    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError:
        db.rollback()
        raise


def update_post(db: Session, post_id: int, post):
    post = db.get(models.Post, post_id)
    if not post:
        return False

    data = post.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(post, k, v)
    try:
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_post(db:Session,post_id):
    post = db.get(models.Post,post_id)

    if not post:
        return False
    
    try:
        db.delete(post)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
