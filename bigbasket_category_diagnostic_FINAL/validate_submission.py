from pathlib import Path
import csv, json, re, sqlite3, sys

ROOT = Path(__file__).resolve().parent
fails = []
passes = []

def check(label, condition, detail=''):
    (passes if condition else fails).append((label, detail))
    print(f"{'PASS' if condition else 'FAIL'}: {label}" + (f" — {detail}" if detail else ''))

# Required files
required = [
    'generate_data.py','bigbasket_capstone.db','orders_raw.csv','products.csv','verify.sql',
    '01_foundations.sql','02_aggregation_joins.sql','03_reporting.sql',
    'monthly_category_revenue.csv','bigbasket_category_crosscheck.xlsx','analysis.ipynb',
    'ai_log.md','DATA_STORY.md','README.md'
]
for name in required:
    check(f'Required file: {name}', (ROOT/name).exists())

# Database checks
conn = sqlite3.connect(ROOT/'bigbasket_capstone.db')
cur = conn.cursor()
expected_counts = {'products':31,'customers':50,'orders':500,'category_targets':6}
for table, expected in expected_counts.items():
    actual = cur.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    check(f'{table} row count', actual == expected, f'actual={actual}, expected={expected}')

status = dict(cur.execute('SELECT status, COUNT(*) FROM orders GROUP BY status').fetchall())
check('Order status split', status == {'Delivered':434,'Cancelled':42,'Pending':24}, str(status))

cat_rows = cur.execute('''
SELECT p.category, SUM(o.amount_inr)
FROM orders o JOIN products p ON p.product_id=o.product_id
WHERE o.status='Delivered'
GROUP BY p.category
''').fetchall()
cat = dict(cat_rows)
expected_cat = {
    'Household Essentials':21715,'Personal Care':16382,'Bakery':15410,
    'Dairy & Eggs':14090,'Snacks & Beverages':10895,'Fruits & Vegetables':9790
}
check('Delivered category totals', cat == expected_cat, str(cat))
check('SQL grand total revenue', sum(cat.values()) == 88282, f'actual={sum(cat.values())}')

zero = cur.execute('''
SELECT p.product_name, COUNT(o.order_id)
FROM products p LEFT JOIN orders o ON o.product_id=p.product_id
GROUP BY p.product_id, p.product_name
HAVING COUNT(o.order_id)=0
''').fetchall()
check('Exactly one zero-order product', zero == [('Premium Face Cream 50g',0)], str(zero))

top_supplier = cur.execute('''
SELECT p.supplier, SUM(o.amount_inr) rev
FROM orders o JOIN products p ON p.product_id=o.product_id
WHERE o.status='Delivered'
GROUP BY p.supplier ORDER BY rev DESC LIMIT 1
''').fetchone()
check('Top SQL supplier', top_supplier == ('HomeEssentials Traders',21715), str(top_supplier))
conn.close()

# CSV checks
with open(ROOT/'monthly_category_revenue.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
check('Monthly CSV columns', list(rows[0].keys()) == ['category','month','order_count','total_revenue','avg_revenue'])
check('Monthly CSV has 36 rows', len(rows)==36, f'actual={len(rows)}')
check('Monthly CSV total revenue', sum(int(r['total_revenue']) for r in rows)==88282)
check('Monthly CSV delivered orders', sum(int(r['order_count']) for r in rows)==434)

with open(ROOT/'orders_raw.csv', newline='', encoding='utf-8') as f:
    raw = list(csv.DictReader(f))
check('Raw CSV has 508 rows', len(raw)==508, f'actual={len(raw)}')
check('Raw order IDs dedupe to 500', len({r['order_id'] for r in raw})==500)
check('Raw missing amount count = 10', sum(1 for r in raw if r['amount_inr']=='')==10)

# SQL script content checks
f1=(ROOT/'01_foundations.sql').read_text(encoding='utf-8').upper()
for label, pattern in [
    ('WHERE', r'\bWHERE\b'), ('DISTINCT', r'\bDISTINCT\b'), ('ORDER BY', r'ORDER\s+BY'),
    ('LIMIT', r'\bLIMIT\s+\d+'), ('AS', r'\bAS\b'), ('IN', r'\bIN\s*\('),
    ('BETWEEN', r'\bBETWEEN\b'), ('NOT BETWEEN', r'NOT\s+BETWEEN'), ('IS NULL', r'IS\s+NULL')
]:
    check(f'01_foundations contains {label}', re.search(pattern, f1) is not None)

f2=(ROOT/'02_aggregation_joins.sql').read_text(encoding='utf-8').upper()
for token in ['INNER JOIN','HAVING','LEFT JOIN','COUNT(O.ORDER_ID)']:
    check(f'02_aggregation_joins contains {token}', token in f2)

f3=(ROOT/'03_reporting.sql').read_text(encoding='utf-8').upper()
for token in ['CASE','STRFTIME','CATEGORY_TARGETS','100.0','BELOW TARGET - WATCH','BELOW TARGET - CRITICAL']:
    check(f'03_reporting contains {token}', token in f3)

# Notebook structural/content checks
nb=json.loads((ROOT/'analysis.ipynb').read_text(encoding='utf-8'))
all_text='\n'.join(''.join(c.get('source',[])) for c in nb.get('cells',[]))
for token in ['drop_duplicates','str.strip','str.title','quantile','clip','pd.to_datetime','groupby','pd.merge','matplotlib']:
    check(f'Notebook contains {token}', token.lower() in all_text.lower())
check('Notebook states Household Essentials', 'Household Essentials' in all_text)
check('Notebook states HomeEssentials Traders', 'HomeEssentials Traders' in all_text)

# README/dashboard link status
readme=(ROOT/'README.md').read_text(encoding='utf-8')
placeholder='PASTE_YOUR_PUBLIC_TABLEAU_URL_HERE' in readme
check('Tableau Public URL replaced', not placeholder, 'Still requires manual publishing to your Tableau Public account.' if placeholder else '')

print('\nSUMMARY')
print(f'Passed: {len(passes)}')
print(f'Failed: {len(fails)}')
if fails:
    print('\nRemaining items:')
    for label, detail in fails:
        print(f'- {label}' + (f': {detail}' if detail else ''))
    sys.exit(1)
print('All automated checks passed.')
