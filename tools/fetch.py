import os
import time
import tweepy as tweepy
import sqlite3
from tweepy.auth import OAuthHandler

import json
import db_task as taskdb

with open('config.json', 'r') as f:
    config = json.load(f)


output = open("train.tsv","a")

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_token"], config["access_token_secret"])
api = tweepy.API(auth)


def limit_handled(cursor, args):
    while True:
        taskdb.commit()
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print("Rate Limit, sleep 15 minutes")
            time.sleep(15 * 60)

def get_tweets(username, number):
        tweets = api.user_timeline(screen_name=username,count=number)
        tmp=[]
        for tweet in tweets:
            tmp.append(tweet.id_str +"\t" + "1" + "\ta\t" + tweet.text)
            output.write(tweet.id_str +"\t" + "1" + "\ta\t" + tweet.text+"\n")
        return tmp


def get_all_follows(screen_name):
    try:
        for follower in limit_handled(tweepy.Cursor(api.followers, screen_name=screen_name).items(), screen_name):
            try:
                taskdb.insert_inputusers(follower.screen_name, following=screen_name)
            except sqlite3.IntegrityError as e: 
                if 'UNIQUE constraint' in str(e):
                    print("skip..")
        return True
    except tweepy.error.TweepError as e: 
        if 'Not authorized' in str(e):
            print("Not authorized. May the account has been suspended. input args: " + screen_name)
            taskdb.mark_task_done(2, screen_name)
            taskdb.commit()
            return False


def task_fetch_followers():
    while True:
        inputusers  = taskdb.load_inputusers();
        for user in inputusers:
            screen_name = user[0]
            print("get followers from: " + screen_name)
            result = get_all_follows(screen_name)
            if result == True:
                print("done:"+ screen_name)
                taskdb.mark_task_done(True, screen_name)
                taskdb.commit()

if __name__ == '__main__':
    task_fetch_followers()
