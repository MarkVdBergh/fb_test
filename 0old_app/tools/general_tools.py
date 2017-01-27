import time
import datetime
import pytz
from pymongo import MongoClient
from pymongo import UpdateOne

from settings import LOCAL_TIMEZONE, LOCAL_DATE_FORMAT, MONGO_HOST, MONGO_PORT


class MyTools():
    ########################################################################################################################
    #                                           Time Functions
    ########################################################################################################################

    # Internal times are in UTC, Only time stings and user input and outpu are in local timezone.
    @classmethod
    def yyyymmdd_to_timestamp(self,Y, m, d, H=0, M=0, S=0):
        '''
        Receives a local timezone time and returns the UTC unix timestamp
        :param Y: int: 4-digit year
        :param m: int
        :param d: int
        :param H: int: 24-hour format
        :param M: int
        :param S: int
        :return: int: unix timestamp in UTC timezone
        '''
        localtimestr = '{}-{}-{} {}:{}:{}'.format(Y, m, d, H, M, S)
        utctimestamp = time.mktime(datetime.datetime.strptime(localtimestr, LOCAL_DATE_FORMAT).timetuple())
        return utctimestamp

    @classmethod
    def timestamp_to_yyyymmdd(self,utctimestamp):
        '''
        Receives a utc unix timestamp and returns a local timezone timestring
        :param utctimestamp: int
        :return: str: local time in format 'yyyy-mm-dd HH:MM:SS'
        '''
        localtz = pytz.timezone(LOCAL_TIMEZONE)
        utc = pytz.utc
        utctime = utc.localize(datetime.datetime.utcfromtimestamp(utctimestamp))  # assign utc to timestamp
        localtimestr = utctime.astimezone(localtz).strftime(LOCAL_DATE_FORMAT)  # convert to local time
        return localtimestr

    @classmethod
    def yyyymmdd_to_datetime(self,Y, m, d, H=0, M=0, S=0):
        localtz = pytz.timezone(LOCAL_TIMEZONE)
        utc = pytz.utc
        dt = datetime.datetime(Y, m, d, H, M, S)
        localdt = localtz.localize(dt)
        utcdt = localdt.astimezone(utc)
        return utcdt

    @classmethod
    def datetime_to_timestamp(self,dt):
        # ToDo: make sure that dt is not naive datetime (without timezone) otherwise : TypeError: can't subtract offset-naive and offset-aware datetimes
        timestamp = (dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        return timestamp

    @classmethod
    def timestamp_to_datetime(self,ts):
        dt = datetime.datetime.fromtimestamp(ts, tz=pytz.utc)  # .strftime('%Y-%m-%d %H:%M:%S')
        return dt

    @classmethod
    def utc_now(self):
        return datetime.datetime.now(tz=pytz.utc)

    ########################################################################################################################
    #                                           MANAGEMENT TOOLS
    ########################################################################################################################
    @classmethod
    def save_blacklist_doc(self,doc, db='maintenance', collection='blacklist'):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = client[db]
        collection = db[collection]
        operation = [UpdateOne({'id': doc['id']}, {'$set': doc}, upsert=True)]
        collection.bulk_write(operation)

    @classmethod
    def get_blacklist(self,db='maintenance', collection='blacklist'):
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT) #ToDo: use the mongo_singleton !!!
        db = client[db]
        collection = db[collection]
        blacklist = []
        for blk in collection.find({}):
            blacklist.append(blk['id'])
        return blacklist

    @classmethod
    def is_blacklisted(self,id):
        blacklist = get_blacklist()
        if id in blacklist:
            blacklisted = True
        else:
            blacklisted = False
        return blacklisted

    @classmethod
    def save_log(self,doc, db='maintenance', collection='log'):
        print doc
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = client[db]
        collection = db[collection]
        collection.save(doc)


########################################################################################################################
# ToDo: OLD !!!! ADAPT SCRAPING ETC TO BE ABLE TO DELETE THIS





########################################################################################################################
#                                           Time Functions
########################################################################################################################

# Internal times are in UTC, Only time stings and user input and outpu are in local timezone.

def yyyymmdd_to_timestamp(Y, m, d, H=0, M=0, S=0):
    '''
    Receives a local timezone time and returns the UTC unix timestamp
    :param Y: int: 4-digit year
    :param m: int
    :param d: int
    :param H: int: 24-hour format
    :param M: int
    :param S: int
    :return: int: unix timestamp in UTC timezone
    '''
    localtimestr = '{}-{}-{} {}:{}:{}'.format(Y, m, d, H, M, S)
    utctimestamp = time.mktime(datetime.datetime.strptime(localtimestr, LOCAL_DATE_FORMAT).timetuple())
    return utctimestamp


def timestamp_to_yyyymmdd(utctimestamp):
    '''
    Receives a utc unix timestamp and returns a local timezone timestring
    :param utctimestamp: int
    :return: str: local time in format 'yyyy-mm-dd HH:MM:SS'
    '''
    localtz = pytz.timezone(LOCAL_TIMEZONE)
    utc = pytz.utc
    utctime = utc.localize(datetime.datetime.utcfromtimestamp(utctimestamp))  # assign utc to timestamp
    localtimestr = utctime.astimezone(localtz).strftime(LOCAL_DATE_FORMAT)  # convert to local time
    return localtimestr


def yyyymmdd_to_datetime(Y, m, d, H=0, M=0, S=0):
    localtz = pytz.timezone(LOCAL_TIMEZONE)
    utc = pytz.utc
    dt = datetime.datetime(Y, m, d, H, M, S)
    localdt = localtz.localize(dt)
    utcdt = localdt.astimezone(utc)
    return utcdt


def datetime_to_timestamp(dt):
    # ToDo: make sure that dt is not naive datetime (without timezone) otherwise : TypeError: can't subtract offset-naive and offset-aware datetimes
    timestamp = (dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
    return timestamp


def timestamp_to_datetime(ts):
    dt = datetime.datetime.fromtimestamp(ts, tz=pytz.utc)  # .strftime('%Y-%m-%d %H:%M:%S')
    return dt


def utc_now():
    return datetime.datetime.now(tz=pytz.utc)


########################################################################################################################
#                                           MANAGEMENT TOOLS
########################################################################################################################

def save_blacklist_doc(doc, db='maintenance', collection='blacklist'):
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[db]
    collection = db[collection]
    operation = [UpdateOne({'id': doc['id']}, {'$set': doc}, upsert=True)]
    collection.bulk_write(operation)


def get_blacklist(db='maintenance', collection='blacklist'):
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[db]
    collection = db[collection]
    blacklist = []
    for blk in collection.find({}):
        blacklist.append(blk['id'])
    return blacklist


def is_blacklisted(id):
    blacklist = get_blacklist()
    if id in blacklist:
        blacklisted = True
    else:
        blacklisted = False
    return blacklisted


def save_log(doc, db='maintenance', collection='log'):
    print doc
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[db]
    collection = db[collection]
    collection.save(doc)

# if __name__ == '__main__':
#     d = datetime.datetime(2000, 1, 1, tzinfo=pytz.utc)
#     # print d
#     ts = datetime_to_timestamp(d)
#     # print ts
#     s = timestamp_to_yyyymmdd(1484245501)
#     print s
#
#     print yyyymmdd_to_datetime(2000, 1, 1)
#
#     print utc_now()
#
#     print datetime_to_timestamp(datetime.datetime.now())
