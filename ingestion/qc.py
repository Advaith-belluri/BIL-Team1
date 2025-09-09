import pandas as pd
import numpy as np

def filter_variants(df, min_qual=None, min_dp=None, max_af=None, af_col="af"):
    x = df.copy()
    if min_qual is not None:
        x = x[(x["qual"].notna()) & (x["qual"] >= float(min_qual))]
    if min_dp is not None and "dp" in x.columns:
        x = x[(x["dp"].notna()) & (x["dp"] >= int(min_dp))]
    if max_af is not None:
        af_series = None
        if af_col in x.columns:
            af_series = x[af_col]
        else:
            af_series = x["info"].apply(lambda d: d.get("AF", np.nan) if isinstance(d, dict) else np.nan)
            af_series = af_series.apply(lambda v: v[0] if isinstance(v, (list, tuple)) and len(v)>0 else v)
        x = x[(af_series.isna()) | (af_series.astype(float) <= float(max_af))]
    return x.reset_index(drop=True)
