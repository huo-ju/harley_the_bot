from flask import Flask, request, render_template, send_from_directory
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from tasks import predict as dpredict
from tasks import predict_byname
from tasks import app as taskbackend
import sys
import json
import tweets



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
config = {}

config_name="config.json"
if len(sys.argv) >= 2:
    config_name = sys.argv[1]

print("config file:" + config_name)

with open(config_name, 'r') as f:
    config = json.load(f)

#testdata={}
#with open('test.json', 'r') as ftest:
#    testdata = json.load(ftest)

predict = {}

enable_remote_workers = False

if ("enable_remote_workers" in config) == True:
    enable_remote_workers = config["enable_remote_workers"] 

if enable_remote_workers == False:
    import modelserver
    predict = modelserver.Predict(config)


def run_predict(input_data, screen_name):
    global enable_remote_workers 
    if enable_remote_workers == True:
        p = dpredict.delay(input_data)
        result = p.get(timeout=config["remote_timeout"])
        return result
    else:
        result = predict.get_predictions(input_data, screen_name)
        return result

def run_predict_byname(screen_name):
    global enable_remote_workers 
    if enable_remote_workers == True:
        p = predict_byname.delay(screen_name)
        result = {"task_id":p.id}
        return result
    else:
        input_data = tweets.tweets_to_inputdata(screen_name, config)
        if len(input_data) >= config["min_text_require"]:
            result = run_predict(input_data)
            return result
        else:
            return {"error":"not enough data"}


class APIIden(Resource):
    def get(self):
        result = run_predict_byname(request.args["screen_name"])
        return jsonify(result)

    def post(self):
        global enable_remote_workers 
        if enable_remote_workers == False:
            screen_name = request.args["screen_name"]
            input_data = request.get_json(force=True)
            result = run_predict(input_data, screen_name)
            return jsonify(result)
        else:
            return jsonify({"error":"server only run under the local mode. set enable_remote_workers = false "})

class APICheck(Resource):
    def get(self):
        task_id = request.args["task_id"]
        p = taskbackend.AsyncResult(task_id)
        result = {"state":p.state}
        return jsonify(result)


api.add_resource(APIIden, '/api/iden') 
api.add_resource(APICheck, '/api/check') 


@app.route('/')
def home():
    return render_template('/index.html', title="Twitter User Analytics")

@app.route('/idenusers')
def iden():
    global enable_remote_workers 

    screen_name = request.args.get('screen_name')
    screen_name =screen_name.replace("@","")

    result_data = run_predict_byname(screen_name)
    if ("err" in result_data) == True:
        return render_template('/err.html', title="Identify User:", err= result_data["err"])
    elif ("task_id" in result_data) == True:
        return render_template('/check.html', title="Working for User:", task_id = result_data["task_id"])
    else:
        return render_template('/iden.html', title="Identify User:", tweets = result_data["results"], screen_name = screen_name, ratio = "%.2f" % (float( result_data["summary"]["ratio"])*100))

@app.route('/idenresult')
def idenbytaskid():
    global enable_remote_workers 
    task_id= request.args.get('task_id')
    p = taskbackend.AsyncResult(task_id)
    result_data = p.get(timeout=5)
    if ("err" in result_data) == True:
        return render_template('/err.html', title="Identify User:", err= result_data["err"])
    else:
        return render_template('/iden.html', title="Identify User:", tweets = result_data["results"], screen_name = result_data["summary"]["screen_name"], ratio = "%.2f" % (float( result_data["summary"]["ratio"])*100))



@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('statics/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('statics/css', path)


if __name__ == '__main__':
    app.run(port=config["port"],host=config["host"])
