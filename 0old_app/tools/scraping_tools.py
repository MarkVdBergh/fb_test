import datetime
import facebook
import requests
import time
from pymongo import MongoClient

from settings import FB_APP_ID, FB_APP_SECRET
from tools.general_tools import datetime_to_timestamp, timestamp_to_yyyymmdd, utc_now, save_blacklist_doc, \
    get_blacklist, is_blacklisted, save_log, timestamp_to_datetime


class FacebookScraping():
    def __init__(self, access_token):
        self.graph = facebook.GraphAPI(access_token=access_token, version='2.8')
        self.access_token = access_token
        self.blacklist = get_blacklist()

    def get_page_profile(self, id):
        """
        Returns the profile of the page, group or user
        :param id: string
        the unique id of the page, group or user

        :return: dict
        the returned profile has the form {u'name': u'Geert Wilders', u'id': u'202064936858448'}
        """
        # ToDo: check if more information is available besides name and id
        profile = self.graph.get_object(id)
        return profile

    def get_all_posts(self, page_id, fields='all', since=None, until=None, limit=100):
        """
        Gets all posts on a page, group or user
        :param page_id: string
        The unique id of the page, group or user
        :param fields: comma separated string, 'all', None
        A description of all fields can be found at: https://developers.facebook.com/docs/graph-api/reference/v2.8/post/
        Can be:
            - Comma separated string: with all fields that need to be retrieved.
            - 'all': comma separated string with default fields
            - None: facebook default fields

        :return: dict
        """
        if fields == 'all':
            # For a list of fields, see:
            # https://developers.facebook.com/docs/graph-api/reference/v2.8/post/
            fields = 'id, name,created_time, from, to, type, status_type, message, link, picture, story, shares'  # , likes,reactions'
            # ToDo: get_connections vs Get_objects. How to use limit

        chunk = self.graph.get_connections(page_id, connection_name='posts', fields=fields, date_format='U',
                                           since=since, until=until)
        # Add data to each post
        posts = []
        profile = self.get_page_profile(page_id)
        while True:  # get all chuncks of 25 posts for a page
            for i, post in enumerate(chunk['data']):
                print '{}/25\t Get data from "{}" for post: {}  \t'.format(i, profile['name'],post['id']),
                post_id = post['id']
                post['profile'] = profile
                post['update_ts'] = datetime_to_timestamp(utc_now())
                post['update_dt'] = datetime.datetime.now() #ToDo: add tz=pytz.utc) ???
                post['comments'] = self.get_all_comments(post_id)
                post['reactions'] = self.get_all_reactions(post_id)
                post['created_time_dt'] = timestamp_to_datetime(post['created_time'])  # local timezone
                posts.append(post)
                print 'comments:{}, \treactions:{}'.format(len(post['comments']), len(post['reactions']))
            # Attempt to make a request to the next page of data, if it exists.
            try:
                chunk = requests.get(chunk['paging']['next']).json()
            except KeyError:  # When there are no more pages (['paging']['next']), break from the loop and end the script.
                break
        # the posts are sorted in decending order in the list [NEW,...,OLD].
        # This is not ideal.
        # When saving the posts in the database, NEW will be saved first. When crash, OLD is not saved. Resume scraping
        # will start from NEW and OLD will be missing in the database.
        # Reversing the order avoids executing a rollback of the inserted posts in case of crash.
        posts.reverse()
        return posts

    def get_all_comments(self, id, limit=500):
        if is_blacklisted(id):
            print '\nComment blacklisted: {}'.format(id)
            return [{'blacklisted': id}]
        # ToDo: get likes for comments
        # ToDo: get_object doesn't retrieve enough fields.
        #ToDo: Try to correct malformed comment ids. Ex. '103536906359022:898483933530978:10103399554941441_898491433530228'



        fields = 'id,created_time,comments.limit(%d){attachment,comment_count,from,id,like_count,message,likes{pic,link,name,username,picture{url,is_silhouette}},created_time}' % limit
        try:
            comments = self.graph.get_object(id, fields=fields, date_format='U')
        except:
            doc = {'id': id, 'timestamp': utc_now(), 'type': 'message'}
            save_blacklist_doc(doc=doc)
            print '\nBlacklisted: {}'.format(id)
            self.blacklist = get_blacklist()  # Update the blacklist in the FacebookScraping instance
            return [{'blacklisted':id}]


        allcomments = []
        while True:
            try:
                for comment in comments['comments']['data']:
                    allcomments.append(comment)
                    if comment['comment_count'] > 0:  # Get sub comments
                        sub_comment = self.get_all_comments(comment['id'])
                        allcomments = allcomments + sub_comment
                # When there are no more pages (['paging']['next']), break from the loop and end the script.
                comments = requests.get(comments['comments']['paging']['next']).json()
            except KeyError:
                break
        return allcomments

    def get_all_likes(self, id, limit=1000):
        # ToDO: total likes don't seem to match the total likes on the webpage:
        # for exapmle: post id= "202064936858448_298306593900948" yields 170 likes while the webpage shows 171 likes
        if is_blacklisted(id):
            print '\nComment blacklisted: {}'.format(id)
            return [{'blacklisted': id}]
        fields = 'likes.limit(%d){id,name,pic}' % limit
        likes = self.graph.get_object(id, fields=fields)  # lieks={likes:{data:[], paging:{}}, id:""}
        if 'likes' not in likes.keys():
            return []
        likes = likes['likes']  # don't need id
        alllikes = []
        while True:
            try:
                alllikes = alllikes + likes['data']  # concaternate 2 lists
                likes = requests.get(likes['paging']['next']).json()
            except KeyError:  # When there are no more pages (['paging']['next']), break from the loop and end the script.
                break
        print len(alllikes),
        return alllikes

    def get_all_reactions(self, id, limit=1000):
        # ToDO: total reactions don't seem to match the total reactions  on the webpage:
        # for exapmle: post id= "202064936858448_298306593900948" yields 208 reactions while the webpage shows 209 reactions
        if is_blacklisted(id):
            print '\nComment blacklisted: {}'.format(id)
            return [{'blacklisted': id}]
        fields = 'reactions.limit(%d){type,id,name,pic}' % limit
        reactions = self.graph.get_object(id, fields=fields)
        if 'reactions' not in reactions:
            return []
        reactions = reactions['reactions']  # don't need id
        allreactions = []
        while True:
            try:
                allreactions = allreactions + reactions['data']  # concaternate 2 lists
                reactions = requests.get(reactions['paging']['next']).json()
            except KeyError:  # When there are no more pages (['paging']['next']), break from the loop and end the script.
                break
        return allreactions

    def check_rate_limit(self, store=True, pause=True):
        # ToDo: Ugly processing !!!
        # Check the response header of an api call to know if rate is limited
        base = 'https://graph.facebook.com/v2.8'
        pageid = '270994524621'
        access = '&access_token={}'.format(self.access_token)
        node = '/{}/posts'.format(pageid)
        fields = '?fields=id,created_time'

        url = base + node + fields + access
        r = requests.get(url)
        timestamp = utc_now()
        rate_limit = r.headers.get('x-app-usage')
        while rate_limit:
            doc = {'type': 'fb_rate_limit', 'status': r.status_code, 'timestamp': timestamp, 'rate_limit': rate_limit}
            if store: save_log(doc)
            print 'Rate is limited !, Pause for 60 sec'
            print doc
            time.sleep(60)
            r = requests.get(url)
            timestamp = utc_now()
            rate_limit = r.headers.get('x-app-usage')
        return


class FacebookProcessing():
    pass


class FacebookStoring():
    # ToDo: read https://docs.mongodb.com/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/
    pass
