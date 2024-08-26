from datetime import datetime
import random
import string
import os

from pymongo import MongoClient

# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['progress']

mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['progress'] 

question_dict = {
    'Comparing Dimensions': '11',
    'Making Iced Tea': '12',
    'Making More Iced Tea': '13',
    'Mixing Paint': '14',
    'Building Buses': '41',
    'Filling the Tub': '42',
    'Building a House': '43',
    'Building a Neighborhood': '44',
    'Using Candles': '45',
    'Using More Candles': '46',
    'Auctioning Paintings': '47'
}

def retrieve_progress(username):
    questions = set()
    batch = collection.find({'user': username})
    for item in batch:
        questions.add(item['question'])
    return list(questions)


    