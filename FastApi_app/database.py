from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@127.0.0.1:3306/autonexus"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={'check_same_thread' : False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
 