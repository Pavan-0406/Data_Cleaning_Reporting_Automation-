# Project Presentation / Viva Notes

## Problem Statement
Manual spreadsheet cleaning is repetitive and error-prone. Analysts often spend time fixing blanks, duplicates, inconsistent labels and invalid numeric values before reporting.

## Proposed Solution
This project automates the complete preprocessing and reporting workflow using Python, Pandas and OpenPyXL. It creates both an audit trail and a management-friendly report.

## Key Cleaning Rules
- Standardize headers to snake_case
- Convert placeholder strings to missing values
- Trim whitespace
- Standardize category/region/channel capitalization
- Convert dates and numeric fields to correct types
- Remove duplicate rows
- Fill missing numeric values with median values
- Fill missing categorical values with mode/fallback labels
- Reject non-positive quantities/prices
- Preserve problematic rows in a Data Issues sheet

## Business KPIs
- Total Net Sales
- Number of Orders
- Units Sold
- Average Order Value
- Data Quality Score
- Rows Removed
- Duplicate Rows

## Expected Internship Outcome
The project demonstrates practical data preprocessing, automation, quality control and reporting skills and produces reusable outputs suitable for Excel or Power BI.
