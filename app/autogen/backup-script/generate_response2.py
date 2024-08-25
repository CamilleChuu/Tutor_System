import os, pickle
import warnings, random
import pandas as pd
import numpy as np
from tqdm import tqdm
import re, json, time
from datetime import datetime

import openai
from pymongo import MongoClient

# from question_list import question_dict
# from message_list import message_dict
# from brieffeedback import feedback_dict

from myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
from utils import llm_predict, symbol_control, find_match_in_sentence, timeout
from ckprompt2 import initial_prompt, role_prompt, inchat_prompt, expectation_prompt

from agent_prompt import responser_message, tutor_message, navigator_message, summarizer_message, checking_message, rephraser_message


def rephrase(_input):
    # main process
    messages = [{"role": "system", "content": rephraser_message}]
    messages.append({"role": "user", "content": '# Input Hint: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.6, max_tokens = 2000, new=True)
    return predict

def answer(_input):
    # main process
    messages = [{"role": "system", "content": responser_message}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.0, max_tokens = 300)
    return predict

def teach(_input):
    # main process
    messages = [{"role": "system", "content": tutor_message}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.0, max_tokens = 300)
    return predict

def courage(_input):
    # main process
    messages = [{"role": "system", "content": navigator_message}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.0, max_tokens = 150)
    return predict

def summarize(_input):
    # main process
    messages = [{"role": "system", "content": summarizer_message}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.0, max_tokens = 180)
    return predict

def check_partial(_input):
    messages = [{"role": "system", "content": checking_message}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 0.1, max_tokens = 10)
    return predict