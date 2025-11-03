from sqlalchemy import Column, Integer, String
from FastApi_app.database import Base

class Cars(Base):
    __tablename__ = "Cars"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(244), index=True)
    price = Column(Integer, index=True)