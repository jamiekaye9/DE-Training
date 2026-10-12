# setup_brightside.py
# Builds the Brightside Bikes practice database (brightside.db) used in the SQL lessons.
# Safe to run as often as you like: it throws away the old tables and rebuilds them
# from scratch, so it's also your "reset button" if you ever mess the data up.

import sqlite3
import os

# Put the database file in the same folder as this script, wherever you run it from
folder = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(folder, "brightside.db")

connection = sqlite3.connect(database_path)
connection.execute("PRAGMA foreign_keys = ON")

# ---------------------------------------------------------------------------
# 1. Create the tables (the empty, labelled shelves)
# ---------------------------------------------------------------------------
connection.executescript("""
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shops;

CREATE TABLE shops (
    shop_id      INTEGER PRIMARY KEY,
    shop_name    TEXT    NOT NULL,
    city         TEXT,
    region       TEXT    NOT NULL,
    opened_date  TEXT    NOT NULL,
    phone        TEXT
);

CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    product_name  TEXT    NOT NULL,
    category      TEXT    NOT NULL,
    price         REAL    NOT NULL,
    in_stock      INTEGER NOT NULL
);

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    first_name    TEXT    NOT NULL,
    last_name     TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    phone         TEXT,
    city          TEXT,
    signup_date   TEXT    NOT NULL,
    newsletter    INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers (customer_id),
    shop_id      INTEGER NOT NULL REFERENCES shops (shop_id),
    order_date   TEXT    NOT NULL,
    status       TEXT    NOT NULL
);

CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders (order_id),
    product_id     INTEGER NOT NULL REFERENCES products (product_id),
    quantity       INTEGER NOT NULL,
    unit_price     REAL    NOT NULL
);
""")

# ---------------------------------------------------------------------------
# 2. The data (one line per row)
# ---------------------------------------------------------------------------
# shop_id, shop_name, city, region, opened_date, phone
shops = [
    (1, 'Brightside Leeds', 'Leeds', 'North', '2015-03-14', '01131234567'),
    (2, 'Brightside Manchester', 'Manchester', 'North', '2016-07-01', '01619876543'),
    (3, 'Brightside Bristol', 'Bristol', 'South West', '2018-11-23', '01175550123'),
    (4, 'Brightside London Bridge', 'London', 'South East', '2019-05-10', '02079460000'),
    (5, 'Brightside Online', None, 'Online', '2017-01-09', None),
    (6, 'Brightside York', 'York', 'North', '2026-10-01', '01904555210'),
]

# product_id, product_name, category, price, in_stock (1 = yes, 0 = no)
products = [
    (101, 'City Commuter Bike', 'Bikes', 549.0, 1),
    (102, 'Roadrunner Road Bike', 'Bikes', 1199.0, 1),
    (103, 'Little Rider Kids Bike', 'Bikes', 189.0, 1),
    (104, 'Volt E-Bike', 'Bikes', 1899.0, 1),
    (105, 'Trailblazer Mountain Bike', 'Bikes', 749.0, 0),
    (106, 'Kids Balance Bike', 'Bikes', 89.0, 1),
    (220, 'Puncture Repair Kit', 'Parts', 6.5, 1),
    (221, 'Inner Tube 700c', 'Parts', 8.99, 1),
    (222, 'Brake Pads (pair)', 'Parts', 12.5, 1),
    (223, 'Chain', 'Parts', 29.99, 0),
    (224, 'Road Tyre 700c', 'Parts', 34.99, 1),
    (301, 'Commuter Helmet', 'Accessories', 89.99, 1),
    (302, 'Kids Helmet', 'Accessories', 34.99, 1),
    (412, 'LED Light Set', 'Accessories', 30.51, 1),
    (413, 'Bike Bell', 'Accessories', 7.99, 1),
    (415, 'Water Bottle', 'Accessories', 6.99, 1),
    (5001, 'Lock, D-shape', 'Accessories', 24.99, 1),
    (501, 'Waterproof Jacket', 'Clothing', 79.0, 1),
    (502, 'Padded Shorts', 'Clothing', 39.99, 1),
    (503, 'Cycling Gloves', 'Clothing', 19.99, 1),
]

