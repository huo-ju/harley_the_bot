from db_utils import db_connect

con = db_connect()
cur = con.cursor()

def insert_tweets(tweet_id, screen_name, tweet, is_replied, likes, retweets, replies, tweet_timestamp, tweet_class=1):
    insert_sql = "INSERT INTO tweets (tweet_id, screen_name, class, tweet, is_replied, likes, retweets, replies, tweet_timestamp) VALUES (?,?,?,?,?,?,?,?,?);"
    cur.execute(insert_sql, (tweet_id, screen_name, tweet_class, tweet, is_replied, likes, retweets, replies, tweet_timestamp))


def load_data_for_clean(start=0, count=50):
    cur.execute("SELECT tweet_id, is_replied, screen_name, tweet FROM tweets limit ?,?;", (start,count))
    tweets = cur.fetchall()
    return tweets

def load_data_for_tag(start=0, count=50):
    cur.execute("SELECT tweet_id, is_replied, screen_name, tweet FROM tweets WHERE tags=0 limit ?,?;", (start,count))
    tweets = cur.fetchall()
    return tweets

def tag_data(t_id, tag, tag_by):

    cur.execute("SELECT t_id FROM tags WHERE t_id=? and tag=?;", (t_id, tag))
    row = cur.fetchone()
    if row is None:
        print('save tag')

        cur.execute("SELECT tags FROM tweets WHERE tweet_id=?;", (t_id,))
        tweet = cur.fetchone()
        tweet_tag_count = tweet[0]

        insert_sql = "INSERT INTO tags (t_id, tag, tagged_by_uid) VALUES (?,?,?);"
        cur.execute(insert_sql, (t_id, tag, tag_by))
        update_sql = "UPDATE tweets set tags=? WHERE tweet_id=?;"
        cur.execute(update_sql, (tweet_tag_count+1, t_id))
        con.commit()
    else:
        print("tag exists")

def load_data_by_tag(tag, limit ):
    select_sql = "SELECT tags.tag, tweets.tweet_id, tweets.tweet FROM tweets INNER JOIN tags ON tags.t_id = tweets.tweet_id WHERE tags.tag=? limit ?;";
    cur.execute(select_sql, (tag,limit))
    tweets = cur.fetchall()
    return tweets

def load_data_no_tag(start, limit):
    select_sql = "SELECT 0,tweet_id, tweet FROM tweets limit ?,?;";
    cur.execute(select_sql, (start,limit))
    tweets = cur.fetchall()
    return tweets


def delete_data(t_id):
    delete_sql = "DELETE FROM tweets WHERE tweet_id=?;"
    cur.execute(delete_sql, (t_id,))
    delete_sql = "DELETE FROM tags WHERE t_id=?;"
    cur.execute(delete_sql, (t_id,))

def commit():
    con.commit()
