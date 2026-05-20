from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter

from typing import List

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas

router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
    )

#CRUD operation.....
# @router.get("/")
# async def root():
#     return {"message":"Hello World!"}


#GET
@router.get("/",response_model=List[schemas.PostRes])
def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts

#Create new POST
@router.post("/",response_model=schemas.PostRes)
def create_post(post:schemas.Post,db:Session = Depends(get_db)):
    new_post = models.Posts(
        **post.model_dump()
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#GET one-post
@router.get("/{id}",response_model=schemas.PostRes)
def get_post(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    return post
 
#DELETE 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id)
    
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return {"message":post}
    
    
#PUT --> update the post
@router.put("/{id}",response_model=schemas.PostRes)
def update_post(id:int,post:schemas.Post,db:Session = Depends(get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = post_query.first()
    
    if existing_post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()