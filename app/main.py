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

from sqlalchemy.orm import Session
from .database import engine,SessionLocal,get_db
from . import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
load_dotenv() 

DB_HOST = os.getenv("DB_HOST")


print("MAIN FILE LOADED")
class Post(BaseModel):
    title:str
    content:str
    published:bool = True






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

        break
    except Exception as error:
        print(f"Attempt {i+1} failed")
        print("Error:", error)
        time.sleep(2)   # wait before retry
else:
    print("Failed to connect after retries")

#logic to find id.....
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

#CRUD operation.....
@app.get("/")
async def root():
    return {"message":"Hello World!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"data":posts}

#GET
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

#POST
@app.post("/posts")
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data":new_post}

#GET one-post
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return {"post details":post} 
 
#DELETE 
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message":deleted_post} 

#PUT --> update the post
@app.put("/post/{id}")
def update_post(id:int,post:Post):
    cursor.execute(
        """UPDATE posts 
        SET title = %s ,content=%s,published=%s 
        WHERE id = %s
        RETURNING * """,
        (post.title,post.content,post.published,id))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    
    return {"data":updated_post}
        
        