from FastApi_app import schemas
import pandas as pd
from sklearn.pipeline import Pipeline

def prediction(car: schemas.PredictionInputSchema, model: Pipeline):
    input_df = pd.DataFrame([car.model_dump()]).rename(columns={'Unnamed': 'Unnamed: 0', 'Km_per_l' : 'Km/L', 'Km_L_e_City' : 'Km/L_e_City', 'Km_L_e_Hwy' : 'Km/L_e_Hwy'})
    prediction = model.predict(input_df)
    return prediction