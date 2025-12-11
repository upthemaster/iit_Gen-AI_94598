import pandas as pd

data = pd.read_csv(r"E:\SUNBEAM INTERNSHIP\DAY_2\iit_Gen-AI_94598\DAY_2\products.csv")
print(data)

print("The total rows of the table is :", len(data))

products = data[data["price"] > 500].shape[0]
print("products with price greater than 500 are :", products)

average_price = data["price"].mean()
print("Average price :", average_price)

user_category = input("Enter the category you want to filter products: ")
filtered_products = data[data["category"].str.lower() == user_category.lower()]
print("Products in the category", user_category, "are :")
print(filtered_products)

total_quantity = data["quantity"].sum()
print("Total quantity of all stock products is :", total_quantity)
