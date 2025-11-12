from FastApi_app import crud, schemas, user_service
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, Path, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from FastApi_app.database import SessionLocal, Base, engine
from FastApi_app.prediction import prediction
from FastApi_app.load_model import load_model
from FastApi_app.auth import verify_password, create_access_token, verify_token
from FastApi_app.home_data import CARS

Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app.mount("/static", StaticFiles(directory="FastApi_app/static"), name="static")

templates = Jinja2Templates(directory="FastApi_app/templates")

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
    cars = CARS.get(category)
    return templates.TemplateResponse(
        "home.html",
        {
            "request" : request,
            'active_category' : category,
            "cars" : cars
        }
    )

@app.get('/category/{cat_name}', response_class=HTMLResponse)
def category_page(request: Request, cat_name: str):
    cars = CARS.get(cat_name.lower())
    return templates.TemplateResponse(
        "home.html",
        {
            "request" : request,
            "active_category" : cat_name.lower(),
            "cars" : cars
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
             limit: int = Query(default=20, le=100, description='Number of records per page'),
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
                "model" : brand_name + ' ' + model_name,
                "cars" : cars
            }
        )

@app.get('/cars/{id}', response_class= HTMLResponse)
def get_car(request: Request, id: int = Path(..., description='id of car you want to fetch', examples=[1,2,3]), db: Session = Depends(get_db)):
    car = crud.get_car(db=db, id=id)
    if car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return templates.TemplateResponse(
        "car_details.html",
        {
            'request' : request,
            'car' : car
        }
    )

@app.post('/cars', response_model=schemas.CarOut)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db=db, new_car=car)

@app.put('/cars/{id}')
def update_car(car: schemas.CarUpdate, id: int = Path(..., description=('unique id of car')), db: Session = Depends(get_db)):
    db_car = crud.update_car(db=db, id=id, update_car=car)
    if db_car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return db_car

@app.delete('/cars/{id}')
def delete_car(id: int = Path(..., description='unique id of car you want to update'), db: Session = Depends(get_db)):
    db_car = crud.delete_car(db=db, id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail='Car not found')
    return JSONResponse(status_code=200, content='Car Deleted Succesfully')

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
    price = prediction(car=car_details, model=model)
    return templates.TemplateResponse(
        "predict.html",
        {
            "request" : request,
            "price" : price
        }
    )