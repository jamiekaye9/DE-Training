import json

with open("order.json", encoding="utf-8") as file:
    order = json.load(file)

print(order["discount_code"])