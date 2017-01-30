from bson import ObjectId
from factory import Sequence, SubFactory
from factory.mongoengine import MongoEngineFactory

from facebook_objects import *


# ToDo: implement different FbRawPost instances with the same profile
# ToDo: solve how to build postid


class Fac_FbRawPost_Profile(MongoEngineFactory):
    class Meta: model = FbRawPost_profile

    name = Sequence(lambda n: 'Page%d' % n)
    id = Sequence(lambda n: '%08d' % n)


class Fac_FbRawPost(MongoEngineFactory):
    class Meta: model = FbRawPosts

    profile = SubFactory(Fac_FbRawPost_Profile)

    id = Sequence(lambda n: ObjectId('1234567890abcdef%08d' % n))
    # postid = profile.id


if __name__ == '__main__':

    r = Fac_FbRawPost.build_batch(10)
    for i in r:
        print i.id
        print i.profile
    pprint.pprint(r)
