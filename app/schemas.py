from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name:str
    email:EmailStr
    telephone:str | None = None
class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name:str | None = None
    email:EmailStr | None = None
    telephone:str | None = None     

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    user: User | None = None
    product: str | None = None
    status: str    

class Order(OrderBase):
    id: int
    class Config:
        from_attributes = True

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: int | None = None
    product_id: int | None = None
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

    