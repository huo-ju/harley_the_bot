from flask import Flask, request, render_template, send_from_directory
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from twitterscraper import query_tweets
import datetime as dt
import json
import re
import modelserver



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
config = {}

with open('config.json', 'r') as f:
    config = json.load(f)

#testdata={}
#with open('test.json', 'r') as ftest:
#    testdata = json.load(ftest)

predict = modelserver.Predict(config)

def clean_text(text):
    text = re.sub(r'(\r|\n)', '', text, flags=re.MULTILINE)
    text = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z0-9\&\.\/\?\:@\-_=#])*', '', text, flags=re.MULTILINE)
    return text

def clean_englishandchar(text):
    text = re.sub(r'[a-zA-Z0-9$@$!%*?&#^-_.\', +/:，。？]+', '', text, flags=re.MULTILINE)
    return text

def tweets_to_inputdata(screen_name):
    begin_date = dt.date.today() + dt.timedelta(days=-30)
    end_date = dt.date.today() + dt.timedelta(days=0)
    tweets = query_tweets("from:"+screen_name, limit=config["fetch_tweet_limit"], begindate=begin_date, enddate=end_date, poolsize=1)
    input_data = []
    for tweet in tweets:
        if len(clean_text(tweet.text)) >= config["min_text_len_require"] and len(clean_englishandchar(tweet.text)) >= config["min_text_len_require"]:
            input_data.append([tweet.tweet_id,tweet.text])
    return input_data

class APIIden(Resource):
    def get(self):
        input_data = tweets_to_inputdata(request.args["screen_name"])
        if len(input_data) >= config["min_text_require"]:
            result = predict.get_predictions(input_data)
            return jsonify(result)
        else:
            return jsonify({"error":"not enough data"})

    def post(self):
        input_data = request.get_json(force=True)
        result = predict.get_predictions(input_data)
        return jsonify(result)


api.add_resource(APIIden, '/api/iden') 

@app.route('/')
def home():
    return render_template('/index.html', title="Twitter User Analytics")

@app.route('/idenusers')
def iden():
    screen_name = request.args.get('screen_name')
    screen_name =screen_name.replace("@","")

    input_data = tweets_to_inputdata(screen_name)
    if len(input_data) >= config["min_text_require"]:
        result_data = predict.get_predictions(input_data)
    #global testdata
    #result_data = testdata
        return render_template('/iden.html', title="Identify User:", tweets = result_data["results"], screen_name = screen_name, ratio = "%.2f" % (float( result_data["summary"]["ratio"])*100))
    else:
        return render_template('/err.html', title="Identify User:", err="not enough data")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('statics/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('statics/css', path)


if __name__ == '__main__':
    app.run(port=config["port"],host=config["host"])
