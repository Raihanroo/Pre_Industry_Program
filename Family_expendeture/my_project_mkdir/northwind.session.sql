ALTER TABLE customers CHANGE COLUMN name Company_name VARCHAR(100);

-- @block
UPDATE customers
SET Company_name = 'Busundhara Group'
WHERE id IN (1, 2, 3, 7, 10);
roleback
-- @endblock

-- @block
SELECT *
from customers
-- @endblock 

-- @block
SELECT * FROM customers WHERE id IN (1,2,3,7,10);
-- @endblock

-- @block
ALTER TABLE customers CHANGE COLUMN id customer_id INT(11) NOT NULL;
-- @endblock

-- @block
SELECT c.first_name,
    i.order_id,
    i.invoice_date,
    od.unit_price
from invoices i,
    order_details od,
    customers c
-- @endblock

-- @block
SELECT c.first_name,
    c.last_name,
    c.job_title,
    c.address,
    c.city,
    c.country_region
from customers c
    JOIN orders o ON c.customer_id = o.customer_id
WHERE c.first_name = 'Francisco';
-- @endblock
-- @block
SELECT *
from customers,
    order_details_status -- @endblock
    -- @block
SELECT DISTINCT c.customer_id,
    c.Company_name,
    c.last_name,
    c.first_name
FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.first_name = 'Francisco';
-- @endblock
-- @block
SELECT 
    *
FROM customers c
    JOIN orders od ON c.customer_id = od.customer_id
-- @endblock



-- @block
SELECT * FROM products

-- @endblock

-- @block
SELECT c.first_name from customers c  JOIN orders od 
ON c.customer_id = od.customer_id LEFT  JOIN orders_status os ON
od.id = os.id
-- @endblock

-- @block
SELECT 
p.product_code,
p.product_name,
od.product_id,
sum(od.quantity) as TotalQuantitySold,
Round(sum(od.unit_price * od.quantity * (1- od.discount))) as TotalRevenus
 from products p
JOIN order_details od ON
p.product_id = od.product_id
GROUP BY p.product_id,p.product_name
HAVING sum(od.quantity) < 200
ORDER BY TotalQuantitySold ASC
-- @endblock