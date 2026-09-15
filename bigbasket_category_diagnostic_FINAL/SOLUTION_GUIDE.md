# Step-by-Step Solution Guide

This guide explains exactly how to run and verify the project package.

## Prerequisites

Install Python 3.10+ and then:

```bash
python -m pip install pandas matplotlib jupyter
```

SQLite is built into Python through `sqlite3`. Tableau Public is free and is only needed for the final hosted dashboard.

## Step 1 — Generate the deterministic dataset

From the repository root:

```bash
python generate_data.py
```

This creates:
- `bigbasket_capstone.db`
- `orders_raw.csv`
- `products.csv`

Do not edit the seed or lists in `generate_data.py`.

Expected database counts:
- products: 31
- customers: 50
- orders: 500
- category_targets: 6
- Delivered: 434
- Cancelled: 42
- Pending: 24

## Step 2 — Run SQL verification and tasks

You can use Python's SQLite shell equivalent or any SQLite client. Example with Python:

```bash
python -c "import sqlite3; c=sqlite3.connect('bigbasket_capstone.db'); print(c.execute('SELECT COUNT(*) FROM orders').fetchone())"
```

Run the files in this order:
1. `verify.sql`
2. `01_foundations.sql`
3. `02_aggregation_joins.sql`
4. `03_reporting.sql`

Critical checks:
- `Premium Face Cream 50g` must appear with 0 orders in the LEFT JOIN output.
- Monthly category report has 36 rows.
- Total revenue across those 36 rows is INR 88,282.

## Step 3 — Monthly export

`monthly_category_revenue.csv` is already included as the direct unedited output of Part 1's monthly report. Do not manually edit it.

Expected category totals:

| Category | Revenue |
|---|---:|
| Household Essentials | 21,715 |
| Personal Care | 16,382 |
| Bakery | 15,410 |
| Dairy & Eggs | 14,090 |
| Snacks & Beverages | 10,895 |
| Fruits & Vegetables | 9,790 |

Grand total: **88,282**.

## Step 4 — Spreadsheet

Open `bigbasket_category_crosscheck.xlsx`.

Sheets:
- `Monthly Data`: exact 36-row CSV import.
- `Category Targets`: fixed six-category target table.
- `Pivot Table`: formula-driven category roll-up from Monthly Data, including SUM of revenue and order_count.
- `Category Summary`: references the Pivot Table, uses XLOOKUP for target, formulas for variance/percentage variance, nested IF for status, and conditional formatting.

Every row in `Matches Part 1 SQL total?` should show `Yes` when calculated in Excel/Google Sheets.

If your grader specifically requires an Insert → PivotTable object rather than the included formula-driven pivot output, select `Monthly Data!A1:E37` in Excel/Google Sheets and insert a Pivot Table with:
- Rows: category
- Values: SUM total_revenue; SUM order_count
Then keep the same category order or update the Summary references accordingly. The underlying totals are identical.

## Step 5 — Tableau Public

Follow `TABLEAU_BUILD_GUIDE.md`. The expected KPIs are:
- Total Revenue: INR 88,282
- Total Delivered Orders: 434
- Average Order Value: INR 203.41
- Categories Meeting Target: 3 of 6

After publishing, paste your public Tableau URL into `README.md` where indicated.

## Step 6 — Python notebook

Launch:

```bash
jupyter notebook analysis.ipynb
```

Run All cells from top to bottom.

Expected key results:
- Raw rows: 508
- Duplicate rows removed: 8
- Clean rows after de-duplication: 500
- Missing `amount_inr`: 10
- Q1: 90.0
- Q3: 275.0
- Upper fence: 552.5
- Delivered rows capped: 16
- Top category: Household Essentials, INR 20,910 after Part 4 cleaning/capping
- Top supplier: HomeEssentials Traders, INR 20,910
- Cleaned/capped Delivered revenue: INR 84,637

## Step 7 — AI log and data story

- `ai_log.md` contains exactly two RCTCF prompts with concrete verification steps.
- `DATA_STORY.md` states every category's target status and contains exactly two recommendations.

## Step 8 — GitHub submission

Create a public repository and commit all files in this folder. Example:

```bash
git init
git add .
git commit -m "Complete BigBasket category performance diagnostic"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Before submitting, open the GitHub repo in an incognito browser and verify files are accessible, then verify the Tableau Public link loads without requiring viewer login.
