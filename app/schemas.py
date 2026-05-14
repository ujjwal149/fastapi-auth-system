
from pydantic import BaseModel,EmailStr
from datetime import datetime

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    
class PostRes(BaseModel):
    title:str
    content:str
    published:bool
    
    class Config:
        from_attributes = True
    
class UserCreate(BaseModel):
    email:EmailStr
    password: str
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    
    class config:
        from_attributes = True
    