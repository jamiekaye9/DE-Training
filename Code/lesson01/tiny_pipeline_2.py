# EXTRACT
raw_sales = ["59.99", "1200.00", "8.50", "34.00"]

# TRANSFORM
total = 0
for sale in raw_sales:
    total = total + float(sale)

# LOAD
print ("Online store total sales: £", total)