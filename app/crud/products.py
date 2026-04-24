
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import Product
from schemas import ProductBase


def get_product(db: Session, product_id: int):
    return db.get(Product, product_id)

def create_product(db: Session, product: ProductBase) -> Product:
    db_product = Product(name=product.name, description=product.description, price=product.price)
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product   
    except SQLAlchemyError:
        db.rollback()
        raise

def update_product(db: Session, product_id: int, product: ProductBase) -> bool:
    product = db.get(Product, product_id)
    if not product:
        return False

    data = product.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(product, k, v)

    try:    
        db.add(data)
        db.commit()
        db.refresh(data)
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_product(db: Session, product_id: int) -> bool:
    product = db.get(Product, product_id)
    if not product:
        return False
    try:
        db.delete(product)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise