

from pymongo import MongoClient, ASCENDING, DESCENDING
import pandas as pd

from mongo_singleton import Mongo

db = Mongo.get_database()
collection = db['facebook']

#########################################
# !!!!!!!!!! DELETE !!!!!!!!!!!!!!!!!!!
# TEMP: FOR LAZY TYPING
db = MongoClient()['politics']
collection = db['facebook']

########################################################################################################################
#   Create
########################################################################################################################

########################################################################################################################
#   Update
########################################################################################################################

def fbUpdatePost(query=None, update=None, since=None, until=None, upsert=False):
    create_time={}
    if since: create_time.update( {'$gt': since})
    if until: create_time.update( {'$lt': until})
    if create_time: query['created_time'] = create_time
    result=collection.update_many(query,update,upsert=upsert)
    return result


########################################################################################################################
#   Read
########################################################################################################################
def fbGetPosts(query={}, projection=None, since=None, until=None, sort={}, limit=None):
    #ToDo: limit doesn't work

    '''
    Returns a cursor for the queryresult for a page
    :param pageid: int
    :param query: dict
    :param projection: dict
    :param since: int: timestamp
    :param until: int: timestamp
    :param sort: list of tuple(s)
    :param limit: int
    :return: cursor
    '''
    create_time={}
    if since: create_time.update( {'$gt': since})
    if until: create_time.update( {'$lt': until})
    if 'created_time' in query.keys():create_time.update(query['created_time'])
    if create_time: query['created_time'] = create_time
    print query
    cursor = collection.find(query, projection)
    if sort:
        cursor.sort(sort)
    if limit: cursor.limit(limit)
    return cursor


def fbAggregatePosts(pipeline):
    cursor = collection.aggregate(pipeline)
    return cursor


def fbGetUniqueValues(field='profile.id', query={}):
    '''
    Returns a dataframe with unique values for field
    :param field: str
    :param query: dict
    :return: dataframe
    '''
    uniq = collection.distinct(key=field, filter=query)
    df = pd.DataFrame(uniq,columns=[field])
    return df

########################################################################################################################
#   Delete
########################################################################################################################
