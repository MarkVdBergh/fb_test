from pprint import pprint

from mongoengine import *

connect('politics')

class Test(DynamicDocument):
    s1=StringField()
    l1=ListField()


    @queryset_manager
    def freq(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        q=queryset.limit(10)
        q=queryset.filter(q_obj=q)
        print q.__len__()
        print type( q), type(queryset)
        print q.count()
        q=q.limit(2)
        return q
    meta={'collection':'facebook'}

ts1=Test.objects.filter(from__id='345644812211706').filter(type='link')
ts1=ts1.limit(3)

pprint(ts1._query)
print ts1
# ts2=Test.freq
# print ts2.message
for t in  ts1.limit:
    print t.type, t.id
    pass
    # print t.created_time
    # pprint(t.message)


#
# class C(DynamicEmbeddedDocument):
#
#     pass
#
#
# class FbTest(DynamicDocument):
#     comments = EmbeddedDocumentListField
#     id = StringField()
#     _id = ObjectIdField()
#     created_time = DateTimeField()
#     fromwho=DictField(db_field='from')
#     meta = {'collection': 'facebook'}
#
#
# pageid = '345644812211706'
#
# f=FbTest
# fo=f.objects(flag=0)
# print fo
#
#
# f=FbTest.objects.first()
# print f.fromwho
# pass
#
# for f in FbTest.objects(fromid=pageid):
#     print f['_id']
#     print f.id
#     print f.comments
