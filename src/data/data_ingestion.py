import logging
import os

import pandas as pd
import yaml

file_name = os.path.basename(__file__)

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(level="DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel(level="DEBUG")

file_handler = logging.FileHandler("reports/errors.log")
file_handler.setLevel(level="DEBUG")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_data(file_path: str) -> pd.DataFrame:
    try:
        train = pd.read_csv(
            "https://raw.githubusercontent.com/akshatsharma2407/cars_ml_test/refs/heads/master/sample.csv"
        ).drop(columns="Unnamed: 0")
        logger.info("train df fetched")
        return train
    except FileNotFoundError:
        logger.error(
            f"{file_name} -> load_data function: Data File does not exists at specified location"
        )
        raise
    except Exception:
        logger.error(
            f"Some unexpected error occured in {file_name} -> load data function"
        )
        raise


def save_data(folder_path: str, train: pd.DataFrame) -> None:
    try:
        os.makedirs(folder_path, exist_ok=True)
        train.to_parquet(os.path.join(folder_path, "train.parquet"))
        logger.info("data saved in local")
    except ModuleNotFoundError:
        logger.error(
            f"{file_name} -> load_data function: Data Folder does not exists at given location"
        )
        raise
    except:
        logger.error(
            f"Some unexpected error occured in {file_name} -> load data function"
        )
        raise


def main() -> None:
    try:
        train = load_data("data/Exp/train.parquet")
        save_data(folder_path="data/raw", train=train)
        logger.info("main function executed successfully")
    except:
        logger.critical(
            f"Some Unexpected error occured in {file_name} -> load data function"
        )
        raise


if __name__ == "__main__":
    main()
