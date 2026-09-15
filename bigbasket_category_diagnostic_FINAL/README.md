# BigBasket Category Performance Diagnostic

## Project Overview

This project analyzes BigBasket-style category performance using a connected workflow across SQLite, Excel, and Python/Pandas. A deterministic dataset is generated and analyzed in SQL, the resulting monthly category revenue export is reconciled in Excel, and a separate raw order export is independently cleaned and analyzed in Pandas.

The SQL benchmark contains **434 Delivered orders** with total Delivered revenue of **INR 88,282**.

## Key Results

| Category | Delivered Revenue (INR) | Target (INR) | Difference vs Target | Status |
|---|---:|---:|---:|---|
| Household Essentials | 21,715 | 17,000 | +4,715 | Above Target |
| Personal Care | 16,382 | 15,500 | +882 | Above Target |
| Bakery | 15,410 | 12,000 | +3,410 | Above Target |
| Dairy & Eggs | 14,090 | 16,500 | -2,410 | Below Target - Watch |
| Snacks & Beverages | 10,895 | 13,000 | -2,105 | Below Target - Critical |
| Fruits & Vegetables | 9,790 | 12,000 | -2,210 | Below Target - Critical |

**Total Delivered Revenue:** INR 88,282  
**Delivered Orders:** 434  
**Average Order Value:** INR 203.41  
**Categories Meeting Target:** 3 of 6

## Repository Structure

```text
.
├── generate_data.py
├── bigbasket_capstone.db
├── orders_raw.csv
├── products.csv
├── monthly_category_revenue.csv
├── verify.sql
├── 01_foundations.sql
├── 02_aggregation_joins.sql
├── 03_reporting.sql
├── bigbasket_category_crosscheck.xlsx
├── analysis.ipynb
├── ai_log.md
├── DATA_STORY.md
├── requirements.txt
└── README.md
```

## Part 1 — SQL Data Setup and Diagnostic

The deterministic database and raw exports are generated using:

```bash
python generate_data.py
```

The generated SQLite database contains:

- 31 products
- 50 customers
- 500 orders
- 6 category targets
- 434 Delivered orders
- 42 Cancelled orders
- 24 Pending orders

SQL files:

- [`verify.sql`](verify.sql) — verification queries
- [`01_foundations.sql`](01_foundations.sql) — foundational filtering, sorting, aliases, range and NULL queries
- [`02_aggregation_joins.sql`](02_aggregation_joins.sql) — aggregations, INNER JOIN, LEFT JOIN and HAVING
- [`03_reporting.sql`](03_reporting.sql) — product tiering, monthly category report and target variance analysis

The reporting export [`monthly_category_revenue.csv`](monthly_category_revenue.csv) contains **36 rows** and a Delivered-revenue grand total of **INR 88,282**.

## Part 2 — Spreadsheet Cross-Check

The workbook [`bigbasket_category_crosscheck.xlsx`](bigbasket_category_crosscheck.xlsx) contains:

- **Monthly Data** — the exact SQL export
- **Category Targets** — the six fixed target values
- **Pivot Table** — category revenue and Delivered-order summary
- **Category Summary** — target lookup, variance, percentage variance, status classification and SQL reconciliation
- **Native Pivot** — native PivotTable with category in Rows and SUM of total_revenue / SUM of order_count in Values

All six category revenue totals reconcile with the SQL benchmark to the rupee.

## Data Story

See [`DATA_STORY.md`](DATA_STORY.md) for the category-level interpretation and recommendations based on the computed results.

## Part 4 — Python/Pandas Cleaning and Cross-Validation

The notebook [`analysis.ipynb`](analysis.ipynb) performs the raw-data cleaning and analysis.

Key audit results:

- Raw rows: 508
- Duplicate rows removed: 8
- Rows after deduplication: 500
- Missing `amount_inr` rows: 10
- IQR Q1: 90.0
- IQR Q3: 275.0
- Upper fence: 552.5
- Delivered rows capped: 16
- Cleaned/capped Delivered revenue: INR 84,637
- Top category: **Household Essentials** — INR 20,910
- Top supplier: **HomeEssentials Traders** — INR 20,910

The Pandas analysis independently confirms the same top category and top supplier as the SQL diagnostic.

## AI-Assisted Prompting Log

See [`ai_log.md`](ai_log.md). It contains two RCTCF-structured prompts:

1. SQL query assistance and verification
2. Pandas cleaning/analysis assistance and verification

## Visualization

The repository contains the complete source data and category-performance results used for visualization. A Tableau Public dashboard link is not included in this repository.

## How to Review the Project

1. Run `generate_data.py` to reproduce the deterministic database and raw exports.
2. Review the SQL scripts in sequence.
3. Open `bigbasket_category_crosscheck.xlsx` and verify the PivotTable and reconciliation.
4. Open `analysis.ipynb` and run all cells.
5. Review `DATA_STORY.md` and `ai_log.md`.

## Submission

This repository is designed to be submitted as a single public GitHub repository containing the database, SQL scripts, CSV exports, workbook, Jupyter notebook, data story, AI log and README.
