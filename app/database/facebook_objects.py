import collections
import pprint

from mongoengine import *

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
    comment_count=IntField()
    pass



class FbRawPosts(DynamicDocument):
    # ToDo: Extend the class with additional fields, like picture, name, message, ...
    """
        Maps facebook Graph Api documents in a FbRawPosts object
        FbRawPosts implements following methods:
        *   flatten_post():

    """
    meta = {'collection': 'facebook'}
    # Rename '_id' and 'id'
    id = ObjectIdField(db_field=('_id'), required=True)
    pageid = StringField(db_field='id')
    created_time = IntField()
    profile = EmbeddedDocumentField(document_type=FbRawPost_profile)
    reactions = EmbeddedDocumentListField(document_type=FbRawPost_reactions)
    comments = EmbeddedDocumentListField(document_type=FbRawPost_comments)
    pass

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

x=FbRawPosts
for i in x.objects:
    for j in i.comments:
        print(j.message)
