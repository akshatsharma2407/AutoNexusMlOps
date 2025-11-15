from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

# env_path = Path(__file__).resolve().parent / ".env" # through ChatGPT
# load_dotenv(env_path)

DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOSTNAME = os.getenv('DB_HOSTNAME')
# DB_PORT = os.getenv('DB_PORT') 
DB_NAME = os.getenv('DB_NAME')


SQLALCHEMY_DATABASE_URL = F"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:3306/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={'check_same_thread' : False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()