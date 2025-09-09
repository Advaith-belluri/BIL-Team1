import pandas as pd

def annotate_variants(variants, annotation_db):
    return variants.merge(annotation_db, on=["chrom", "pos", "ref", "alt"], how="left")
