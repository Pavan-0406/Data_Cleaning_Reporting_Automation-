# Data Cleaning & Reporting Automation

## Internship Project

A professional Python-based data cleaning and reporting automation system designed for a Data Analyst internship.

### Project objective
Automate the repetitive workflow of taking messy business data, identifying data-quality issues, cleaning and validating it, and producing an executive-ready Excel report plus an interactive dashboard.

## Requirements covered

| Internship requirement | Implementation |
|---|---|
| Python / Excel / Power BI automation | Python + Pandas + OpenPyXL + Excel-compatible outputs |
| Missing values | Detect, audit and fill type-appropriate missing values |
| Duplicates | Detect and remove duplicate records while preserving an issues log |
| Inconsistent data | Normalize headers, whitespace, capitalization, IDs and numeric types |
| Automated reports | Excel workbook generated automatically |
| Visual summaries | Excel charts + Streamlit/Plotly dashboard |
| Data preprocessing | Validation, type coercion, standardization and business-rule checks |
| Reporting efficiency | One command regenerates cleaned data and report |

## Workflow

Raw CSV
→ Data Quality Audit
→ Header/Text/Type Normalization
→ Duplicate Detection
→ Missing Value Handling
→ Invalid Transaction Checks
→ KPI Calculation
→ Clean CSV
→ Excel Report
→ Interactive Dashboard

## Project structure

```text
Data_Cleaning_Reporting_Automation/
├── data/
│   ├── raw/raw_sales_data.csv
│   └── processed/
├── output/
├── src/
│   ├── cleaning.py
│   ├── reporting.py
│   └── main.py
├── dashboard/app.py
├── docs/
├── tests/
├── requirements.txt
└── README.md
```

## How to run in VS Code

### 1. Open the project folder
Open `Data_Cleaning_Reporting_Automation` in VS Code.

### 2. Create virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Run the automation
```bash
python src/main.py
```

This generates:
- `data/processed/cleaned_sales_data.csv`
- `data/processed/data_issues.csv`
- `data/processed/data_quality_audit.csv`
- `output/automated_sales_report.xlsx`

### 5. Launch dashboard
```bash
streamlit run dashboard/app.py
```

## Excel report sheets

- **Executive Summary** — data-quality and business KPIs
- **Monthly Trend** — monthly sales trend
- **Category Analysis** — category performance
- **Region Analysis** — regional performance
- **Top Products** — top products by net sales
- **Cleaned Data** — final analytics-ready dataset
- **Data Issues** — rows requiring attention
- **Quality Audit** — missingness and uniqueness profile

## Cleaning logic

The pipeline:
1. Reads raw CSV data.
2. Recognizes common missing-value placeholders.
3. Normalizes column names.
4. Trims and standardizes text.
5. Converts dates and numeric fields.
6. Detects duplicates.
7. Fills appropriate missing values.
8. Flags/removes impossible quantities and prices.
9. Calculates gross sales, discount amount and net sales.
10. Exports clean data and an audit trail.
11. Builds a formatted Excel report.
12. Powers the dashboard from the cleaned dataset.

## Power BI compatibility

The generated `cleaned_sales_data.csv` is ready to import into Power BI. Recommended visuals:
- Card: Net Sales
- Card: Orders
- Card: Units Sold
- Line chart: Monthly Net Sales
- Bar chart: Sales by Category
- Bar chart: Sales by Region
- Bar chart: Top Products
- Slicers: Region, Category, Channel, Order Date

## Dataset

The included dataset is synthetic and intentionally contains missing values, duplicate rows, inconsistent text, numeric text and invalid quantities so the automation can be demonstrated safely.

## Resume bullet

**Data Cleaning & Reporting Automation:** Built a Python/Pandas data-quality pipeline that automated missing-value treatment, duplicate detection, data standardization, validation and KPI generation; produced formatted Excel reports and an interactive Streamlit dashboard for business reporting.

## Skills demonstrated

Python • Pandas • NumPy • Excel Automation • OpenPyXL • Data Cleaning • Data Validation • Data Quality • KPI Reporting • Plotly • Streamlit • Power BI-ready Data • ETL Workflow
