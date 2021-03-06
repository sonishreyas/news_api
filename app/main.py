import os
from os import environ

from flask import Flask, json
from flask import jsonify
from flask import request
from dotenv import load_dotenv
from AppUtil import AppUtil
from wrapper import MongoWrapper
from RateLimiter import RateLimiter
from flask_cors import CORS, cross_origin

class DataBackendFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                pass
        super(DataBackendFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = DataBackendFlaskApp(__name__)  
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.run()

load_dotenv('../app/configs/.env.dev')
print("SESSION_WINDOW_IN_SECONDS = ", environ.get('SESSION_WINDOW_IN_SECONDS'))
SESSION_WINDOW_IN_SECONDS = int(environ.get('SESSION_WINDOW_IN_SECONDS'))
MAX_REQUEST = int(environ.get('MAX_REQUEST'))

app_util = AppUtil()
rate_limiter = RateLimiter(SESSION_WINDOW_IN_SECONDS, MAX_REQUEST)
mongoWrapper = MongoWrapper()

@app.route("/create_collection", methods=["POST"])
@cross_origin()
def create_collection():
    user_ip = app_util.get_ip(request)
    if rate_limiter.allow(user_ip):
        received_json_data = json.loads(request.data)

        collection_name = received_json_data['name']
        status = mongoWrapper.create_collection(collection_name)
        return jsonify({'ip': user_ip,
                        'succeeded': status,
                        }), 200

    return "More than 10 requests originated from this IP in last 10 seconds. Please wait few seconds before you try again."


@app.route("/ingest", methods=["POST"])
@cross_origin()
def ingest():
    user_ip = app_util.get_ip(request)
    if rate_limiter.allow(user_ip):
        received_json_data = json.loads(request.data)
        status = mongoWrapper.ingest_data(data=received_json_data)
        return jsonify({'ip': user_ip,
                        'succeeded': status,
                        }), 200

    return "More than 10 requests originated from this IP in last 10 seconds. Please wait few seconds before you try again."

@app.route("/get_data", methods=["GET"])
def get_data():
    topic = request.args.get("topic","")
    user_ip = app_util.get_ip(request)
    if rate_limiter.allow(user_ip):

        try:
            received_json_data = json.loads(request.data)
        except:
            received_json_data = {}
        received_json_data['is_summarized'] = 1
        if topic != "":
            received_json_data['topic'] = topic
        
        result = mongoWrapper.get_data(collection_name= "articles",search=received_json_data)
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route("/get_data_by_language", methods=["GET"])
def get_data_by_language():
    topic = request.args.get("topic","")
    language = request.args.get("language","English")
    user_ip = app_util.get_ip(request)
    if rate_limiter.allow(user_ip):

        try:
            received_json_data = json.loads(request.data)
        except:
            received_json_data = {}
        if language == "English":
            language = ""
        else:
            language += "_"

        received_json_data['is_summarized'] = 1
        if topic != "":
            received_json_data['topic'] = topic
        
        result = mongoWrapper.get_data_by_language(collection_name= "articles",search=received_json_data,language=language)
        response = jsonify(result)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response