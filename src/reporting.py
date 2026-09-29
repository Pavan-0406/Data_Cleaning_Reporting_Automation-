
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.utils import get_column_letter

def build_report(cleaned, issues, audit, summary, output_path):
    output_path = Path(output_path)
    cleaned = cleaned.copy()
    cleaned["order_date"] = pd.to_datetime(cleaned["order_date"])

    kpis = pd.DataFrame({
        "Metric": ["Raw Rows","Clean Rows","Rows Removed","Duplicate Rows","Data Quality Score",
                   "Total Net Sales","Average Order Value","Total Units Sold"],
        "Value": [summary["Raw Rows"], summary["Clean Rows"], summary["Rows Removed"],
                  summary["Duplicate Rows"], summary["Data Quality Score %"]/100,
                  cleaned["net_sales"].sum(), cleaned["net_sales"].mean(),
                  cleaned["quantity"].sum()]
    })

    monthly = (cleaned.assign(Month=cleaned["order_date"].dt.to_period("M").astype(str))
               .groupby("Month", as_index=False)["net_sales"].sum()
               .rename(columns={"net_sales":"Net Sales"}))

    category = (cleaned.groupby("category", as_index=False)
                .agg(Net_Sales=("net_sales","sum"), Units=("quantity","sum"))
                .sort_values("Net_Sales", ascending=False))

    region = (cleaned.groupby("region", as_index=False)
              .agg(Net_Sales=("net_sales","sum"), Orders=("order_id","nunique"))
              .sort_values("Net_Sales", ascending=False))

    product = (cleaned.groupby("product", as_index=False)
               .agg(Net_Sales=("net_sales","sum"), Units=("quantity","sum"))
               .sort_values("Net_Sales", ascending=False).head(15))

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="Executive Summary", index=False, startrow=2)
        monthly.to_excel(writer, sheet_name="Monthly Trend", index=False)
        category.to_excel(writer, sheet_name="Category Analysis", index=False)
        region.to_excel(writer, sheet_name="Region Analysis", index=False)
        product.to_excel(writer, sheet_name="Top Products", index=False)
        cleaned.to_excel(writer, sheet_name="Cleaned Data", index=False)
        issues.to_excel(writer, sheet_name="Data Issues", index=False)
        audit.to_excel(writer, sheet_name="Quality Audit", index=False)

    wb = load_workbook(output_path)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    accent_fill = PatternFill("solid", fgColor="D9EAF7")
    white_font = Font(color="FFFFFF", bold=True)
    title_font = Font(size=18, bold=True, color="1F4E78")
    thin = Side(style="thin", color="D9E2F3")

    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.sheet_view.showGridLines = False
        for cell in ws[1]:
            cell.font = white_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center")
        for col in ws.columns:
            max_len = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(max_len + 2, 10), 32)

    ws = wb["Executive Summary"]
    ws["A1"] = "DATA CLEANING & REPORTING AUTOMATION"
    ws["A1"].font = title_font
    ws.merge_cells("A1:B1")
    ws["A2"] = "Automated executive summary generated from the cleaned dataset"
    ws["A2"].font = Font(italic=True, color="666666")
    ws["A4"].number_format = "0.0%"
    # Find and format KPI values
    for row in range(4, 12):
        ws[f"A{row}"].fill = accent_fill
        ws[f"A{row}"].font = Font(bold=True)
        ws[f"A{row}"].border = Border(bottom=thin)
    ws["B8"].number_format = "0.0%"
    ws["B9"].number_format = '#,##0.00'
    ws["B10"].number_format = '#,##0.00'

    # Charts
    cat_ws = wb["Category Analysis"]
    chart = BarChart()
    chart.title = "Net Sales by Category"
    chart.y_axis.title = "Net Sales"
    chart.x_axis.title = "Category"
    data = Reference(cat_ws, min_col=2, min_row=1, max_row=cat_ws.max_row)
    cats = Reference(cat_ws, min_col=1, min_row=2, max_row=cat_ws.max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.height = 7
    chart.width = 13
    ws.add_chart(chart, "D4")

    trend_ws = wb["Monthly Trend"]
    line = LineChart()
    line.title = "Monthly Net Sales Trend"
    data = Reference(trend_ws, min_col=2, min_row=1, max_row=trend_ws.max_row)
    cats = Reference(trend_ws, min_col=1, min_row=2, max_row=trend_ws.max_row)
    line.add_data(data, titles_from_data=True)
    line.set_categories(cats)
    line.height = 7
    line.width = 14
    trend_ws.add_chart(line, "D2")

    # Currency formatting
    for sheet in ["Monthly Trend","Category Analysis","Region Analysis","Top Products"]:
        ws2 = wb[sheet]
        for row in ws2.iter_rows():
            for cell in row:
                if cell.column == 2 and cell.row > 1:
                    cell.number_format = '#,##0.00'
    wb.save(output_path)
