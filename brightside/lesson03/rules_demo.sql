-- Try to add a second shop with the ID 1
INSERT INTO shops VALUES (1, 'Brightside Leeds Two', 'Leeds', 'North', '2026-10-11', NULL);

-- Try to add an order for a shop that doesn't exist
INSERT INTO orders VALUES (99999, 2087, 99, '2026-10-11', 'completed');

-- Try to add a customer with an email someone already has
INSERT INTO customers VALUES (2999, 'Pat', 'Shah', 'priya.shah@example.com', NULL, 'Leeds', '2026-10-11', 0);

-- Try to add a product with no name
INSERT INTO products VALUES (999, NULL, 'Bikes', 499.00, 1);