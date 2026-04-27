# extract.py  —  Step 1: Read the real CSV file
# ────────────────────────────────────────────────────────────────────────────

import pandas as pd
import logging
from config import CSV_FILE


def extract() -> pd.DataFrame:
    """
    Reads the real-world bank transaction CSV and returns a DataFrame.
    Raises FileNotFoundError if the CSV is missing.
    """
    logging.info(f"[EXTRACT] Reading: {CSV_FILE}")

    if not __import__("os").path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"CSV not found at: {CSV_FILE}\n"
            f"Make sure 'bank_transactions.csv' is inside the 'data/' folder."
        )

    df = pd.read_csv(CSV_FILE)

    print(f"\n{'='*60}")
    print(f"  📥  STEP 1 — EXTRACT")
    print(f"{'='*60}")
    print(f"  File   : {CSV_FILE}")
    print(f"  Rows   : {len(df):,}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  Preview (first 3 rows):")
    print(df.head(3).to_string(index=False))

    logging.info(f"[EXTRACT] Loaded {len(df)} rows, {len(df.columns)} columns")
    return df
