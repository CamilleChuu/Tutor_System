import hashlib
import time
import random

from pymongo import MongoClient

db = MongoClient('localhost', 27017)['tutor_sys']
collection = db['session']

def generate_session_id(topic, user, seed=random.randint(1, 10000)):
    current_time = str(int(time.time()))
    combined_string = f"{current_time}-{topic}-{user}-{seed}"
    hashed_string = hashlib.sha256(combined_string.encode()).hexdigest()
    collection.insert_one({'user': user, 'topic': topic, 'time':current_time, 'session': hashed_string})
    return hashed_string