from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DECIMAL, func, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Car(Base):
    __tablename__ = "Car"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Model_Year = Column(Integer, nullable=False)
    Brand_Name = Column(String(100), nullable=False)
    Model_Name = Column(String(255), nullable=False)
    Image_List = Column(JSON)
    Stock_Type = Column(String(50))
    Mileage = Column(DECIMAL(10, 2))
    Price = Column(DECIMAL(12, 2))
    Exterior_Color = Column(String(100))
    Interior_Color = Column(String(100))
    Drivetrain = Column(String(50))
    Km_per_l = Column(DECIMAL(6, 2))
    Fuel_Type = Column(String(50))
    Accidents_Or_Damage = Column(Boolean)
    Clean_Title = Column(Boolean)
    One_Owner_Vehicle = Column(String(100))
    Personal_Use_Only = Column(String(100))
    Level2_Charging = Column(DECIMAL(6, 2))
    Dc_Fast_Charging = Column(DECIMAL(6, 2))
    Battery_Capacity = Column(DECIMAL(6, 2))
    Expected_Range = Column(DECIMAL(6, 2))
    Gear_Spec = Column(String(50))
    Engine_Size = Column(DECIMAL(6, 2))
    Cylinder_Config = Column(String(50))
    Valves = Column(String(50))
    Seller_Site = Column(String(255))
    Seller_Name = Column(String(255))
    Km_L_e_City = Column(DECIMAL(6, 2))
    Km_L_e_Hwy = Column(DECIMAL(6, 2))
    Street_Address = Column(String(500))
    ZIP = Column(String(20))
    City = Column(String(200))
    STATE = Column(String(200))
    ST = Column(String(10))
    lat = Column(DECIMAL(9, 6))
    LONG = Column(DECIMAL(9, 6))