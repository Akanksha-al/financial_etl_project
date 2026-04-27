# ai_report.py  —  Step 5: AI-generated plain-English report using Claude
# ────────────────────────────────────────────────────────────────────────────
# Requires:  pip install anthropic
# Requires:  ANTHROPIC_API_KEY set in config.py or as env variable
# ────────────────────────────────────────────────────────────────────────────

import logging
import json
from datetime import datetime
from config import ANTHROPIC_API_KEY, AI_MODEL, AI_MAX_TOKENS, REPORT_FILE


def generate_report(issues: dict, db_summary: dict, duration: float) -> str:
    """
    Asks Claude to write a professional ETL run report.
    Falls back to a plain text report if the API key is missing.
    Returns the report text.
    """
    print(f"\n{'='*60}")
    print(f"  📄  STEP 5 — AI REPORT")
    print(f"{'='*60}")

    report_text = _call_claude(issues, db_summary, duration)

    # Print to console
    print(f"\n{'-'*60}")
    print(report_text)
    print(f"{'-'*60}")

    # Save to file
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"ETL Run Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(report_text)

    print(f"\n  ✅ Report saved to: {REPORT_FILE}")
    logging.info("[AI_REPORT] Report generated and saved.")
    return report_text


def _call_claude(issues: dict, db_summary: dict, duration: float) -> str:
    """Internal: call Anthropic API. Falls back to manual report if no API key."""

    if not ANTHROPIC_API_KEY:
        print("  ⚠️  No ANTHROPIC_API_KEY found — generating plain report instead.")
        print("      To enable AI report: set ANTHROPIC_API_KEY in config.py or as env variable.")
        return _plain_report(issues, db_summary, duration)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = f"""
You are a senior data engineer writing a concise ETL pipeline run report for a financial data team.

Run details:
{json.dumps({
    "rows_loaded": db_summary["rows"],
    "avg_transaction_amount_INR": db_summary["avg_amount"],
    "transaction_types": db_summary["by_type"],
    "risk_distribution": db_summary["by_risk"],
    "status_breakdown": db_summary["by_status"],
    "data_issues_found": issues,
    "duration_seconds": round(duration, 2)
}, indent=2)}

Write a 150–200 word professional report covering:
- What data was processed (source, rows, columns)
- What data quality issues were found and how they were fixed
- Key statistics from the cleaned data
- Pipeline performance
- One actionable recommendation

Write in plain paragraphs only. No bullet points, no headers, no markdown formatting.
"""
        print("  🤖 Asking Claude AI to write the report...")
        message = client.messages.create(
            model=AI_MODEL,
            max_tokens=AI_MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        logging.warning(f"[AI_REPORT] Claude API call failed: {e}. Using plain report.")
        print(f"  ⚠️  Claude API error: {e}")
        print(f"      Falling back to plain report.")
        return _plain_report(issues, db_summary, duration)


def _plain_report(issues: dict, db_summary: dict, duration: float) -> str:
    """Generates a plain-text report without AI (fallback)."""
    lines = [
        f"The ETL pipeline processed the real-world Indian bank transactions dataset.",
        f"A total of {db_summary['rows']} records were successfully loaded into the SQLite database.",
        f"",
        f"Data quality issues detected and resolved:",
    ]
    if issues:
        for k, v in issues.items():
            lines.append(f"  - {k}: {v}")
    else:
        lines.append("  - No issues found. Data was clean.")

    lines += [
        f"",
        f"Key statistics from cleaned data:",
        f"  - Average transaction amount : Rs {db_summary['avg_amount']:,}",
        f"  - Transaction types          : {db_summary['by_type']}",
        f"  - Risk distribution          : {db_summary['by_risk']}",
        f"  - Status breakdown           : {db_summary['by_status']}",
        f"",
        f"Pipeline completed in {round(duration, 2)} seconds.",
        f"Recommendation: Schedule this pipeline daily and add email alerts for HIGH-risk transactions.",
    ]
    return "\n".join(lines)
