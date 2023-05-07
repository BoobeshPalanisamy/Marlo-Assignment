import csv


class Product:
    def __init__(self, name, barcode, brand, description, price, available):
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.description = description
        self.price = price
        self.available = available

    def to_list(self):
        return [self.name, self.barcode, self.brand, self.description, self.price, self.available]


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

# Create Product object
product = Product(name, barcode, brand, description, price, available)

# Append data to CSV file
append_to_csv('product.csv', product.to_list())
