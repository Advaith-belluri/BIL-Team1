import os
import tempfile
import pandas as pd
from ingestion.vcf_parser import parse_vcf_per_sample
from ingestion.qc import filter_variants
from ingestion.encoding import add_encoding_columns
from ingestion.collapsing import collapse_gene_level

VCF_TEXT = """##fileformat=VCFv4.2
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts1\ts2
1\t1000\trs1\tA\tG\t50\tPASS\tAF=0.005;CADD=12.3;GENEINFO=GENE1:1\tGT:DP\t0/1:20\t0/0:18
1\t2000\trs2\tC\tT\t10\tPASS\tAF=0.05;CADD=5.1;GENEINFO=GENE2:2\tGT:DP\t0/1:8\t0/1:5
"""

def write_temp_vcf(text):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".vcf")
    tmp.write(text.encode())
    tmp.close()
    return tmp.name

def test_end_to_end():
    path = write_temp_vcf(VCF_TEXT)
    df = parse_vcf_per_sample(path)
    assert not df.empty
    assert set(df["sample_id"]) == {"s1","s2"}
    df2 = filter_variants(df, min_qual=20, min_dp=10, max_af=0.01)
    assert (df2["qual"] >= 20).all()
    assert (df2["dp"] >= 10).all()
    if "af" in df2.columns:
        assert (df2["af"].fillna(0) <= 0.01).all()
    enc = add_encoding_columns(df2)
    assert any([c.startswith("oh_") for c in enc.columns])
    feat = collapse_gene_level(enc)
    assert {"sample_id","gene_symbol","n_variants","n_rare","max_impact"}.issubset(set(feat.columns))
    os.remove(path)
