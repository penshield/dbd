__author__ = 'snouto'


from pymongo import MongoClient

from common import *

class DatabaseManager(object):

    def __init__(self,collection_name=DATABASE_COLLECTION):
        self.client = MongoClient(host=DATABASE_HOST,port=DATABASE_PORT)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[collection_name]


    def insert(self,record):
        self.collection.insert_one(record)

    def insert_many(self,many):

        if many:
            for record in many:
                self.insert(record)



    def delete(self,record):
        self.collection.remove({"_id":record._id})


    def close(self):
        self.client.close()



