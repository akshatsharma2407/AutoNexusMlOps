import pandas as pd
import yaml
import os
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator

logger = logging.getLogger(name=os.path.basename(__file__))
logger.setLevel(level='DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel(level='DEBUG')

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(level='DEBUG')

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

file_name = os.path.basename(__file__)

def load_data(data_path: str) -> pd.DataFrame:
    try:
        train_processed = pd.read_parquet(data_path)
        logger.info('train_processed df loaded')
        return train_processed
    except FileNotFoundError:
        logger.error(f'{file_name} -> load_data function: Data File does not exists at specified location')
        raise
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> load_data function')
        raise

def load_encoder(encoder_path: str) -> ColumnTransformer:
    try:
        encoder = joblib.load(encoder_path)
        logger.info('trained encoder loaded')
        return encoder
    except FileNotFoundError:
        logger.error(f'{file_name} -> load_data function: Data File does not exists at specified location')
        raise
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> load_encoder function')
        raise


def train_model(train_processed_df: pd.DataFrame) -> BaseEstimator:
    try:
        xtrain = train_processed_df.drop(columns='Price')
        ytrain = train_processed_df['Price'].copy()

        regressor = RandomForestRegressor(
                n_estimators=100,
                max_depth=30,
                bootstrap=True,
                max_features=None,
                min_samples_leaf=2,
                random_state=42,
                min_samples_split=8
            )
        
        regressor.fit(xtrain,ytrain)
        logger.info('model training done')
        return regressor
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> train_model function')
        raise

def create_pipeline(encoder: BaseEstimator, model: BaseEstimator) -> Pipeline:
    try:
        prediction_pipe = Pipeline(
            [
                ('Encoder',encoder),
                ('Regressor',model)
            ]
        )
        logger.info('encoder + model -> pipeline created')
        return prediction_pipe
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> create_pipeline function')
        raise


def save_artifact(prediction_pipe: Pipeline,pipe_path: str) -> None:
    try:
        joblib.dump(prediction_pipe, pipe_path)
        logger.info('pipeline saved')
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> save_artifact function')
        raise

def main() -> None:
    try:
        train_processed = load_data(data_path='../data/processed/trained_processed.parquet')
        encoder = load_encoder('../models/encoder.joblib')
        regressor = train_model(train_processed_df=train_processed)
        prediction_pipe = create_pipeline(encoder=encoder, model=regressor)
        save_artifact(prediction_pipe=prediction_pipe,pipe_path='../models/prediction_pipe.joblib')
        logger.info('main function executed')
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> main function')
        raise

if __name__ == '__main__':
    main()