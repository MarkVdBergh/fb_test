from __future__ import absolute_import

import pprint
import unittest

from mongoengine import connect

from app.database.facebook_objects_factory import FbPost_Factory
from tools.development_tools import object_info

from app.database.facebook_objects import FbPost


# ToDo: Test for min/max fields (timestamp)
class Test_FbRawPosts(object):
    """ Base class for testing FbRawPost class"""

    def test_set_collection(self):
        rawpost = FbPost()
        # self.assertEqual(rawpost.meta, {'collection': 'facebook'})
        # self.assertNotEqual(rawpost.meta, {'collection': 'temp'})

    def test_keyname_input_convertion(self):
        ''' _id->id, id->postid'''
        pass

    # def test_keyname_output_convertion(self):
    #     ''' _id->id, id->postid'''
    #     pass

    def test_empty_document(self):
        pass


class Test_FbRawPosts_Mongo(unittest.TestCase, Test_FbRawPosts):
    '''
        Unittest for testing crud on MongoDb
    '''
    def setUp(self):
        # connect(db='test')
        FbPost_Factory.create_batch(1)
        pass

    def tearDown(self):
        # FbPost.drop_collection()
        pass


class Test_FbRawPosts_DictList(unittest.TestCase, Test_FbRawPosts):
    # def setUp(self):
    #     pass
    #
    # def tearDown(self):
    #     pass
    pass

if __name__ == '__main__':
    unittest.main()
