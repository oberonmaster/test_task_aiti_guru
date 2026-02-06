WITH 
month_sales AS (SELECT oi.nomenclature_id, SUM(oi.quantity) as total_quantity FROM order_items oi JOIN orders o ON oi.order_id = o.id WHERE o.order_date >= date('now', '-1 month') GROUP BY oi.nomenclature_id), 
category_roots AS (SELECT c.id,(SELECT name FROM categories WHERE id = COALESCE((SELECT parent_id FROM categories WHERE id = c.parent_id),c.parent_id, c.id )) as root_name FROM categories c)
SELECT 
n.name as product_name,
cr.root_name as top_level_category,
ms.total_quantity as total_sold
FROM 
month_sales ms
JOIN 
nomenclature n ON ms.nomenclature_id = n.id
LEFT JOIN
category_roots cr ON n.category_id = cr.id
ORDER BY
ms.total_quantity DESC
LIMIT 5;