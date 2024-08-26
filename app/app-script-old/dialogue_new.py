import os, pickle
import warnings, random
import pandas as pd
import numpy as np
from tqdm import tqdm
import re, json, time
from datetime import datetime

import openai
from pymongo import MongoClient

from .question_list import question_dict
# from .message_list import message_dict
# from .message_list2 import message_dict
from .brieffeedback import feedback_dict

from .myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
from .rephrase import rephrase
from .utils import llm_predict, llm_answer, symbol_control, find_match_in_sentence, timeout
# from .preprocessing import preprocess1, preprocess2
from .ckprompt2 import initial_prompt, role_prompt, role_prompt2, inchat_prompt, expectation_prompt
from .unreach_retrieve import get_unreach_records
# from .mykey import key

#### envs for gpt ####
# os.environ["OPENAI_API_KEY"] = key
# openai.api_key = os.getenv("OPENAI_API_KEY")
key = os.environ["OPENAI_API_KEY"]

# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['demo']
mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['demo'] 

def hint_output(_input = 'As the dimensions get larger, the ratios get closer to 1.', question = 'Comparing Dimensions', session_id='0', exp_list=[1]):
    path = os.path.join(os.getcwd(), 'app/json')
    for file in os.listdir(path): 
        if question in file:
            with open(os.path.join(path, file), 'r') as f:    message_tmp = json.load(f)
    message_tmp = message_tmp[list(message_tmp.keys())[0]]
    # previous reached exp
    expectation_log, last_attempt_id = get_reached_exp(session_id)
    


def gpt_dialogue(_input = 'As the dimensions get larger, the ratios get closer to 1.', question = 'Comparing Dimensions', session_id='0'):
    path = os.path.join(os.getcwd(), 'app/json')
    for file in os.listdir(path): 
        if question in file:
            with open(os.path.join(path, file), 'r') as f:    message_tmp = json.load(f)

    message_tmp = message_tmp[list(message_tmp.keys())[0]]

    # exps
    exp_keys = [k for k in message_tmp.keys() if 'Expectation' in k]
    expectations = ["""\"{}\":\"{}\"""".format(idx, message_tmp['Expectation'+str(idx)]['Expectation']) for idx in range(1, len(exp_keys)+1)]
    expectations = "{" + ', '.join(expectations) + "}"

    # ques
    question_text = message_tmp['Prompt']

    # previous reached exp
    expectation_log, last_attempt_id = get_reached_exp(session_id)

    # previous unreach-expectation answer:
    previous_answers = None
    if collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)]):
        if collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['target'] == -1:
            previous_answers = get_unreach_records(collection, session_id)

    # main process
    expectation_output = json.loads(expectations)
    messages = [{"role": "system", "content": role_prompt}]
    query = initial_prompt + '# Input Data' + str({'question':question_text, 'Expectations':expectations})
    messages.append({"role": "user", "content": query})
    _output = []
    if previous_answers:
        user_input = previous_answers + '. ' + str(_input)
    else:
        user_input = str(_input)

    query = inchat_prompt + '# Input Data' + user_input
    messages.append({"role": "user", "content": query})
    predict = llm_predict(messages, max_tokens=10)
    messages.append({"role": "assistant", "content": predict})

    reached_exp = re.findall('\d', predict)
    if len(reached_exp)>0: # if reached any expectations
        for d in reached_exp: expectation_log.add(d)
        feedback_tmp = str(random.choice(feedback_dict['PositiveFeedback']))
    else: # if did not reach any expectations
        feedback_tmp = str(random.choice(feedback_dict['NeutralFeedback']))
    
    if len(reached_exp)>0:
        # if there are new expectation to cover
        target = induce_exp_idx(expectation_log, expectation_output.keys())
        
        if target is not None:
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'end':0})

            _output.append({"type":"text", "content": feedback_tmp, 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

            # select a hint
            hint_keys = [k for k in message_tmp['Expectation'+str(target)].keys() if 'Hint' in k]
            if str(target) != str(last_attempt_id):
                hint_key_tmp = random.choice(hint_keys)
            else:
                last_hint = collection.find_one({'session': session_id, 'speaker': 'system', 'target':target}, sort=[('_id', -1)])['target2']
                hint_key_tmp = random.choice([e for e in hint_keys if e != last_hint])

            if isinstance(message_tmp['Expectation'+str(target)][hint_key_tmp], list):
                hint_list_tmp = message_tmp['Expectation'+str(target)][hint_key_tmp]
            else:
                hint_list_tmp = [message_tmp['Expectation'+str(target)][hint_key_tmp]]

            for hint_content in hint_list_tmp:
                if not hint_content.endswith(')'): # text hint
                    hint_tmp = rephrase(str(hint_content))
                    _output.append({"type":"text", "content": hint_tmp, 'end':0})
                    collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
                else: # action hint
                    _output.append({"type":'action', "content":str(hint_content), 'end':0})
                    collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(hint_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
            
        else: # target is None; end of the dialogue
            ## keep records
            print("\nKeep Records?\n")
            user = db['session'].find_one({"session":session_id})['user']
            db['progress'].insert_one({'session':session_id, 'question':question, 'time':datetime.utcnow().timestamp(), 'user': user})

            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':1})

            _output.append({"type":"text", "content": feedback_tmp, 'end':1})
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})

            closing_message = []
            for closing_k in ["Conclusion", "Closing", "Summary Content"]:
                if closing_k in message_tmp.keys():
                    closing_message.extend(message_tmp[closing_k])

            for conclusion_content in closing_message:
                if not conclusion_content.endswith(')'): # text conclusion
                    _output.append({"type":"text", "content":conclusion_content, 'end':1})
                    collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':conclusion_content, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
                else:
                    _output.append({"type":'action', "content":str(conclusion_content), 'end':1})
                    collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(conclusion_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})

            # # pop up white board when ending a question
            # _output.append({"type":"action", "content":"openPopupWhiteboard()", 'end':1})
            # collection.insert_one({'session':session_id, 'question':question, 'action':"openPopupWhiteboard", 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
    else:
        collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'end':0})

        _output.append({"type":"text", "content": feedback_tmp, 'end':0})
        collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

        hint_tmp = rephrase("Can you say more to explain your answer?")
        _output.append({"type":"text", "content": hint_tmp, 'end':0})
        collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})
        
    # print(str(_output))
    return _output

