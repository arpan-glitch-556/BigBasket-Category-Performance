# Final Submission Checklist

Use this immediately before pushing the repository to GitHub.

## Already built and validated

- [x] `bigbasket_capstone.db` — 31 products, 50 customers, 500 orders, 6 category targets.
- [x] Status split — 434 Delivered, 42 Cancelled, 24 Pending.
- [x] `monthly_category_revenue.csv` — 36 rows, 434 Delivered orders, INR 88,282 total revenue.
- [x] SQL scripts cover the required foundations, joins/HAVING, LEFT JOIN zero-order case, CASE tiering, monthly report, and target variance logic.
- [x] Spreadsheet contains the exact monthly export, targets, category roll-up, XLOOKUP, variance, percentage variance, nested IF status, conditional formatting, and six Yes reconciliations.
- [x] Pandas notebook contains deduplication, text cleanup, missing-value handling, IQR capping, dates/derived fields, merge/groupby analysis, charts, and three structured insights.
- [x] SQL top category: Household Essentials.
- [x] SQL/Pandas top supplier: HomeEssentials Traders.
- [x] README, data story, AI log, Tableau guide, and full solution guide are included.

## Must be completed by the submitter

- [ ] Open `analysis.ipynb` and use **Run All** once on your machine/Colab.
- [ ] Run `python validate_submission.py` and review all PASS lines.
- [ ] If your grader insists on a native PivotTable object, create one in Excel/Google Sheets using `Monthly Data!A1:E37`: Rows = category; Values = SUM(total_revenue), SUM(order_count).
- [ ] Build/publish the Tableau Public dashboard using `TABLEAU_BUILD_GUIDE.md`.
- [ ] Confirm the Tableau link opens in an incognito/private window without login.
- [ ] Replace `PASTE_YOUR_PUBLIC_TABLEAU_URL_HERE` in `README.md` with the live URL.
- [ ] Run `python validate_submission.py` again. The Tableau URL check should now PASS.
- [ ] Push the final repository to GitHub and verify every required file is visible.
- [ ] Submit only the public GitHub repository link.
