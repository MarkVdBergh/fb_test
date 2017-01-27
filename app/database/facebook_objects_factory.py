import factory
from facebook_objects import *


class Factory_FbRawPosts(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = FbRawPosts
    id='1'
    postid='1000'

p=Factory_FbRawPosts.build()
print p


