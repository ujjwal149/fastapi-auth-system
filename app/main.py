# from typing import Optional
from enum import auto


from fastapi import FastAPI,Response,HTTPException,status,Depends
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import time
import os
from typing import List

from sqlalchemy.orm import Session
from .database import engine,SessionLocal,get_db
from . import models,schemas,utils

from .routers import post,user,auth





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
            row_factory = dict_row #type:ignore
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

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message":"Hello World!"}

