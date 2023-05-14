from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

from ..config import settings

# Estbalish database connection (non-ORM)
# while True:
#     try:
#         conn = psycopg2.connect(host=settings.db_host, database=settings.database, user=settings.db_host, password=settings.db_password, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was sucessful.")
#         break
#     except Exception as error:
#         print("Database connection failed.")
#         print(f"Error: {error}")
#         time.sleep(3)

# Provide database information
SQLALCHEMY__DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.database}"

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