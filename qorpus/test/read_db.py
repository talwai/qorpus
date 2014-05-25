import pickle
from pymongo import MongoClient

client = MongoClient()
db = client.tries_db
collection = db.main_collection
wiz = collection.find_one({'artist': 'Wiz Khalifa'})
tr = pickle.loads(wiz['trie'])
print('Smoke appears', tr.lookup('smoke'), 'times')
