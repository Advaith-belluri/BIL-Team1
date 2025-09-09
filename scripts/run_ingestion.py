import argparse
import pandas as pd
from ingestion.vcf_parser import parse_vcf_per_sample
from ingestion.annotator import annotate_variants
from ingestion.qc import filter_variants
from ingestion.encoding import add_encoding_columns
from ingestion.collapsing import collapse_gene_level
from ingestion.io_utils import save_dataframe

parser = argparse.ArgumentParser()
parser.add_argument("--vcf", required=True)
parser.add_argument("--samples", nargs="*", default=None)
parser.add_argument("--annotation", required=False)
parser.add_argument("--min-qual", type=float, default=None)
parser.add_argument("--min-dp", type=int, default=None)
parser.add_argument("--max-af", type=float, default=None)
parser.add_argument("--encode", action="store_true")
parser.add_argument("--collapse", action="store_true")
parser.add_argument("--out-name", default="genomics_processed")
args = parser.parse_args()

df = parse_vcf_per_sample(args.vcf, args.samples)
if args.annotation:
    ann = pd.read_parquet(args.annotation)
    df = annotate_variants(df, ann)
df = filter_variants(df, min_qual=args.min_qual, min_dp=args.min_dp, max_af=args.max_af)
if args.encode:
    df = add_encoding_columns(df)
out_main = save_dataframe(df, args.out_name)
if args.collapse:
    features = collapse_gene_level(df)
    out_c = save_dataframe(features, f"{args.out_name}_gene")
    print(out_c)
print(out_main)
