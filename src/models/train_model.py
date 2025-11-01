import pandas as pd
import yaml
import json
import os
import mlflow
import dagshub
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator

dagshub.init(repo_owner='akshatsharma2407', repo_name='AutoNexusMlOps', mlflow=True)
mlflow.set_tracking_uri(uri='https://dagshub.com/akshatsharma2407/AutoNexusMlOps.mlflow')

logger = logging.getLogger(name=os.path.basename(__file__))
logger.setLevel(level='DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel(level='DEBUG')

file_handler = logging.FileHandler('reports/errors.log')
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
        xtrain = train_processed_df.drop(columns=['remainder__Price'])
        ytrain = train_processed_df['remainder__Price'].copy()

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

def model_signature_and_save_run_id(regressor: BaseEstimator, train: pd.DataFrame, path: str ,run_id : int) -> None:
    try:
        xtrain = train.drop(columns='remainder__Price')
        ytrain = train['remainder__Price']
        
        model_name = 'model'
        signature = mlflow.models.infer_signature(model_input = xtrain, model_output = ytrain)
        mlflow.sklearn.log_model(regressor, model_name, signature=signature)

        model_info = {'run_id': run_id, 'model_name': model_name}

        with open(path, 'w') as file:
            json.dump(model_info, file)
        logger.info('save model signature and run id')
    except:
        logger.error(f'Some unexpected error occured in {file_name} -> model_signature_and_save_run_id')
        raise


def main() -> None:
    try:
        mlflow.set_experiment(experiment_name='Regressor for Deployment')
        mlflow.sklearn.autolog()
        with mlflow.start_run() as run:
            train_processed = load_data(data_path='data/processed/trained_processed.parquet')
            encoder = load_encoder('models/encoder.joblib')
            regressor = train_model(train_processed_df=train_processed)
            prediction_pipe = create_pipeline(encoder=encoder, model=regressor)
            save_artifact(prediction_pipe=prediction_pipe,pipe_path='models/prediction_pipe.joblib')
            model_signature_and_save_run_id(regressor=regressor, train=train_processed, path='reports/run_info.json', run_id=run.info.run_id)
            logger.info('main function executed')
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> main function')
        raise

if __name__ == '__main__':
    main()