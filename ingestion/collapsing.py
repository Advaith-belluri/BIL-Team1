import pandas as pd
import numpy as np

def collapse_gene_level(df, gene_col="gene_symbol", sample_col="sample_id", impact_col="impact_score", rare_af_threshold=0.01, af_col="af"):
    x = df.copy()
    if gene_col not in x.columns:
        x[gene_col] = None
    if af_col not in x.columns:
        x[af_col] = x["info"].apply(lambda d: d.get("AF", np.nan) if isinstance(d, dict) else np.nan)
        x[af_col] = x[af_col].apply(lambda v: v[0] if isinstance(v, (list, tuple)) and len(v)>0 else v)
    x["is_rare"] = x[af_col].apply(lambda v: True if pd.isna(v) else float(v) <= float(rare_af_threshold))
    if impact_col not in x.columns:
        x[impact_col] = x["info"].apply(lambda d: d.get("CADD", 0) if isinstance(d, dict) else 0)
    grp = x.groupby([sample_col, gene_col], dropna=False)
    features = grp.agg(
        n_variants=("pos","count"),
        n_rare=("is_rare","sum"),
        max_impact=(impact_col,"max")
    ).reset_index()
    features["n_variants"] = features["n_variants"].astype(int)
    features["n_rare"] = features["n_rare"].astype(int)
    return features
