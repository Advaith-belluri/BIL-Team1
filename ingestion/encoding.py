import pandas as pd
import numpy as np

NUCS = ["A","C","G","T"]
PAIR = [a+b for a in NUCS for b in NUCS]

def one_hot_snp_pair(ref, alt):
    if ref not in NUCS or alt not in NUCS:
        return [0]*16
    idx = PAIR.index(ref+alt)
    v = [0]*16
    v[idx] = 1
    return v

def add_encoding_columns(df):
    x = df.copy()
    x["is_snp"] = (x["ref"].str.len()==1) & (x["alt"].str.len()==1)
    oh = x.apply(lambda r: one_hot_snp_pair(str(r["ref"]), str(r["alt"])) if r["is_snp"] else [0]*16, axis=1, result_type="expand")
    oh.columns = [f"oh_{p}" for p in PAIR]
    x = pd.concat([x, oh], axis=1)
    x["kmer2"] = (x["ref"].astype(str) + x["alt"].astype(str)).str[:2]
    return x
