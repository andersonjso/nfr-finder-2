import json

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Sort data for each system and area based on total_%
for system in data:
    for area in data[system]:
        data[system][area] = sorted(data[system][area], key=lambda x: x['total_%'], reverse=True)

# Print sorted data
print(json.dumps(data, indent=4))