from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Connect to MongoDB Atlas
mongo_uri = "mongodb+srv://koscha:k0schaf0rCab1fy@cabifycloud.zugoye4.mongodb.net/?retryWrites=true&w=majority&appName=CabifyCloud"
client = MongoClient(mongo_uri)

# Select the database
db = client['CabifyHistory']

# Define a function to update the documents with error handling
def update_documents(collection):
    try:
        documents = collection.find()
        for doc in documents:
            try:
                new_hour = (doc['Hour'] + 3) % 24
                new_day_of_week = (doc['DayOfWeek'] + (doc['Hour'] + 3) // 24) % 7

                collection.update_one(
                    {'_id': doc['_id']},
                    {'$set': {'Hour': new_hour, 'DayOfWeek': new_day_of_week}}
                )
            except KeyError as e:
                print(f"KeyError: {e} in document with _id {doc['_id']}")
            except PyMongoError as e:
                print(f"PyMongoError: {e} in document with _id {doc['_id']}")
            except Exception as e:
                print(f"Unexpected error: {e} in document with _id {doc['_id']}")
    except PyMongoError as e:
        print(f"PyMongoError while fetching documents: {e}")
    except Exception as e:
        print(f"Unexpected error while fetching documents: {e}")

# Iterate over all collections in the database with error handling
try:
    for collection_name in db.list_collection_names():
        print(f"Updating collection: {collection_name}")
        collection = db[collection_name]
        update_documents(collection)
        print(f"Finished collection {collection_name}")
except PyMongoError as e:
    print(f"PyMongoError while listing collections: {e}")
except Exception as e:
    print(f"Unexpected error while listing collections: {e}")

print("Update complete")
