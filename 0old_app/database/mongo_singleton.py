from pymongo import MongoClient

from settings import MONGO_HOST, MONGO_PORT,MONGO_DATABASE


class Mongo():
    '''
    This class opens a session wide MongoDB connection
    It's bad practice to open and close MongoDB connections all the time.
    By using this singleton, connections are persistant.
    '''
    __connection = None

    @classmethod
    def get_database(cls):
        if cls.__connection == None:
            cls.__connection = MongoClient(MONGO_HOST, MONGO_PORT)
            print 'New MongoClient created'
        db = cls.__connection[MONGO_DATABASE]
        return db
