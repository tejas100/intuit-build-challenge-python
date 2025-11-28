import csv
import logging
from dataclasses import dataclass
from functools import reduce
from typing import List, Dict, Callable, Any, Tuple


# ---------------------------------------------------------
# Data Model
# ---------------------------------------------------------
@dataclass(frozen=True)
class SaleRecord:
    date: str
    region: str
    product: str
    units_sold: int
    unit_price: float

    @property
    def revenue(self) -> float:
        return self.units_sold * self.unit_price


class SalesAnalysis:
    REQUIRED_FIELDS = {"date", "region", "product", "units_sold", "unit_price"}

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data: List[SaleRecord] = self._load_csv()

    # CSV Loader 
    def _load_csv(self) -> List[SaleRecord]:
        records = []

        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)

            for idx, row in enumerate(reader, start=2):
                try:
                    if all(not (v or "").strip() for v in row.values()):
                        logging.warning(f"Skipping empty row at line {idx}")
                        continue

                    if not self.REQUIRED_FIELDS.issubset(row.keys()):
                        logging.warning(f"Invalid row at line {idx}: Missing columns → {row}")
                        continue

                    if not row["product"]:
                        logging.warning(f"Skipping row (missing product) at line {idx}: {row}")
                        continue

                    if not row["region"]:
                        logging.warning(f"Skipping row (missing region) at line {idx}: {row}")
                        continue

                    try:
                        units = int(row["units_sold"])
                        price = float(row["unit_price"])
                    except Exception:
                        logging.warning(f"Invalid numeric value at line {idx}: {row}")
                        continue

                    if units < 0:
                        logging.warning(f"Negative units_sold at line {idx}: {row}")
                        continue

                    if price <= 0:
                        logging.warning(f"Invalid or missing unit_price at line {idx}: {row}")
                        continue

                    record = SaleRecord(
                        date=row["date"],
                        region=row["region"],
                        product=row["product"],
                        units_sold=units,
                        unit_price=price,
                    )
                    records.append(record)

                except Exception as e:
                    logging.warning(f"Unexpected error at line {idx}: {row} → {e}")

        return records

    # ---------------------------------------------------------
    # 1. Total revenue 
    # ---------------------------------------------------------
    def total_revenue(self) -> float:
        return reduce(lambda acc, r: acc + r.revenue, self.data, 0.0)

    # ---------------------------------------------------------
    # 2. Revenue by region 
    # ---------------------------------------------------------
    def revenue_by_region(self) -> Dict[str, float]:
        def reducer(acc: Dict[str, float], r: SaleRecord) -> Dict[str, float]:
            acc[r.region] = acc.get(r.region, 0.0) + r.revenue
            return acc
        return reduce(reducer, self.data, {})

    # ---------------------------------------------------------
    # 3. Units sold by product 
    # ---------------------------------------------------------
    def units_sold_by_product(self) -> Dict[str, int]:
        def reducer(acc: Dict[str, int], r: SaleRecord) -> Dict[str, int]:
            acc[r.product] = acc.get(r.product, 0) + r.units_sold
            return acc
        return reduce(reducer, self.data, {})

    # ---------------------------------------------------------
    # 4. Filter sales by revenue threshold 
    # ---------------------------------------------------------
    def filter_sales_by_revenue(self, threshold: float) -> List[SaleRecord]:
        return list(filter(lambda r: r.revenue >= threshold, self.data))

    # ---------------------------------------------------------
    # 5. Average unit price per product 
    # ---------------------------------------------------------
    def avg_unit_price_by_product(self) -> Dict[str, float]:
        def reducer(acc: Dict[str, Tuple[float, int]], r: SaleRecord):
            total, cnt = acc.get(r.product, (0.0, 0))
            acc[r.product] = (total + r.unit_price, cnt + 1)
            return acc

        sums_counts = reduce(reducer, self.data, {})

        return {
            product: total / count
            for product, (total, count) in sums_counts.items()
            if count > 0
        }

    # ---------------------------------------------------------
    # 6. Custom Higher-Order Query Executor
    # ---------------------------------------------------------
    def run_query(self, query_fn: Callable[[List[SaleRecord]], Any]):
        return query_fn(self.data)

    # ---------------------------------------------------------
    # 7. sales trend grouped by (year, month) 
    # ---------------------------------------------------------
    def sales_trend(self) -> Dict[Tuple[int, int], float]:
        def extract_year_month(record: SaleRecord):
            try:
                year, month, _ = record.date.split("-")
                return int(year), int(month)
            except Exception:
                return None

        def reducer(acc: Dict[Tuple[int, int], float], r: SaleRecord):
            ym = extract_year_month(r)
            if ym is None:
                return acc
            acc[ym] = acc.get(ym, 0.0) + r.revenue
            return acc

        return reduce(reducer, self.data, {})

    # ---------------------------------------------------------
    # 8. month-over-month % change 
    # ---------------------------------------------------------
    def month_over_month(self, trend: Dict[Tuple[int, int], float]) -> Dict[Tuple[int, int], float]:
        if not trend:
            return {}

        keys = sorted(trend.keys())
        consecutive_pairs = zip(keys[1:], keys[:-1])  # (curr, prev)

        def compute_change(pair):
            curr, prev = pair
            prev_val = trend[prev]
            if prev_val == 0:
                return None
            pct = ((trend[curr] - prev_val) / prev_val) * 100.0
            return (curr, pct)

        return dict(filter(None, map(compute_change, consecutive_pairs)))


