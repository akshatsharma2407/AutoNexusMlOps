from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import schemas, models

def get_cars(db: Session, sortby: str = "id", orderby: str = "asc"):
    sort_column = getattr(models.Cars, sortby)
    if orderby == "asc":
        sort_column = asc(sort_column)
    else:
        sort_column = desc(sort_column)
    return db.query(models.Cars).order_by(sort_column).all()

def get_car(db: Session, id: int):
    return (
        db
        .query(models.Cars)
        .filter(models.Cars.id == id)
        .first()
    )

def create_car(db: Session, new_car: schemas.CarCreate):
    db_car = models.Cars(
        name=new_car.name,
        price=new_car.price
    )

    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def update_car(db: Session, id: int, update_car: schemas.CarUpdate):
    db_car = db.query(models.Cars).filter(models.Cars.id == id).first()
    if db_car:
        updated_info = update_car.model_dump(exclude_unset=True)
        for key, value in updated_info.items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
    return db_car

def delete_car(db: Session, id: int):
    db_car = db.query(models.Cars).filter(models.Cars.id == id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
    return db_car