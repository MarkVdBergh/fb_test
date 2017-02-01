import factory
from bson import ObjectId
from factory import Dict
from factory import Faker
from factory import LazyAttribute
from factory import LazyAttributeSequence
from factory import List
from factory import SelfAttribute
from factory import Sequence, SubFactory
from factory import debug
from factory import sequence
from factory.fuzzy import FuzzyText, reseed_random, get_random_state, set_random_state, FuzzyInteger, FuzzyChoice
from factory.mongoengine import MongoEngineFactory

from facebook_objects import *

# Set random to generate the same data set each time
seed = 42
reseed_random(seed)  # set random seed for factory.fuzzy
Faker._get_faker().seed(seed)  # set random state for factory.Faker


# ToDo: implement different FbRawPost instances with the same profile
#   see: http://stackoverflow.com/questions/39345286/how-to-create-factory-boy-factories-for-django-models-with-the-same-foreign-key
# ToDo: why does 'create' upserts document ?
# Tweak: make length of lists (comment, likes,..) random, and not =n
# Tweak: Make like_count and comment_count the numer of likes and comments iso random int




class Fac_FbRawPost_profile(MongoEngineFactory):
    class Meta: model = FbRawPost_profile

    id = Sequence(lambda n: '1%07d' % n)
    name = Faker(provider='name', locale='nl_NL')


class Fac_FbRawPost_user(MongoEngineFactory):
    class Meta: model = FbRawPost_user

    id = Sequence(lambda n: '2%07d' % n)
    name = Faker(provider='name', locale='nl_NL')
    link = Faker(provider='uri')
    # Tweak: picture seems to take a lot of time
    picture = Dict({'data': Dict({'uri': Faker(provider='uri'),
                                  'is_silhouette': FuzzyChoice([True, False])})})


class Fac_FbRawPost_reactions(MongoEngineFactory):
    class Meta: model = FbRawPost_reactions

    id = Sequence(lambda n: '3%07d' % n)
    type = FuzzyChoice(['LIKE', 'LOVE', 'ANGRY', 'WOW', 'HAHA', 'SAD', 'THANKFUL'])
    name = Faker(provider='name', locale='nl_NL')
    pic = Faker(provider='uri')


class Fac_FbRawPost_comments(MongoEngineFactory):
    class Meta: model = FbRawPost_comments

    id = Sequence(lambda n: '4%05d_5%07d' % (n, n))
    created_time = FuzzyInteger(low=1041379200, high=2524608000)
    comment_from = SubFactory(Fac_FbRawPost_user)
    message = Faker(provider='text', max_nb_chars=100)

    @sequence
    def likes(n):
        # _likes = List([Fac_FbRawPost_user() for _ in xrange(n)])
        _likes = [Fac_FbRawPost_user() for _ in xrange(n)]
        print type(_likes)
        return {'data': _likes}
        # return _likes

    # like_count=
    comment_count = FuzzyInteger(low=0, high=20)


class Fac_FbRawPost(MongoEngineFactory):
    class Meta:
        model = FbRawPosts
        exclude = ('_postid1', '_postid2',)

    id = Sequence(lambda n: ObjectId('1234567890abcdef%08d' % n))
    created_time = FuzzyInteger(low=1041379200, high=2524608000)
    _postid1 = SelfAttribute(attribute_name='profile.id')
    _postid2 = Sequence(lambda n: '2%05d' % n)
    postid = LazyAttribute(lambda obj: '{}_{}'.format(obj._postid1, obj._postid2))
    profile = SubFactory(Fac_FbRawPost_profile)

    @sequence
    def reactions(n):
        # Tweak: now reactions() generates lists of size 0,1,2,3,... Improve with random length
        # Tweak: Rewrite method to comments = Sequence([....])
        # _react = List([Fac_FbRawPost_reactions() for _ in xrange(n)])  # List doesn't work
        _react = [Fac_FbRawPost_reactions() for _ in xrange(n)]
        return _react

    @sequence
    def comments(p):
        _comm = [Fac_FbRawPost_comments() for _ in xrange(p)]
        return _comm

    shares = Dict({'count': FuzzyInteger(low=0, high=100)})
    from_user = SubFactory(Fac_FbRawPost_user)
    to_user = SubFactory(Fac_FbRawPost_user)
    message = Faker(provider='paragraph', locale='nl_NL', nb_sentences=5, variable_nb_sentences=True)
    picture = Faker(provider='uri')
    name = Faker(provider='sentence', nb_words=6, variable_nb_words=True)
    link = Faker(provider='uri')
    type = FuzzyChoice(['event', 'uri', 'music', 'note', 'photo', 'status', 'video'])
    status_type = FuzzyChoice([None, 'added_photos', 'added_video', 'created_event', 'created_note', 'mobile_status_update', 'published_story', 'shared_story', 'wall_post'])
    story = Faker(provider='sentence', nb_words=6, variable_nb_words=True)


if __name__ == '__main__':
    # r = Fac_FbRawPost.build
    # _batch(10)
    r = Fac_FbRawPost.create_batch(10)
    # with debug(): r = Fac_FbRawPost.create()
    # for i in r:
    #     print i.id
    #     print i.profile
    pprint.pprint(r)
    # print type(r[0].to_json())
    # print r[0]
