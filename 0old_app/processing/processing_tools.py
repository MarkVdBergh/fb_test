import pandas as pd

from tools.general_tools import utc_now


class FacebookPageDailyStatistics():
    def __init__(self, pageid, since, till):
        self.pageid=pageid
        if not since: self.since = 0
        if not till:self.till=utc_now()
        self.all_posts=None
        # Create document template
        day_stat_data_template= {
            'reactions':{
                'like':0,
                'love':0,
                'haha':0,
                'wow':0,
                'sad':0,
                'angry':0},
            'comments':{
                'nr':0,
                'likes':0}
            }

        day_stat={'{i}':day_stat_template for i in range(1,32)}
        self.doc={
            'id':pageid,
            'date':0,
            'day_stats':day_stat}
        pass

    def calculate_posts_per_day(self):
        pass




class FacebookPostStatistics():
    def __init__(self):
        pass

    def calc_likes_from_post(self, post):
        """
        Receives a post dict
        The funcion returns a dict:
        :param post: dict
        :return likes: dict
        """
        postlikes = len(post['likes'])
        comments = post['comments']
        commentslikes = 0
        if comments:  # not empty
            # DataFrame to avoid iterating over each comment
            commentsdf = pd.DataFrame(comments)
            commentslikes = commentsdf['like_count'].sum()
        likes = {'post_likes': postlikes, 'comments_likes': commentslikes}
        return likes

    def calc_reactions_from_post(self, post):
        reactions = post['reactions']

        if reactions:
            reactionsdf = pd.DataFrame(reactions)
            reactionsdf['type'] = reactionsdf['type'].str.lower()  # make the reactiontype lowercase
            # print reactionsdf['type']
            # print type(reactionsdf['type'])
            # add a count column
            reactionsdf['count'] = 1
            reactioncount = reactionsdf[['type', 'count']].groupby('type').count()
            reactions = reactioncount['count'].to_dict()
            # reactions['_id'] = post['_id']
            return reactions

    def calc_shares_from_posts(self, post):
        if 'shares' in post.keys():
            shares = post['shares']['count']
        else:
            shares = 0
        return {'shares': shares}
