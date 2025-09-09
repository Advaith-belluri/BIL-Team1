import os
import pandas as pd
from .config import OUTPUT_DIR

def save_dataframe(df, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.parquet")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_parquet(path, index=False)
    return path
