from pydantic import BaseModel, Field, field_validator, computed_field, StrictInt
from typing import Annotated, Optional, Literal

class CarBase(BaseModel):
    name: Annotated[str, Field(..., max_length=30, min_length=3)]
    price: Annotated[int, Field(..., ge=0)]

    @field_validator('name')
    @classmethod
    def name_title(cls, value) -> str:
        return value.upper()
    
    @computed_field
    @property
    def price_rs(cls) -> float:
        return cls.price*87

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    name: Annotated[Optional[str], Field(None, min_length=3, description='Name of Car', examples=['SUV 300', 'Punch'])]
    price: Annotated[Optional[int], Field(None, ge=0, description='Price of Car in Dollars', examples=[2463,636331])]

    @field_validator('name')
    @classmethod
    def name_title(cls, value) -> str:
        return value.upper() if value else value
    
    @computed_field
    @property
    def price_rs(cls) -> float:
        return cls.price*87 if cls.price else cls.price

class CarOut(CarBase):
    id: int

    class Config:
        from_attributes = True

class PredictionInputSchema(BaseModel):
    Unnamed : Annotated[int, Field(..., alias='Unnamed: 0')]
    Model_Year: Annotated[StrictInt, Field(..., description='Manufacture year of the car', examples=[1990,2026,2020])]
    Mileage: Annotated[int, Field(..., description='How many miles your car run till now?', examples=[2463,636356])]
    Brand_Name: Annotated[str, Field(..., description='Brand of the Car', examples=['Audi', 'Mercedes', 'BMW'])]
    Model_Name: Annotated[str, Field(..., description='Model of the Car', examples=['Model Y', 'Miata', 'Challenger'])]
    Stock_Type: Annotated[Literal['New', 'Used', 'Certified'], Field(..., description='Stock Type of Model', examples=['New', 'Used', 'Certified'])]
    Exterior_Color: Annotated[Literal['gray',  'black',  'white', 'yellow', 'silver',
                                      'green',    'red',   'blue',  'brown',  'beige',
                                      'orange', 'purple',  'pink', 'violet'],
                                       Field(..., description='Color of Car from given fields, if not found give closest color', examples=['gray','silver','beige'])]
    Interior_Color: Annotated[Literal['gray', 'black', 'yellow', 'red', 'beige', 'brown', 'silver',
                                      'blue', 'white', 'green', 'orange','purple'],
                                       Field(..., description='Interior color of Car, if not give the closest one', examples=['gray','silver','blue'])]
    Drivetrain: Annotated[Literal['AWD', '4WD', 'FWD', 'RWD'],
                                       Field(..., description='Drive Train of the car', examples=['AWD', '4WD', 'FWD', 'RWD'])]
    Km_per_l: Annotated[float, Field(..., description='The present fuel economy of car (km/L)', alias='Km/L')]
    Fuel_Type: Annotated[Literal['Electric', 'Flex Fuel',  'Gasoline', 'Hybrid',
                                       'Diesel', 'Plug-in Hybrid', 'CNG/LPG', 'Other'],
                                        Field(..., description='Fuel Type of Car', examples=['Electric','Gasoline'])]
    Accidents_Or_Damage: Annotated[bool, Field(..., description='Whether the car is accidental or not?', examples=[True, False])]
    Clean_Title: Annotated[bool, Field(..., description='Whether Car has clean title or not?', examples=[True, False])]
    One_Owner_Vehicle: Annotated[bool, Field(..., description='Whether Car is sold by First Owner or not', examples=[True, False])]
    Personal_Use_Only: Annotated[bool, Field(..., description='Whether Car is used for personal use or commercial use?', examples=[True, False])]
    Level2_Charging: Annotated[float, Field(..., description='Time taken by car when charged by Level2 Charging, give 0 for non-electric car (in hrs)', examples=[0, 2, 4.5])]
    Dc_Fast_Charging: Annotated[float, Field(..., description='Time taken by car when charged by Dc_Fast_Charging, give 0 in case of non-electric car (in mins)', examples=[0, 24, 50])]
    Battery_Capacity: Annotated[float, Field(..., description='Battery Capacity of car in mAh, give 0 in case of non-electric car', examples=[70, 65])]
    Expected_Range: Annotated[float, Field(..., description='Range upto the electric car can run when full charged, give 0 in case of non electric', examples=[300, 246])]
    Gear_Spec: Annotated[StrictInt, Field(..., description='Speed Transmission in car', examples=[5, 6, 4])]
    Engine_Size: Annotated[float, Field(..., description='Engine size (in litre)', examples=[2.4, 5, 3])]
    Cylinder_Config: Annotated[Literal['NA', 'V8', 'I4', 'V6', 'I6', 'H4', 'I5',
                                       'I3', 'H6', 'V4', 'V2', 'V12', 'V10'],
                                        Field(..., description='Cylinder Config of the car, give NA in case of electric car', examples=['V8','I4'])]
    Valves: Annotated[Literal[0, 32, 16, 24, 12, 20, 18, 48, 8, 30],
                                        Field(..., description='Total Number of valves in engine')]
    Km_L_e_City: Annotated[float, Field(..., description='Km/L equivelent in electric cars (for city), give 0 in case of non-electric', examples=[31, 60], alias='Km/L_e_City')]
    Km_L_e_Hwy: Annotated[float, Field(..., description='Km/L equivelent in electric cars (for Highway), give 0 in case of non-electric', examples=[50, 80], alias='Km/L_e_Hwy')]
    City: Annotated[str, Field(..., description='location of dealer/owner')]
    STATE: Annotated[str, Field(..., description='name of US states', examples=['Alaska', 'California', 'Texas'])]

class PredictionOutputSchema(BaseModel):
    Price: Annotated[float, Field(..., description='Price of model predicted by ML algo')]