from settings import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient, DESCENDING, ASCENDING


def create_indexes():
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client['politics']
    collection = db['facebook']
    collection.create_index([('id', ASCENDING)], unique=True)
    collection.create_index([('profile.id', ASCENDING)], unique=False)
    collection.create_index([('created_time', DESCENDING)], unique=False)
    collection.create_index([('type', ASCENDING)], unique=False)
    collection.create_index([('from.id', ASCENDING)], unique=False)


create_indexes()
