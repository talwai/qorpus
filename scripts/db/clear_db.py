from pymongo import MongoClient
client = MongoClient()
db = client.tries_db
collection = db.main_collection
print("Before", collection.count())
collection.remove({})
print("After", collection.count())
