import logging
import os

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
import os
import gdown

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


def load_data(file_id: str) -> pd.DataFrame:
    try:
        url = f"https://drive.google.com/uc?id={file_id}"
        output = 'data/external/ml.parquet'
        print(url)
        
        gdown.download(url, output, quiet=False)

        df = pd.read_parquet(output)

        train, test = train_test_split(df, test_size=0.2, shuffle=True)
        logger.info("train & test df fetched")
        return train, test
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


def save_data(folder_path: str, train: pd.DataFrame, test: pd.DataFrame) -> None:
    try:
        os.makedirs(folder_path, exist_ok=True)
        train.to_parquet(os.path.join(folder_path, "train.parquet"), index=False)
        test.to_parquet(os.path.join(folder_path, "test.parquet"), index=False)
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
        file_id = os.getenv('TRAINING_DATA')
        train, test = load_data(file_id)
        save_data(folder_path="data/raw", train=train, test=test)
        logger.info("main function executed successfully")
    except:
        logger.critical(
            f"Some Unexpected error occured in {file_name} -> load data function"
        )
        raise


if __name__ == "__main__":
    main()
