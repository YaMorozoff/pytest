

from sqlalchemy.exc import SQLAlchemyError

from models import Order


def get_order(db, order_id):
    return db.get(Order, order_id)

def create_order(db, order):
    db_order = Order(user_id=order.user_id, product_id=order.product_id, quantity=order.quantity)
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order   
    except SQLAlchemyError:
        db.rollback()
        raise   

def update_order(db, order_id, order)->bool:
    order = db.get(Order, order_id)
    if not order:
        return False

    data = order.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(order, k, v)

    try:    
        db.add(data)
        db.commit()
        db.refresh(data)
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_order(db, order_id) -> bool:
    order = db.get(Order, order_id)
    if not order:
        return False
    try:
        db.delete(order)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise   