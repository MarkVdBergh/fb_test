import datetime
from collections import Counter  # subclass of dict. Used for combining 2 dicts

from settings import *
from tools.database_tool_MIGRATE import MongoDb
from tools.general_tools import yyyymmdd_to_datetime, utc_now, datetime_to_timestamp, timestamp_to_datetime
from tools.scraping_tools import FacebookScraping


class Engine():
    def __init__(self, pageidlist=None, access_token=None, since=None, until=None):
        """
        :param pageidlist: [str, str, ...]
        :param access_token:
        :param since: (yyyy,m,d): local date
        :param until: (yyyy,m,d): local date
        """
        MON = MongoDb(collection='facebook')
        if not access_token:
            self.access_token = FB_APP_ID + "|" + FB_APP_SECRET
        else:
            self.access_token = access_token
        if not pageidlist:
            self.pageidlist = PAGE_LIST
        else:
            self.pageidlist = pageidlist

        # convert local date (yyyy,mm,dd) into utc datetime
        if not since:
            self.since = yyyymmdd_to_datetime(2000, 1, 1, 0, 0, 0)
        else:
            self.since = yyyymmdd_to_datetime(since[0], since[1], since[2], 0, 0, 0)
        if not until:
            self.until = utc_now()
        else:
            self.until = yyyymmdd_to_datetime(until[0], until[1], until[2], 23, 59, 59)

    def run_scraping(self, pageidlist, resume=True, bulkdays=45):
        '''

        :param resume: bool: continue scraping starting at the latest time from the saved posts from page.
        :param bulkdays: int: max days to scrape posts from a page in one iteration
        :return: True
        '''
        bulk = datetime.timedelta(bulkdays)

        access_token = self.access_token
        if not pageidlist: pageidlist = self.pageidlist

        FS = FacebookScraping(access_token)
        MON = MongoDb(collection='facebook')
        for pageid in pageidlist:
            if resume:
                # get the last created_time for page
                lastpost = MON.get_last_post_for_page(pageid) #ToDo: Useless to retrieve everything. Use projection
                if lastpost:
                    since = lastpost['created_time']
                    since = timestamp_to_datetime(since) #ToDo: convert time to datetime and later again to timestamp
                else:
                    since = self.since
                print 'last post: ----------------->', since
                until = self.until
            else:
                since = self.since
                until = self.until
            print since, until
            s = since
            while until > s:
                u = s + bulk
                print 'Scraping page:{}, since:{}, until:{}'.format(pageid, s, u)
                FS.check_rate_limit()
                posts = FS.get_all_posts(pageid, since=datetime_to_timestamp(s), until=datetime_to_timestamp(u))
                if posts:
                    # store docs
                    results = MON.upsert_fb_documents(documents=posts)
                    print datetime.datetime.now(), 'Documents inserted: {}, selected: {}, updated or replaced: {}, upserted: {}'.format(
                        results.inserted_count, results.matched_count, results.modified_count, results.upserted_count)
                s += bulk
        return True


if __name__ == '__main__':
    E = Engine(pageidlist=['446368145415026'], since=None, until=None)
    E.run_scraping(resume=True)
    # E.run_statistics()
    pass