# customer_id, first_name, last_name, email, phone, city, signup_date, newsletter (1 = yes, 0 = no)
customers = [
    (2080, 'Tom', 'Hughes', 'tom.hughes@example.com', None, None, '2024-07-17', 1),
    (2081, 'Aisha', 'Khan', 'aisha.khan@example.com', '07819600133', 'Manchester', '2025-10-31', 0),
    (2082, 'Liam', "O'Connor", 'liam.oconnor@example.com', None, 'Sheffield', '2026-01-21', 1),
    (2083, 'Sophie', 'Taylor', 'sophie.taylor@example.com', '07026542351', 'York', '2023-07-09', 1),
    (2084, 'Daniel', 'Evans', 'daniel.evans@example.com', '07940781618', 'London', '2024-08-23', 0),
    (2085, 'Grace', 'Wilson', 'grace.wilson@example.com', '07593103413', 'Bath', '2023-07-26', 1),
    (2086, 'Mohammed', 'Ali', 'mohammed.ali@example.com', '07525534192', 'York', '2025-12-29', 0),
    (2087, 'Priya', 'Shah', 'priya.shah@example.com', None, 'Leeds', '2025-02-16', 1),
    (2088, 'Emily', 'Clarke', 'emily.clarke@example.com', '07350305641', None, '2024-03-08', 0),
    (2089, 'James', 'Walker', 'james.walker@example.com', '07537672423', 'Bath', '2026-02-23', 1),
    (2090, 'Chloe', 'Wright', 'chloe.wright@example.com', '07965328710', 'Bath', '2023-08-13', 1),
    (2091, 'Ryan', 'Patel', 'ryan.patel@example.com', '07691669784', 'Manchester', '2026-02-07', 0),
    (2092, 'Hannah', 'Roberts', 'hannah.roberts@example.com', '07184514627', 'Leeds', '2023-01-07', 0),
    (2093, 'Oliver', 'Green', 'oliver.green@example.com', '07281489325', 'Bristol', '2023-11-27', 1),
    (2094, 'Zoë', 'Martin', 'zoe.martin@example.com', '07957015430', 'Sheffield', '2024-05-08', 0),
    (2095, 'Jack', 'Thompson', 'jack.thompson@example.com', None, 'Leeds', '2025-09-22', 0),
    (2096, 'Amelia', 'White', 'amelia.white@example.com', '07278248963', 'Sheffield', '2026-01-09', 0),
    (2097, 'Harry', 'Hall', 'harry.hall@example.com', '07657871331', 'Manchester', '2024-11-23', 1),
    (2098, 'Isla', 'Lewis', 'isla.lewis@example.com', None, 'Sheffield', '2024-03-27', 1),
    (2099, 'George', 'Young', 'george.young@example.com', None, None, '2023-05-19', 0),
    (2100, 'Fatima', 'Begum', 'fatima.begum@example.com', None, 'London', '2024-05-02', 1),
    (2101, 'Charlie', 'King', 'charlie.king@example.com', None, 'York', '2023-09-28', 0),
    (2102, 'Ella', 'Scott', 'ella.scott@example.com', '07376311656', 'Bath', '2025-04-21', 1),
    (2103, 'Noah', 'Baker', 'noah.baker@example.com', '07106513338', 'Leeds', '2025-07-07', 1),
    (2104, 'Mia', 'Adams', 'mia.adams@example.com', None, 'Manchester', '2024-05-26', 0),
    (2105, 'Leo', 'Turner', 'leo.turner@example.com', '07810801326', 'Leeds', '2025-09-21', 1),
    (2106, 'Ruby', 'Phillips', 'ruby.phillips@example.com', '07260647468', 'London', '2025-09-23', 1),
    (2107, 'Oscar', 'Campbell', 'oscar.campbell@example.com', None, 'Bristol', '2023-04-30', 0),
    (2108, 'Lily', 'Parker', 'lily.parker@example.com', None, 'Sheffield', '2024-10-04', 1),
    (2109, 'Alfie', 'Edwards', 'alfie.edwards@example.com', '07820812191', 'Bath', '2024-04-26', 1),
]

