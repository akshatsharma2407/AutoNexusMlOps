from mlflow.client import MlflowClient
import os
import mlflow
from dotenv import load_dotenv

load_dotenv()

def access_dagshub():
    uri = 'https://dagshub.com/akshatsharma2407/AutoNexusMlOps.mlflow'
    dagshub_token = os.getenv('DAGSHUB_PAT')
    if not dagshub_token:
        raise ValueError('Dagshub token not set')
    
    os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_token
    os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token
    mlflow.set_tracking_uri(uri=uri)

def get_latest_model_version(model_name: str):
    access_dagshub()
    client = MlflowClient()
    latest_version = client.get_model_version_by_alias(model_name, 'Production')
    return latest_version.version if latest_version else None

model = None

def load_model():
    global model
    if model is None:
        model_name = 'RF_Price_Prediction_Regressor'
        model_version = get_latest_model_version(model_name=model_name)

        if model_version is None:
            raise ValueError('No Valid Model Version found in Production')

        model_uri = f'models:/{model_name}/{model_version}'
        model = mlflow.pyfunc.load_model(model_uri)
    return model