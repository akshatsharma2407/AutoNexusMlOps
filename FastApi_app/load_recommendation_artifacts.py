import joblib
from scipy.sparse import load_npz

def load_artifacts(sparse_matrix_path: str = './data/recommendation/transformed_df.npz', transformer_path : str = './models/recommendation_transformer.joblib'):
    transformed_df = load_npz(sparse_matrix_path)
    transformer = joblib.load(transformer_path)
    return transformed_df, transformer