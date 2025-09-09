import argparse
from ingestion.annotation_fetch import fetch_and_build_parquet

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True)
parser.add_argument("--name", required=True)
args = parser.parse_args()

out = fetch_and_build_parquet(args.url, args.name)
print(out)
