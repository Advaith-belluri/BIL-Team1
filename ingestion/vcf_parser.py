import cyvcf2
import pandas as pd
import numpy as np

def parse_vcf_per_sample(path, samples=None):
    vcf = cyvcf2.VCF(path)
    if samples:
        vcf.set_samples(samples)
    selected_samples = list(vcf.samples)
    rows = []
    for rec in vcf:
        alts = rec.ALT or []
        if not alts:
            continue
        dp_arr = None
        try:
            dp_arr = rec.format('DP')
        except Exception:
            dp_arr = None
        gts = rec.genotypes or []
        for s_idx, s in enumerate(selected_samples):
            gt = gts[s_idx] if s_idx < len(gts) else None
            if gt is None:
                continue
            alleles = gt[:2] if len(gt) >= 2 else [0,0]
            if 1 not in alleles and 2 not in alleles and 3 not in alleles:
                continue
            dp = None
            if dp_arr is not None:
                try:
                    dp_val = dp_arr[s_idx]
                    if isinstance(dp_val, np.ndarray):
                        dp = int(dp_val[0]) if len(dp_val) > 0 and dp_val[0] is not None else None
                    else:
                        dp = int(dp_val) if dp_val is not None else None
                except Exception:
                    dp = None
            alt_idx = 1 if 1 in alleles else (2 if 2 in alleles else 1)
            alt_base = alts[alt_idx-1] if len(alts) >= alt_idx else alts[0]
            rows.append({
                "sample_id": s,
                "chrom": rec.CHROM,
                "pos": int(rec.POS),
                "id": rec.ID,
                "ref": rec.REF,
                "alt": str(alt_base),
                "qual": float(rec.QUAL) if rec.QUAL is not None else None,
                "filter": None if rec.FILTER is None else str(rec.FILTER),
                "dp": dp,
                "info": dict(rec.INFO)
            })
    return pd.DataFrame(rows)
