import csv

class Product:
    def __init__(self, name, barcode, brand, description, price, available, reviews=None, rating=None):
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.description = description
        self.price = price
        self.available = available
        self.reviews = reviews or []
        self.rating = rating

    def to_list(self):
        return [self.name, self.barcode, self.brand, self.description, self.price, self.available, self.reviews, self.rating]

def append_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        print("Data appended successfully!")

# Prompt user for product information
name = input("Enter product name: ")
barcode = input("Enter product barcode: ")
brand = input("Enter product brand: ")
description = input("Enter product description: ")
price = int(input("Enter product price: "))
available = input("Enter product availability: ")
reviews = input("Enter product reviews: ")
rating = int(input("Enter product rating: "))

# Create Product object
product = Product(name, barcode, brand, description, price, available, reviews, rating)

# Append data to CSV file
append_to_csv('product.csv', product.to_list())
