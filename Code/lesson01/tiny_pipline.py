# A tiny pipeline: Extract, Transform, Load

# EXTRACT: Raw sales from the Leeds shop till (pretend data, stored as text).
raw_sales = ["120.50", "89.99", "15.00", "250.00", "42.75"]

# TRANSFORM: Turn each piece of text into a number and add it to a running total.
total = 0
for sale in raw_sales:
    total = total + float(sale)

# LOAD: Deliver the result (here, just to the screen).
print("Leeds shop total sales: £", total)