def gpt_answer(_input = 'Does the ratios get closer to 1?', question = 'Comparing Dimensions', session_id='0'):
    path = os.path.join(os.getcwd(), 'app/json')
    for file in os.listdir(path): 
        if question in file:
            with open(os.path.join(path, file), 'r') as f:    message_tmp = json.load(f)

    message_tmp = message_tmp[list(message_tmp.keys())[0]]

    # exps
    exp_keys = [k for k in message_tmp.keys() if 'Expectation' in k]
    expectations = ["""\"{}\":\"{}\"""".format(idx, message_tmp['Expectation'+str(idx)]['Expectation']) for idx in range(1, len(exp_keys)+1)]
    expectations = "{" + ', '.join(expectations) + "}"

    # ques
    question_text = message_tmp['Prompt']

    # previous reached exp
    expectation_log, last_attempt_id = get_reached_exp(session_id)

    # previous unreach-expectation answer:
    previous_question = None
    if collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)]):
        if collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['target'] == -1:
            previous_question = get_unreach_records(collection, session_id, 3)

    messages = [{"role": "system", "content": role_prompt2}]
    query = '# Input Data: ' + str({'## User Question':str(previous_question) + ' ' + _input, '## Original Expectations': expectations, '## Background Question': question_text})
    messages.append({"role": "user", "content": query})

    hint_tmp = llm_answer(messages, max_tokens=512)
    _output = [{"type":"text", "content": hint_tmp, 'end':0}]
    collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})
    return _output

def get_reached_exp(session_id):
    # prepare the expectation log set
    try:
        if int(collection.find_one({'session': session_id}, sort=[('_id', -1)])['end']) ==0: # last record is the middle step
            expectation_log = set(collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['reached'])
            last_attempt_id = collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['target']
        else:
            expectation_log = set()
            last_attempt_id = -1
    except: 
        expectation_log = set()
        last_attempt_id = -1
    return expectation_log, last_attempt_id

# def process_input(_input = 'As the dimensions get larger, the ratios get closer to 1.', question = 'Comparing Dimensions', session_id='0'):
#     # previous reached exp
#     expectation_log, last_attempt_id = get_reached_exp(session_id)

#     isdeclarative = int(preprocess1(_input))
#     if isdeclarative:
#         isutterance = int(preprocess2(_input))
#         if isutterance:
#             _output = gpt_dialogue(_input, question, session_id)
#         else:
#             hint_tmp = rephrase("Let's continue on this question.")
#             _output = [{"type":"text", "content": hint_tmp, 'end':0}]
#             collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})
#     else:
#          _output = gpt_answer(_input, question, session_id)
#     return _output