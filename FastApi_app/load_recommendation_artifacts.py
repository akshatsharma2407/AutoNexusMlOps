import joblib
from scipy.sparse import load_npz
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def load_artifacts(
    BUCKET: str = 'recommendation-system-artifacts',
    s3_sparse_path: str = 'artifacts/transformed_df.npz',
    s3_transformer_path: str = 'artifacts/recommendation_transformer.joblib',
    local_transformer_path: str = 'FastApi_app/recommendation_artifacts/recommendation_transformer.joblib',
    local_sparse_path: str = 'FastApi_app/recommendation_artifacts/recommendation_matrix.npz'
):
    print('Loading artifacts...')

    os.makedirs('FastApi_app/recommendation_artifacts', exist_ok=True)

    s3 = boto3.client( 
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('REGION_NAME')
    )

    s3.download_file(BUCKET, s3_sparse_path, local_sparse_path)
    s3.download_file(BUCKET, s3_transformer_path, local_transformer_path)

    transformed_df = load_npz(local_sparse_path)
    transformer = joblib.load(local_transformer_path)

    return transformed_df, transformer