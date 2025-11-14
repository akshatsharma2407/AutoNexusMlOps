from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from FastApi_app import schemas, models
from typing import List

def get_cars(db: Session,brand_name: str, model_name: str,page : int, limit : int, sortby: str = "id", orderby: str = "asc"):
    sort_column = getattr(models.Car, sortby)
    if orderby == "asc":
        sort_column = asc(sort_column)
    else:
        sort_column = desc(sort_column)
    
    skip = (page - 1)*limit
    search_pattern = f"%{model_name}%"
    return db.query(models.Car).filter(models.Car.Brand_Name == brand_name, models.Car.Model_Name.ilike(search_pattern)).order_by(sort_column).offset(skip).limit(limit).all()

def get_car(db: Session, id: int):
    return (
        db
        .query(models.Car)
        .filter(models.Car.id == id)
        .first()
    )

def create_car(db: Session, new_car: schemas.CarCreate):
    db_car = models.Car(
        **new_car.model_dump()
    )

    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def update_car(db: Session, id: int, update_car: schemas.CarUpdate):
    db_car = db.query(models.Car).filter(models.Car.id == id).first()
    if db_car:
        updated_info = update_car.model_dump(exclude_unset=True)
        updated_info.update({'id' : id})
        for key, value in updated_info.items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
    return db_car

def delete_car(db: Session, id: int):
    db_car = db.query(models.Car).filter(models.Car.id == id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
    return db_car

def recommmended_car_details(db: Session, car_ids: List[int]):
    results = db.query(models.Car).filter(models.Car.id.in_(car_ids)).all()
    return results