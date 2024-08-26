import os, pickle
import warnings, random
import pandas as pd
import numpy as np
from tqdm import tqdm
import re, json, time
from datetime import datetime

import openai
from pymongo import MongoClient

# from .question_list import question_dict
# from .message_list2 import message_dict
from .myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
from .utils import llm_predict, symbol_control, find_match_in_sentence, timeout
# from .ckprompt2 import initial_prompt, role_prompt, inchat_prompt, expectation_prompt

#### envs ####
# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['demo']

mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['demo'] 

def opening(question_input='Comparing Dimensions', session_id='0'):
    path = os.path.join(os.getcwd(), 'app/json')
    for file in os.listdir(path): 
        if question_input in file:
            with open(os.path.join(path, file), 'r') as f: message_tmp = json.load(f)
    message_tmp = message_tmp[list(message_tmp.keys())[0]]

    _output = []

    for item in message_tmp['Introduction']:
        if item.endswith(")") or item.startswith("openNewImage"):
            _output.append({"type":"action", 'content':str(item), 'end':-1})
            collection.insert_one({'session':session_id, 'question':question_input, 'type':'action', 'content':str(item), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':-1})
        else:
            _output.append({"type":"text", 'content':str(item), 'end':-1})
            collection.insert_one({'session':session_id, 'question':question_input, 'type':'action', 'content':str(item), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':-1})

    if 'BeginningText' in message_tmp.keys():
        _output.append({"type":"text", 'content':str(message_tmp['BeginningText']), 'end':-1})
        collection.insert_one({'session':session_id, 'question':question_input, 'type':'text', 'content':str(message_tmp['BeginningText']), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':-1})
    
    _output += opening_prompts(message_tmp, 'Stage1', question_input, session_id, )
    return _output

def opening_prompts(message_tmp, stage, question_input='Comparing Dimensions', session_id='0', ):
    _output = []
    sub_message_tmp = message_tmp[stage]
    if not isinstance(sub_message_tmp['Prompt'], list):
        sub_message_tmp['Prompt'] = [sub_message_tmp['Prompt']]

    for item in sub_message_tmp['Prompt']:
        if item.endswith(")") or item.startswith("openNewImage"):
            _output.append({"type":"action", 'content':str(item), 'end':-1})
            collection.insert_one({'session':session_id, 'question':question_input, 'type':'action', 'content':str(item), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':-1})
        else:
            _output.append({"type":"text", 'content':str(item), 'end':-1})
            collection.insert_one({'session':session_id, 'question':question_input, 'type':'action', 'content':str(item), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':-1})
    return _output