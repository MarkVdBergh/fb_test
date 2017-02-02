import pprint
# from mongoengine import *
from mongoengine import connect, EmbeddedDocument, StringField, DictField, BooleanField, URLField, DynamicEmbeddedDocument, IntField, EmbeddedDocumentField, \
    EmbeddedDocumentListField, DynamicDocument, ObjectIdField, register_connection
from profilehooks import timecall

# Register MongoDb databases
from app.settings import TESTING

register_connection(alias='test', name='test')
register_connection(alias='default', name='xxx')


# ToDo: connect() seems unecessary. It uses the default db automatically
# connect(db='test')
# connect('xxx')


class Profile(EmbeddedDocument):
    id = StringField(required=True)
    name = StringField()


class User(EmbeddedDocument):
    id = StringField(required=False)
    name = StringField()
    link = StringField()
    picture = DictField(data={'url': StringField(),
                              'is_silhouette': BooleanField()})


class Reactions(EmbeddedDocument):
    id = StringField()
    type = StringField()
    name = StringField()
    pic = URLField()


# ToDo: Why Dynamic?
class Comments(DynamicEmbeddedDocument):
    id = StringField()
    created_time = IntField()
    comment_from = EmbeddedDocumentField(db_field='from', document_type=User)
    message = StringField()
    likes = DictField(data=EmbeddedDocumentListField(document_type=User))
    like_count = IntField()
    comment_count = IntField()


class FbPost(DynamicDocument):
    # Tweak: Extend the class with additional fields, like picture, name, message, ...
    # ToDo: Rename class variables
    # ToDo: Add indexes
    """
        Maps facebook Graph Api documents in a FbPost object.
        FbRawPost retrieves documents from Mongo or accepts a list of documents (directly from facebook scraper)
        FbPost implements following methods:
        *   flatten_post():

    :cvar pageid The facebook pahe id

    """
    # meta={}
    meta = {'collection': 'facebook'}  # Otherwise documents will be saved in the 'fb_post' collection. (Default collection is classname in smallcaps
    if TESTING:  # Swith to the test database, otherwise use default one.
        meta['db_alias'] = 'test'

    id = ObjectIdField(db_field=('_id'), required=True, primary_key=True)
    created_time = IntField(min_value=1041379200, max_value=2524608000)
    postid = StringField(db_field='id')
    profile = EmbeddedDocumentField(document_type=Profile)
    reactions = EmbeddedDocumentListField(document_type=Reactions)
    comments = EmbeddedDocumentListField(document_type=Comments)
    shares = DictField()
    from_user = EmbeddedDocumentField(document_type=User, default=User())
    to_user = EmbeddedDocumentField(document_type=User, default=User())
    message = StringField()
    picture = StringField()
    name = StringField()
    link = StringField()
    type = StringField()
    status_type = StringField()
    story = StringField()

    def __unicode__(self):
        return self.to_json()


# @profile()
@timecall()
def test():
    x = FbPost
    # for i in x.objects(shares__count__gte=13000):
    # This doesn't work ! see: https://docs.mongodb.com/manual/reference/operator/query/size/#_S_size. "create a counter field that you increment when you add elements to a field."

    # for i in x.objects(comments__size__gte=100):
    # for i in x.objects(comments__1600__exists=True):
    #     print '=' * 100
    #     print 'http://facebook.com/{}'.format(i.postid)
    #     print('{}:   postid: {}, comments: {}'.format(i.profile.name,i.postid, len(i.comments)))
    #     print i.created_time_local, i.created_time_dt
    #     print i.message
    #     print '=' * 100



    # j=json.dumps({'id':9999,'profile':{'id':100,'name':'MMMM'}})
    # y=x.from_json(j)
    # print y.to_json()
    # x.set_collection('facebook_test')
    # y = x.objects(shares__count__gte=10000)
    print (type(x))
    y = x.objects.count()
    pprint.pprint(y)


if __name__ == '__main__':
    test()
