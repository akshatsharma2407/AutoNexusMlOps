import crud, schemas, models
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from typing import List
from database import SessionLocal, Base, engine
from prediction import prediction
from load_model import load_model

Base.metadata.create_all(bind=engine)

app = FastAPI()

model = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/cars', response_model=List[schemas.CarOut])
def get_cars(sortby: str = Query('id', description='name of col on which you want to sort'), orderby: str = Query('asc', description='order by, either "asc" or "desc"'), db: Session = Depends(get_db)):
    if sortby not in ['id', 'price']:
        raise HTTPException(status_code=400, detail='wrong attribute, select from id or price')
    if orderby not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='wrong attribute, select from asc or desc')
    return crud.get_cars(db=db, sortby=sortby, orderby=orderby)

@app.get('/cars/{id}', response_model= schemas.CarOut)
def get_car(id: int = Path(..., description='id of car you want to fetch', examples=[1,2,3]), db: Session = Depends(get_db)):
    car = crud.get_car(db=db, id=id)
    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return car

@app.post('/cars', response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate = Path(..., description='car details'), db: Session = Depends(get_db)):
    return crud.create_car(db=db, new_car=car)

@app.put('/cars', response_model=schemas.CarOut)
def update_car(car: schemas.CarUpdate = Path(..., description='details of car you want to update'),id: int = Path(..., description=('unique id of car')), db: Session = Depends(get_db)):
    db_car = crud.update_car(db=db, id=id, update_car=car)
    if db_car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return db_car

@app.delete('/cars', response_model= schemas.CarOut)
def delete_car(id: int = Path(..., description='unique id of car you want to update'), db: Session = Depends(get_db)):
    db_car = crud.delete_car(db=db, id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return db_car

@app.post('/prediction', response_model=schemas.PredictionOutputSchema)
def predict_price(car_details: schemas.PredictionInputSchema):
    model = load_model()
    price = prediction(car=car_details, model=model)
    return schemas.PredictionOutputSchema(Price=price)