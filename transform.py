# transform.py  —  Step 3: Clean and enrich the data
# ────────────────────────────────────────────────────────────────────────────

import pandas as pd
import logging
from datetime import datetime
from config import GST_RATE, OUTLIER_PERCENTILE


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw data and adds enriched columns.
    Returns the cleaned DataFrame.
    """
    print(f"\n{'='*60}")
    print(f"  ⚙️   STEP 3 — TRANSFORM")
    print(f"{'='*60}")

    original_rows = len(df)

    # ── 3a. Remove duplicates ────────────────────────────────────────────────
    df = df.drop_duplicates()
    removed = original_rows - len(df)
    if removed:
        print(f"  ✅ Removed {removed} duplicate rows")

    # ── 3b. Handle null values ───────────────────────────────────────────────
    if df["amount"].isnull().sum():
        median_amt = df["amount"].median()
        df["amount"] = df["amount"].fillna(median_amt)
        print(f"  ✅ Null amount → filled with median ₹{median_amt:,.2f}")

    if df["balance"].isnull().sum():
        df["balance"] = df["balance"].fillna(0)
        print(f"  ✅ Null balance → filled with 0")

    # ── 3c. Normalize 'status' column ───────────────────────────────────────
    df["status"] = df["status"].str.strip().str.lower().str.capitalize()
    print(f"  ✅ Status normalized → {sorted(df['status'].unique().tolist())}")

    # ── 3d. Cap outliers at 99th percentile ─────────────────────────────────
    cap = df["amount"].quantile(OUTLIER_PERCENTILE / 100)
    outlier_count = int((df["amount"] > cap).sum())
    if outlier_count:
        df["amount"] = df["amount"].clip(upper=cap)
        print(f"  ✅ {outlier_count} outlier(s) capped at ₹{cap:,.2f} ({OUTLIER_PERCENTILE}th percentile)")

    # ── 3e. Add GST column ───────────────────────────────────────────────────
    df["amount_with_gst"] = (df["amount"] * (1 + GST_RATE)).round(2)
    print(f"  ✅ Added 'amount_with_gst' ({int(GST_RATE*100)}% GST) column")

    # ── 3f. Add risk flag ────────────────────────────────────────────────────
    def assign_risk(row):
        if row.get("default") == "yes" or row.get("balance", 0) < 0:
            return "HIGH"
        elif row.get("loan") == "yes":
            return "MEDIUM"
        return "LOW"

    df["risk_flag"] = df.apply(assign_risk, axis=1)
    risk_counts = df["risk_flag"].value_counts().to_dict()
    print(f"  ✅ Risk flags assigned  : {risk_counts}")

    # ── 3g. Add age group ────────────────────────────────────────────────────
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 30, 45, 60, 120],
        labels=["Young(≤30)", "Mid(31-45)", "Senior(46-60)", "Elder(61+)"]
    ).astype(str)
    age_counts = df["age_group"].value_counts().to_dict()
    print(f"  ✅ Age groups created   : {age_counts}")

    # ── 3h. Add processing timestamp ─────────────────────────────────────────
    df["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  ✅ 'processed_at' timestamp added")

    print(f"\n  Final row count : {len(df):,} clean rows ready to load")
    logging.info(f"[TRANSFORM] Done. {len(df)} rows after cleaning.")
    return df
