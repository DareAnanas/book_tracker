my_dict = {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Get the items view
items_view = my_dict.items()
print(items_view)

# Iterate through the key-value pairs
for key, value in items_view:
    print(f"Key: {key}, Value: {value}")

# Demonstrate dynamic update
my_dict['occupation'] = 'Engineer'
print(items_view)