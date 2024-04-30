# Sample list of dictionaries
list_of_dicts = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

# New dictionary with the updated values
new_dict = {"id": 2, "name": "Barbara"}

# ID to search for
search_id = 2

# Iterate over the list and replace the dictionary with the new one
for i, d in enumerate(list_of_dicts):
    if d["id"] == search_id:
        list_of_dicts[i] = new_dict
        break

# Print the updated list
print(list_of_dicts)
