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
from .message_list import message_dict
from .brieffeedback import feedback_dict

from .myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
from .utils import llm_predict, symbol_control, find_match_in_sentence, timeout
from .ckprompt2 import initial_prompt, role_prompt, inchat_prompt, expectation_prompt

def rephrase(_input):
    # main process
    messages = [{"role": "system", "content": "A helpful assistant rephrasing the Input Text, without changing, adding or removing the main points. Do not make outputs too long and verbose. Do not change formulas and equations (such like 7/10=70%, x*y*y=xy^2, etc.). Do not change the mathematical terms and concepts. Please keep the sentence mood (interrogative or declarative). Remember you just need to give the rephrased content of input, DO NOT add explanations or section header, do not answer it."}]
    messages.append({"role": "user", "content": '# Input Text: ' + str(_input)})
    predict = llm_predict(messages, temperature = 1.6, max_tokens = 2000)
    return predict