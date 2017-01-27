from __future__ import absolute_import

import pprint
import unittest

from tools.development_tools import object_info

from app.database.facebook_objects import FbRawPosts


class Test_FbRawPosts(unittest.TestCase):
    @unittest.skip('Need to implement <set_collection>')
    def test_set_collection(self):
        rawpost = FbRawPosts()
        self.assertEqual(rawpost.meta, {'collection': 'facebook'})
        self.assertNotEqual(rawpost.meta, {'collection': 'temp'})

    @unittest.skip('Need to improve <flatten_post>')
    def test_flatten_post(self):
        rawpost = FbRawPosts()
        post = {'a': [0, 1], 'b': [{'c': 3, 'd': 4}], 'e': {'f': 1, 'g': 2}}
        fp = rawpost.flatten_post(post)
        fp_expect = {'a': [0, 1], 'b': [{'c': 3, 'd': 4}], 'e_g': 2, 'e_f': 1}
        self.assertDictEqual(fp, fp_expect)
        post = {'a': 1, 'b': {'c': 2, 'd': {'e': 3, 'f': 4}}}
        fp = rawpost.flatten_post(post)
        fp_expect = {'a': 1, 'b_c': 2, 'b_d_e': 3, 'b_d_f': 4}
        self.assertDictEqual(fp, fp_expect)
        post = {'a': 1, 'b': [{'c': 2, 'd': {'e': 3, 'f': 4}}]}
        fp = rawpost.flatten_post(post)
        fp_expect = {'a': 1, 'b':[{'c': 2, 'd_f': 4, 'd_e': 3}]}
        self.assertDictEqual(fp, fp_expect)


if __name__ == '__main__':
    unittest.main()
