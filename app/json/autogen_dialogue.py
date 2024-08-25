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
from autogen.agentchat import ConversableWritableAgent
from autogen.agentchat import AssistantWriteAgent

from autogen.agentchat.assistant_exp_agent import AssistantExpAgent

# from autogen.agentchat import UserProxyAgent
# from autogen.agentchat import AssistantAgent
from autogen.agentchat.groupchat_exp import GroupChatExp, GroupChatManagerExp
from agent_prompt import user_message, judger_message, allocator_message, rephraser_message, responser_message, manager_message, agent_description
from exp_utils import process_output, json_converter
os.environ['AUTOGEN_USE_DOCKER'] = '0'

import argparse

today = datetime.now().strftime("%Y%m%d")

from autogen import config_list_from_json

if int(4) == 4: 
    gpt_name = "gpt-4-1106-preview"
else:
    gpt_name = "gpt-3.5-turbo-1106"
config_list_gpt4 = config_list_from_json(
    "./notebook/OAI_CONFIG_LIST",
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

user_proxy = AssistantWriteAgent( # put in user utterance
    name="User",
    system_message=user_message,
    code_execution_config=False,
    llm_config=gpt4_config2,
    human_input_mode='NEVER'
)

judger = AssistantExpAgent( # check if reaching expectation
    name = 'Judger',
    system_message = judger_message, 
    description = agent_description, 
    llm_config=gpt4_config, 
    human_input_mode='NEVER'
)

allocator = AssistantExpAgent( # check the condition and go to next step
    name = 'Allocator',
    system_message = allocator_message, 
    description = agent_description, 
    llm_config=gpt4_config, 
    human_input_mode='NEVER'
)

rephraser = AssistantExpAgent( # if yes, rephrase hints
    name = 'Rephraser',
    system_message = rephraser_message, 
    description = agent_description, 
    llm_config=gpt4_config2,
    human_input_mode='NEVER'
)

responser = AssistantWriteAgent( # if no, generate new response
    name="responser",
    system_message= responser_message,
    description = "A helpful AI assistant who has strong language skills, generating responses to a dialogue.",
    llm_config=gpt4_config, human_input_mode='NEVER', writedown = True
)

# control the group logic
groupchat = GroupChatExp(
    agents=[user_proxy, judger, allocator, rephraser, responser], messages=[], max_round=50, speaker_selection_method='auto'
)

manager = GroupChatManagerExp(groupchat=groupchat, llm_config=gpt4_config, human_input_mode='NEVER', system_message=manager_message, writedown=False, writedir='log')

for agent in groupchat.agents:
    agent.reset()

def run_one(input):
    user_proxy.initiate_chat(
    manager,
    message=input)
    return 1


input_data_template =  {
    "Question": "Dimensions of the four rectangles are given as: 7 by 10 feet, 17 by 20 feet, 27 by 30 feet, 37 by 40 feet. Which rectangle do you think looks more like a square? Explain your reasoning.",
    "Expectations": """{"1": "The closer the ratio of width to length of a rectangle is to 1, the more it looks like a square.", "2": "The larger the sides of the rectangle with a 3-unit difference, the more it looks like a square.", "3": "The answer is 37 feet by 40 feet."} """ },
main_input = """# Question = "{}"; # Expectations = "{}"; """.format(input_data_template["Question"], input_data_template["Expectations"])

conversation_log = [{'content': 'I feel  little confused', 'speaker': 'user'}, {'content': 'is this the end of this question?', 'speaker': 'user'}]

query = main_input + '# Input Data' + str(conversation_log)

run_one(query)