import geojson
import random
from collections import Counter

def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n+1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersect:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def generate_random_coordinate(polygon):
    min_x = min(coord[0] for coord in polygon)
    max_x = max(coord[0] for coord in polygon)
    min_y = min(coord[1] for coord in polygon)
    max_y = max(coord[1] for coord in polygon)
    
    while True:
        random_x = random.uniform(min_x, max_x)
        random_y = random.uniform(min_y, max_y)
        if is_point_in_polygon([random_x, random_y], polygon):
            return [random_x, random_y]

import json

def process_geojson(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = []
    for feature in data['features']:
        district_name = feature['properties']['NAME']
        okato_ao = feature['properties'].get('OKATO_AO', 'Unknown')
        geometry = feature['geometry']
        
        if geometry['type'] == 'Polygon':
            polygon = geometry['coordinates'][0]
        elif geometry['type'] == 'MultiPolygon':
            polygons = geometry['coordinates']
            polygon = random.choice(polygons)[0]
        
        random_coordinate = generate_random_coordinate(polygon)
        
        new_feature = {
            "type": "Feature",
            "properties": {
                "NAME": district_name,
                "OKATO_AO": okato_ao
            },
            "geometry": {
                "type": "Point",
                "coordinates": random_coordinate
            }
        }
        features.append(new_feature)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False)

# Read JSON file
with open(r'C:\Users\Kostya\Cabify_git\cabify\Analytics\origin_coords.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the "NAME" properties from each feature
names = [feature['properties']['NAME'] for feature in data['features']]

# Count the occurrences of each name
name_counts = Counter(names)

# Print the results
for name, count in name_counts.items():
    print(f"{name}: {count}")

print(len(names))

# # Usage
# input_file = 'moscow.geojson'
# output_file = 'origin_coords.json'
# process_geojson(input_file, output_file)
