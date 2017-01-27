import pandas as pd

from database.facebook_queries import *
from tools.general_tools import MyTools as mt


class Fbstats(object):
    xxx = 888
    status_df = None

    def __init__(self):
        self.xxxxxxxx = {'pageid': 0,
                         'id': 'xxx',
                         'updated': 0,
                         'stats': {'share': [0],
                                   'like': [0],
                                   'love': [0],
                                   'haha': [0],
                                   'wow': [0],
                                   'sad': [0],
                                   'angry': [0],
                                   'comment': [0],
                                   'comment_like': [0],
                                   'animo': [0],
                                   'type': ['x']},  # A KPI calculated with [W0(share)+W1(like)+ ...]/[avg(???)]
                         'people': {'share': [0],
                                    'like': [0],
                                    'love': [0],
                                    'haha': [0],
                                    'wow': [0],
                                    'sade': [0],
                                    'angry': [0],
                                    'comment': [0],
                                    'comment_like': [0],

                                    }

                         }

    @classmethod
    def makeId(cls):  # cls ???  automatically when @classmethod
        # classmethod to make my own id to use in other documents as refference to this document. Also for easier find?
        # class has the class variables from Master class and Parent class: documents, status_df and xxx

        id = ObjectId('abcabcabcabc')  # bson it must be a 12-byte input or a 24-character hex string
        print id
        return 'xxx'

    @classmethod
    def calculateAnimo(self):
        # A KPI calculated with [W0(share)+W1(like)+ ...]/[avg(???)]
        pass
        return 0

    @classmethod
    def calculateUniquePeople(self):
        pass
        return 0


