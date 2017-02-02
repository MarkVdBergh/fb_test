import random

from bson import ObjectId
from factory import Dict, Faker, LazyAttribute, SelfAttribute, Sequence, SubFactory, sequence
from factory.fuzzy import reseed_random, FuzzyInteger, FuzzyChoice
from factory.mongoengine import MongoEngineFactory
from profilehooks import profile

from facebook_objects import *

# Set random to generate the same data set each time
seed = 4
random.seed(seed)
reseed_random(seed)  # set random seed for factory.fuzzy
Faker._get_faker().seed(seed)  # set random state for factory.Faker


# ToDo: implement different FbRawPost instances with the same profile
#   see: http://stackoverflow.com/questions/39345286/how-to-create-factory-boy-factories-for-django-models-with-the-same-foreign-key
# ToDo: why does 'create' upserts document ?
# Tweak: make length of lists (comment, likes,..) random, and not =n
# Tweak: Make like_count and comment_count the numer of likes and comments iso random int




class Profile_SubFactory(MongoEngineFactory):
    class Meta: model = Profile

    id = Sequence(lambda n: '1%07d' % n)
    name = Faker(provider='name', locale='nl_NL')


class User_SubFactory(MongoEngineFactory):
    class Meta: model = User

    id = Sequence(lambda n: '2%07d' % n)
    name = Faker(provider='name', locale='nl_NL')
    link = Faker(provider='uri')
    # Tweak: picture seems to take a lot of time
    picture = Dict({'data': Dict({'uri': Faker(provider='uri'),
                                  'is_silhouette': FuzzyChoice([True, False])})})


class Reactions_SubFactory(MongoEngineFactory):
    class Meta: model = Reactions

    id = Sequence(lambda n: '3%07d' % n)
    type = FuzzyChoice(['LIKE', 'LOVE', 'ANGRY', 'WOW', 'HAHA', 'SAD', 'THANKFUL'])
    name = Faker(provider='name', locale='nl_NL')
    pic = Faker(provider='uri')


class Comments_SubFactoy(MongoEngineFactory):
    class Meta:
        model = Comments

    id = Sequence(lambda n: '4%05d_5%07d' % (n, n))
    created_time = FuzzyInteger(low=1041379200, high=2524608000)
    comment_from = SubFactory(User_SubFactory)
    message = Faker(provider='text', max_nb_chars=100)

    @sequence
    def likes(n):
        _r = random.randint(0, 5)
        _likes = [User_SubFactory() for _ in xrange(_r)]
        return {'data': _likes}

    like_count = FuzzyInteger(low=0, high=20)
    comment_count = FuzzyInteger(low=0, high=20)


class FbPost_Factory(MongoEngineFactory):
    class Meta:
        model = FbPost
        exclude = ('_postid1', '_postid2')

    id = Sequence(lambda n: ObjectId('1234567890abcdef%08d' % n))
    created_time = FuzzyInteger(low=1041379200, high=2524608000)
    _postid1 = SelfAttribute(attribute_name='profile.id')
    _postid2 = Sequence(lambda n: '2%05d' % n)
    postid = LazyAttribute(lambda obj: '{}_{}'.format(obj._postid1, obj._postid2))
    profile = SubFactory(Profile_SubFactory)

    @sequence
    def reactions(n):
        # Tweak: now reactions() generates lists of size 0,1,2,3,... Improve with random length
        # Tweak: Rewrite method to comments = Sequence([....])
        _r = random.randint(0, 10)
        _react = [Reactions_SubFactory() for _ in xrange(_r)]
        return _react

    @sequence
    def comments(p):
        _r = random.randint(0, 10)
        _comm = [Comments_SubFactoy() for _ in xrange(_r)]
        return _comm

    shares = Dict({'count': FuzzyInteger(low=0, high=100)})
    from_user = SubFactory(User_SubFactory)
    to_user = SubFactory(User_SubFactory)
    message = Faker(provider='paragraph', locale='nl_NL', nb_sentences=5, variable_nb_sentences=True)
    picture = Faker(provider='uri')
    name = Faker(provider='sentence', nb_words=6, variable_nb_words=True)
    link = Faker(provider='uri')
    type = FuzzyChoice(['event', 'uri', 'music', 'note', 'photo', 'status', 'video'])
    status_type = FuzzyChoice([None, 'added_photos', 'added_video', 'created_event', 'created_note', 'mobile_status_update', 'published_story', 'shared_story', 'wall_post'])
    story = Faker(provider='sentence', nb_words=6, variable_nb_words=True)


if __name__ == '__main__':
    # @profile()
    def test():
        r = FbPost_Factory.create_batch(10)
        pprint.pprint(r)


    test()
