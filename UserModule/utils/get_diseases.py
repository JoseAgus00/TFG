import json
from collections import defaultdict

# Load data from the file
with open('patients.json', 'r') as file:
    data = json.load(file)

# Get all different diseases
diseases = set()
for patient in data:
    diseases.add(patient['Disease'])

disease_totals = defaultdict(float)
disease_counts = defaultdict(int)

for patient in data:
    disease_totals[patient['Disease']] += int(patient['Dangerousness'].rstrip('%'))
    disease_counts[patient['Disease']] += 1

disease_averages = {}
for disease in diseases:
    disease_averages[disease] = disease_totals[disease] / disease_counts[disease]

print("\nPromedio de Dangerousness por enfermedad:")
for disease, average in disease_averages.items():
    print(f"{disease}: {average//10 if (average // 10) != 0 else 1}")

