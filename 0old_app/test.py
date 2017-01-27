# import facebook
# from pymongo import MongoClient
# import json
# import datetime
#
# from tools.scraping_tools import FacebookScraping
# from tools.database_tool import MongoDb
# from tools.processing_tools import FacebookStatistics
#
# client = MongoClient()
# db = client['fb']
#
# # app_id and app_secret for the MD_Statistics app can be generated here: https://developers.facebook.com/apps/389697021376688/dashboard/
# app_id = "389697021376688"
# app_secret = "c0a82eab32865e71c2674137ace14d0a"  # DO NOT SHARE WITH ANYONE!
# access_token = app_id + "|" + app_secret
#
# id = '202064936858448_298515443880063'
# id = "56605856504_10153695947326505"
#
# # fbst=FacebookScraping(access_token)
# # print fbst.get_all_comments(id)
# db = MongoDb('fb', 'politics')
# # db.delete_duplicates()
# posts = db.get_posts_from_page(pageid='54970503767')
# fs = FacebookStatistics()
#
# post = posts.next()
# print post
# stat = fs.calc_likes_from_post(post)
# print stat
# # posts=db.get_posts_from_page(pageid='53668151866')











# class MyClassA(object):
#     stuff = []
#     def __init__(selfie):
#         a=0
#         selfie.a=100
#         print a
#         print selfie.a
#         selfie.stuff=['XXX']
#
# class MyClassB(MyClassA):
#      def __init__(foobar):
#          super(MyClassB,foobar).__init__()
#          # `foobar` points at the instance of `MyClassB` class.
#
#          # MyClassA.stuff gets `1` object appended to it.
#          foobar.stuff.append(1)
#
#          # This should print '[1]'
#          print foobar.stuff
#
#          # `MyClassB` object gets a _new_ attribute named `stuff` pointing at a list.
#          # foobar.stuff = []
#
#          # This should print '[]'.
#          print foobar.stuff
# X=MyClassB()
# print X.stuff
# X.stuff=999
# Y=MyClassB()
# pass

class Yes(object):
    a = 1
    def __init__(self):
        pass

    def yes(self):
        if Yes.a==1:
            print "Yes"
        else:
            print "No, but yes"
            print a
    @classmethod
    def cyes(self):
        if Yes.a==1:
            print "Yes"
        else:
            print "No, but yes"
            print a

class No(Yes):

    def __init__(self):
        super(No,self).__init__()

    def no(self):
        a=self.yes()
        b=Yes().yes()
        c=self.cyes()
        d=Yes.cyes()

    def nott(self):
        if Yes.a==1:
            print "No"
        else:
            print "Yes, but no"
        Yes.a-=1 #Note this line

a=Yes().yes()
b=No().no()
c=Yes().yes()
d=No().no()
No().yes()
x=No().a
y=No.a
No.yes()
No().yes()
pass