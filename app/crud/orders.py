from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Order


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order(db: Session, order_id: int):
    return db.get(Order, order_id)


def create_order(db: Session, order_data, user_id: int):
    db_order = Order(
        user_id=user_id, 
        product_id=order_data.product_id, 
        quantity=order_data.quantity
    )
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order   
    except SQLAlchemyError:
        db.rollback()
        raise   

def update_order(db: Session, order_id: int, order_update_data)->bool:
    db_order = db.get(Order, order_id)
    if not db_order:
        return False

  
    update_data = order_update_data.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_order, key, value)

    try:    
    
        db.commit()
        db.refresh(db_order)
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_order(db: Session, order_id: int) -> bool:
    db_order = db.get(Order, order_id)
    if not db_order:
        return False
    try:
        db.delete(db_order)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise