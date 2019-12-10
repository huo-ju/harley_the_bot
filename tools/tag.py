from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import os
import sys
import time
import sqlite3
import db_data as datadb

by_user_id = 215 #my_user_id_default

mapping = { 'normal':0, 'sunxiaochuan':1, 'drop':-1, 'exit': 'exit' }

questions =  {
        'type': 'rawlist',
        'name': 'tag',
        'message': 'Tag the message as: ',
        'choices': [
            'sunxiaochuan',
            'normal',
            'drop',
            'exit'
        ],
        'filter': lambda val: mapping[val]
    }

def loadtweets():
    while True:
        tweets = datadb.load_data_for_tag();
        for tweet in tweets:
            print(tweet[3] +" \t" + tweet[0])
            answers = prompt(questions)
            if answers["tag"]=="exit":
                sys.exit()
            print("set tags:"+str(tweet[0])+" to "+str(answers["tag"]))
            datadb.tag_data(tweet[0], answers["tag"], by_user_id)


if __name__ == '__main__':
    loadtweets()