class FbPostStats(Fbstats):
    # ToDo: rename and reorder the document, variables and methods
    # ToDo: replace dict[key] with dict.get(key, default). Default when key doesn't exist
    # probably useless to have class inheritance for page stats. Not much in common with the other classes
    documents = []

    def __init__(self, fb_document):
        self.fb_document = fb_document
        super(FbPostStats, self).__init__()
        self.make_post_stats_document()

    def make_post_stats_document(self):
        '''
        Receives a facebook post document returns a page stats document
        :param fb_document:
        :return:
        '''
        # Why arrays iso int for stats? Consistency with the other statsclas pages?
        post_stats_doc = {'id': '',  # str: Generated id
                          'pageid': 'xxx',  # str: Facebook page id ('xxxxxxx')
                          'postid': 'xxx',  # str: Facebook post id ('xxxxxxx_yyyyy')
                          'created_dt': -9,  # int: Facebook timestamp time when post was posted
                          'updated_dt': -9,  # int: timestamp time when the document was last updated
                          'type': 'xxx',  # str: Facebook post type ('photo', 'link', ...)
                          'stat': {'tn_share': -1,  # int: the nr of people the post was shared
                                   'tn_reaction': -1,  # int: the nr of times the post was reacted. This is the sum of all reactions
                                   'tn_comment': -1,  # int: the nr of times the post was commented
                                   'tn_comment_like': -1,  # int: the nr of times the post comments were liked

                                   'reaction': {'n_like': -1,  # int: the nr of times the post was liked
                                                'n_love': -1,  # int: the nr of times the post was loved
                                                'n_haha': -1,  # int: the nr of times the post was haha-ed
                                                'n_wow': -1,  # int: the nr of times the post was wowed
                                                'n_sad': -1,  # int: the nr of times the post was saded
                                                'n_angry': -1,  # int: the nr of times the post was angried
                                                'u_like': ['xxx'],  # list of str: the Facebook id of the users that liked the post
                                                'u_love': ['xxx'],  # list of str: the Facebook id of the users that loved the post
                                                'u_haha': ['xxx'],  # list of str: the Facebook id of the users that haha-ed the post
                                                'u_wow': ['xxx'],  # list of str: the Facebook id of the users that wowed the post
                                                'u_sad': ['xxx'],  # list of str: the Facebook id of the users that saded the post
                                                'u_angry': ['xxx'],  # list of str: the Facebook id of the users that angy-edthe post
                                                },
                                   'comment': {'comment_id': ['xxx'],  # list of str: list of the Facebook comments ids
                                                'comment_dt': [-9],  # list of datetime: list of times a comment was made
                                                'u_comment': ['xxx'],  # list of str: the Facebook ids of the users that commented
                                                'n_comment_like': [-1],  # list of int: list of the nr of times the comment was liked
                                                'u_comment_like': ['xxx']  # list of str: list with Facebook id from the users that liked a comment
                                                },
                                   'user': {
                                       'u_unique': ['xxx'],  # list of int: the number of unique people that reacted to the post, commented or liked a comment
                                       'u_unique_comment': ['xxx'],  # list of int: list of unique people that commented to the post
                                       'u_unique_like': ['xxx'],  # list of int: list of unique users that reacted or liked a comment
                                       'n_unique': ['xxx'],  # list of int: the number of unique people that reacted to the post, commented or liked a comment
                                       'n_unique_comment': ['xxx'],  # list of int: list of unique people that commented to the post
                                       'n_unique_like': ['xxx'],  # list of int: list of unique users that reacted or liked a comment
                                   }, },
                          'ratio': {'animo': 0,  # int:
                                    'impact': 0,  # int:
                                    'discussion': 0  # int: f(n_comments, u_unique_comment).
                                    }, }

        _metadata = self._make_metadata()
        post_stats_doc.update(_metadata)
        _stat = self._make_stat()
        post_stats_doc['stat'].update(_stat)
        pprint(post_stats_doc)
        return 0

    def _make_stat(self):
        _df_comm = pd.DataFrame(self.fb_document['comments'])
        _df_reac = pd.DataFrame(self.fb_document['reactions'])[['id', 'type']]
        stat = {'reaction': {}, 'comment': {}, 'user': {}}

        stat['tn_share'] = self.fb_document.get('shares', {}).get('count', 0)  # is the same as 'fb_document['shares']['count'] but will not raise error if no key.
        stat['tn_comment_like'] = _df_comm['like_count'].sum()
        stat['tn_comment'] = _df_reac.shape[0]
        # n_reactions
        _df_reac['type'] = _df_reac['type'].str.lower()
        _dfg = _df_reac.groupby(['type']).count()
        _fb_reacts = _dfg.to_dict()['id']
        _n_reactions = {'n_' + k: _fb_reacts[k] for k in _fb_reacts}  # Rename the keys (like -> n_like)
        # u_reaction
        _df_reac['type'] = _df_reac['type'].str.lower()
        _dfg = _df_reac.groupby(['type'])  # tuple of (str,df)
        _react = {_react[0]: [r for r in _react[1]['id']] for _react in _dfg}  # _react is a tuple (type, series). r is the string id from the user
        _u_reactions = {'u_' + k: _react[k] for k in _react}  # Rename the keys (like -> n_like)
        stat['reaction'].update(_n_reactions)
        stat['reaction'].update(_u_reactions)
        stat['tn_reaction'] = sum(_n_reactions.values())

        # comment
        stat['comment']['comment_id'] = _df_comm['id'].tolist()
        stat['comment']['comment_dt'] = pd.to_datetime(_df_comm['created_time'].tolist(), utc=True,unit='s')
        stat['comment']['u_comment'] = [comm['from']['id'] for comm in self.fb_document['comments']]
        stat['comment']['n_comment_like'] = _df_comm['like_count'].tolist()
        # users that liked a comment
        _likes = _df_comm['likes'].dropna()
        _lst = []
        [_lst.extend(map(lambda x: x['id'], _lks['data'])) for _lks in _likes]  # Updates the list 'lst'
        stat['comment']['u_comment_like'] = _lst

        # user
        stat['user']['u_unique_comment'] = list(set(stat['comment']['u_comment']))
        _u_reac = []
        [_u_reac.extend(u) for u in _u_reactions.values()]
        stat['user']['u_unique_like'] = list(set(_u_reac + stat['comment']['u_comment']))
        stat['user']['u_unique'] = list(set(stat['user']['u_unique_comment'] + stat['user']['u_unique_like']))
        stat['user']['n_unique_comment'] = len(stat['user']['u_unique_comment'])
        stat['user']['n_unique_like'] = len(stat['user']['u_unique_like'])
        stat['user']['n_unique'] = len(stat['user']['u_unique'])
        return stat

    def _make_metadata(self):
        _id = self.makeId()  # what is self when classmethod is used ????
        _pageid = self.fb_document['profile']['id']
        _postid = self.fb_document['id']
        _created_dt = mt.timestamp_to_datetime(self.fb_document['created_time']),
        _updated_dt = mt.utc_now()
        _type = self.fb_document['type']
        metadata = {'id': _id, 'pageid': _pageid, 'postid': _postid, 'created_dt': _created_dt, 'updated_dt': _updated_dt, 'type': _type}
        return metadata


from  database.sample_documents import SampleDocuments as SD

fbp = SD.facebook_post()
ps = FbPostStats(fbp)
ps.make_post_stats_document()


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
