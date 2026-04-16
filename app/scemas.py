

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name:str
    email:EmailStr

class PostBase(BaseModel):
    title:str
    body:str
    author_id:int
    author:UserBase
    tags:TagBase
class TagBase(BaseModel):    
    name:str
    posts:list[PostBase] = []   
