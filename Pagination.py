import csv
from prettytable import PrettyTable

# Read the CSV file
with open('product.csv', newline='') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Sort the rows based on the values in the 'rating' column
rows.sort(key=lambda row: (row['rating']
          is not None, row['rating']), reverse=True)


# Create a table and add the rows to it
table = PrettyTable()
table.field_names = ['Name', 'Barcode', 'Brand',
                     'Description', 'Price', 'Available', 'Reviews', 'Rating']
for row in rows:
    table.add_row([row['name'], row['barcode'], row['brand'], row['description'],
                  row['price'], row['available'], row['review'], row['rating']])

# Print the table
print(table)
