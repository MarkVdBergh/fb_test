from pprint import pprint

from mongoengine import *
from mongoengine import queryset

connect('politics')


class FbPost(DynamicDocument):
    # Need this to make a difference between 'id' and '_id'
    id = StringField()
    _id = ObjectIdField()

    @queryset_manager
    def get_all_for_page(doc_cls, queryset, pageid):
        queryset = queryset.filter(profile__id=pageid)
        return queryset

    @queryset_manager
    def get_all_for_date(doc_cls, queryset, date):
        pass

    @queryset_manager
    def get_all_for_slice(doc_cls, queryset, slice=[0, 0]):
        queryset = queryset[slice[0]: slice[1]]
        return queryset

    meta = {'collection': 'facebook'}


class Page(Document):
    pageid = StringField(required=True, unique=True)
    pass
    # meta = {'collection': 'fb_statistics'}



class User(Document):
    pass


class FbStatistics(Document):
    page = ReferenceField(Page, required=True)
    meta = {'allow_inheritance': True}


class PostStat(FbStatistics):
    x = IntField()

    pass


class DayStat(FbStatistics):
    y = IntField()
    pass


if __name__ == '__main__':
    page = Page.objects(pageid='62130106444').first()
    # page.save()
    post = PostStat(page=page,x=0)
    day = DayStat(page=page, y=0)
    print post.to_mongo()
    # print page.to_mongo()
    post.save()
    # day.save()



    # fbp = FbPost.objects.only('created_time','comments').filter(id=0)
    # fbp = FbPost.get_all_for_page(pageid='62130106444')
    # fbp = FbPost.get_all_for_slice(slice=[0, 1000])
    #
    #
    # print type(fbp)
    # # print fbp.comments
    # # print fbp.id
    # pprint(fbp.count())
    #
    # for f in fbp:
    #     print f._id,   f.comments
    # for p in fbp:
    #     print(p.comments)
    #     print len(p.comments)
    #     print p['id']
