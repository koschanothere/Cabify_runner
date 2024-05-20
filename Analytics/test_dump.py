import json

# Read the original JSON file
with open('districts_dictionary.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# Swap keys and values
swapped_data = {v: k for k, v in original_data.items()}

# Write the swapped data to a new JSON file
with open('districts_dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(swapped_data, f, ensure_ascii=False)
