# load.py  —  Step 4: Save clean data to SQLite database
# ────────────────────────────────────────────────────────────────────────────

import sqlite3
import pandas as pd
import logging
from config import DB_FILE


def load(df: pd.DataFrame) -> dict:
    """
    Saves the cleaned DataFrame to a SQLite database.
    Returns a summary dict with row count and key stats.
    """
    print(f"\n{'='*60}")
    print(f"  💾  STEP 4 — LOAD")
    print(f"{'='*60}")

    # Connect and write
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("bank_transactions", conn, if_exists="replace", index=False)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_id ON bank_transactions(transaction_id)")
    conn.commit()

    # Summary queries
    row_count  = conn.execute("SELECT COUNT(*) FROM bank_transactions").fetchone()[0]
    avg_amount = conn.execute("SELECT ROUND(AVG(amount), 2) FROM bank_transactions").fetchone()[0]
    by_type    = dict(conn.execute(
        "SELECT transaction_type, COUNT(*) FROM bank_transactions GROUP BY transaction_type"
    ).fetchall())
    by_risk    = dict(conn.execute(
        "SELECT risk_flag, COUNT(*) FROM bank_transactions GROUP BY risk_flag"
    ).fetchall())
    by_status  = dict(conn.execute(
        "SELECT status, COUNT(*) FROM bank_transactions GROUP BY status"
    ).fetchall())
    conn.close()

    print(f"  ✅ Saved to        : {DB_FILE}")
    print(f"  ✅ Rows loaded     : {row_count:,}")
    print(f"  📊 Avg amount      : ₹{avg_amount:,}")
    print(f"  📊 By type         : {by_type}")
    print(f"  📊 By risk         : {by_risk}")
    print(f"  📊 By status       : {by_status}")

    logging.info(f"[LOAD] {row_count} rows saved to {DB_FILE}")

    return {
        "rows": row_count,
        "avg_amount": avg_amount,
        "by_type": by_type,
        "by_risk": by_risk,
        "by_status": by_status,
    }
