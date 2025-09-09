import os
import gzip
import shutil
import requests
import pandas as pd
from .config import REFERENCE_DIR

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
    return dest_path

def gunzip_if_needed(path):
    if path.endswith(".gz"):
        out_path = path[:-3]
        with gzip.open(path, "rb") as f_in, open(out_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return out_path
    return path

def vcf_to_parquet(vcf_path, out_parquet):
    from cyvcf2 import VCF
    v = VCF(vcf_path)
    rows = []
    for rec in v:
        alts = rec.ALT or []
        for alt in alts:
            info = dict(rec.INFO)
            gene = None
            if "GENEINFO" in info and isinstance(info["GENEINFO"], str):
                gene = str(info["GENEINFO"]).split("|")[0].split(":")[0]
            clnsig = info.get("CLNSIG", None)
            af = info.get("AF", None)
            if isinstance(af, (list, tuple)):
                af = af[0] if len(af) > 0 else None
            rows.append({
                "chrom": rec.CHROM,
                "pos": int(rec.POS),
                "ref": rec.REF,
                "alt": str(alt),
                "id": rec.ID,
                "gene_symbol": gene,
                "clinical_significance": clnsig,
                "af": float(af) if af is not None else None
            })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_parquet), exist_ok=True)
    df.to_parquet(out_parquet, index=False)
    return out_parquet

def fetch_and_build_parquet(url, name):
    os.makedirs(REFERENCE_DIR, exist_ok=True)
    local = os.path.join(REFERENCE_DIR, os.path.basename(url))
    downloaded = download_file(url, local)
    decompressed = gunzip_if_needed(downloaded)
    out = os.path.join(REFERENCE_DIR, f"{name}.parquet")
    return vcf_to_parquet(decompressed, out)
