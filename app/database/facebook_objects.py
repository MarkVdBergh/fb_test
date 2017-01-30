import json

import pprint
from mongoengine import *
from profilehooks import timecall

connect('politics')


class FbRawPost_profile(EmbeddedDocument):
    name = StringField()
    id = StringField(required=True, unique=True)

    def __unicode__(self):
        return self.to_json()


class FbRawPost_user(EmbeddedDocument):
    name = StringField()
    id = StringField(required=True, unique=True)

    def __unicode__(self):
        return self.to_json()


class FbRawPost_reactions(EmbeddedDocument):
    type = StringField()
    id = StringField()
    name = StringField()
    pic = URLField()

    def __unicode__(self):
        return self.to_json()


class FbRawPost_comments(DynamicEmbeddedDocument):
    id = StringField()
    created_time = IntField()
    comment_from = EmbeddedDocumentField(db_field='from', document_type=FbRawPost_user)
    like_count = IntField()
    comment_count = IntField()

    def __unicode__(self):
        return self.to_json()


class FbRawPosts(DynamicDocument):
    # ToDo: Extend the class with additional fields, like picture, name, message, ...
    # ToDo: the field 'created_time_dt' is called 'created_time_local' in some documents !

    """
        Maps facebook Graph Api documents in a FbRawPosts object.
        FbRawPost retrieves documents from Mongo or accepts a list of documents (directly from facebook scraper)
        FbRawPosts implements following methods:
        *   flatten_post():

    :cvar pageid The facebook pahe id

    """
    meta = {'collection': 'facebook_tests'}
    # Rename '_id' and 'id'
    id = ObjectIdField(db_field=('_id'), required=True, primary_key=True)
    postid = StringField(db_field='id')
    # created_time = IntField()
    profile = EmbeddedDocumentField(document_type=FbRawPost_profile)
    reactions = EmbeddedDocumentListField(document_type=FbRawPost_reactions)
    comments = EmbeddedDocumentListField(document_type=FbRawPost_comments)
    shares = DictField()
    message = StringField()
    created_time_dt = DateTimeField()
    created_time_local = DateTimeField()

    def __str__(self):
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
    pass

    y = x.objects(shares__count__gte=10000).to_json()
    print(y)


if __name__ == '__main__':
    test()
