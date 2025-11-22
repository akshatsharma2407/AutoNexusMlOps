import os
import unittest

import mlflow
import pandas as pd
from mlflow.client import MlflowClient
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score, root_mean_squared_error


class TestModelLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dagshub_token = os.getenv("DAGSHUB_PAT")
        if not dagshub_token:
            raise ValueError("DAGSHUB_PAT environment variable is not set")

        os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

        mlflow.set_tracking_uri(
            uri="https://dagshub.com/akshatsharma2407/AutoNexusMlOps.mlflow"
        )

        model_name = "RF_Price_Prediction_Regressor"
        model_version = cls.get_latest_model_version(model_name)

        if not model_version:
            raise ValueError("Model not found in Staging")

        model_uri = f"models:/{model_name}/{model_version}"
        cls.model = mlflow.pyfunc.load_model(model_uri)

        cls.holdout_data = pd.read_csv("../raw/test.parquet")

    @staticmethod
    def get_latest_model_version(model_name):
        client = MlflowClient()
        latest_version = client.get_model_version_by_alias(
            name=model_name, alias="Staging"
        )
        return latest_version.version if latest_version else None

    def test_model_loaded_properly(self):
        self.assertIsNotNone(self.model)

    def test_model_performance(self):
        x_holdout = self.holdout_data.drop(columns="Price")
        y_holdout = self.holdout_data["Price"].copy()

        y_pred = self.model.predict(x_holdout)

        mae = mean_absolute_error(y_holdout, y_pred)
        r2 = r2_score(y_holdout, y_pred)
        mse = root_mean_squared_error(y_holdout, y_pred)

        expected_r2 = 0.50
        expected_rmse = 20000
        expected_mae = 8000

        self.assertLessEqual(
            mae, expected_mae, f"MAE should be less than {expected_mae} USD"
        )
        self.assertLessEqual(
            mse, expected_rmse, f"MSE should be less than {expected_rmse} USD"
        )
        self.assertGreaterEqual(r2, expected_r2, f"R2 should be at least {expected_r2}")


if __name__ == "__main__":
    unittest.main()
