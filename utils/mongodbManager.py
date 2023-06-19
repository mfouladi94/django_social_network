from django_social_network.settings import MONGODB
from pymongo import *


connect_string = MONGODB['connectionString']
client = MongoClient(connect_string)
db = client['socialNetwork']

def get_db_client():
    return client

def get_collection(name):
    return db[name]
