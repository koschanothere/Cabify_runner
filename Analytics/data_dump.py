import pymongo
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your JSON data from a file
data_file = "data.json"
with open(data_file, "r", encoding='utf-8') as f:
    json_data = json.load(f)

# Load district name mappings from JSON file
with open(r"districts_dictionary.json", "r", encoding='utf-8') as f:
    district_names = json.load(f)

def connect_to_mongodb(uri):
    # Connect to MongoDB and return the client
    try:
        client = pymongo.MongoClient(uri)
        logger.info("Connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def insert_data_into_collections(client, data, district_names):
    # Insert data into MongoDB collections based on district names
    db = client.get_database("CabifyHistory")
    for entry in data:
        district_key = entry["District"]
        district_name = district_names.get(str(district_key), f"district_{district_key}")  # Use district name if available, otherwise default to key
        collection = db.get_collection(district_name)
        try:
            collection.insert_one(entry)
            logger.info(f"Inserted document into collection {district_name}")
        except Exception as e:
            logger.error(f"Failed to insert document into collection {district_name}: {e}")

def main():
    mongo_uri = os.getenv('MONGO_URI')  # Read MongoDB URI from environment variable
    if not mongo_uri:
        logger.error("MONGO_URI environment variable not set")
        return

    try:
        client = connect_to_mongodb(mongo_uri)
        insert_data_into_collections(client, json_data, district_names)
        logger.info("Data inserted into MongoDB collections.")
        
        # Clear the JSON data file after uploading
    #     with open(data_file, 'w') as f:
    #         f.truncate(0)
    #     logger.info("Cleared the JSON data file.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
