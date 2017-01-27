# from blaze import *
from blaze import data, compute
# from blaze import Table
# from blaze.mongo import *
from blaze.utils import example
from odo import resource

import pymongo

from blaze import  compute


# The names of account holders with negative balance
# deadbeats = accounts[accounts['amount'] < 0]['name']
# db = pymongo.MongoClient().db
# db.mycollection.insert([{'id': 1, 'name': 'Alice',   'amount':  100},
#                         {'id': 2, 'name': 'Bob',     'amount': -200},
#                         {'id': 3, 'name': 'Charlie', 'amount':  300},
#                         {'id': 4, 'name': 'Dennis',  'amount':  400},
#                         {'id': 5, 'name': 'Edith',   'amount': -500}])

x=data(resource('mongodb://localhost/politics::facebook'), dshape='json', fields=['ide'])
print x.peek(),'rrr'

print x.fields
