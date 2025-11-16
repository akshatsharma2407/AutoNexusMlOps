from pydantic import BaseModel, Field, field_validator, computed_field, StrictInt, EmailStr, Json
from fastapi import Form
from typing import Annotated, Optional, Literal
from typing import List, Optional
from datetime import datetime

class CarBase(BaseModel):
    Model_Year: Annotated[Optional[StrictInt], Field(default=None, description='Manufacture year of the car', examples=[1990,2026,2020])]
    Brand_Name: Annotated[Optional[str], Field(default=None, description='Brand of the Car', examples=['Audi', 'Mercedes', 'BMW'])]
    Model_Name: Annotated[Optional[str], Field(default=None, description='Model of the Car', examples=['Model Y', 'Miata', 'Challenger'])]
    Stock_Type: Annotated[Optional[Literal['New', 'Used', 'Certified']], Field(default=None, description='Stock Type of Model', examples=['New', 'Used', 'Certified'])]
    Mileage: Annotated[Optional[int], Field(default=None, description='How many miles your car run till now?', examples=[2463,636356])]
    Exterior_Color: Annotated[Optional[Literal['gray',  'black',  'white', 'yellow', 'silver',
                                      'green',    'red',   'blue',  'brown',  'beige',
                                      'orange', 'purple',  'pink', 'violet']],
                                       Field(default=None, description='Color of Car from given fields, if not found give closest color', examples=['gray','silver','beige'])]
    Interior_Color: Annotated[Optional[Literal['gray', 'black', 'yellow', 'red', 'beige', 'brown', 'silver',
                                      'blue', 'white', 'green', 'orange','purple']],
                                       Field(default=None, description='Interior color of Car, if not give the closest one', examples=['gray','silver','blue'])]
    Drivetrain: Annotated[Optional[Literal['AWD', '4WD', 'FWD', 'RWD']],
                                       Field(default=None, description='Drive Train of the car', examples=['AWD', '4WD', 'FWD', 'RWD'])]
    Km_per_l: Annotated[Optional[int], Field(default=None, description='The present fuel economy of car (km/L)')]
    Fuel_Type: Annotated[Optional[Literal['Electric', 'Flex Fuel',  'Gasoline', 'Hybrid',
                                       'Diesel', 'Plug-in Hybrid', 'CNG/LPG', 'Other']],
                                        Field(default=None, description='Fuel Type of Car', examples=['Electric','Gasoline'])]
    Accidents_Or_Damage: Annotated[Optional[bool], Field(default=None, description='Whether the car is accidental or not?', examples=[True, False])]
    Clean_Title: Annotated[Optional[bool], Field(default=None, description='Whether Car has clean title or not?', examples=[True, False])]
    Level2_Charging: Annotated[Optional[float], Field(default=0, description='Time taken by car when charged by Level2 Charging, give 0 for non-electric car (in hrs)', examples=[0, 2, 4.5])]
    Dc_Fast_Charging: Annotated[Optional[float], Field(default=0, description='Time taken by car when charged by Dc_Fast_Charging, give 0 in case of non-electric car (in mins)', examples=[0, 24, 50])]
    Battery_Capacity: Annotated[Optional[float], Field(default=0, description='Battery Capacity of car in mAh, give 0 in case of non-electric car', examples=[70, 65])]
    Expected_Range: Annotated[Optional[float], Field(default=0, description='Range upto the electric car can run when full charged, give 0 in case of non electric', examples=[300, 246])]
    Gear_Spec: Annotated[Optional[int], Field(default=None, description='Speed Transmission in car', examples=[5, 6, 4])]
    Engine_Size: Annotated[Optional[float], Field(default=None, description='Engine size (in litre)', examples=[2.4, 5, 3])]
    Cylinder_Config: Annotated[Optional[Literal[None, 'NA', 'V8', 'I4', 'V6', 'I6', 'H4', 'I5',
                                       'I3', 'H6', 'V4', 'V2', 'V12', 'V10']],
                                        Field(default=None, description='Cylinder Config of the car, give NA in case of electric car', examples=['V8','I4'])]
    Km_L_e_City: Annotated[Optional[float], Field(default=None, description='Km/L equivelent in electric cars (for city), give 0 in case of non-electric', examples=[31, 60])]
    Km_L_e_Hwy: Annotated[Optional[float], Field(default=None, description='Km/L equivelent in electric cars (for Highway), give 0 in case of non-electric', examples=[50, 80])]   
    City: Annotated[Optional[str], Field(default=None, description='location of dealer/owner')]
    STATE: Annotated[Optional[str], Field(default=None, description='name of US states', examples=['Alaska', 'California', 'Texas'])]

    Image_List: Annotated[Optional[List[str]], Field(default=None)]
    Price: Annotated[Optional[int], Field(default=None, ge=0)]
    One_Owner_Vehicle: Annotated[Optional[Literal[None, 'one','more','not_owned_yet']], Field(default=None, description='Is car owned by one owner only or more')]
    Personal_Use_Only: Annotated[Optional[Literal[None, 'no', 'yes', 'not_in_use_yet']], Field(default=None, description='is car used for personal use or commercial')]
    Open_Recall: Annotated[Optional[Literal[None, 'not_in_use_yet', 'yes']], Field(default=None, description='any Open Recall reported')]
    Seller_Name: Annotated[Optional[str], Field(default=None, description='name of seller (showroom name)')]
    Valves: Annotated[Optional[Literal[None, '0', '32', '16', '24', '12', '20', '18', '48', '8', '30']],
                      Field(default=None, description='Total Number of valves in engine')]
    Seller_Site: Annotated[Optional[str], Field(default=None, description='website url of seller')]
    Street_Address: Annotated[Optional[str], Field(default=None, description='Street Address of shop or dealer location')]
    ZIP: Annotated[Optional[StrictInt], Field(default=None, description='ZIP Code of the location')]
    ST: Annotated[Optional[str], Field(default=None, description='abbrivation of state')]
    lat: Annotated[Optional[float], Field(default=None, description='latitude of dealer location')]
    LONG: Annotated[Optional[float], Field(default=None, description='Longitude of dealer location')]

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class CarOut(CarBase):
    id: Annotated[int, Field(..., description='id of Car')]

    class Config:
        from_attributes = True

