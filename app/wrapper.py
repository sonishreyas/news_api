from os import environ
from pymongo import MongoClient
import datetime
from flask.cli import load_dotenv

class MongoWrapper():

    def __init__(self):
        load_dotenv('/home/ubuntu/BE/news_api/configs/.env.dev')
        self.client =  MongoClient(f'mongodb://{environ.get("MONGO_IP")}:{environ.get("MONGO_PORT")}/')  
        self.mydb = self.client[environ.get("MONGO_DATABASE")]
        # self.mydb.authenticate(environ.get('MONGO_USER'),environ.get('MONGO_PWD'))

    def create_collection(self,name):
        mycol = self.mydb[name]
        return True

    def ingest_data(self, data):
        object_id = self.mydb.news.insert_many(data)
        return True
        
    def get_data(self, kwargs):
        result_json = []
        for post in self.mydb.news.find(kwargs):
            post['_id'] = str(post['_id'])
            result_json.append(post)
        return result_json