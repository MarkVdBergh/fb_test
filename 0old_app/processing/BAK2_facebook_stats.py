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
        id = ObjectId('abcabcabcabc')  # bson it must be a 12-byte input or a 24-character hex string
        return 'xxx'

    @classmethod
    def calculateAnimo(self):
        # A KPI calculated with [W0(share)+W1(like)+ ...]/[avg(???)]
        pass
        return 0


class FbPostStats(Fbstats):
    # probably useless to have class inheritance for page stats. Not much in common with the other classes
    # ToDo: solve missing keys in facebook documents.
    # Update a standard facebook document with default valus for the required fields?
    # Then I don't need to check for each key if it exists.
    # Drop unnecessary fields to have leaner (faster) document
    # ToDo: add a key 'own_comment' to count how many times the pageowner commented/replied
    # Interesting for discussion ratio


    def __init__(self, fb_document):
        self.fb_document = fb_document
        super(FbPostStats, self).__init__()
        self.make_post_stats_document()

    # @timecall()
    # @coverage
    # @profile()
    def make_post_stats_document(self):
        '''
        Receives a facebook post document returns a page stats document
        :param fb_document:
        :return:
        '''
        # Why arrays iso int for stats? Consistency with the other statsclas pages?
        self.post_stats_doc = {'id': '',  # str: Generated id
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
        _metadata = self._make_metadata()
        self.post_stats_doc.update(_metadata)
        # stat
        self.post_stats_doc['stats']['tn_share'] = self.fb_document.get('shares', {}).get('count',0)  # same as 'fb_document['shares']['count'] but will not raise error if no key.
        # stat/reaction
        if self.fb_document['reactions']:
            reacts = self._make_reactions_stats()
            self.post_stats_doc['stats'].update(reacts)  # update, because not all reactions present in all documents
        # stat/comments
        if self.fb_document['comments']:
            comms = self._make_comments_stats()
            self.post_stats_doc['stats'].update(comms)
        users = self._make_users_stats()
        self.post_stats_doc['stats'].update(users)

        return self.post_stats_doc

    def _make_metadata(self):
        _id = self.makeId()
        _pageid = self.fb_document['profile']['id']
        _postid = self.fb_document['id']
        _created_dt = mt.timestamp_to_datetime(self.fb_document['created_time']),
        _updated_dt = mt.utc_now()
        _type = self.fb_document['type']
        metadata = {'id': _id, 'pageid': _pageid, 'postid': _postid, 'created_dt': _created_dt, 'updated_dt': _updated_dt, 'type': _type}
        return metadata

    def _make_reactions_stats(self):
        reaction = {'reactions': {}, 'tn_reaction': 0}
        _df_reac = pd.DataFrame(self.fb_document['reactions'])[['id', 'type']]
        # n_reactions
        _df_reac['type'] = _df_reac['type'].str.lower()  # LIKE->like
        _dfg = _df_reac.groupby(['type']).count()
        _fb_reacts = _dfg.to_dict()['id']
        _n_reactions = {'n_' + k: _fb_reacts[k] for k in _fb_reacts}  # Rename the keys (like -> n_like)
        # u_reaction
        _df_reac['type'] = _df_reac['type'].str.lower()
        _dfg = _df_reac.groupby(['type'])  # tuple of (str,df)
        _react = {_react[0]: [r for r in _react[1]['id']] for _react in _dfg}  # _react is a tuple (type, series). r is the string id from the user
        _u_reactions = {'u_' + k: _react[k] for k in _react}  # Rename the keys (like -> n_like)
        reaction['reactions'].update(_n_reactions)
        reaction['reactions'].update(_u_reactions)
        reaction['tn_reaction'] = sum(_n_reactions.values())
        return reaction

    def _make_comments_stats(self):
        comment = {'comments':{}}
        _df_comm = pd.DataFrame(self.fb_document['comments'])
        comment['tn_comment_like'] = _df_comm['like_count'].sum()
        comment['tn_comment'] = _df_comm.shape[0]
        # comment
        comment['comments']['comment_id'] = _df_comm['id'].tolist()
        comment['comments']['comment_dt'] = pd.to_datetime(_df_comm['created_time'].tolist(), utc=True, unit='s')
        comment['comments']['u_comment'] = [comm['from']['id'] for comm in self.fb_document['comments']]
        comment['comments']['n_comment_like'] = _df_comm['like_count'].tolist()
        # users that liked a comment
        _likes = _df_comm['likes'].dropna()
        _lst = []
        [_lst.extend(map(lambda x: x['id'], _lks['data'])) for _lks in _likes]  # Updates the list 'lst'
        comment['comments']['u_comment_like'] = _lst
        return comment

    def _make_users_stats(self):
        # Todo: Example problem: post 53668151866_143877720555. There are only 'u_like' reactions, so it crashes on other keys
        keys = ['u_like', 'u_love', 'u_haha', 'u_wow', 'u_sad', 'u_angry']  # ToDo: Rewrite this method!!! Don't hard-code the reaction-types.
        keys = ['u_like']
        user = {}
        user['u_unique_comment'] = list(set(self.post_stats_doc['stats']['comments']['u_comment']))
        _u_reac = []  # combining all users that like, wow, ...
        [_u_reac.extend(self.post_stats_doc['stats']['reactions'][k]) for k in keys]  # ToDo: Rewrite this method ??? Not consistent. Only this method uses self.post_stats_doc
        user['u_unique_like'] = list(set(_u_reac + self.post_stats_doc['stats']['comments']['u_comment']))
        user['u_unique'] = list(set(user['u_unique_comment'] + user['u_unique_like']))
        user['n_unique_comment'] = len(user['u_unique_comment'])
        user['n_unique_like'] = len(user['u_unique_like'])
        user['n_unique'] = len(user['u_unique'])
        return {'users': user}


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
