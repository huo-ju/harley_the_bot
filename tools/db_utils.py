import os
import sqlite3
import json

with open('config.json', 'r') as f:
    config = json.load(f)

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), config["database"])

def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

