from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

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

# User login model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        orm_mode = True

# Vote model
class Vote(PostBase):
    post_id: int
    dir: conint(le=1)

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data model
class TokenData(BaseModel):
    id: Optional[str] = None