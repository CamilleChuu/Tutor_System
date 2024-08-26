import sys, os, pickle
import warnings, random
import pandas as pd
import numpy as np
from tqdm import tqdm
import re, json, time
from datetime import datetime
sys.path.insert(0, '/')

# import autogen
# from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent
from .autogen.agentchat import ConversableWritableAgent
from .autogen.agentchat import AssistantWriteAgent

from .autogen.agentchat.assistant_exp_agent import AssistantExpAgent

# from autogen.agentchat import UserProxyAgent
# from autogen.agentchat import AssistantAgent
from app.autogen.autogen.agentchat.groupchat_exp import GroupChatExp, GroupChatManagerExp
from app.autogen.agent_prompt import user_message, judger_message, allocator_message, rephraser_message, responser_message, agent_description
from app.autogen.agent_prompt import manager_message1, manager_message2, manager_message3
from app.autogen.exp_utils import process_output, json_converter
from app.autogen.unreach_retrieve import get_unreach_records
os.environ['AUTOGEN_USE_DOCKER'] = '0'

from app.autogen.autogen_support import dialogue_output, hint_output
from app.autogen.autogen_support2 import dialogue_output2, hint_output2

import argparse

from pymongo import MongoClient
# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['demo']
# collection2 = db['cache']
mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['demo'] 
collection2 = db['cache']

from app.autogen.autogen import config_list_from_json

today = datetime.now().strftime("%Y%m%d")

gpt_name = "gpt-4-1106-preview"

config_list_gpt4 = config_list_from_json(
    "./app/autogen/notebook/OAI_CONFIG_LIST",
    filter_dict={
        "model": [gpt_name],
    },
)


gpt4_config1 = {
    "cache_seed": 46,  # change the cache_seed for different trials
    "temperature": 0.3,
    "config_list": config_list_gpt4,
    "timeout": 30,
}

gpt4_config2 = {
    "cache_seed": 49,  # change the cache_seed for different trials
    "temperature": 1.5,
    "config_list": config_list_gpt4,
    "timeout": 30,
}

# allocator = AssistantExpAgent( # check the condition and go to next step
#     name = 'Allocator',
#     system_message = allocator_message, 
#     description = agent_description, 
#     llm_config=gpt4_config1, 
#     human_input_mode='NEVER', 
#     writedown=False
# )

# rephraser = AssistantExpAgent( # if yes, rephrase hints
#     name = 'Rephraser',
#     system_message = rephraser_message, 
#     description = agent_description, 
#     llm_config=gpt4_config2,
#     human_input_mode='NEVER'
# )

# responser = AssistantWriteAgent( # if no, generate new response
#     name="responser",
#     system_message= responser_message,
#     description = "A helpful AI assistant who has strong language skills, generating responses to a dialogue.",
#     llm_config=gpt4_config1, human_input_mode='NEVER', writedown = False
# )

# input_data_template =  {
#     "Question": "Dimensions of the four rectangles are given as: 7 by 10 feet, 17 by 20 feet, 27 by 30 feet, 37 by 40 feet. Which rectangle do you think looks more like a square? Explain your reasoning.",
#     "Expectations": """{"1": "The closer the ratio of width to length of a rectangle is to 1, the more it looks like a square.", "2": "The larger the sides of the rectangle with a 3-unit difference, the more it looks like a square.", "3": "The answer is 37 feet by 40 feet."} """ }

# conversation_log = [{'content': 'I feel  little confused', 'speaker': 'user'}, {'content': 'is this the end of this question?', 'speaker': 'user'}]
# conversation_log = [{'content': 'I think the answer is', 'speaker': 'user'}, {'content': '37 by 40 feet', 'speaker': 'user'}]

