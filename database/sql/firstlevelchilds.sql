SELECT 
    parent.name AS category_name,
    COUNT(child.id) AS first_level_childs_count
FROM categories parent
LEFT JOIN categories child ON parent.id = child.parent_id
GROUP BY parent.name
ORDER BY first_level_childs_count DESC;