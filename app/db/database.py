from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define environment variables
DB_HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DATABASE')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')

# Provide database information
SQLALCHEMY__DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}"

engine = create_engine(SQLALCHEMY__DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Establish database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()