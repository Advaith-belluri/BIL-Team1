import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
REFERENCE_DIR = os.path.join(BASE_DIR, "data", "reference")
OUTPUT_DIR = os.path.join(BASE_DIR, "preprocessed")
