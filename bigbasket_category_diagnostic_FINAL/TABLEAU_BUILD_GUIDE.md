# Tableau Public Build Guide

Use **only `monthly_category_revenue.csv`** as the Tableau data source. The source has 36 rows and INR 88,282 total Delivered revenue.

## 1. Connect and set field roles
- Open Tableau Public → Connect → Text file → `monthly_category_revenue.csv`.
- `category`: Dimension / String.
- `month`: Dimension. For easiest Jan–Jun ordering, create `Month Date`:
  ```
  DATE([month] + '-01')
  ```
- `order_count`: Number (Whole).
- `total_revenue`: Number (Whole), currency INR if desired.
- `avg_revenue`: Number (Decimal).

## 2. Calculated fields

### Category Target
```
CASE [category]
WHEN 'Fruits & Vegetables' THEN 12000
WHEN 'Dairy & Eggs' THEN 16500
WHEN 'Snacks & Beverages' THEN 13000
WHEN 'Personal Care' THEN 15500
WHEN 'Household Essentials' THEN 17000
WHEN 'Bakery' THEN 12000
END
```

### Category Revenue (LOD)
```
{ FIXED [category] : SUM([total_revenue]) }
```

### Target Status
```
IF [Category Revenue (LOD)] >= [Category Target] THEN 'Above Target'
ELSEIF ([Category Target] - [Category Revenue (LOD)]) / [Category Target] <= 0.15 THEN 'Below Target - Watch'
ELSE 'Below Target - Critical'
END
```

### Average Order Value
```
SUM([total_revenue]) / SUM([order_count])
```
Expected overall AOV = **203.4147465** (88282 / 434), so display approximately **INR 203.41**.

### Category Meets Target Flag
```
IF [Category Revenue (LOD)] >= [Category Target] THEN 1 ELSE 0 END
```

### Categories Meeting Target
Use `SUM({ FIXED [category] : MIN([Category Meets Target Flag]) })` or create a category-level sheet and display the count. Expected = **3 of 6**.

## 3. Required worksheets

### Monthly Revenue Trend
- Columns: `Month Date` (continuous Month).
- Rows: `SUM(total_revenue)`.
- Marks: Line.
- Title: **Monthly Delivered Revenue — Jan to Jun 2026**.

### Category Revenue by Target Status
- Rows: `category`.
- Columns: `SUM(total_revenue)`.
- Sort descending by SUM(total_revenue).
- Color: `Target Status`.
- Show labels.
- Expected descending order: Household Essentials, Personal Care, Bakery, Dairy & Eggs, Snacks & Beverages, Fruits & Vegetables.

### KPI — Total Revenue
- Text: `SUM(total_revenue)` → **INR 88,282**.

### KPI — Total Delivered Orders
- Text: `SUM(order_count)` → **434**.

### KPI — Average Order Value
- Text: calculated `Average Order Value` → **INR 203.41**.

### KPI — Categories Meeting Target
- Text → **3 of 6**.

## 4. Dashboard
- New Dashboard, desktop size around 1200×800.
- Use floating layout as required.
- KPI cards across the top.
- Monthly trend and category bars below.
- Add `category` as a visible filter and choose **Apply to Worksheets → All Using This Data Source** so it affects every worksheet.
- Keep the Target Status legend visible.
- Use consistent fonts and three distinct status colors. No dollar signs.

## 5. Publish
- Save to Tableau Public.
- Verify the view opens in a private/incognito browser without login.
- Copy the live URL and replace the placeholder in `README.md`.

The live Tableau URL cannot be created locally because publishing requires signing into the submitter's Tableau Public account. Everything else needed to build and verify the dashboard is included here.
