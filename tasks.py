from celery import Celery
import json
import requests
import tweets

tasks_config = {}
with open('tasks_config.json', 'r') as f:
    tasks_config = json.load(f)


config = {}
with open('config.json', 'r') as f:
    config = json.load(f)

app = Celery('tasks', backend=tasks_config["backend"], broker=tasks_config["broker"] )

headers = {'Content-Type': 'application/json'}


@app.task(track_started=True)
def predict(input_data):
    response = requests.post(tasks_config["api_url"], headers=headers, json=input_data)
    result = json.loads(response.content)
    return result

@app.task(track_started=True)
def predict_byname(screen_name):
    input_data = tweets.tweets_to_inputdata(screen_name, config)
    response = requests.post(tasks_config["api_url"]+"?screen_name="+screen_name, headers=headers, json=input_data)
    result = json.loads(response.content)
    return result

