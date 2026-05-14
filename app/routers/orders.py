from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from security import get_current_user
from crud.orders import get_order, create_order, get_orders_by_user, update_order, delete_order
from schemas import Order, OrderCreate, OrderUpdate, UserCreate, UserUpdate, User
from database import SessionLocal



orders_router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@orders_router.post("/", response_model=OrderCreate)
def router_create_order(order: OrderCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return create_order(db, order, user_id=current_user.id)

@orders_router.get("/", response_model=list[Order])
def router_read_orders(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_orders_by_user(db, user_id=current_user.id)

@orders_router.put("/{order_id}", response_model=OrderUpdate )
def router_update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    if not update_order(db, order_id, order):
        raise HTTPException(status_code=404, detail="Order not found")
    return get_order(db, order_id)        

@orders_router.delete("/{order_id}")
def router_delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    order = get_order(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or access denied")
    
    delete_order(db, order_id)
    return {"detail": "Order deleted successfully"}   
