from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.orders import get_order, create_order, update_order, delete_order
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
def router_create_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, order)

@orders_router.get("/", response_model=list[Order])
def router_read_orders(id: int, db: Session = Depends(get_db)):
    return get_order(db, id)

@orders_router.put("/{order_id}", response_model=OrderUpdate )
def router_update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    if not update_order(db, order_id, order):
        raise HTTPException(status_code=404, detail="Order not found")
    return get_order(db, order_id)        

@orders_router.delete("/{order_id}")
def router_delete_order(order_id: int, db: Session = Depends(get_db)):
    if not delete_order(db, order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}        