def process_input(_input = 'As the dimensions get larger, the ratios get closer to 1.', question = 'Comparing Dimensions', session_id='0'):
    # multiagent section 
    user_proxy = AssistantWriteAgent( # put in user utterance
        name="User",
        system_message=user_message,
        code_execution_config=False,
        llm_config=gpt4_config1,
        human_input_mode='NEVER'
    )

    judger = AssistantExpAgent( # check if reaching expectation
        name = 'Judger',
        system_message = judger_message, 
        description = agent_description, 
        llm_config=gpt4_config2, 
        human_input_mode='NEVER',
        writedown=True, writedir='log1-{}'.format(str(session_id))
    )
    groupchat = GroupChatExp(
        agents=[user_proxy, judger], messages=[], max_round=50, speaker_selection_method='round_robin'
    )

    manager = GroupChatManagerExp(groupchat=groupchat, llm_config=gpt4_config2, human_input_mode='NEVER', system_message=manager_message1, writedown=False, writedir='log1-{}'.format(str(session_id)))

    for agent in groupchat.agents:
        agent.reset()

    def run_one(input):
        user_proxy.initiate_chat(
        manager,
        message=input)
        return 1

    # path = os.path.join('/var/www/tutor/app/json')
    path = os.path.join(os.getcwd(), 'app', 'json')
    for file in os.listdir(path): 
        if question in file:
            with open(os.path.join(path, file), 'r') as f:    message_tmp = json.load(f)
    message_tmp = message_tmp[list(message_tmp.keys())[0]] # get the main content
    print(f"\nMessage_Tmp: {message_tmp}\n")

    # stages
    stage_keys = [k for k in message_tmp.keys() if 'Stage' in k]
    max_stage = max([int(re.findall('\d', item)[0]) for item in stage_keys])
    if collection.find_one({'session': session_id, 'type':'transit'}, sort=[('_id', -1)]):
        stage_now = collection.find_one({'session': session_id, 'type':'transit'}, sort=[('_id', -1)])['stage_now']
    else:
        stage_now = 'Stage1'
    # exps
    sub_message_tmp = message_tmp[stage_now]
    question_text = [item for item in sub_message_tmp["Prompt"] if not item.endswith(")")]
    exp_keys = [k for k in sub_message_tmp.keys() if 'Expectation' in k]
    expectations = ["""\"{}\":\"{}\"""".format(idx, sub_message_tmp['Expectation'+str(idx)]['Expectation']) for idx in range(1, len(exp_keys)+1)]
    expectations = "{" + ', '.join(expectations) + "}"
    true_expectations = ["""{}""".format(sub_message_tmp['Expectation'+str(idx)]['Expectation']) for idx in range(1, len(exp_keys)+1)]
    print("\nTrue Expectations\n")
    print(true_expectations)

    if True in [item.startswith("checkEquation(") for item in true_expectations]:
        expectation = true_expectations[0]
        pattern = r'checkEquation\((.*)\)$'
        equation = re.findall(pattern, expectation)[0]
        if "," in equation:
            correct_answer = equation.split(",")
        else:
            correct_answer = [equation]
        correct_answer = [item.strip() for item in correct_answer]
        if str(_input) in correct_answer:
            exp_list = [1] 
        else:
            exp_list = []
    else:
        main_input = """# Question = "{}"; # Expectations = "{}"; """.format(question_text, expectations)
        # conversation_log = []
        # for item in collection.find({'session': session_id, 'speaker': 'user'}, {'_id': 0, 'speaker': 1, 'content': 1}, sort=[('_id', -1)], limit=5).sort('_id', 1): conversation_log.append(item)

        # previous unreach-expectation answer:
        previous_answers = None
        if collection.find_one({'session': session_id, 'speaker': 'user', 'stage_now': stage_now}, sort=[('_id', -1)]):
            if collection.find_one({'session': session_id, 'speaker': 'user', 'stage_now': stage_now}, sort=[('_id', -1)])['target'] == -1:
                previous_answers = get_unreach_records(collection, session_id, 3)
        if previous_answers:
            user_input = previous_answers + '. ' + str(_input)
        else:
            user_input = str(_input)

        query = main_input + '# Response: ' + str(user_input)
        print("\nQuery\n")
        print(query)

        run_one(query)

        ## read in the log data
        with open('log1-{}'.format(str(session_id)), 'rb') as f: 
            allocator_data = pickle.load(f)
        allocator_data = allocator_data.replace('TERMINATE', '')
        if os.path.exists('log1-{}'.format(session_id)):
            os.remove('log1-{}'.format(session_id))
        allocator_data = allocator_data.replace('\\', '')
        print(">>>", allocator_data)
        
        try: 
            exp_list = json.loads(allocator_data)['output']
        except: 
            exp_list = []
        
    collection2.insert_one({'session_id':session_id, 'data':exp_list})

    if question != "Classroom Demographics":
        if len(exp_list)==0: # no expectation covered
            return dialogue_output(question = question, session_id=session_id, user_input = _input,main_input=main_input, message_tmp=message_tmp, expectations=expectations, stage_now=stage_now, max_stage=max_stage)
        else:
            return hint_output(question = question, session_id=session_id, user_input = _input, reached_exp=exp_list, message_tmp=message_tmp, expectations=expectations, stage_now=stage_now, max_stage=max_stage)
    else:
        return hint_output(question = question, session_id=session_id, user_input = _input, reached_exp=exp_list, message_tmp=message_tmp, expectations=expectations, stage_now=stage_now, max_stage=max_stage)

if __name__ == "__main__":
    print(process_input())