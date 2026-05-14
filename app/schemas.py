from pydantic import BaseModel, EmailStr
from enum import Enum

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    name: str
    email: EmailStr
    telephone: str | None = None

class UserCreate(UserBase):
    password: str 

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    
class User(UserBase):
    id: int
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    status: str
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
  
    quantity: int | None = None
    status: str | None = None

    
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    description: str | None = None
    price: int  
class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None    
