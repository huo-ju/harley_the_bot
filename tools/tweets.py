import sqlite3
import datetime as dt
from twitterscraper import query_tweets
import db_data as dbdata
import db_task as dbtask


def get_tweets(screen_name, begin_date, end_date, limit=200, poolsize =1):
    max_id = 0;
    tweets =  query_tweets("from:"+screen_name, limit=limit, begindate=begin_date, enddate=end_date, poolsize=poolsize)
    if len(tweets) > 0:
        for tweet in tweets:
            try:
                dbdata.insert_tweets(tweet.tweet_id, tweet.screen_name, tweet.text,tweet.is_replied, tweet.likes, tweet.retweets, tweet.replies, tweet.timestamp_epochs)
                if int(tweet.tweet_id) > max_id:
                    max_id=int(tweet.tweet_id)
            except sqlite3.IntegrityError as e: 
                if 'UNIQUE constraint' in str(e):
                    print("skip..")
        dbdata.commit()
        return max_id
    else:
        return -1;


if __name__ == '__main__':
    while True:
        inputusers = dbtask.load_users_for_fetch()
        for user in inputusers:
            screen_name = user[0]
            print(screen_name)
            begin_date = dt.date.today() + dt.timedelta(days=-60)
            end_date = dt.date.today() + dt.timedelta(days=2)
            max_id = get_tweets(screen_name, begin_date, end_date);
            if max_id>0 or max_id==-1:
                dbtask.update_maxtweet_id(screen_name, max_id)
             

            #dbtask.update_maxtweet_id(screen_name, "110110")

