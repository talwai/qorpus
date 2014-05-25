from pymongo import MongoClient
client = MongoClient()
db = client.tries_db
collection = db.main_collection
print(db.command("dbstats"))
print("Count", collection.count())
