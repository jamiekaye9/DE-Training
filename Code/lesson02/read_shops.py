import csv

total = 0

with open("products.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        total = total + float(row["price"])

print('total of all prices: £', total)