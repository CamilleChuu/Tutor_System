from datetime import datetime
import random
import string
import os

from pymongo import MongoClient

# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['account']

mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['account'] 

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def register_account(username, password, nickname=None):
    if collection.find_one({'username': username}):
        return {"type": "text", "content": 'User Name exists (please set another one)'}
    elif len(str(password))< 8:
        return {"type": "text", "content": 'Password too short (at least 8 characters)'}
    else:
        if len(str(nickname)) == 0:
            nickname = "USER_" + generate_random_string(8)
        collection.insert_one({'username':username, 'password':password, 'nickname':nickname})
        print('success create user', username)
        return {"type": "text", "content": 'Successful Registration!'}

def login_account(username, password):
    if collection.find_one({'username': username, 'password':password}):
        nickname = collection.find_one({'username': username, 'password':password})['nickname']
        return {"type": "text", "content": nickname, 'success':1}
    else:
        return {"type": "text", 'success':0}

    
