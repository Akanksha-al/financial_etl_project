# 🏦 Adaptive Financial ETL Pipeline — Real-World Data

A complete ETL pipeline using **real Indian bank transaction data**,
built to run directly in **PyCharm** with no extra setup.

---

## 📁 Project Structure

```
financial_etl_project/
│
├── main.py            ← ▶ RUN THIS FILE in PyCharm
├── config.py          ← All settings (paths, API key, GST rate)
├── extract.py         ← Step 1: Read CSV
├── validate.py        ← Step 2: Detect data quality issues
├── transform.py       ← Step 3: Clean + enrich data
├── load.py            ← Step 4: Save to SQLite database
├── ai_report.py       ← Step 5: Claude AI generates run report
│
├── data/
│   └── bank_transactions.csv   ← Real-world input data (100 rows)
│
├── output/            ← Created automatically when you run
│   ├── financial_etl.db        ← Clean data in SQLite
│   └── etl_report.txt          ← AI-generated report
│
├── logs/              ← Created automatically when you run
│   └── etl.log                 ← Full run log
│
└── requirements.txt   ← Python packages needed
```

---

## ▶️ How to Run in PyCharm (Step by Step)

### Step 1 — Open the project
- Open PyCharm
- Click **File → Open**
- Select the `financial_etl_project` folder
- Click **OK**

### Step 2 — Install packages
- Open the terminal inside PyCharm: **View → Tool Windows → Terminal**
- Run this command:
```
pip install -r requirements.txt
```

### Step 3 — Run the pipeline
- In the left panel, right-click on **main.py**
- Click **Run 'main'**
- Or press **Shift + F10**

That's it! The pipeline runs all 5 steps automatically.

---

## 📊 What the Pipeline Does

| Step | File | What Happens |
|------|------|-------------|
| 1 | extract.py | Reads `bank_transactions.csv` |
| 2 | validate.py | Finds nulls, duplicates, bad data |
| 3 | transform.py | Cleans data, adds GST & risk columns |
| 4 | load.py | Saves to SQLite database |
| 5 | ai_report.py | Claude AI writes a run report |

---

## 🔍 About the Input Data

`data/bank_transactions.csv` contains **100 real-world style** Indian bank transactions with:
- Real Indian customer names and job categories
- Actual transaction types: deposit, withdrawal, transfer
- Real data issues built in: nulls, inconsistent status casing, negative balances, failed transactions

**Intentional data problems (for ETL practice):**
- Row 51: missing `balance`
- Row 52: missing `amount`
- Multiple rows: status written as `completed`, `COMPLETED`, `Completed` (inconsistent)
- 8 customers with negative balance
- 10 failed transactions

---

## 🤖 AI Report (Optional)

To enable the Claude AI report, add your API key:

**Option 1 — Environment variable (recommended):**
```bash
# Mac/Linux:
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows:
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Option 2 — Paste directly in config.py:**
```python
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

Get your free API key at: https://console.anthropic.com/keys

If no key is set, the pipeline still runs fully — it just generates a plain text report instead.

---

## 🔧 How to Customize

| What to change | Where |
|---|---|
| Input CSV file | `config.py` → `CSV_FILE` |
| GST rate | `config.py` → `GST_RATE` |
| Database location | `config.py` → `DB_FILE` |
| API key | `config.py` → `ANTHROPIC_API_KEY` |
| Add new cleaning rules | `transform.py` |
| Add new validations | `validate.py` |
| Use your own CSV | Replace `data/bank_transactions.csv` |

---

## 📦 Output Files

After running, check the `output/` folder:
- **financial_etl.db** — Open with DB Browser for SQLite (free tool)
- **etl_report.txt** — Plain text AI-generated summary

And `logs/etl.log` for the full technical log.
