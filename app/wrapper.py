from os import environ
from pymongo import MongoClient
import datetime
from dotenv import load_dotenv

class MongoWrapper():

    def __init__(self):
        load_dotenv('../app/configs/.env.prod')
        self.client = MongoClient(f"mongodb://{environ.get('MONGO_USER')}:{environ.get('MONGO_PWD')}@{environ.get('MONGO_IP')}:{environ.get('MONGO_PORT')}/{environ.get('MONGO_DATABASE')}",authSource=environ.get("MONGO_DATABASE_AUTHENTICATION")) 
        self.mydb = self.client[environ.get("MONGO_DATABASE")]

    def create_collection(self,name):
        mycol = self.mydb[name]
        return True

    def ingest_data(self, collection_name, data):
        collection = getattr(self.mydb, collection_name)
        object_id = collection.insert_many(data)
        return object_id
        
    def get_data(self, collection_name, search={}):
        collection = getattr(self.mydb, collection_name)
        result = []
        for post in collection.find(search,{"_id":0,"description":0,"source_id":0,"is_summarized": 0,"is_translated": 0}).sort("time",-1):
            result.append(post)
        return result