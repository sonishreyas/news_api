from os import environ
from pymongo import MongoClient
import datetime
from flask.cli import load_dotenv

class MongoWrapper():

    def __init__(self):
        load_dotenv('/home/ubuntu/BE/news_api/configs/.env.prod')
        self.client =  MongoClient(f'mongodb://{environ.get("MONGO_IP")}:{environ.get("MONGO_PORT")}/')  
        self.mydb = self.client[environ.get("MONGO_DATABASE")]
        self.mydb.authenticate(environ.get('MONGO_USER'),environ.get('MONGO_PWD'))

    def create_collection(self,name):
        mycol = self.mydb[name]
        return True

    def ingest_data(self, collection_name='articles', data):
        collection = getattr(self.mydb, collection_name)
        object_id = collection.insert_many(data)
        return object_id
        
     def get_data(self, collection_name='articles', search={}):
        collection = getattr(self.mydb, collection_name)
        result = []
        for post in collection.find(search):
            result.append(post)
        return result