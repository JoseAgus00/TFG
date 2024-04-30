import csv
import json

csv_file_path = 'updated_csv_file.csv'
json_file_path = 'patients.json'

data = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

with open(json_file_path, mode='w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"CSV convertido a JSON con éxito. {len(data)}")
