

from tools.database_tool_MIGRATE import MongoDb
from processing.facebook_stats import FbPostStats
import datetime
import pprint
from profilehooks import profile,coverage,timecall

mon=MongoDb('facebook')
stat=MongoDb('stats')

print datetime.datetime.now()

filtr={'id':'53668151866_52950943815'}
filtr={}
fb=mon.get_posts_from_page(pageid='345644812211706', limit=100,filtr=filtr)


# @timecall()
# @coverage
# @profile()
def xx():
    docs=[]
    for i, doc in enumerate(fb):
        # pprint.pprint(doc)
        # print doc['id']
        fbp = FbPostStats(doc).make_post_stats_document()

        docs.append(fbp)
        # print fbp['postid']
        if i%9==0:
            # pprint.pprint(docs)
            stat.insert_fb_documents(docs)



    print datetime.datetime.now()

xx()
