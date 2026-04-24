from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.products import create_product, delete_product, get_product, update_product
from schemas import Product, ProductCreate, ProductUpdate
from database import SessionLocal

products_router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@products_router.post("/", response_model=ProductCreate)
def router_create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@products_router.get("/", response_model=list[Product])
def router_read_products(id: int, db: Session = Depends(get_db)):
    return get_product(db, id)

@products_router.put("/{product_id}", response_model=ProductUpdate)
def router_update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    if not update_product(db, product_id, product):
        raise HTTPException(status_code=404, detail="Product not found")
    return get_product(db, product_id)        

@products_router.delete("/{product_id}")
def router_delete_product(product_id: int, db: Session = Depends(get_db)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}    