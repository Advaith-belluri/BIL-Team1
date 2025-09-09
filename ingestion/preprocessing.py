import pandas as pd

def preprocess_variants(df):
    df = df.dropna(subset=["alt"])
    df["is_snp"] = (df["ref"].str.len() == 1) & (df["alt"].str.len() == 1)
    df["variant_length"] = df["alt"].str.len() - df["ref"].str.len()
    df["impact_score"] = df["info"].apply(lambda x: x.get("CADD", 0) if isinstance(x, dict) else 0)
    return df
