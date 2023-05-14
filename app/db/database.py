from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# Load environment variables
load_dotenv()

# Define environment variables
DB_HOST = os.getenv('DB_HOST')
DATABASE = os.getenv('DATABASE')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USERNAME = os.getenv('DB_USERNAME')

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