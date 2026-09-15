-- 1. SELECT / WHERE: Delivered orders placed by customers in Bengaluru
SELECT o.order_id, c.name AS customer_name, c.city, o.order_date, o.amount_inr, o.status
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.city = 'Bengaluru' AND o.status = 'Delivered'
ORDER BY o.order_date, o.order_id;

-- 2. DISTINCT: every distinct product category
SELECT DISTINCT category
FROM products
ORDER BY category;

-- 3. ORDER BY + LIMIT: five highest-value orders
SELECT order_id, customer_id, product_id, order_date, amount_inr, status
FROM orders
ORDER BY amount_inr DESC, order_id ASC
LIMIT 5;

-- 4. Alias (AS): count all orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- 5. IN: orders paid by either UPI or Credit Card
SELECT order_id, payment_mode, amount_inr, status
FROM orders
WHERE payment_mode IN ('UPI', 'Credit Card')
ORDER BY order_id;

-- 6a. BETWEEN: orders between INR 100 and INR 500 inclusive
SELECT order_id, amount_inr, status
FROM orders
WHERE amount_inr BETWEEN 100 AND 500
ORDER BY amount_inr, order_id;

-- 6b. NOT BETWEEN: orders outside INR 100 to INR 500
SELECT order_id, amount_inr, status
FROM orders
WHERE amount_inr NOT BETWEEN 100 AND 500
ORDER BY amount_inr, order_id;

-- 7. IS NULL: orders with no rating (Cancelled/Pending)
SELECT order_id, status, rating
FROM orders
WHERE rating IS NULL
ORDER BY order_id;
