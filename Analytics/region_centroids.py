import geojson

def calculate_centroid(polygon):
    # Calculate centroid of a polygon
    total_area = 0
    centroid_x = 0
    centroid_y = 0
    
    for i in range(len(polygon) - 1):
        xi, yi = polygon[i]
        xiplus1, yiplus1 = polygon[i + 1]
        
        area = (xi * yiplus1) - (xiplus1 * yi)
        total_area += area
        centroid_x += (xi + xiplus1) * area
        centroid_y += (yi + yiplus1) * area
    
    total_area *= 0.5
    centroid_x /= (6 * total_area)
    centroid_y /= (6 * total_area)
    
    return [centroid_x, centroid_y]

def process_geojson(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = geojson.load(f)
    
    features = []
    for feature in data['features']:
        region_name = feature['properties']['NAME']
        okato_code = feature['properties']['OKATO']
        geometry = feature['geometry']
        
        if geometry['type'] == 'MultiPolygon':
            polygons = geometry['coordinates']
            # Calculate centroid for each polygon in MultiPolygon
            centroids = [calculate_centroid(polygon[0]) for polygon in polygons]
            # Use the average of centroids as the centroid of the region
            centroid_x = sum(point[0] for point in centroids) / len(centroids)
            centroid_y = sum(point[1] for point in centroids) / len(centroids)
        elif geometry['type'] == 'Polygon':
            centroid_x, centroid_y = calculate_centroid(geometry['coordinates'][0])
        
        new_feature = {
            "type": "Feature",
            "properties": {
                "NAME": region_name,
                "OKATO": okato_code
            },
            "geometry": {
                "type": "Point",
                "coordinates": [centroid_x, centroid_y]
            }
        }
        features.append(new_feature)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        geojson.dump({"type": "FeatureCollection", "features": features}, f, ensure_ascii=False)

# Usage
input_file = 'ao.geojson'
output_file = 'region_centroid.json'
process_geojson(input_file, output_file)
