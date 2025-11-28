import os
import csv
import pytest
from assignment2.sales_analysis import SalesAnalysis, SaleRecord



# -------------------------------------------------------------------
# write a temporary CSV using provided rows
# -------------------------------------------------------------------
def write_temp_csv(tmp_path, filename, rows):
    file_path = tmp_path / filename
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "region", "product", "units_sold", "unit_price"])
        writer.writerows(rows)
    return str(file_path)


# -------------------------------------------------------------------
# 1. basic loading and clean records
# -------------------------------------------------------------------
def test_load_valid_records(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "25.50"],
        ["2024-01-02", "South", "Mouse", "20", "15.00"],
    ]

    csv_path = write_temp_csv(tmp_path, "small.csv", rows)
    analysis = SalesAnalysis(csv_path)

    assert len(analysis.data) == 2
    assert isinstance(analysis.data[0], SaleRecord)
    assert analysis.data[0].revenue == 255.0  


# -------------------------------------------------------------------
# 2.loader must skip invalid & malformed rows (edge-case testing)
# ---------------------------------------------------------------------
def test_loader_skips_invalid_rows(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "25.50"],     # valid
        ["2024-01-18", "", "Keyboard", "10", "25.50"],          # missing region
        ["2024-01-18", "North", "Mouse", "abc", "15.00"],       # invalid units
        ["2024-01-19", "South", "", "12", "25.50"],             # missing product
        ["2024-01-19", "East", "Monitor", "-3", "120.00"],      # negative units
        ["2024-01-20", "West", "Keyboard", "10", ""],           # missing price
        ["hello", "this", "is", "not", "valid"],                # broken row
        ["2024-01-21", "North", "Keyboard", "10"],              # wrong number of columns
    ]

    csv_path = write_temp_csv(tmp_path, "edge.csv", rows)
    analysis = SalesAnalysis(csv_path)

    # Only 1 valid row should remain
    assert len(analysis.data) == 1
    assert analysis.data[0].product == "Keyboard"


# -------------------------------------------------------------------
# 3. total revenue 
# -------------------------------------------------------------------
def test_total_revenue(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "20.00"],    # 200
        ["2024-01-02", "South", "Mouse", "5", "10.00"],       # 50
    ]

    csv_path = write_temp_csv(tmp_path, "rev.csv", rows)
    analysis = SalesAnalysis(csv_path)

    assert analysis.total_revenue() == 250.0


# -------------------------------------------------------------------
# 4. revenue by region 
# -------------------------------------------------------------------
def test_revenue_by_region(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "10"],   # 100
        ["2024-01-02", "North", "Mouse", "2", "20"],       # 40
        ["2024-01-03", "South", "Laptop", "1", "100"],     # 100
    ]

    csv_path = write_temp_csv(tmp_path, "region.csv", rows)
    analysis = SalesAnalysis(csv_path)

    result = analysis.revenue_by_region()
    assert result["North"] == 140
    assert result["South"] == 100


# -------------------------------------------------------------------
# 5.units sold by product
# -------------------------------------------------------------------
def test_units_sold_by_product(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "5", "20.00"],
        ["2024-01-02", "South", "Keyboard", "7", "20.00"],
        ["2024-01-03", "East", "Mouse", "3", "15.00"],
    ]

    csv_path = write_temp_csv(tmp_path, "product.csv", rows)
    analysis = SalesAnalysis(csv_path)

    result = analysis.units_sold_by_product()
    assert result["Keyboard"] == 12
    assert result["Mouse"] == 3


# -------------------------------------------------------------------
# 6.filter by revenue threshold
# -------------------------------------------------------------------
def test_filter_sales_by_revenue(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "10"],  # 100
        ["2024-01-02", "South", "Mouse", "1", "10"],      # 10
    ]

    csv_path = write_temp_csv(tmp_path, "filter.csv", rows)
    analysis = SalesAnalysis(csv_path)

    results = analysis.filter_sales_by_revenue(50)
    assert len(results) == 1
    assert results[0].product == "Keyboard"


# -------------------------------------------------------------------
# 7. average unit price per product 
# -------------------------------------------------------------------
def test_avg_unit_price(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "20.00"],
        ["2024-01-02", "South", "Keyboard", "5", "30.00"],
    ]

    csv_path = write_temp_csv(tmp_path, "avg.csv", rows)
    analysis = SalesAnalysis(csv_path)

    result = analysis.avg_unit_price_by_product()
    assert result["Keyboard"] == pytest.approx(25.0)


# -------------------------------------------------------------------
# 8. trend: Revenue grouped by (year, month)
# -------------------------------------------------------------------
def test_sales_trend(tmp_path):
    rows = [
        ["2024-01-10", "North", "Keyboard", "10", "10"],   # 100
        ["2024-01-20", "South", "Mouse", "5", "20"],      # 100
        ["2024-02-15", "East", "Laptop", "1", "300"],     # 300
    ]

    csv_path = write_temp_csv(tmp_path, "trend.csv", rows)
    analysis = SalesAnalysis(csv_path)

    trend = analysis.sales_trend()
    assert trend[(2024, 1)] == 200
    assert trend[(2024, 2)] == 300


# -------------------------------------------------------------------
# 9. Month-over-month % change (Functional FP version)
# -------------------------------------------------------------------
def test_month_over_month(tmp_path):
    rows = [
        ["2024-01-10", "North", "Keyboard", "10", "10"],   # 100
        ["2024-02-10", "South", "Mouse", "5", "20"],      # 100
        ["2024-03-10", "East", "Laptop", "2", "100"],     # 200
    ]

    csv_path = write_temp_csv(tmp_path, "mom.csv", rows)
    analysis = SalesAnalysis(csv_path)

    trend = analysis.sales_trend()
    mom = analysis.month_over_month(trend)

    # February to January: 100 -> 100 = 0%
    assert mom[(2024, 2)] == 0.0

    # March to February: 100 -> 200 = +100%
    assert mom[(2024, 3)] == 100.0


# -------------------------------------------------------------------
# 10. run_query 
# -------------------------------------------------------------------
def test_run_query(tmp_path):
    rows = [
        ["2024-01-01", "North", "Keyboard", "10", "10"],
        ["2024-01-02", "South", "Mouse", "1", "10"],
    ]

    csv_path = write_temp_csv(tmp_path, "query.csv", rows)
    analysis = SalesAnalysis(csv_path)

    result = analysis.run_query(lambda rows: max(rows, key=lambda r: r.revenue))
    assert result.product == "Keyboard"
    assert result.revenue == 100
