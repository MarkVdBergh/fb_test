import collections
import pprint

from mongoengine import *
from profilehooks import timecall, profile

connect('politics')


class FbRawPost_profile(EmbeddedDocument):
    name = StringField()
    id = StringField()


class FbRawPost_user(EmbeddedDocument):
    name = StringField()
    id = StringField()


class FbRawPost_reactions(EmbeddedDocument):
    type = StringField()
    id = StringField()
    name = StringField()
    pic = URLField()


class FbRawPost_comments(DynamicEmbeddedDocument):
    id = StringField()
    created_time = IntField()
    comment_from = EmbeddedDocumentField(db_field='from', document_type=FbRawPost_user)
    like_count = IntField()
    comment_count = IntField()
    pass


class FbRawPosts(DynamicDocument):
    # ToDo: Extend the class with additional fields, like picture, name, message, ...
    # ToDo: the field 'created_time_dt' is called 'created_time_local' in some documents !

    """
        Maps facebook Graph Api documents in a FbRawPosts object
        FbRawPosts implements following methods:
        *   flatten_post():

    :cvar pageid The facebook pahe id

    """
    meta = {'collection': 'facebook'}
    # Rename '_id' and 'id'
    id = ObjectIdField(db_field=('_id'), required=True)
    postid = StringField(db_field='id')
    created_time = IntField()
    profile = EmbeddedDocumentField(document_type=FbRawPost_profile)
    reactions = EmbeddedDocumentListField(document_type=FbRawPost_reactions)
    comments = EmbeddedDocumentListField(document_type=FbRawPost_comments)
    shares = DictField()
    message = StringField()
    created_time_dt = DateTimeField()
    created_time_local = DateTimeField()

    def set(self):
        self.meta = 1

    def flatten_post(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flatten_post(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)


# @profile()
@timecall()
def test():
    x = FbRawPosts
    # for i in x.objects(shares__count__gte=10000):
    # This doesn't work ! see: https://docs.mongodb.com/manual/reference/operator/query/size/#_S_size. "create a counter field that you increment when you add elements to a field."
    # for i in x.objects(comments__size__gte=100):
    for i in x.objects(comments__1600__exists=True):
        print '=' * 100
        print 'http://facebook.com/{}'.format(i.postid)
        print('{}:   postid: {}, comments: {}'.format(i.profile.name,i.postid, len(i.comments)))
        print i.created_time_local, i.created_time_dt
        print i.message
        print '=' * 100


test()
