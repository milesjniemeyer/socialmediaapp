from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .db import db_models
from .db.database import engine
from .routers import post, user, auth, vote

# Create FastAPI object
app = FastAPI(
    docs_url='/docs',
    title="FastAPI - SocialMediaApp",
    description="This is a basic API made by @milesjniemeyer meant to resemble the functionality of a social media platform."
)

# Create database table with SQLAlchemy
db_models.Base.metadata.create_all(bind=engine)

# Include the applicable routes for the API
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# ROOT ROUTE
@app.get("/")
def root():
    response = RedirectResponse(url='/docs')

    return response