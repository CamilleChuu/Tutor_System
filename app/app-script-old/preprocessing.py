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
# from .message_list import message_dict
# from .brieffeedback import feedback_dict

from .myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
from .utils import llm_predict, symbol_control, find_match_in_sentence, timeout
from .ckprompt2 import initial_prompt, role_prompt, inchat_prompt, expectation_prompt

def preprocess1(_input): # check question or not 
    output = 'ERROR'
    # main process
    while output not in [0, 1]:
        messages = [{"role": "system", "content": "A helpful assistant checking if the input text is declarative sentence or interrogative sentence. If the text is declarative sentence, output 1. If the text is interrogative sentence, output 0. Just reply with 0 or 1 without further explanation. Output format: a value in [0, 1]."}]
        messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
        predict = llm_predict(messages, temperature = 0.3, max_tokens = 5)
        output = find_match_in_sentence(predict,  [0, 1])
    return output

def preprocess2(_input): # for declarative ones, further check if meaningful or not
    output = 'ERROR'
    # main process
    while output not in [0, 1]:
        messages = [{"role": "system", "content": "A helpful assistant checking if the input text is meaningful utterance or filler words. If the text is meaningful utterance (words, phrases or sentences), output 1. If the text is filler words (such as 'okay', 'well'), output 0. Just reply with 0 or 1 without further explanation. Output format: a value in [0, 1]."}]
        messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
        predict = llm_predict(messages, temperature = 0.3, max_tokens = 5)
        output = find_match_in_sentence(predict,  [0, 1])
    return output