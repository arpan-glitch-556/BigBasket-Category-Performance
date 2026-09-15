# AI-Assisted Prompting Log

## Prompt 1 — SQL reporting query (RCTCF)

**Role:** Act as a senior SQL analyst reviewing SQLite reporting logic for a grocery category-performance diagnostic.

**Context:** I have four SQLite tables: `orders`, `products`, `customers`, and `category_targets`. Only Delivered orders count toward revenue. I need category-level revenue compared with fixed category targets, and SQLite integer division must not truncate the percentage variance.

**Task:** Draft a query that calculates each category's Delivered revenue, target revenue, variance (`target - actual`), percentage variance (`(actual - target) * 100 / target`), and a three-way status: Above Target; Below Target - Watch when shortfall is within 15%; otherwise Below Target - Critical.

**Constraints:** SQLite syntax only; join to `category_targets`; do not count Cancelled or Pending revenue; force floating-point percentage calculation; return one row per category.

**Format:** Return one runnable SQL query with a CTE and readable aliases, followed by a short explanation of the tier logic.

**Verification evidence produced during project build:** The retained query was run against `bigbasket_capstone.db` and all six category totals were checked against an independent Delivered-only `GROUP BY category` query; the results were Household Essentials 21715, Personal Care 16382, Bakery 15410, Dairy & Eggs 14090, Snacks & Beverages 10895, and Fruits & Vegetables 9790, with a grand total of 88282.

## Prompt 2 — Pandas IQR capping (RCTCF)

**Role:** Act as a senior Python/Pandas data analyst reviewing an outlier-treatment step.

**Context:** My raw order export has duplicates, missing `amount_inr`, and injected extreme revenue values. Revenue analysis should use only Delivered rows with non-null revenue. The project requires IQR-based upper-fence capping rather than dropping outliers.

**Task:** Show concise Pandas code to calculate Q1, Q3, IQR, and the upper fence on Delivered non-null `amount_inr`, then cap only those Delivered values above the upper fence using `.clip()` while preserving missing values.

**Constraints:** Do not impute missing revenue; do not remove rows for being outliers; compute the IQR only on Delivered, non-null revenue; retain an auditable capped revenue column.

**Format:** Return a short code snippet plus one sentence explaining why `.clip(upper=...)` meets the requirement.

**Verification evidence produced during project build:** The capping logic was re-run on the generated `orders_raw.csv`; Q1 was 90.0, Q3 was 275.0, the upper fence was 552.5, exactly 16 Delivered non-null rows exceeded the fence, and manual checks confirmed capped values equal 552.5 while non-outlier and missing values remain unchanged.


## Final submitter verification

Before submission, run `python validate_submission.py` and `Run All` in `analysis.ipynb`. This ensures the submitter has personally checked the reproducible evidence rather than relying only on generated text. After doing so, you may accurately describe those checks as personally performed if your course requires that wording.
