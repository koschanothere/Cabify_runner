import pymongo
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your JSON data from a file
data_file = "test_data.json"
with open(data_file, "r", encoding='utf-8') as f:
    json_data = json.load(f)

# Load district name mappings from JSON file
with open("swapped_districts.json", "r", encoding='utf-8') as f:
    district_names = json.load(f)


def insert_data_into_collections(data, district_names):
    # Insert data into MongoDB collections based on district names
    for entry in data:
        logger.info(f"Running entry: {entry}")
        district_key = str(entry["District"])
        logger.info(f"District key: {district_key}, {type(district_key)}")
        district_name = district_names.get(district_key, f"district_{district_key}")  # Use district name if available, otherwise default to key
        logger.info(f"Distrit name: {district_name} \n")


def main():
    
    insert_data_into_collections(json_data, district_names)
    logger.info("Data inserted into MongoDB collections.")
    

if __name__ == "__main__":
    main()
