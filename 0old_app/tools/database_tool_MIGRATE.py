from pymongo import MongoClient, DESCENDING
from pymongo import UpdateMany
from pymongo import UpdateOne

from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from tools.general_tools import utc_now
from database.mongo_singleton import Mongo

#ToDo: Rewrite to avoid using a class

'''
    Problem:
    First you have to create an db class instance in order to use database operations in other modules (processing_tools).
    No reason for complications when only one instance of the class is created per module,
    and then only use the functions in orde to create a document

    Solution:
    Migrate from a class object with functions to
        - functions only + a separate document class to form a json to store.
        - each document in mongo has a coresponding child class that inherit functions and templates from a parent class.
'''

class MongoDb:
    def __init__(self, collection, db=MONGO_DATABASE):
        # self.client = MongoClient(host=MONGO_HOST, port=MONGO_PORT) #ToDo: THIS IS SO WRONG !!!
        # self.db = self.client[db]
        self.db=Mongo.get_database()
        self.collection = self.db[collection]

    def get_posts_from_page(self, pageid, since=0, until=utc_now(),limit=0, filtr={}, projection=None):
        """
        :param pageid:
        :param since:
        :param until:
        :param filtr:
        :param projection:
        :return:
        """
        # filtr['created_time'] = {'$gte': since, '$lt': until}

        posts = self.collection.find(filtr, projection).limit(limit)
        return posts

    def upsert_fb_documents(self, documents):
        if len(documents)==0:return # no documents
        print 'Saving {} documents'.format( len(documents))
        i = 0
        operations = []
        for doc in documents:
            operations.append(UpdateOne({'id': doc['id']}, {'$set':doc}, upsert=True))
            print i, doc["id"]


        result = self.collection.bulk_write(operations)
        return result

    def insert_fb_documents(self, documents):
        result = False
        # ToDo: This inserts many documents. I have the impression if doc10 is a duplicate, doc1...doc9 get insterted, then it crashes and the remaining are not updated
        # See: http://stackoverflow.com/questions/16210863/how-to-recover-from-error-during-bulk-insert-in-mongodb

        if len(documents) is not 0:
            result = self.collection.insert_many(documents=documents)
        return result

    def delete_duplicates(self):
        pipeline = [{"$group": {"_id": "$id", "count": {"$sum": 1}}},
                    {"$match": {"count": {"$gt": 1}}}
                    ]
        while True:  # Iterate till all duplicates are removed
            duplicates = self.collection.aggregate(pipeline=pipeline, useCursor=False)  # Returns a CommandCursor
            # It's also possible to get aggregate by using db.command(). This returns a dict {ok:1, result:[doc0, doc1, ...]}
            # db.command('aggregate', "politics", pipeline=pl, explain=False)
            # ToDo: can I delete multiple documents without looping?
            maxdup = 1
            for dup in duplicates:
                maxdup = max(dup['count'], maxdup)  # is maxdup == 1 then no duplicates exist
                result = self.collection.delete_one({"id": dup["_id"]})  # Delete 1 duplicate
                print "deleted: ", result.deleted_count, dup
            print 'Next pass ...'
            if maxdup == 1:
                print 'Break ...'
                break
        print "Next iteration ..."

    def get_last_post_for_page(self, pageid):
        lastpost = self.collection.find({'profile.id': pageid}).sort('created_time', DESCENDING).limit(1)
        if lastpost.count(
                with_limit_and_skip=True) == 1:  # with_limit_and_skip = True otherwise count doesn't take limit(1) into account
            return lastpost.next()
        else:
            return None

    def convert_all_dates(self):

        pass
