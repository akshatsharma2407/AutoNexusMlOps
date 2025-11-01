from mlflow.tracking import MlflowClient
import mlflow
import os
import logging
import json
import dagshub

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(level='DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel(level='DEBUG')

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(level='DEBUG')

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

uri='https://dagshub.com/akshatsharma2407/AutoNexusMlOps.mlflow'
dagshub.init(repo_owner='akshatsharma2407', repo_name='AutoNexusMlOps', mlflow=True)

mlflow.set_tracking_uri(uri=uri)
client = MlflowClient(tracking_uri=uri)

file_name = os.path.basename(__file__)

def load_run_info(path: str):
    try:
        with open(path) as f:
            run_info = json.load(f)
        return run_info
    except FileNotFoundError:
        logger.error(f'{file_name} -> load_data function: run_info.json does not exists at given location')
        raise
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> load_run_info function')
        raise


def register_model_to_staging(run_info) -> None:
    try:
        model_uri = f"runs:/{run_info['run_id']}/{run_info['model_name']}"

        results = mlflow.register_model(model_uri=model_uri,name="RF_Price_Prediction_Regressor")

        client.update_model_version(
            name=results.name,
            version=results.version,
            description='A New Version of Model in Staging'
        )

        client.set_registered_model_alias(
            name=results.name,
            version=results.version,
            alias=f'Staging_v{results.version}'
        )
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> register_model_to_staging function')
        raise


def main() -> None:
    try:
        run_info = load_run_info(path='reports/run_info.json')
        register_model_to_staging(run_info)
    except:
        logger.error(f'Unexpected error occured in {file_name} -> main')
        raise
        

if __name__ == '__main__':
    main()