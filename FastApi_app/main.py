import crud, schemas, user_service
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Path, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from database import SessionLocal, Base, engine
from prediction import prediction
from load_model import load_model
from auth import verify_password, create_access_token, verify_token
from recommend import recommend_car_idx
import json
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

cars = requests.get('https://raw.githubusercontent.com/akshatsharma2407/Car-Data-API/refs/heads/master/cars.json').json()

model = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    category = "electric"
    home_cars = cars.get(category)
    return templates.TemplateResponse(
        "home.html",
        {
            "request" : request,
            'active_category' : category,
            "cars" : home_cars
        }
    )

@app.get('/category/{cat_name}', response_class=HTMLResponse)
def category_page(request: Request, cat_name: str = Path(..., description='Category of the car', examples=['SUV', 'Electric'])):
    home_cars = cars.get(cat_name)
    return templates.TemplateResponse(
        "home.html",
        {
            "request" : request,
            "active_category" : cat_name.lower(),
            "cars" : home_cars
        }
    )

@app.post('/register_user', response_model=schemas.UserOut)
def register_user(user: schemas.User, db: Session = Depends(get_db)):
    if user_service.get_user_details(db=db, email=user.email):
        raise HTTPException(status_code=400, detail='User already Exists')
    new_user = user_service.register_user(db=db, user=user)
    return new_user

@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.get_user_details(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Invalid email')
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail='Invalid Password')
    
    access_token = create_access_token(data={'sub':form_data.username})
    return {'access_token' : access_token, 'token_type' : 'bearer'}

@app.get('/cars/{brand_name}/{model_name}', response_model=List[schemas.CarOut])
def get_cars(request: Request,
             brand_name: str = Path(..., description='name of brand'),
             model_name: str = Path(..., description='model name'),
             page: int = Query(default=1, ge=1, description='Page Number'),
             limit: int = Query(default=20, le=50, description='Number of records per page'),
             sortby: str = Query('id', description='name of col on which you want to sort'),
             orderby: str = Query('asc', description='order by, either "asc" or "desc"'),
             db: Session = Depends(get_db)):
        if sortby not in ['id', 'Price']:
            raise HTTPException(status_code=400, detail='wrong attribute, select from id or price')
        if orderby not in ['asc', 'desc']:
            raise HTTPException(status_code=400, detail='wrong attribute, select from asc or desc')
        cars =  crud.get_cars(db=db, brand_name=brand_name, model_name=model_name,page=page, limit=limit, sortby=sortby, orderby=orderby)
        return templates.TemplateResponse(
            "models_list.html",
            {
                "request" : request,
                "next_page" : page + 1,
                'limit' : limit,
                "brand_name" : brand_name,
                "model_name" : model_name,
                "cars" : cars
            }
        )

@app.get('/cars/{id}', response_class= HTMLResponse)
def get_car(request: Request, id: int = Path(..., description='id of car you want to fetch', examples=[1,2,3]), db: Session = Depends(get_db)):
    car = crud.get_car(db=db, id=id)
    idx = recommend_car_idx(car)
    recommended_cars = crud.recommmended_car_details(car_ids=idx, db=db)

    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return templates.TemplateResponse(
        "car_details.html",
        {
            'request' : request,
            'car' : car,
            'recommended_cars' : recommended_cars
        }
    )

@app.post('/cars', response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_token(token):
        return crud.create_car(db=db, new_car=car)
    else:
        raise HTTPException(status_code=401, detail='Unauthorized access or time out')

@app.put('/cars/{id}')
def update_car(car: schemas.CarUpdate, id: int = Path(..., description=('unique id of car')), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_token(token):
        db_car = crud.update_car(db=db, id=id, update_car=car)
        if db_car is None:
            raise HTTPException(status_code=404, detail='Car not found')
        return db_car
    else:
        raise HTTPException(status_code=401, detail='Unauthorized access or time out')

@app.delete('/cars/{id}')
def delete_car(id: int = Path(..., description='unique id of car you want to update'), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if verify_token(token):
        db_car = crud.delete_car(db=db, id=id)
        if db_car is None:
            raise HTTPException(status_code=404, detail='Car not found')
        return JSONResponse(status_code=200, content='Car Deleted Succesfully')
    else:
        return HTTPException(status_code=401, detail='Unauthorized access or time out')

@app.get('/predict/{cat}', response_class=HTMLResponse)
def prediction_page(request: Request, cat: str = 'Electric'):
    return templates.TemplateResponse(
        'predict.html',
        {
            'request' : request,
            'cat' : cat
        }
    )

@app.post('/prediction', response_model=schemas.PredictionOutputSchema)
def predict_price(request: Request, car_details: schemas.PredictionInputSchema = Depends(schemas.PredictionInputSchema.as_form)):
    model = load_model()
    print(car_details)
    price = prediction(car=car_details, model=model)
    return templates.TemplateResponse(
        "predict.html",
        {
            "request" : request,
            "price" : round(price[0],2)
        }
    )