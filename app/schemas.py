from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Define posts schema in which data needs to be recieved and/or sent to the user
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

# Create post model
class CreatePost(PostBase):
    pass

# Posts response model
class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

# Create user model
class CreateUser(BaseModel):
    email: EmailStr
    password: str

# User reponse model
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True