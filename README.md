# Intuit SWE I Build Challenge - Python Solution

[![Language](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[![Pattern](https://img.shields.io/badge/Pattern-Producer%20Consumer-orange.svg)]()



> This repo includes a complete, end-to-end solution to the Intuit Build Challenge, implemented using clean Python. 

---
## 📖 Prerequisites
### 1. Clone the repo

```bash
git clone https://github.com/tejas100/intuit-build-challenge-python
cd intuit-build-challenge-python
```

### 2. Create a virtual env & install `requirements.txt`

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
# .venv\Scripts\activate    # Windows PowerShell

pip install -r requirements.txt
```
### 3. The folder structure should look like this

```bash
intuit-build-challenge-python/
│
├── assignment1/
│   ├── producer_consumer.py           # Assignment 1 implementation
│   ├── test_producer_consumer.py      # Unit tests for Assignment 1
│   ├── README.md                      # Documentation for Assignment 1
│   └── __init__.py
│
├── assignment2/
│   ├── sales_analysis.py              # Assignment 2 implementation
│   ├── test_sales_analysis.py         # Unit tests for Assignment 2
│   ├── data/                          # CSV files for analysis
│   │   ├── sales_large.csv
│   │   └── sales_small.csv
│   ├── README.md                      # Documentation for Assignment 2
│   └── __init__.py
│
├── README.md                          # Root project README
├── requirements.txt                   # Python dependencies
└── .gitignore                         # Git ignore rules

```
## Assignment 1: Producer-Consumer Pattern 
> **Assignment 1:** Implement a producer-consumer pattern with thread synchronization, blocking queues, and a robust wait/notify mechanism.
## 📖 Overview

This project implements a thread-safe **Producer-Consumer pipeline** without relying on Python's high-level `queue.Queue`. Instead, it demonstrates a deep understanding of concurrency by manually implementing a **Monitor Object pattern** using `threading.Condition`, `threading.Lock`, and `wait()`/`notify()` semantics.

The system simulates concurrent data transfer where a Producer thread reads from a source and safely pushes to a bounded buffer, while a Consumer thread retrieves and processes data, ensuring zero race conditions or deadlocks.

### Project Structure

```bash
assignment1/
│
├── producer_consumer.py     # Main implementation
├── test_producer_consumer.py # Unit tests
└── README.md                # This file
```
## 🧠 Design Overview

<table style="border-collapse: collapse; width: 100%;">

  <!-- Header Row -->
  <tr>
    <th style="border:1px solid #ccc; padding:10px; background:#f8f8f8;">Component</th>
    <th style="border:1px solid #ccc; padding:10px; background:#f8f8f8;">Description</th>
  </tr>

  <!-- BlockingQueue -->
  <tr>
    <td style="border:1px solid #ccc; padding:10px;"><b>1. BlockingQueue&lt;T&gt;</b><br>(Custom Bounded Blocking Queue)</td>
    <td style="border:1px solid #ccc; padding:10px;">
      Generic FIFO queue implemented manually to demonstrate concurrency.<br><br>
      <b>Purpose:</b> Show mastery of <code>threading.Lock</code>, <code>Condition</code>, wait/notify, and bounded buffering.<br><br>
      <b>Key Behaviors:</b>
      <ul>
        <li>Fixed max size (bounded)</li>
        <li><code>put()</code>: blocks when full → notifies consumer</li>
        <li><code>get()</code>: blocks when empty → notifies producer</li>
        <li>Thread-safe for multiple producers/consumers</li>
      </ul>
      <b>Internal Details:</b>
      <ul>
        <li>Stores items in <code>deque</code> (O(1) ops)</li>
        <li>One shared lock + two conditions: <code>not_full</code> & <code>not_empty</code></li>
        <li>Uses <code>while</code> loops for <code>wait()</code> (prevents spurious wakeups)</li>
      </ul>
      <b>Why not use <code>queue.Queue</code>?</b><br>
      Challenge requires manual synchronization → custom implementation used.
    </td>
  </tr>

  <!-- Producer -->
  <tr>
    <td style="border:1px solid #ccc; padding:10px;"><b>2. Producer Thread</b></td>
    <td style="border:1px solid #ccc; padding:10px;">
      Reads items from a source list and enqueues them.<br><br>
      <b>Key Features:</b>
      <ul>
        <li>Calls <code>queue.put()</code> for each element</li>
        <li>Logs activity</li>
        <li>Uses <code>try/finally</code> to guarantee sentinel delivery</li>
      </ul>
      <b>Shutdown:</b> Always pushes a unique sentinel to signal completion.
    </td>
  </tr>

  <!-- Consumer -->
  <tr>
    <td style="border:1px solid #ccc; padding:10px;"><b>3. Consumer Thread</b></td>
    <td style="border:1px solid #ccc; padding:10px;">
      Continuously dequeues and stores items.<br><br>
      <b>Key Features:</b>
      <ul>
        <li>Looping <code>queue.get()</code> calls</li>
        <li>Stops only when sentinel is received</li>
        <li>Appends non-sentinel items to destination</li>
        <li>Logs consumption</li>
      </ul>
      <b>Graceful Shutdown:</b> No busy waiting, no flags — sentinel triggers clean exit.
    </td>
  </tr>

  <!-- Pipeline -->
  <tr>
    <td style="border:1px solid #ccc; padding:10px;"><b>4. Pipeline Orchestration<br>(run_pipeline)</b></td>
    <td style="border:1px solid #ccc; padding:10px;">
      Coordinates producer-consumer execution.<br><br>
      <b>Flow:</b><br>
      Source → Producer → BlockingQueue → Consumer → Destination<br><br>
      <b>Responsibilities:</b>
      <ul>
        <li>Create queue + destination list</li>
        <li>Start Producer & Consumer threads</li>
        <li>Join threads</li>
        <li>Measure runtime and return results</li>
      </ul>
    </td>
  </tr>

  <!-- Sentinel -->
  <tr>
    <td style="border:1px solid #ccc; padding:10px;"><b>5. Sentinel Design</b></td>
    <td style="border:1px solid #ccc; padding:10px;">
      Uses a unique object (<code>SENTINEL = object()</code>) to signal termination.<br><br>
      <b>Benefits:</b>
      <ul>
        <li>Guaranteed unique (identity-based)</li>
        <li>Avoids collisions with real data (even <code>None</code>)</li>
        <li>Simple, safe, and explicit shutdown mechanism</li>
      </ul>
    </td>
  </tr>

</table>

## ▶️ Running assignment1

### Run the script

```bash
cd intuit-build-challenge-python/assignment1
python producer_consumer.py
```
### Sample Output from `assignment1`

```bash
[Producer] Produced: 1 | Queue size: 1
[Consumer] Consumed: 1 | Queue size: 0
[Producer] Produced: 2 | Queue size: 1
[Consumer] Consumed: 2 | Queue size: 0
[Producer] Produced: None | Queue size: 1
[Consumer] Consumed: None | Queue size: 0
[Producer] Produced: 4 | Queue size: 1
[Consumer] Consumed: 4 | Queue size: 0
[Producer] Sentinel sent.
[Consumer] Received sentinel. Exiting.

=== Pipeline Summary ===
Produced:  4 items
Consumed:  4 items
Time:      0.0002s
```



## Assignment 2: CSV Sales Data Analysis
> **Assignment 2:** Perform data analysis on CSV sales data using functional programming, stream-style transformations, and higher-order operations.
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

### 1. Selecting the right csv `(large / small)`
Please select your csv file under the `__main__` funtion as shown below
```bash
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="[WARN] %(message)s")
    
    analysis = SalesAnalysis("data/sales_small.csv") # Please select your CSV file here (small or large)
    # analysis = SalesAnalysis("data/sales_large.csv") 

```
### 2. Run the script

```bash
cd intuit-build-challenge-python/assignment2
python sales_analysis.py
```
### Sample Output from `assignment2`
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

## ▶️ Running the test on both assignment1 and assignment2
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

### 🏁 Project Summary


This repository contains my full solution to the Intuit Build Challenge for SWE I, covering both concurrency (Assignment 1) and functional data analytics (Assignment 2). The project demonstrates clean architecture, robust error handling, and complete test coverage across two assignment.

- Correct use of thread synchronization, `Lock`, and `Condition`
- A fully custom bounded blocking queue (Monitor pattern)
- Clean Producer–Consumer pipeline with shutdown
- Immutable dataclasses & validated CSV ingestion
- Functional transformations using reduce / map / filter
- Declarative analytics: grouping, trends, MoM %, and higher-order queries
- Flexible higher-order query execution
- Comprehensive, edge-case-focused pytest test suites
