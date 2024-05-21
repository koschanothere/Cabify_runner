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


def connect_to_mongodb(uri):
    # Connect to MongoDB and return the client
    try:
        client = pymongo.MongoClient(uri)
        logger.info("Connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def insert_data_into_collections(client, data):
    # Insert data into MongoDB collections based on district names
    db = client.get_database("CabifyHistory")
    for entry in data:
        collection = db.get_collection("TestCollection")
        try:
            collection.insert_one(entry)
            logger.info(f"Inserted document into collection")
        except Exception as e:
            logger.error(f"Failed to insert document into collection: {e}")

def main():
    mongo_uri = "mongodb+srv://koscha:k0schaf0rCab1fy@cabifycloud.zugoye4.mongodb.net/?retryWrites=true&w=majority&appName=CabifyCloud"  # Read MongoDB URI from environment variable
    if not mongo_uri:
        logger.error("MONGO_URI environment variable not set")
        return

    try:
        client = connect_to_mongodb(mongo_uri)
        insert_data_into_collections(client, json_data)
        logger.info("Data inserted into MongoDB collections.")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