class PredictionInputSchema(BaseModel):
    Model_Year: Annotated[StrictInt, Field(default=None, description='Manufacture year of the car', examples=[1990,2026,2020])]
    Brand_Name: Annotated[str, Field(default=None, description='Brand of the Car', examples=['Audi', 'Mercedes', 'BMW'])]
    Model_Name: Annotated[str, Field(default=None, description='Model of the Car', examples=['Model Y', 'Miata', 'Challenger'])]
    Stock_Type: Annotated[Literal['New', 'Used', 'Certified'], Field(default=None, description='Stock Type of Model', examples=['New', 'Used', 'Certified'])]
    Mileage: Annotated[int, Field(default=None, description='How many miles your car run till now?', examples=[2463,636356])]
    Exterior_Color: Annotated[Literal['Gray',  'Black',  'White', 'Yellow', 'Silver',
                                      'Green',  'Red',   'Blue',  'Brown',  'Beige',
                                      'Orange', 'Purple',  'Pink', 'Violet'],
                                       Field(default=None, description='Color of Car from given fields, if not found give closest color', examples=['Gray','Silver','Beige'])]
    Interior_Color: Annotated[Literal['Gray', 'Black', 'Yellow', 'Red', 'Beige', 'Brown', 'Silver',
                                      'Blue', 'White', 'Green', 'Orange','Purple'],
                                       Field(default=None, description='Interior color of Car, if not give the closest one', examples=['Gray','Silver','Blue'])]
    Drivetrain: Annotated[Literal['AWD', '4WD', 'FWD', 'RWD'],
                                       Field(default=None, description='Drive Train of the car', examples=['AWD', '4WD', 'FWD', 'RWD'])]
    Km_per_l: Annotated[float, Field(default=None, description='The present fuel economy of car (km/L)')]
    Fuel_Type: Annotated[Literal['Electric', 'Flex Fuel',  'Gasoline', 'Hybrid',
                                       'Diesel', 'Plug-in Hybrid', 'CNG/LPG', 'Other'],
                                        Field(default=None, description='Fuel Type of Car', examples=['Electric','Gasoline'])]
    Accidents_Or_Damage: Annotated[bool, Field(default=None, description='Whether the car is accidental or not?', examples=[True, False])]
    Clean_Title: Annotated[bool, Field(default=None, description='Whether Car has clean title or not?', examples=[True, False])]
    One_Owner_Vehicle: Annotated[bool, Field(default=None, description='Whether Car is sold by First Owner or not', examples=[True, False])]
    Personal_Use_Only: Annotated[bool, Field(default=None, description='Whether Car is used for personal use or commercial use?', examples=[True, False])]
    Level2_Charging: Annotated[float, Field(default=0, description='Time taken by car when charged by Level2 Charging, give 0 for non-electric car (in hrs)', examples=[0, 2, 4.5])]
    Dc_Fast_Charging: Annotated[float, Field(default=0, description='Time taken by car when charged by Dc_Fast_Charging, give 0 in case of non-electric car (in mins)', examples=[0, 24, 50])]
    Battery_Capacity: Annotated[float, Field(default=0, description='Battery Capacity of car in mAh, give 0 in case of non-electric car', examples=[70, 65])]
    Expected_Range: Annotated[float, Field(default=0, description='Range upto the electric car can run when full charged, give 0 in case of non electric', examples=[300, 246])]
    Gear_Spec: Annotated[int, Field(default=None, description='Speed Transmission in car', examples=[5, 6, 4])]
    Engine_Size: Annotated[float, Field(default=None, description='Engine size (in litre)', examples=[2.4, 5, 3])]
    Cylinder_Config: Annotated[Literal[None, 'NA', 'V8', 'I4', 'V6', 'I6', 'H4', 'I5',
                                       'I3', 'H6', 'V4', 'V2', 'V12', 'V10'],
                                        Field(default=None, description='Cylinder Config of the car, give NA in case of electric car', examples=['V8','I4'])]
    Valves: Annotated[Literal[None, 0, 32, 16, 24, 12, 20, 18, 48, 8, 30],
                                        Field(default=None, description='Total Number of valves in engine')]
    Km_L_e_City: Annotated[float, Field(default=None, description='Km/L equivelent in electric cars (for city), give 0 in case of non-electric', examples=[31, 60])]
    Km_L_e_Hwy: Annotated[float, Field(default=None, description='Km/L equivelent in electric cars (for Highway), give 0 in case of non-electric', examples=[50, 80])]   
    City: Annotated[str, Field(default=None, description='location of dealer/owner')]
    STATE: Annotated[str, Field(default=None, description='name of US states', examples=['Alaska', 'California', 'Texas'])]

    @field_validator("City")
    @classmethod
    def name_correction(cls, name : str):
        return name.strip().replace('  ', ' ').lower()
    
    @field_validator("Model_Name")
    @classmethod
    def name_correction(cls, name : str):
        return name.strip().replace('  ', ' ')
    
    @field_validator("Model_Year")
    @classmethod
    def year_validator(cls, year : int):
        return year if year > 2000 else (year//10)*10
    
    @field_validator("Interior_Color", "Exterior_Color", "STATE")
    @classmethod
    def cap_color(cls, color: str):
        return color.lower()

    @classmethod
    def as_form(
        cls,
        Model_Year: int = Form(...),
        Mileage: int = Form(...),
        Brand_Name: str = Form(...),
        Model_Name: str = Form(...),
        Stock_Type: str = Form(...),
        Exterior_Color: str = Form(...),
        Interior_Color: str = Form(...),
        Drivetrain: str = Form(...),
        Fuel_Type: str = Form(...),
        Accidents_Or_Damage: bool = Form(...),
        Clean_Title: bool = Form(...),
        One_Owner_Vehicle: bool = Form(...),
        Personal_Use_Only: bool = Form(...),
        Engine_Size: float = Form(0),
        Km_per_l: float = Form(0),
        Cylinder_Config: str = Form('NA'),
        Valves: int = Form(0),
        Gear_Spec : int =Form(0),
        Level2_Charging: float = Form(0),
        Dc_Fast_Charging: float = Form(0),
        Battery_Capacity: float = Form(0),
        Expected_Range: float = Form(0),
        Km_L_e_City: float = Form(0),
        Km_L_e_Hwy: float = Form(0),
        City: str = Form(...),
        STATE: str = Form(...),
    ):
        return cls(
            Model_Year=Model_Year,
            Mileage=Mileage,
            Brand_Name=Brand_Name,
            Model_Name=Model_Name,
            Stock_Type=Stock_Type,
            Exterior_Color=Exterior_Color,
            Interior_Color=Interior_Color,
            Drivetrain=Drivetrain,
            Fuel_Type=Fuel_Type,
            Accidents_Or_Damage=Accidents_Or_Damage,
            Clean_Title=Clean_Title,
            One_Owner_Vehicle=One_Owner_Vehicle,
            Personal_Use_Only=Personal_Use_Only,
            Engine_Size=Engine_Size,
            Km_per_l=Km_per_l,
            Gear_Spec=Gear_Spec,
            Cylinder_Config=Cylinder_Config,
            Valves=Valves,
            Level2_Charging=Level2_Charging,
            Dc_Fast_Charging=Dc_Fast_Charging,
            Battery_Capacity=Battery_Capacity,
            Expected_Range=Expected_Range,
            Km_L_e_City=Km_L_e_City,
            Km_L_e_Hwy=Km_L_e_Hwy,
            City=City,
            STATE=STATE,
        )

class PredictionOutputSchema(BaseModel):
    Price: Annotated[float, Field(..., description='Price of model predicted by ML algo')]


class User(BaseModel):
    first_name: Annotated[str, Field(..., description='first name of the person')]
    last_name: Annotated[str, Field(..., description='last name of the person')]
    email: Annotated[EmailStr, Field(..., description='email of the person')]
    password_hash: Annotated[str, Field(..., description='password of user')]

class UserOut(User):
    id : int
    is_active : bool
    created_at : datetime
    updated_at : datetime
    
    class Config:
        from_attributes = True
