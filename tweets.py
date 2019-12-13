import datetime as dt
import re
from twitterscraper import query_tweets

def clean_text(text):
    text = re.sub(r'(\r|\n)', '', text, flags=re.MULTILINE)
    text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\.\/\?\:@\-_=#])*', '', text, flags=re.MULTILINE)
    return text

def clean_englishandchar(text):
    text = re.sub(r'[a-zA-Z0-9$@$!%*?&#^-_.\', +/:，。？]+', '', text, flags=re.MULTILINE)
    return text

def tweets_to_inputdata(screen_name, config):
    begin_date = dt.date.today() + dt.timedelta(days=-30)
    end_date = dt.date.today() + dt.timedelta(days=0)
    tweets = query_tweets("from:"+screen_name, limit=config["fetch_tweet_limit"], begindate=begin_date, enddate=end_date, poolsize=1)
    input_data = []
    for tweet in tweets:
        if len(clean_text(tweet.text)) >= config["min_text_len_require"] and len(clean_englishandchar(tweet.text)) >= config["min_text_len_require"]:
            input_data.append([tweet.tweet_id,tweet.text])
    return input_data



