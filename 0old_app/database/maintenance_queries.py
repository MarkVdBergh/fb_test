from pprint import pprint

from pymongo import MongoClient, ASCENDING, DESCENDING

from mongo_singleton import Mongo
from facebook_crud import *
from tools.general_tools import yyyymmdd_to_timestamp, timestamp_to_datetime

db = Mongo.get_database()
collection = db['facebook']

#########################################
# !!!!!!!!!! DELETE !!!!!!!!!!!!!!!!!!!
# TEMP: FOR LAZY TYPING
db = MongoClient()['politics']
collection = db['facebook']


##########################################

def fbConvert_created_date_dt_ToDate(since=None, until=None):
    '''
    From timestamp in_field, convert it to datetime and store it in out_field
    :param in_field:
    :param out_field:
    :param since:
    :param until:
    :return: {'matched':int, 'updated':int}
    '''
    # Get documents where date_time_id is not of type: date
    # ToDO: {'created_time_dt': {'$ne': {'$type': 'date'}}} doesn't work.
    q = {'created_time_dt': {'$ne': {'$type': 'date'}}}
    # Till above query is repaired I just select all, and keep track with a flag in the document
    q = {'flag':{'$ne':1}}
    p = {'created_time_dt': 1, 'created_time': 1}
    cursor = fbGetPosts(q, p, since=since, until=until)
    # Update/create the created_time_dt field to have date type
    matched = 0
    modified = 0
    for i, post in enumerate(cursor):
        if i % 500:print i,
        q = {'_id': post['_id']}
        dt = timestamp_to_datetime(post['created_time']).isoformat()
        u = {'$set': {'created_time_dt': dt, 'flag': 1}}  # Flag field to keep trak what was updated already
        result = fbUpdatePost(query=q, update=u)
        matched += 1
        modified += 1
    return {'matched': matched, 'modified': modified}
# c = fbConvert_created_date_dt_ToDate(since=yyyymmdd_to_timestamp(2017, 1, 10),
#                                      until=yyyymmdd_to_timestamp(2016, 5, 11))
# for i in c:
#     print i
# print c


def fbResetFlag(flag=0):
    q={'flag':{'$ne':flag}}
    u={'$set':{'flag':flag}}
    result =fbUpdatePost(query=q, update=u)
    print result.raw_result

fbResetFlag(0)



# print fbConvert_created_date_dt_ToDate(since=yyyymmdd_to_timestamp(2017, 1, 10))
# for i in fbGetPosts({}, projection={'id': 1, 'created_time_dt': 1},
#                       since=yyyymmdd_to_timestamp(2017, 1, 10)):
#     print i
