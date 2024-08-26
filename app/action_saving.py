import os, pickle
import warnings, random
import pandas as pd
import numpy as np
from tqdm import tqdm
import re, json, time
from datetime import datetime

import openai
from pymongo import MongoClient

#### envs ####
# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['demo']

mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['demo'] 

def action_saving(action_type, action_content, session_id='0'):
    _output.append({"type":'action_log', 'action_type':str(action_type), 'action_content': str(action_content)})
    collection.insert_one({'session':session_id, "type":'action_log', 'action_type':str(action_type), 'action_content': str(action_content), 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'end':0})
    return _output