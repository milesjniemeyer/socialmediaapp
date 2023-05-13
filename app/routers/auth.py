from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, utils
from ..db import db_models
from ..db.database import get_db

router = APIRouter(
    tags=['authentication']
)

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Determine if provided email exists in the database
    user = db.query(db_models.User).filter(db_models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # Determine if provided password matches the hashed password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    return {"token": "example token"}