from fastapi import  APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, oauth2
from ..db import db_models
from ..db.database import get_db

# Create APIRouter object
router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

# GET ALL POSTS
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(db_models.Post).filter(db_models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # To make it so the logged in user can only see their own posts, use the line below instead of the one above
    # posts = db.query(db_models.Post).filter(db_models.Post.owner_id == current_user.id).all()

    return posts

# GET POST BY ID
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(db_models.Post).filter(db_models.Post.id == id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    # Use the below lines to make it so the user can only find their own posts
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

# CREATE POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Post the data to the database
    new_post = db_models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# DELETE POST
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE POST
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()