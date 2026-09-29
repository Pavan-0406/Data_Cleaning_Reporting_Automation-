
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from cleaning import normalize_headers, normalize_text, coerce_types, clean_data

def test_header_normalization():
    df = pd.DataFrame({"Order ID": [1], "Customer Name": ["A"]})
    out = normalize_headers(df)
    assert list(out.columns) == ["order_id", "customer_name"]

def test_cleaning_removes_duplicates_and_invalid_quantity():
    df = pd.DataFrame({
        "order_id":["1","1","2"],
        "order_date":["2026-01-01","2026-01-01","2026-01-02"],
        "customer_id":["C1","C1","C2"],
        "product":["A","A","B"],
        "category":["Electronics","Electronics","Accessories"],
        "region":["South","South","North"],
        "channel":["Online","Online","Retail"],
        "quantity":[2,2,-1],
        "unit_price":[100,100,200],
        "discount":[0,0,0],
        "customer_name":["A","A","B"]
    })
    df = normalize_headers(df)
    df = normalize_text(df)
    df = coerce_types(df)
    cleaned, issues, _, summary = clean_data(df)
    assert len(cleaned) == 1
    assert summary["Duplicate Rows"] == 1
