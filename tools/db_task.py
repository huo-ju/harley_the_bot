from db_utils import db_connect

con = db_connect()
cur = con.cursor()

def load_inputusers():
    cur.execute("SELECT * FROM inputusers WHERE done=false limit 10;")
    inputusers = cur.fetchall()
    return inputusers 

def load_users_for_fetch():
    cur.execute("SELECT screen_name FROM inputusers WHERE last_fetch_id=0 and done=0 limit 10;")
    inputusers = cur.fetchall()
    return inputusers 



def insert_inputusers(screen_name, done=False, user_class=1,last_fetch_id='0', following=''):
    insert_sql = "INSERT INTO inputusers (screen_name,done,class,last_fetch_id,following) VALUES (?,?,?,?,?);"
    cur.execute(insert_sql, (screen_name, done, user_class, last_fetch_id, following))

def mark_task_done(status, screen_name):
    update_sql = "UPDATE inputusers SET done=? where screen_name=?;"
    cur.execute(update_sql, (status,screen_name))


def update_maxtweet_id(screen_name, max_id):
    update_sql = "UPDATE inputusers SET last_fetch_id=? where screen_name=?;"
    cur.execute(update_sql, (max_id,screen_name))
    con.commit()

def commit():
    con.commit()
