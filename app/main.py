# from typing import Optional
from fastapi import FastAPI,Response,HTTPException,status,Depends
from dotenv import load_dotenv
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
import os
from typing import List

from sqlalchemy.orm import Session
from .database import engine,SessionLocal,get_db
from . import models,schemas

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
load_dotenv() 

DB_HOST = os.getenv("DB_HOST")









#pgAdmin connection using psycopg..
retries = 5
for i in range(retries):
    try:
        conn = psycopg.connect(
            host = os.getenv("DB_HOST"),
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            row_factory=dict_row
        )
        cursor = conn.cursor()
        print("Database connected sucessfully!")
        break
    except Exception as error:
        print(f"Attempt {i+1} failed")
        print("Error:", error)
        time.sleep(2)   # wait before retry
else:
    print("Failed to connect after retries")



#CRUD operation.....
@app.get("/")
async def root():
    return {"message":"Hello World!"}


#GET
@app.get("/posts",response_model=List[schemas.PostRes])
def get_post(db:Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts

#Create new POST
@app.post("/posts",response_model=schemas.PostRes)
def create_post(post:schemas.Post,db:Session = Depends(get_db)):
    new_post = models.Posts(
        **post.dict()
        # title=post.title,content = post.content,published = post.published
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#GET one-post
@app.get("/posts/{id}",response_model=schemas.PostRes)
def get_post(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return post
 
#DELETE 
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return {"message":post}
    
    
#PUT --> update the post
@app.put("/post/{id}",response_model=schemas.PostRes)
def update_post(id:int,post:schemas.Post,db:Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    
    return post_query.first()
        
         