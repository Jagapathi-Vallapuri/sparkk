import csv
import random

# Data generation settings
records = 1000
countries = ['USA', 'UK', 'Germany', 'France', 'India', 'Canada']
products = [('Laptop', 1200), ('Mouse', 25), ('Keyboard', 50), ('Monitor', 300), ('HDMI Cable', 10)]

print("Generating sales.csv...")
with open('sales.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Header
    writer.writerow(['TransactionID', 'Country', 'Product', 'Quantity', 'Price', 'CustomerID'])
    
    # Rows
    for i in range(records):
        prod, price = random.choice(products)
        writer.writerow([
            i + 1,
            random.choice(countries),
            prod,
            random.randint(1, 5),  # Quantity
            price,
            random.randint(100, 200) # CustomerID
        ])
print("Done! 'sales.csv' created.")