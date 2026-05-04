from pydantic import BaseModel
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
        orm_mode = True
    