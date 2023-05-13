from fastapi import FastAPI, Response, status, HTTPException, Depends
from dotenv import load_dotenv
import os
# import psycopg2
# from psycopg2.extras import RealDictCursor

from .db import db_models
from .db.database import engine, get_db
from .routers import post, user, auth

# Load environment variables
load_dotenv()

# Define environment variables
DB_HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DATABASE')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')

# Create FastAPI object
app = FastAPI(
    docs_url='/docs',
    title="FastAPI - SocialMediaApp",
    description="This is a basic API made by @milesjniemeyer meant to resemble the functionality of a social media platform."
)

# Create database table with SQLAlchemy
db_models.Base.metadata.create_all(bind=engine)

# Estbalish database connection (non-ORM)
# while True:
#     try:
#         conn = psycopg2.connect(host=DB_HOST, database=DATABASE, user=DB_USERNAME, password=DB_PASSWORD, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucessful.")
#         break
#     except Exception as error:
#         print("Database connection failed.")
#         print(f"Error: {error}")
#         time.sleep(3)

# Include the applicable routes for the API
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# ROOT ROUTE
@app.get("/")
def root():
    return {"message": "Hello world!"}