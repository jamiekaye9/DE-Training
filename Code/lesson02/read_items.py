import csv

total = 0

with open("order_items.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        total = total + float(row["unit_price"])
        
print("overall price: £", total)