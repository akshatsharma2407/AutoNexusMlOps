import pandas as pd
import yaml
import os
import logging
import joblib
from sklearn.compose import ColumnTransformer
from feature_engine.encoding import CountFrequencyEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.base import BaseEstimator

file_name = os.path.basename(__file__)

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(level='DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel(level='DEBUG')

file_handler = logging.FileHandler(filename='errors.log')
file_handler.setLevel(level='DEBUG')

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_data(train_path: str) -> pd.DataFrame:
    try:
        train = pd.read_parquet(train_path)
        logger.info('train data loaded')
        return train
    except FileNotFoundError:
        logger.error(f'{file_name} -> load_data function: Data File does not exists at given location')
        raise
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> load_data function')
        raise

def create_encoder() -> ColumnTransformer:
    try:
        encoder = ColumnTransformer(
            [
                (
                    'Ordinal_Encoder',
                    OrdinalEncoder(categories=[['New','Certified','Used']]),
                    ['Stock_Type']
                ),
                (
                    'Nominal_Encoder',
                    CountFrequencyEncoder(encoding_method='frequency'),
                    ['Brand_Name', 'Model_Name', 'Exterior_Color',
                    'Interior_Color', 'Drivetrain', 'Fuel_Type',
                    'Cylinder_Config', 'City', 'STATE']
                )
            ],
            remainder='passthrough'
        )
        encoder.set_output(transform='pandas')
        logger.info('encoder defined')
        return encoder
    except Exception:
        logger.error(f'Some unexpected error occured in {file_name} -> create_encoder function')
        raise

def transform_data(train: pd.DataFrame, encoder: ColumnTransformer) -> tuple[pd.DataFrame, ColumnTransformer]:
    try:
        train_processed = encoder.fit_transform(train)
        logger.info('data transformed with encoder')
        return train_processed, encoder
    except:
        logger.error(f'Some unexpected error occured in {file_name} -> transform_data function')
        raise

def save_artifacts(train_processed: pd.DataFrame, trained_encoder: ColumnTransformer, interim_data_dir: str, encoder_path: str) -> None:
    try:
        os.makedirs(interim_data_dir, exist_ok=True)
        train_processed.to_parquet(os.path.join(interim_data_dir,'train_processed.parquet'))
        joblib.dump(trained_encoder, encoder_path)
        logger.info('data and encoder saved')
    except OSError:
        logger.error(f'OS Error occured in {file_name} -> save_artifacts')
        raise
    except:
        logger.error(f'Some unexpected error occured in {file_name} -> save_artifacts function')
        raise


def main() -> None:
    try:
        train = load_data(train_path='data/raw/train.parquet')
        encoder = create_encoder()
        train_processed, trained_encoder = transform_data(train=train, encoder=encoder)
        save_artifacts(train_processed=train_processed,
                         trained_encoder=trained_encoder,
                         interim_data_dir='data/processed',
                         encoder_path='models/encoder.joblib')
        logger.info('main function executed')
    except:
        logger.error(f'Some unexpected error occured in {file_name} -> main function')
        raise

if __name__ == '__main__':
    main()