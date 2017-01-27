

from pprint import pprint
import pandas as pd
from bson import ObjectId

from database.facebook_crud import fbAggregatePosts, fbGetUniqueValues

def fbGetPageids(since=None, until=None):
    ''''
    Returns a dataframe with pageid's for time range
    :param since: int
    :param until: int
    :return: dataframe
    '''
    query = {}
    create_time={}
    if since: create_time.update( {'$gt': since})
    if until: create_time.update( {'$lt': until})
    if create_time: query['created_time'] = create_time
    df=fbGetUniqueValues('profile.id', query)
    df.columns=['pageid']
    return df





def test():
    pipe = [{'$match': {'profile.id': '311935738907850'}},
            {'$group': {'_id': {'$dayOfMonth': '$created_time_dt'}, 'count': {'$sum': 1}}},
            {'$sort': {'count': 1}}]
    pipe = [
        {"$project": {"fieldType1": {"$type": "$created_time_dt"}, "fieldType2": {"$type": "$update_dt"}}},
        {"$limit": 10}
    ]
    pipe = [
        {"$project": {"fieldType1": {"$type": "created_time_dt"}, "fieldType2": {"$type": "$created_time"}}},
        # {'$match': {'fieldType1': 'date'}},
        {'$match':{'_id':ObjectId('587fc79b56e54f3de9c90265')}},
        # {'$group': {'_id': None, 'count': {'$sum': 1}}},
        {'$limit':10}
    ]
    return fbAggregatePosts(pipeline=pipe)


if __name__ == '__main__':
    # print fbGetPageids()
    # print test().next()
    pass
