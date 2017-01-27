import pandas as pd
from profilehooks import profile, coverage, timecall

from database.facebook_queries import *
from tools.general_tools import MyTools as mt


class Fbstats(object):
    def __init__(self):
        pass

    def makeId(cls):  # cls ???  automatically when @classmethod
        # classmethod to make my own id to use in other documents as refference to this document. Also for easier find?
        # class has the class variables from Master class and Parent class: documents, status_df and xxx
        # id = ObjectId('abcabcabcabc')  # bson it must be a 12-byte input or a 24-character hex string
        return 'xxx'

    @classmethod
    def calculateAnimo(self):
        # A KPI calculated with [W0(share)+W1(like)+ ...]/[avg(???)]
        pass
        return 0


class FbPostStats(Fbstats):
    # probably useless to have class inheritance for page stats. Not much in common with the other classes

    # ToDo: add a key 'own_comment' to count how many times the pageowner commented/replied
    # Interesting for discussion ratio

    # ToDo: make this class inherit 'dict'. http://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
    # Now its just a function accessible by a class again

    def __init__(self, fb_document):
        self.fb_doc = fb_document
        super(FbPostStats, self).__init__()
        self.make_post_stats_document()

    # @timecall()
    # @coverage
    # @profile()
    def make_post_stats_document(self):
        # ToDo: This is just a mess
        # Restructure so that df.to_dict or df.to_json gives the right mongo doc ???

        # Why arrays iso int for stats? Consistency with the other statsclas pages?
        post_stats_doc = {'id': '',  # str: Generated id
                          'pageid': 'xxx',  # str: Facebook page id ('xxxxxxx')
                          'postid': 'xxx',  # str: Facebook post id ('xxxxxxx_yyyyy')
                          'created_dt': -9,  # int: Facebook timestamp time when post was posted
                          'updated_dt': -9,  # int: timestamp time when the document was last updated
                          'type': 'xxx',  # str: Facebook post type ('photo', 'link', ...)
                          'stats': {'tn_share': 0,  # int: the nr of people the post was shared
                                    'tn_reaction': 0,  # int: the nr of times the post was reacted. This is the sum of all reactions
                                    'tn_comment': 0,  # int: the nr of times the post was commented
                                    'tn_comment_like': 0,  # int: the nr of times the post comments were liked
                                    'n_unique': 0,  # int: the number of unique people that reacted to the post, commented or liked a comment
                                    'n_unique_comment': 0,  # int: list of unique people that commented to the post
                                    'n_unique_like': 0,  # int: list of unique users that reacted to the post or liked a comment
                                    'reactions': {'n_like': 0,  # int: the nr of times the post was liked
                                                  'n_love': 0,  # int: the nr of times the post was loved
                                                  'n_haha': 0,  # int: the nr of times the post was haha-ed
                                                  'n_wow': 0,  # int: the nr of times the post was wowed
                                                  'n_sad': 0,  # int: the nr of times the post was saded
                                                  'n_angry': 0,  # int: the nr of times the post was angried
                                                  'u_like': [],  # list of str: the Facebook id of the users that liked the post
                                                  'u_love': [],  # list of str: the Facebook id of the users that loved the post
                                                  'u_haha': [],  # list of str: the Facebook id of the users that haha-ed the post
                                                  'u_wow': [],  # list of str: the Facebook id of the users that wowed the post
                                                  'u_sad': [],  # list of str: the Facebook id of the users that saded the post
                                                  'u_angry': [],  # list of str: the Facebook id of the users that angy-edthe post
                                                  },
                                    'comments': {'comment_id': [],  # list of str: list of the Facebook comments ids
                                                 'comment_dt': [],  # list of datetime: list of times a comment was made
                                                 'u_comment': [],  # list of str: the Facebook ids of the users that commented
                                                 'n_comment_like': [],  # list of int: list of the nr of times the comment was liked
                                                 'u_comment_like': []  # list of str: list with Facebook id from the users that liked a comment
                                                 },
                                    'users': {'u_unique': [],  # list of str: list of Facbook ids of unique people that reacted to the post, commented or liked a comment
                                              'u_unique_comment': [],  # list of str: list of Facbook ids of unique people that commented to the post
                                              'u_unique_like': [],  # list of str: list of Facbook ids of unique users that reacted or liked a comment
                                              }, },
                          'ratios': {'animo': 0,  # int:
                                     'impact': 0,  # int:
                                     'discussion': 0  # int: f(n_comments, u_unique_comment, own_comment).
                                     }, }
        # metadata
        post_stats_doc['id'] = self.makeId()
        post_stats_doc['pageid'] = self.fb_doc['profile']['id']
        post_stats_doc['postid'] = self.fb_doc['id']
        # post_stats_doc['created_dt'] = mt.timestamp_to_datetime(self.fb_doc['created_time']),
        # post_stats_doc['updated_dt'] = mt.utc_now()
        post_stats_doc['type'] = self.fb_doc['type']

        # stat
        post_stats_doc['stats']['tn_share'] = self.fb_doc.get('shares', {}).get('count', 0)  # = fb_document['shares']['count'] but will not raise error if no key.

        # stat/reaction
        if self.fb_doc['reactions']:  # <> []
            _df_reac = pd.DataFrame(self.fb_doc['reactions'])[['id', 'type']]
            _df_reac['type'] = _df_reac['type'].str.lower()  # LIKE->like
            _dfg = _df_reac.groupby(['type'])  # tuple of (str,df)
            # n_reactions
            _fb_reactions = _dfg.count().to_dict()['id']
            # Maybe better df['type'] = 'n_'+df['type'] ????
            _n_reactions = {'n_' + k: _fb_reactions[k] for k in _fb_reactions}  # Rename the keys (like -> n_like)
            # u_reaction
            # ToDo: Check if this puts the user ids with correct keys
            _u_reactions = {'n_' + _react[0]: [r for r in _react[1]['id']] for _react in _dfg}  # _react is a tuple (type, series). r is the string id from the user
            # Update otherwise I overwrite the ['stats']['connections']
            post_stats_doc['stats']['reactions'].update(_n_reactions)
            post_stats_doc['stats']['reactions'].update(_u_reactions)
            post_stats_doc['stats']['tn_reaction'] = sum(_n_reactions.values())

        # stat/comments
        if self.fb_doc['comments']:
            _df_comm = pd.DataFrame(self.fb_doc['comments'])
            post_stats_doc['stats']['tn_comment_like'] = _df_comm['like_count'].sum()
            post_stats_doc['stats']['tn_comment'] = _df_comm.shape[0]
            # comment
            post_stats_doc['stats']['comments']['comment_id'] = _df_comm['id'].tolist()
            # DATE PROBLEM !!!! (timestamp)
            # post_stats_doc['stats']['comments']['comment_dt'] = pd.to_datetime(_df_comm['created_time'], box=True,utc=True, unit='s').tolist()
            post_stats_doc['stats']['comments']['u_comment'] = [comm['from']['id'] for comm in self.fb_doc['comments']]
            post_stats_doc['stats']['comments']['n_comment_like'] = _df_comm['like_count'].tolist()

            try: # UGLY
                # I can also check if fb_doc['comments'][0]['likes'] exists
                # users that liked a comment
                _likes = _df_comm['likes'].dropna()
                _lst = []
                [_lst.extend(map(lambda x: x['id'], _lks['data'])) for _lks in _likes]  # Updates the list 'lst'
                post_stats_doc['stats']['comments']['u_comment_like'] = _lst
            except:
                pass


            # Ugly !!!
            post_stats_doc['stats']['users']['u_unique_comment'] = list(set(post_stats_doc['stats']['comments']['u_comment']))

            # ToDo: MESSY MESSY + Bad naming of variables
        if self.fb_doc['reactions']:
            _reactions = []  # combining all users that like, wow, ...
            [_reactions.extend(u) for u in _u_reactions.values()]
            post_stats_doc['stats']['users']['u_unique_like'] = list(set(_reactions + post_stats_doc['stats']['comments']['u_comment']))
            post_stats_doc['stats']['users']['u_unique'] = list(set(post_stats_doc['stats']['users']['u_unique_comment']+ post_stats_doc['stats']['users']['u_unique_like']))
        post_stats_doc['stats']['n_unique_comment'] = len(post_stats_doc['stats']['users']['u_unique_comment'])
        post_stats_doc['stats']['n_unique_like'] = len(post_stats_doc['stats']['users']['u_unique_like'])
        post_stats_doc['stats']['n_unique'] = len(post_stats_doc['stats']['users']['u_unique'])

        return self.fb_doc


class FbDayStats(Fbstats):
    counter = 0

    def __init__(cls):
        pass
        # te=cls.template

    def test(self):
        self.template


class FbWeekStats(Fbstats):
    pass


class FbMonthStats(Fbstats):
    def __init__(self):
        pass


class FbYearStats(Fbstats):
    def __init__(self):
        pass


if __name__ == '__main__':
    from database.sample_documents import SampleDocuments

    sd = SampleDocuments()
    doc = FbPostStats(sd.facebook_post_1()).make_post_stats_document()

    pprint(doc)
