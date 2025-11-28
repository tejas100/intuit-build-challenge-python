# Intuit Build Challenge: CSV Sales Data Analysis (Functional Programming & Streams)

[![Language](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[![Pattern](https://img.shields.io/badge/Pattern-Producer%20Consumer-orange.svg)]()

[![Assignment](https://img.shields.io/badge/Assignment-2-blueviolet.svg)]()

> **Assignment 2:** Perform data analysis on CSV sales data using functional programming, stream-style transformations, and higher-order operations.

---

## 📖 Overview

This project implements a functional-style sales analytics engine that processes CSV data using:

- Higher-order functions
- `reduce`, `filter`, and `map` transformations
- Pure data models with `@dataclass`
- Functional aggregation/grouping
- Declarative query execution
- Error-resistant CSV ingestion with validation

The design mirrors stream processing pipelines found in Java Streams, Spark, and modern data engineering systems, but implemented in clean, idiomatic Python, tailored to the Intuit Challenge requirements.

### Project Structure

```bash
assignment2/
│
├── data/
│   └── sales_large.csv               # Sample LARGE input dataset
|   └── sales_small.csv               # Sample SMALL input dataset
│
├── sales_analysis.py                 # Core implementation
├── test_sales_analysis.py            # unit tests
└── README.md                         # This file
```

## 🧠 Design Overview

### 1. SaleRecord (Data Model)
A simple, immutable `@dataclass` representing each row of the CSV.

- **Fields:** 
    - `date: str`
    - `region: str`
    - `product: str`
    - `units_sold: int`
    - `unit_price: float`
- **Computed property:** 
`revenue` → Returns `units_sold * unit_price`

- **Analysis Methods** 
<table>
  <tr>
    <th style="border:1px solid #ccc; padding:8px;">Method</th>
    <th style="border:1px solid #ccc; padding:8px;">Description</th>
    <th style="border:1px solid #ccc; padding:8px;">FP Pattern</th>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>total_revenue()</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Sum of all sales revenue</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>reduce</code></td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>revenue_by_region()</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Revenue aggregated by region</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>reduce</code> with dict accumulator</td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>units_sold_by_product()</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Units sold grouped by product</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>reduce</code> with dict accumulator</td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>filter_sales_by_revenue(threshold)</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Filter sales above threshold</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>filter</code> + <code>lambda</code></td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>avg_unit_price_by_product()</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Average price per product</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>reduce</code> + dict comprehension</td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>sales_trend()</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Revenue grouped by (year, month)</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>reduce</code> with tuple keys</td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>month_over_month(trend)</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Percentage change between months</td>
    <td style="border:1px solid #ccc; padding:8px;"><code>map</code> + <code>filter</code> + <code>zip</code></td>
  </tr>

  <tr>
    <td style="border:1px solid #ccc; padding:8px;"><code>run_query(query_fn)</code></td>
    <td style="border:1px solid #ccc; padding:8px;">Execute custom higher-order query</td>
    <td style="border:1px solid #ccc; padding:8px;">Higher-order function</td>
  </tr>

</table>



## ▶️ Running the Program

### 1. Clone the repo

```bash
git clone https://github.com/tejas100/intuit-build-challenge-python
cd intuit-build-challenge-python/assignment2
```
### 2. Selecting the right csv `(large / small)`
Please select your csv file under the `__main__` funtion as shown below
```bash
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="[WARN] %(message)s")
    
    analysis = SalesAnalysis("data/sales_small.csv") # Please select your CSV file here (small or large)
    # analysis = SalesAnalysis("data/sales_large.csv") 

```
### 2. Run the script

```bash
python sales_analysis.py
```
### Sample Output
The sample output is shown from the mix of both large and the small dataset, as I'm illustrating all the analysis methods

```bash
(.venv) (base) tejas@Tejass-MacBook assignment2 % python sales_analysis.py

============================================================
SALES ANALYSIS REPORT
============================================================

============================================================
1. Total Revenue
============================================================
$19,770.00

============================================================
2. Revenue by Region
============================================================
Region               | Revenue ($)
------------------------------------------------------------
North                | 4360.0
South                | 2398.0
East                 | 7229.0
West                 | 5783.0

============================================================
3. Units Sold by Product
============================================================
Product              | Units Sold
------------------------------------------------------------
Keyboard             | 112
Mouse                | 188
Laptop               | 12
Monitor              | 42

============================================================
4. High Revenue Sales (>= $500)
============================================================
Date         Region     Product      Units    Price      Revenue
----------------------------------------------------------------------
2024-01-02   East       Laptop       3        $750.00    $2250.00
2024-01-04   East       Monitor      5        $120.00    $600.00
2024-01-05   West       Laptop       2        $760.00    $1520.00
2024-01-07   East       Monitor      7        $115.00    $805.00
2024-01-07   North      Laptop       1        $780.00    $780.00
2024-01-09   East       Monitor      6        $119.00    $714.00
2024-01-09   West       Laptop       3        $765.00    $2295.00
2024-01-12   North      Laptop       2        $770.00    $1540.00
2024-01-13   East       Monitor      5        $118.00    $590.00
2024-01-15   East       Monitor      8        $120.00    $960.00
2024-01-15   West       Laptop       1        $780.00    $780.00
2024-01-17   East       Monitor      7        $118.00    $826.00

============================================================
5. Average Unit Price by Product
============================================================
Product              | Avg Price
------------------------------------------------------------
Keyboard             | $25.55
Mouse                | $14.67
Laptop               | $767.50
Monitor              | $118.71

============================================================
6. Sales Trend (Revenue by Month)
============================================================
Month                | Revenue
------------------------------------------------------------
2024-01              | $19,770.00

============================================================
7. Month-Over-Month Change (%)
============================================================
Month                | % Change
------------------------------------------------------------
2023-02              | -15.62%
2023-03              | 16.66%
2023-04              | -13.07%
2023-05              | 14.13%
2023-06              | -3.58%
2023-07              | -10.85%
2023-08              | 1.07%
2023-09              | -3.98%
2023-10              | 15.15%
2023-11              | -0.96%
2023-12              | -10.23%
2024-01              | 11.96%
2024-02              | -5.86%
2024-03              | -2.80%
2024-04              | -9.56%
2024-05              | 10.91%
2024-06              | -7.77%
2024-07              | 33.11%
2024-08              | -7.88%
2024-09              | -11.68%
2024-10              | 11.49%
2024-11              | 3.69%
2024-12              | 12.48%

============================================================
8. Top Revenue Item
============================================================
Field           | Value
----------------------------------------
Date            | 2023-03-16
Region          | North
Product         | Laptop
Units Sold      | 40
Unit Price      | $798.78
Revenue         | $31,951.20

```

### 3. Running the tests
From the home directory `intuit-build-challenge-python/`

```bash
pytest -v
```
### Test results
The below test result is from both `assignment1` and `assignment2`

```bash
(.venv) (base) tejas@Tejass-MacBook intuit-build-challenge-python % pytest -v               
========================================================== test session starts ===========================================================
platform darwin -- Python 3.11.5, pytest-7.4.0, pluggy-1.0.0 -- /Users/temp/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/temp/Documents/Projects/intuit-build-challenge-python
plugins: anyio-3.5.0
collected 24 items                                                                                                                       

assignment1/test_producer_consumer.py::test_queue_initial_size PASSED                                                              [  4%]
assignment1/test_producer_consumer.py::test_queue_put_and_get PASSED                                                               [  8%]
assignment1/test_producer_consumer.py::test_queue_reject_zero_size PASSED                                                          [ 12%]
assignment1/test_producer_consumer.py::test_queue_blocks_when_empty PASSED                                                         [ 16%]
assignment1/test_producer_consumer.py::test_queue_blocks_when_full PASSED                                                          [ 20%]
assignment1/test_producer_consumer.py::test_sentinel_is_unique_and_safe PASSED                                                     [ 25%]
assignment1/test_producer_consumer.py::test_producer_produces_items_and_sentinel PASSED                                            [ 29%]
assignment1/test_producer_consumer.py::test_producer_exception_still_sends_sentinel PASSED                                         [ 33%]
assignment1/test_producer_consumer.py::test_consumer_consumes_all_items PASSED                                                     [ 37%]
assignment1/test_producer_consumer.py::test_consumer_stops_on_sentinel PASSED                                                      [ 41%]
assignment1/test_producer_consumer.py::test_pipeline_simple_run PASSED                                                             [ 45%]
assignment1/test_producer_consumer.py::test_pipeline_with_none_values PASSED                                                       [ 50%]
assignment1/test_producer_consumer.py::test_large_pipeline PASSED                                                                  [ 54%]
assignment1/test_producer_consumer.py::test_pipeline_queue_capacity_stress PASSED                                                  [ 58%]
assignment2/test_sales_analysis.py::test_load_valid_records PASSED                                                                 [ 62%]
assignment2/test_sales_analysis.py::test_loader_skips_invalid_rows PASSED                                                          [ 66%]
assignment2/test_sales_analysis.py::test_total_revenue PASSED                                                                      [ 70%]
assignment2/test_sales_analysis.py::test_revenue_by_region PASSED                                                                  [ 75%]
assignment2/test_sales_analysis.py::test_units_sold_by_product PASSED                                                              [ 79%]
assignment2/test_sales_analysis.py::test_filter_sales_by_revenue PASSED                                                            [ 83%]
assignment2/test_sales_analysis.py::test_avg_unit_price PASSED                                                                     [ 87%]
assignment2/test_sales_analysis.py::test_sales_trend PASSED                                                                        [ 91%]
assignment2/test_sales_analysis.py::test_month_over_month PASSED                                                                   [ 95%]
assignment2/test_sales_analysis.py::test_run_query PASSED                                                                          [100%]

=========================================================== 24 passed in 0.25s ===========================================================

```

### 🏁 Summary


This Assignment 2 submission demonstrates:

- CSV ingestion with validation
- Immutable dataclasses and clean data modeling
- Functional transformations (reduce, map, filter)
- Declarative analytics pipeline
- Time-based grouping and trend analysis
- MoM percentage change calculation
- Flexible higher-order query execution
- Complete, robust unit test suite

