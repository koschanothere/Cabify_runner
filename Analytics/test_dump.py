import pymongo
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Read MongoDB URI from environment variable
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        logger.error("MONGO_URI environment variable not set")
        return

    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)
        logger.info("Connected to MongoDB")

        # Specify the database name
        db_name = "test_database"
        db = client[db_name]
        
        # Specify the test collection name
        collection_name = "test_collection"
        collection = db[collection_name]
        
        # Insert a test document
        test_document = {"test_key": "test_value"}
        result = collection.insert_one(test_document)
        logger.info(f"Inserted document with _id: {result.inserted_id}")

        # Verify the insertion
        inserted_document = collection.find_one({"_id": result.inserted_id})
        if inserted_document:
            logger.info(f"Document found: {inserted_document}")
        else:
            logger.error("Document not found")
        
        # Clean up: delete the test document
        collection.delete_one({"_id": result.inserted_id})
        logger.info("Deleted the test document")

        # Clean up: delete the test collection (optional)
        db.drop_collection(collection_name)
        logger.info("Dropped the test collection")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
