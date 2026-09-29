
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))

from cleaning import run_pipeline
from reporting import build_report

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "raw_sales_data.csv"
OUT = ROOT / "data" / "processed"
REPORT = ROOT / "output" / "automated_sales_report.xlsx"

def main():
    cleaned, issues, audit, summary = run_pipeline(RAW, OUT)
    build_report(cleaned, issues, audit, summary, REPORT)
    print("\n=== DATA CLEANING & REPORTING AUTOMATION ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print(f"\nCleaned data: {OUT/'cleaned_sales_data.csv'}")
    print(f"Data issues:  {OUT/'data_issues.csv'}")
    print(f"Excel report: {REPORT}")

if __name__ == "__main__":
    main()
