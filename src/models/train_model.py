import json
import logging
import os
import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

dagshub_token = os.getenv("DAGSHUB_PAT")

if not dagshub_token:
    raise ValueError("DAGSHUB_PAT envir" "onment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

mlflow.set_tracking_uri(
    uri="https://dagshub.com/akshatsharma2407/AutoNexusMlOps.mlflow"
)

logger = logging.getLogger(name=os.path.basename(__file__))
logger.setLevel(level="DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel(level="DEBUG")

file_handler = logging.FileHandler("reports/errors.log")
file_handler.setLevel(level="DEBUG")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

file_name = os.path.basename(__file__)


def load_params(params_path: str) -> dict:
    try:
        model_params = yaml.safe_load(open(params_path, "r"))["train_model"]
        return model_params
    except FileNotFoundError:
        logger.error(
            f"{file_name} -> load_params function: Params File does not exists at specified location"
        )
        raise
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> load_params function"
        )
        raise


def load_data(
    train_raw_data_path: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        train_raw_data = pd.read_parquet(train_raw_data_path)
        logger.info("train_raw df loaded")
        return train_raw_data
    except FileNotFoundError:
        logger.error(
            f"{file_name} -> load_data function: Data File does not exists at specified location"
        )
        raise
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> load_data function"
        )
        raise


def load_encoder(encoder_path: str) -> ColumnTransformer:
    try:
        encoder = joblib.load(encoder_path)
        logger.info("trained encoder loaded")
        return encoder
    except FileNotFoundError:
        logger.error(
            f"{file_name} -> load_data function: Data File does not exists at specified location"
        )
        raise
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> load_encoder function"
        )
        raise


def create_model(model_params: dict) -> BaseEstimator:
    try:
        regressor = RandomForestRegressor(**model_params)
        logger.info("model training done")
        return regressor
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> train_model function"
        )
        raise


def train_pipeline(encoder: BaseEstimator, model: BaseEstimator, train_raw_data: pd.DataFrame) -> Pipeline:
    try:
        prediction_pipe = Pipeline([("Encoder", encoder), ("Regressor", model)])
        prediction_pipe.fit(train_raw_data.drop(columns='Price'),train_raw_data['Price'])
        logger.info("encoder + model -> pipeline created")
        return prediction_pipe
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> create_pipeline function"
        )
        raise


def save_artifact(prediction_pipe: Pipeline, pipe_path: str) -> None:
    try:
        joblib.dump(prediction_pipe, pipe_path)
        logger.info("pipeline saved")
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> save_artifact function"
        )
        raise


def model_signature_and_save_run_id(
    prediction_pipe: Pipeline, train_raw_data: pd.DataFrame, path: str, run_id: int
) -> None:
    try:
        xtrain = train_raw_data.drop(columns="Price")

        model_name = "model"
        signature = mlflow.models.infer_signature(
            model_input=xtrain.head(5),
            model_output=prediction_pipe.predict(xtrain.head(5)),
        )
        mlflow.sklearn.log_model(prediction_pipe, model_name, signature=signature)

        model_info = {"run_id": run_id, "model_name": model_name}

        with open(path, "w") as file:
            json.dump(model_info, file)
        logger.info("save model signature and run id")
    except:
        logger.error(
            f"Some unexpected error occured in {file_name} -> model_signature_and_save_run_id"
        )
        raise


def main() -> None:
    try:
        mlflow.set_experiment(experiment_name="Regressor for Deployment")
        mlflow.sklearn.autolog()
        with mlflow.start_run() as run:
            model_params = load_params(params_path="params.yaml")
            train_raw_data = load_data(
                train_raw_data_path="data/raw/train.parquet"
            )
            encoder = load_encoder("models/encoder.joblib")
            regressor = create_model(
                model_params=model_params
            )
            prediction_pipe = train_pipeline(encoder=encoder, model=regressor, train_raw_data=train_raw_data)
            save_artifact(
                prediction_pipe=prediction_pipe,
                pipe_path="models/prediction_pipe.joblib",
            )
            model_signature_and_save_run_id(
                prediction_pipe=prediction_pipe,
                train_raw_data=train_raw_data,
                path="reports/run_info.json",
                run_id=run.info.run_id,
            )
            logger.info("main function executed")
    except Exception:
        logger.error(f"Some unexpected error occured in {file_name} -> main function")
        raise


if __name__ == "__main__":
    main()
