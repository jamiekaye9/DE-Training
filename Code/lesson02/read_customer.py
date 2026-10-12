import json

with open("customer.json", encoding="utf-8") as file:
    customer = json.load(file)
    
print(customer["first_name"])
print(customer["address"]["city"])