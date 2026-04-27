# config.py
# ─────────────────────────────────────────────
# All project settings live here.
# Change paths or keys in this ONE file only.
# ─────────────────────────────────────────────

import os

# ── Paths ────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
LOG_DIR     = os.path.join(BASE_DIR, "logs")

CSV_FILE    = os.path.join(DATA_DIR,   "bank_transactions.csv")
DB_FILE     = os.path.join(OUTPUT_DIR, "financial_etl.db")
LOG_FILE    = os.path.join(LOG_DIR,    "etl.log")
REPORT_FILE = os.path.join(OUTPUT_DIR, "etl_report.txt")

# ── Anthropic API Key ────────────────────────
# Option 1 (recommended): set env variable →  export ANTHROPIC_API_KEY=sk-ant-...
# Option 2 (quick test):  paste key directly below (don't share your code!)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── ETL Settings ─────────────────────────────
GST_RATE          = 0.18          # 18% GST applied to amounts
OUTLIER_PERCENTILE = 99           # cap amounts above this percentile
AI_MODEL          = "claude-opus-4-5"
AI_MAX_TOKENS     = 1200
