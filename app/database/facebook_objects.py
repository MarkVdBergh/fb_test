import json

import pprint
from mongoengine import *
from mongoengine.base import EmbeddedDocumentList
from profilehooks import timecall

from app.settings import TESTING

connect(db='test')


class FbRawPost_profile(EmbeddedDocument):
    id = StringField(required=True)
    name = StringField()

    # def __unicode__(self):
    #     return self.to_json()


class FbRawPost_user(EmbeddedDocument):
    id = StringField(required=False)
    name = StringField()
    link = StringField()
    picture = DictField(data={'url': StringField(),
                              'is_silhouette': BooleanField()})
    pic = StringField()

    # def __unicode__(self):
    #     return self.to_json()


class FbRawPost_reactions(EmbeddedDocument):
    id = StringField()
    type = StringField()
    name = StringField()
    pic = URLField()

    # def __unicode__(self):
    #     return self.to_json()


class FbRawPost_comments(DynamicEmbeddedDocument):
    id = StringField()
    created_time = IntField()
    comment_from = EmbeddedDocumentField(db_field='from', document_type=FbRawPost_user)
    message = StringField()
    likes = DictField(data=EmbeddedDocumentListField(document_type=FbRawPost_user))
    # likes = {'data':EmbeddedDocumentListField(document_type=FbRawPost_user)}
    like_count = IntField()
    comment_count = IntField()

    # def __unicode__(self):
    #     return self.to_json()


class FbRawPosts(DynamicDocument):
    # Tweak: Extend the class with additional fields, like picture, name, message, ...
    # ToDo: Rename class variables
    # ToDo: Add indexes
    """
        Maps facebook Graph Api documents in a FbRawPosts object.
        FbRawPost retrieves documents from Mongo or accepts a list of documents (directly from facebook scraper)
        FbRawPosts implements following methods:
        *   flatten_post():

    :cvar pageid The facebook pahe id

    """

    meta = {'collection': 'facebook'}
    # def __new__(cls, collection='facebookx'):
    #     cls.meta = {'collection': collection}
    #     super(FbRawPosts,cls)

    id = ObjectIdField(db_field=('_id'), required=True, primary_key=True)
    created_time = IntField(min_value=1041379200, max_value=2524608000)
    postid = StringField(db_field='id')
    profile = EmbeddedDocumentField(document_type=FbRawPost_profile)
    reactions = EmbeddedDocumentListField(document_type=FbRawPost_reactions)

    comments = EmbeddedDocumentListField(document_type=FbRawPost_comments)

    shares = DictField()
    from_user = EmbeddedDocumentField(document_type=FbRawPost_user, default=FbRawPost_user())
    to_user = EmbeddedDocumentField(document_type=FbRawPost_user, default=FbRawPost_user())
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
    x = FbRawPosts
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
    print type(x)
    y = x.objects.count()
    pprint.pprint(y)


if __name__ == '__main__':
    test()
