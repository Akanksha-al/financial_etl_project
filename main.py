# main.py  —  Entry point. Run this file in PyCharm.
# ────────────────────────────────────────────────────────────────────────────
#
#   HOW TO RUN IN PYCHARM:
#   1. Open this project folder in PyCharm
#   2. Open terminal in PyCharm  (View → Tool Windows → Terminal)
#   3. Run:  pip install -r requirements.txt
#   4. Right-click main.py → Run 'main'   (or press Shift+F10)
#
# ────────────────────────────────────────────────────────────────────────────

import logging
import os
from datetime import datetime

from config import LOG_FILE, OUTPUT_DIR, LOG_DIR
from extract    import extract
from validate   import validate
from transform  import transform
from load       import load
from ai_report  import generate_report

# ── Ensure output folders exist ───────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR,    exist_ok=True)

# ── Setup logging ─────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


def run_pipeline():
    print("\n" + "=" * 60)
    print("  🏦  ADAPTIVE FINANCIAL ETL PIPELINE  (Real-World Data)")
    print("=" * 60)

    start = datetime.now()
    logging.info("Pipeline started")

    try:
        # Step 1 — Extract
        df = extract()

        # Step 2 — Validate
        issues = validate(df)

        # Step 3 — Transform
        df = transform(df)

        # Step 4 — Load
        db_summary = load(df)

        # Step 5 — AI Report
        duration = (datetime.now() - start).total_seconds()
        generate_report(issues, db_summary, duration)

        # Done
        print(f"\n{'='*60}")
        print(f"  ✅  PIPELINE COMPLETE")
        print(f"  ⏱️  Duration  : {duration:.1f} seconds")
        print(f"  📁  Database : output/financial_etl.db")
        print(f"  📄  Report   : output/etl_report.txt")
        print(f"  📋  Log      : logs/etl.log")
        print(f"{'='*60}\n")
        logging.info(f"Pipeline complete in {duration:.1f}s")

    except FileNotFoundError as e:
        print(f"\n❌  FILE ERROR: {e}")
        logging.error(f"FileNotFoundError: {e}")

    except Exception as e:
        print(f"\n❌  PIPELINE FAILED: {e}")
        logging.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()
