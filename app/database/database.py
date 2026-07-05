import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
# Load variables from .env into the system environment
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / "config.env"

load_dotenv(ENV_PATH)



# """Tradational Way to Connect with PostgreSQL(databases) """
# database_Param = {
#         "host":os.getenv('DB_HOST'),
#         "database":os.getenv('DB_NAME'),
#         "user":os.getenv('DB_USER'),
#         "password":os.getenv('DB_PASS'),
#         "port":os.getenv('DB_PORT'),
#         "cursor_factory":RealDictCursor
#         }

# def get_connection():
#     while True:
#         try:
#             postgreconn = psycopg2.connect(**database_Param)
#             if postgreconn:
#                 return postgreconn
#         except Exception as e:
#             print('Error In DB Connection' ,e)
#             time.sleep(2)
    

#""" Modern Way to Connect with Databases Using ORM(sqlalchemy) """
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = os.getenv('POSTGRE_SQL_URL')
if not SQLALCHEMY_DB_URL:
    print("Error with Importing SQL string ")
engine = create_engine(SQLALCHEMY_DB_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()
