import mlflow
import os

def promote_model():
    dagshub_token = os.getenv('DAGSHUB_PAT')
    if not dagshub_token:
        raise ValueError('Dagshub token not set')
    
    os.environ['MLFLOW_TRACKING_USERNAME'] = dagshub_token
    os.environ['MLFLOW_TRACKING_PASSWORD'] = dagshub_token

    mlflow.set_tracking_uri('https://dagshub.com/akshatsharma2407/cars_ml_test.mlflow')

    client = mlflow.MlflowClient()

    model_name = "RF_Price_Prediction_Regressor"

    latest_version_staging = client.get_model_version_by_alias(name= model_name, alias='Staging').version

    try:
        prod_version = client.get_model_version_by_alias(name=model_name, alias='Production')
    except:
        prod_version = None
    
    if prod_version:
        client.set_registered_model_alias(
            name=model_name,
            version=prod_version.version,
            alias=f'Archived_{prod_version.version}'
        )
    
    client.set_registered_model_alias(
        name=model_name,
        version=latest_version_staging,
        alias='Production'
    )

    client.delete_registered_model_alias(
        name=model_name,
        alias='Staging'
    )

    print(f'Model Version {latest_version_staging} promoted to Production')

if __name__ == "__main__":
    promote_model()
