import csv

# Path to your CSV file
csv_file_path = 'dataset.csv'

# List of Result values
result_values = [
    "70%", "10%", "30%", "80%", "90%", "70%", "95%", "90%", "0%", "0%", "90%", "10%", "8%", "2%", "20%", "85%",
    "90%", "70%", "95%", "80%", "60%", "65%", "67%", "80%", "84%", "98%", "92%", "60%", "30%", "40%", "25%",
    "87%", "60%", "80%", "80%", "88%", "70%", "88%", "88%", "88%", "90%", "20%", "0%", "95%", "80%", "90%",
    "92%", "99%"
]

# Read the existing CSV file and create a new CSV file with the "Result" column
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the header row
    rows = [row + [result_values[i]] for i, row in enumerate(reader)]  # Append the "Result" column to each row

    # Write the updated data to a new CSV file
    with open('updated_csv_file.csv', 'w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(headers + ['Dangerousness'])  # Write the updated header row
        writer.writerows(rows)  # Write the updated rows