# order_id, customer_id (None = walk-in customer we don't know), shop_id, order_date, status
orders = [
    (10380, None, 2, '2026-07-02', 'completed'),
    (10381, None, 1, '2026-07-02', 'completed'),
    (10382, None, 3, '2026-07-06', 'completed'),
    (10383, 2081, 5, '2026-07-07', 'refunded'),
    (10384, 2103, 5, '2026-07-09', 'completed'),
    (10385, 2093, 5, '2026-07-10', 'cancelled'),
    (10386, 2087, 4, '2026-07-10', 'completed'),
    (10387, 2086, 1, '2026-07-11', 'completed'),
    (10388, 2090, 1, '2026-07-12', 'completed'),
    (10389, 2092, 2, '2026-07-13', 'cancelled'),
    (10390, 2085, 5, '2026-07-14', 'completed'),
    (10391, 2099, 4, '2026-07-14', 'completed'),
    (10392, 2097, 5, '2026-07-15', 'completed'),
    (10393, 2083, 4, '2026-07-17', 'refunded'),
    (10394, 2084, 2, '2026-07-17', 'completed'),
    (10395, 2097, 4, '2026-07-18', 'refunded'),
    (10396, 2094, 4, '2026-07-20', 'completed'),
    (10397, 2103, 5, '2026-07-21', 'completed'),
    (10398, 2082, 4, '2026-07-27', 'completed'),
    (10399, 2104, 1, '2026-07-27', 'completed'),
    (10400, 2092, 4, '2026-07-27', 'completed'),
    (10401, 2083, 5, '2026-07-28', 'refunded'),
    (10402, 2083, 3, '2026-07-31', 'completed'),
    (10403, 2094, 3, '2026-08-01', 'cancelled'),
    (10404, 2103, 5, '2026-08-01', 'completed'),
    (10405, 2102, 1, '2026-08-02', 'completed'),
    (10406, 2092, 1, '2026-08-03', 'refunded'),
    (10407, None, 3, '2026-08-03', 'completed'),
    (10408, None, 2, '2026-08-03', 'completed'),
    (10409, 2097, 2, '2026-08-03', 'cancelled'),
    (10410, 2092, 2, '2026-08-03', 'completed'),
    (10411, 2098, 5, '2026-08-04', 'completed'),
    (10412, 2081, 1, '2026-08-06', 'completed'),
    (10413, 2092, 5, '2026-08-06', 'completed'),
    (10414, 2091, 1, '2026-08-08', 'completed'),
    (10415, 2087, 4, '2026-08-08', 'completed'),
    (10416, 2083, 1, '2026-08-08', 'completed'),
    (10417, 2083, 4, '2026-08-10', 'completed'),
    (10418, 2092, 4, '2026-08-10', 'completed'),
    (10419, None, 4, '2026-08-10', 'completed'),
    (10420, 2095, 1, '2026-08-13', 'completed'),
    (10421, 2103, 4, '2026-08-14', 'completed'),
    (10422, 2094, 5, '2026-08-17', 'refunded'),
    (10423, 2082, 5, '2026-08-20', 'completed'),
    (10424, 2080, 4, '2026-08-23', 'completed'),
    (10425, 2090, 5, '2026-08-26', 'completed'),
    (10426, 2093, 1, '2026-08-28', 'completed'),
    (10427, 2082, 3, '2026-08-28', 'completed'),
    (10428, 2096, 3, '2026-09-01', 'completed'),
    (10429, 2088, 4, '2026-09-03', 'completed'),
    (10430, 2102, 5, '2026-09-03', 'completed'),
    (10431, 2099, 3, '2026-09-05', 'completed'),
    (10432, 2089, 2, '2026-09-06', 'completed'),
    (10433, None, 1, '2026-09-07', 'completed'),
    (10434, 2083, 5, '2026-09-08', 'completed'),
    (10435, 2083, 2, '2026-09-09', 'cancelled'),
    (10436, 2089, 1, '2026-09-09', 'completed'),
    (10437, 2087, 4, '2026-09-11', 'completed'),
    (10438, 2081, 2, '2026-09-11', 'completed'),
    (10439, 2097, 1, '2026-09-11', 'completed'),
    (10440, 2081, 4, '2026-09-13', 'completed'),
    (10441, 2100, 4, '2026-09-13', 'completed'),
    (10442, None, 2, '2026-09-13', 'completed'),
    (10443, 2094, 5, '2026-09-13', 'completed'),
    (10444, 2082, 3, '2026-09-13', 'refunded'),
    (10445, 2098, 4, '2026-09-13', 'completed'),
    (10446, 2100, 1, '2026-09-13', 'refunded'),
    (10447, 2090, 4, '2026-09-13', 'completed'),
    (10448, 2097, 5, '2026-09-13', 'refunded'),
    (10449, 2092, 2, '2026-09-13', 'completed'),
    (10450, 2100, 2, '2026-09-13', 'completed'),
    (10451, 2094, 3, '2026-09-13', 'completed'),
    (10452, 2087, 1, '2026-09-13', 'completed'),
    (10453, 2097, 1, '2026-09-24', 'completed'),
    (10454, None, 3, '2026-09-24', 'refunded'),
    (10455, 2087, 5, '2026-09-24', 'completed'),
    (10456, 2096, 5, '2026-09-26', 'completed'),
    (10457, 2093, 5, '2026-09-29', 'completed'),
    (10458, 2098, 1, '2026-09-30', 'completed'),
    (10459, 2092, 2, '2026-09-30', 'completed'),
]

