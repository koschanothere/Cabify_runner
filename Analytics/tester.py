import hashlib
import json

def feature_hashing_district(district, num_buckets):
    return int(hashlib.sha256(district.encode('utf-8')).hexdigest(), 16) % num_buckets

def create_districts_dictionary():
    with open(r'Analytics\origin_coords.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    districts_dict = {}
    for entry in data['features']:
        if 'properties' in entry and 'NAME' in entry['properties']:
            district_name = entry['properties']['NAME']
            district_hash = feature_hashing_district(district_name, num_buckets=1000)
            districts_dict[district_name] = district_hash

    # Print the dictionary
    print("Districts Dictionary:")
    for district, hash_value in districts_dict.items():
        print(f"{district}: {hash_value}")

    # Save the dictionary to a JSON file
    with open('districts_dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(districts_dict, f, ensure_ascii=False, indent=4)
    
    print("Districts dictionary saved to 'districts_dictionary.json'.")

create_districts_dictionary()
