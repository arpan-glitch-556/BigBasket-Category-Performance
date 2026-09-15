-- (a) INNER JOIN + GROUP BY + HAVING, Delivered orders only
SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    SUM(o.amount_inr) AS total_revenue,
    AVG(o.amount_inr) AS avg_revenue
FROM orders AS o
INNER JOIN products AS p
    ON p.product_id = o.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
HAVING SUM(o.amount_inr) > 10000
ORDER BY total_revenue DESC;

-- (b) LEFT JOIN: preserve products that received zero orders
-- COUNT(o.order_id), not COUNT(*), ensures the unmatched product returns 0.
SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS total_orders
FROM products AS p
LEFT JOIN orders AS o
    ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_orders ASC, p.product_id ASC;
