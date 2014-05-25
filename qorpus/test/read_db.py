import os
import pickle
from pymongo import MongoClient

MONGOHQ_URL = os.environ['MONGOHQ_URL'] if 'MONGOHQ_URL' in os.environ else 'NIL'

client = MongoClient(MONGOHQ_URL)
db = client.tries_db
collection = db.main_collection
wiz = collection.find_one({'artist': 'Wiz Khalifa'})
tr = pickle.loads(wiz['trie'])
print('Smoke appears', tr.lookup('smoke'), 'times')
