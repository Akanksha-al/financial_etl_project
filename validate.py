# validate.py  —  Step 2: Detect data quality issues
# ────────────────────────────────────────────────────────────────────────────

import pandas as pd
import logging


def validate(df: pd.DataFrame) -> dict:
    """
    Scans the DataFrame for common data quality problems.
    Returns a dict of issues found (empty dict = clean data).
    """
    print(f"\n{'='*60}")
    print(f"  🔍  STEP 2 — VALIDATE")
    print(f"{'='*60}")

    issues = {}

    # 1. Null / missing values
    nulls = df.isnull().sum()
    null_cols = {col: int(count) for col, count in nulls.items() if count > 0}
    if null_cols:
        issues["NULLS"] = null_cols
        print(f"  🔴 Null values found    : {null_cols}")
    else:
        print(f"  ✅ No null values")

    # 2. Duplicate rows
    dupe_count = int(df.duplicated().sum())
    if dupe_count:
        issues["DUPLICATES"] = dupe_count
        print(f"  🔴 Duplicate rows       : {dupe_count}")
    else:
        print(f"  ✅ No duplicate rows")

    # 3. Negative bank balances
    if "balance" in df.columns:
        neg_balance = int((df["balance"] < 0).sum())
        if neg_balance:
            issues["NEGATIVE_BALANCE"] = neg_balance
            print(f"  🟡 Negative balances    : {neg_balance} customers")

    # 4. Inconsistent status casing (e.g. 'completed' vs 'COMPLETED' vs 'Completed')
    if "status" in df.columns:
        unique_statuses = df["status"].dropna().unique().tolist()
        lower_set = set(s.strip().lower() for s in unique_statuses)
        if len(unique_statuses) != len(lower_set):
            issues["STATUS_CASING"] = unique_statuses
            print(f"  🟡 Inconsistent status  : {unique_statuses}")
        else:
            print(f"  ✅ Status values clean  : {unique_statuses}")

    # 5. Failed transactions
    if "status" in df.columns:
        failed = int((df["status"].str.lower().str.strip() == "failed").sum())
        if failed:
            issues["FAILED_TXN"] = failed
            print(f"  🟡 Failed transactions  : {failed}")

    # 6. Amount outliers (> 3 standard deviations)
    if "amount" in df.columns:
        amt = df["amount"].dropna()
        outliers = int(((amt - amt.mean()).abs() > 3 * amt.std()).sum())
        if outliers:
            issues["OUTLIERS"] = outliers
            print(f"  🟡 Amount outliers (3σ) : {outliers}")

    if not issues:
        print(f"  ✅ Data is clean — no issues found!")

    print(f"\n  Total issues detected: {len(issues)}")
    logging.info(f"[VALIDATE] Issues: {issues}")
    return issues