# order_item_id, order_id, product_id, quantity, unit_price
order_items = [
    (1, 10380, 223, 1, 29.99),
    (2, 10380, 220, 1, 6.5),
    (3, 10381, 105, 1, 749.0),
    (4, 10381, 502, 1, 39.99),
    (5, 10381, 102, 1, 1199.0),
    (6, 10382, 224, 1, 34.99),
    (7, 10383, 221, 1, 8.99),
    (8, 10383, 222, 1, 12.5),
    (9, 10383, 104, 1, 1899.0),
    (10, 10384, 222, 2, 12.5),
    (11, 10385, 301, 1, 89.99),
    (12, 10386, 104, 1, 1899.0),
    (13, 10387, 415, 1, 6.99),
    (14, 10387, 302, 1, 34.99),
    (15, 10388, 103, 1, 189.0),
    (16, 10389, 502, 1, 39.99),
    (17, 10389, 301, 2, 89.99),
    (18, 10390, 223, 1, 29.99),
    (19, 10390, 102, 1, 1199.0),
    (20, 10391, 104, 1, 1899.0),
    (21, 10391, 412, 1, 30.51),
    (22, 10391, 221, 1, 8.99),
    (23, 10392, 221, 1, 8.99),
    (24, 10392, 302, 2, 34.99),
    (25, 10393, 224, 1, 34.99),
    (26, 10393, 501, 1, 79.0),
    (27, 10394, 412, 1, 30.51),
    (28, 10395, 224, 1, 34.99),
    (29, 10395, 503, 1, 19.99),
    (30, 10396, 221, 1, 8.99),
    (31, 10397, 103, 1, 189.0),
    (32, 10398, 222, 1, 12.5),
    (33, 10398, 224, 1, 34.99),
    (34, 10399, 413, 2, 7.99),
    (35, 10400, 101, 1, 549.0),
    (36, 10401, 222, 2, 12.5),
    (37, 10401, 220, 1, 6.5),
    (38, 10402, 415, 1, 6.99),
    (39, 10403, 501, 1, 79.0),
    (40, 10403, 413, 2, 7.99),
    (41, 10404, 415, 2, 6.99),
    (42, 10404, 223, 1, 29.99),
    (43, 10404, 222, 1, 12.5),
    (44, 10405, 223, 1, 29.99),
    (45, 10406, 221, 1, 8.99),
    (46, 10406, 103, 1, 189.0),
    (47, 10407, 412, 2, 30.51),
    (48, 10407, 101, 1, 549.0),
    (49, 10408, 412, 2, 30.51),
    (50, 10409, 222, 1, 12.5),
    (51, 10409, 5001, 1, 24.99),
    (52, 10410, 415, 3, 6.99),
    (53, 10410, 105, 1, 749.0),
    (54, 10411, 101, 1, 549.0),
    (55, 10411, 103, 1, 189.0),
    (56, 10412, 301, 1, 89.99),
    (57, 10413, 413, 1, 7.99),
    (58, 10414, 103, 1, 189.0),
    (59, 10415, 101, 1, 549.0),
    (60, 10416, 221, 1, 8.99),
    (61, 10416, 415, 1, 6.99),
    (62, 10417, 220, 1, 6.5),
    (63, 10417, 224, 1, 34.99),
    (64, 10418, 221, 1, 8.99),
    (65, 10418, 103, 1, 189.0),
    (66, 10418, 222, 1, 12.5),
    (67, 10419, 102, 1, 1199.0),
    (68, 10419, 302, 1, 34.99),
    (69, 10419, 413, 1, 7.99),
    (70, 10420, 302, 1, 34.99),
    (71, 10421, 223, 1, 29.99),
    (72, 10422, 503, 1, 19.99),
    (73, 10423, 415, 1, 6.99),
    (74, 10424, 301, 1, 89.99),
    (75, 10425, 223, 1, 29.99),
    (76, 10426, 222, 1, 12.5),
    (77, 10427, 412, 1, 30.51),
    (78, 10428, 502, 1, 39.99),
    (79, 10429, 221, 1, 8.99),
    (80, 10430, 221, 1, 8.99),
    (81, 10431, 104, 1, 1899.0),
    (82, 10432, 502, 1, 39.99),
    (83, 10433, 105, 1, 749.0),
    (84, 10434, 503, 1, 19.99),
    (85, 10434, 224, 1, 34.99),
    (86, 10434, 5001, 1, 24.99),
    (87, 10435, 412, 1, 30.51),
    (88, 10435, 5001, 1, 24.99),
    (89, 10436, 222, 1, 12.5),
    (90, 10437, 412, 2, 30.51),
    (91, 10437, 415, 1, 6.99),
    (92, 10438, 104, 1, 1899.0),
    (93, 10438, 221, 1, 8.99),
    (94, 10439, 101, 1, 549.0),
    (95, 10440, 224, 1, 34.99),
    (96, 10441, 221, 1, 8.99),
    (97, 10441, 413, 1, 7.99),
    (98, 10442, 224, 1, 34.99),
    (99, 10443, 224, 1, 34.99),
    (100, 10444, 413, 1, 7.99),
    (101, 10444, 301, 1, 89.99),
    (102, 10445, 223, 1, 29.99),
    (103, 10445, 102, 1, 1199.0),
    (104, 10445, 220, 1, 6.5),
    (105, 10446, 103, 1, 189.0),
    (106, 10446, 5001, 1, 24.99),
    (107, 10447, 5001, 1, 24.99),
    (108, 10448, 103, 1, 189.0),
    (109, 10449, 101, 1, 549.0),
    (110, 10449, 502, 1, 39.99),
    (111, 10449, 415, 1, 6.99),
    (112, 10450, 102, 1, 1199.0),
    (113, 10451, 5001, 3, 24.99),
    (114, 10451, 104, 1, 1899.0),
    (115, 10451, 101, 1, 549.0),
    (116, 10452, 301, 1, 89.99),
    (117, 10452, 412, 1, 30.51),
    (118, 10453, 222, 3, 12.5),
    (119, 10454, 5001, 1, 24.99),
    (120, 10454, 224, 1, 34.99),
    (121, 10455, 105, 1, 749.0),
    (122, 10456, 105, 1, 749.0),
    (123, 10456, 103, 1, 189.0),
    (124, 10457, 501, 1, 79.0),
    (125, 10458, 5001, 1, 24.99),
    (126, 10458, 105, 1, 749.0),
    (127, 10459, 301, 2, 89.99),
]

# ---------------------------------------------------------------------------
# 3. Put the data on the shelves
# ---------------------------------------------------------------------------
connection.executemany("INSERT INTO shops VALUES (?, ?, ?, ?, ?, ?)", shops)
connection.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)
connection.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", customers)
connection.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
connection.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", order_items)

connection.commit()
connection.close()

print("Brightside database built at:", database_path)
print("  shops:      ", len(shops), "rows")
print("  products:   ", len(products), "rows")
print("  customers:  ", len(customers), "rows")
print("  orders:     ", len(orders), "rows")
print("  order_items:", len(order_items), "rows")