# ---------------------------------------------------------
# Logging 
# ---------------------------------------------------------

def print_section(title: str):
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)

def print_dict_table(data: Dict[Any, Any], key_header="Key", value_header="Value"):
    print(f"{key_header:<20} | {value_header}")
    print("-" * 60)
    for k, v in data.items():
        print(f"{str(k):<20} | {v}")

def print_sales_list(records: List[SaleRecord]):
    print(f"{'Date':<12} {'Region':<10} {'Product':<12} {'Units':<8} {'Price':<10} {'Revenue'}")
    print("-" * 70)
    for r in records:
        print(f"{r.date:<12} {r.region:<10} {r.product:<12} "
              f"{r.units_sold:<8} ${r.unit_price:<9.2f} ${r.revenue:.2f}")

def print_single_sale(record: SaleRecord):
    print(f"{'Field':<15} | Value")
    print("-" * 40)
    print(f"{'Date':<15} | {record.date}")
    print(f"{'Region':<15} | {record.region}")
    print(f"{'Product':<15} | {record.product}")
    print(f"{'Units Sold':<15} | {record.units_sold}")
    print(f"{'Unit Price':<15} | ${record.unit_price:,.2f}")
    print(f"{'Revenue':<15} | ${record.revenue:,.2f}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="[WARN] %(message)s")

    analysis = SalesAnalysis("data/sales_small.csv")

    print_section("SALES ANALYSIS REPORT")

    print_section("1. Total Revenue")
    print(f"${analysis.total_revenue():,.2f}")

    print_section("2. Revenue by Region")
    print_dict_table(analysis.revenue_by_region(), "Region", "Revenue ($)")
    
    print_section("3. Units Sold by Product")
    print_dict_table(analysis.units_sold_by_product(), "Product", "Units Sold")

    print_section("4. High Revenue Sales (>= $500)")
    high_rev = analysis.filter_sales_by_revenue(500)
    print_sales_list(high_rev)

    print_section("5. Average Unit Price by Product")
    avg_prices = {k: f"${v:,.2f}" for k, v in analysis.avg_unit_price_by_product().items()}
    print_dict_table(avg_prices, "Product", "Avg Price")

    print_section("6. Sales Trend (Revenue by Month)")
    trend = analysis.sales_trend()
    trend_fmt = {f"{y}-{m:02d}": f"${v:,.2f}" for (y, m), v in trend.items()}
    print_dict_table(trend_fmt, "Month", "Revenue")

    print_section("7. Month-Over-Month Change (%)")
    mom = analysis.month_over_month(trend)
    mom_fmt = {f"{y}-{m:02d}": f"{v:.2f}%" for (y, m), v in mom.items()}
    print_dict_table(mom_fmt, "Month", "% Change")

    print_section("8. Top Revenue Item")
    top_item = analysis.run_query(lambda rows: max(rows, key=lambda r: r.revenue))
    print_single_sale(top_item)

    


