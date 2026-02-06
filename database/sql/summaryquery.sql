SELECT c.name AS client_name, SUM(oi.quantity * oi.price) AS total_sum
FROM clients c
JOIN orders o ON c.id = o.client_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name
ORDER BY total_sum DESC;