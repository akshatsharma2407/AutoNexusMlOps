import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from FastApi_app.load_recommendation_artifacts import load_artifacts

def recommend_car_idx(input_car, k=5):
    input_car = pd.DataFrame(data=[{
        'Brand_Name' : input_car.Brand_Name,
        'Stock_Type' : input_car.Stock_Type,
        'Drivetrain' : input_car.Drivetrain,
        'Fuel_Type' : input_car.Fuel_Type,
        'One_Owner_Vehicle' : input_car.One_Owner_Vehicle,
        'Personal_Use_Only' : input_car.Personal_Use_Only,
        'Gear_Spec' : input_car.Gear_Spec,
        'Cylinder_Config': input_car.Cylinder_Config,
        'Valves' : input_car.Valves,
        'ST' : input_car.ST,
        'Model_Name' : input_car.Model_Name,
        'Seller_Name' : input_car.Seller_Name,
        'Model_Year' : input_car.Model_Year,
        'Mileage' : input_car.Mileage,
        'Price' : input_car.Price,
        'Km_per_l' : input_car.Km_per_l,
        'Dc_Fast_Charging' : input_car.Dc_Fast_Charging,
        'Battery_Capacity' : input_car.Battery_Capacity,
        'Expected_Range' : input_car.Expected_Range,
        'Engine_Size' : input_car.Engine_Size,
        'Km_L_e_City' : input_car.Km_L_e_City,
        'Km_L_e_Hwy' : input_car.Km_L_e_Hwy,
        'Accidents_Or_Damage' : input_car.Accidents_Or_Damage,
        'Clean_Title' : input_car.Clean_Title
    }])
    df, transformer = load_artifacts()
    similarity_matrix = cosine_similarity(transformer.transform(input_car), df)
    idx = np.argsort(similarity_matrix.ravel())[-k-1:][::-1][1:]
    return [int(id_) for id_ in idx] #convert np.int to int