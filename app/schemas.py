

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