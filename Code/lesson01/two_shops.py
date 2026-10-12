# EXTRACT
leeds_sales = ["120.50", "89.99", "15.00", "250.00"]
manchester_sales = ["300.00", "45.50", "19.99"]

#TRANSFORM
total_leeds = 0
total_manchester = 0

for sale in leeds_sales:
    total_leeds = total_leeds + float(sale)

for sale in manchester_sales:
    total_manchester = total_manchester + float(sale)

two_shops_total = total_leeds + total_manchester

#LOAD

print("Leeds Sales: £", total_leeds)
print("Manchester Sales: £", total_manchester)
print("Total Sales: £", two_shops_total)

