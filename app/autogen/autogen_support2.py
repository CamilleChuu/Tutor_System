# from app.autogen.brieffeedback import feedback_dict
from app.autogen.myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
import random, json, os, re
from datetime import datetime
from app.autogen.generate_response import rephrase, answer, teach, courage, summarize
from app.autogen.unreach_retrieve import count_unreach_records

from pymongo import MongoClient
db = MongoClient('localhost', 27017)['tutor_sys']
collection = db['demo']

def get_reached_exp(session_id):
    # prepare the expectation log set
    try:
        if int(collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['end']) ==0: # last record is the middle step
            expectation_log = set(collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['reached'])
            last_attempt_id = collection.find_one({'session': session_id, 'speaker': 'user'}, sort=[('_id', -1)])['target']
        else:
            expectation_log = set()
            last_attempt_id = -1
    except: 
        expectation_log = set()
        last_attempt_id = -1
    return expectation_log, last_attempt_id

def hint_output2(question, session_id, user_input, reached_exp, message_tmp, expectations):
    _output = []
    
    # previous reached exp
    expectation_output = json.loads(expectations)
    full_exp_order = [int(d) for d in expectation_output.keys()]
    expectation_log, last_attempt_id = get_reached_exp(session_id)
    for d in reached_exp: expectation_log.add(int(d))
    # if there are new expectation to cover
    target = induce_exp_idx(expectation_log, full_exp_order)
    # if len(reached_exp) > 0:
        # feedback_tmp = str(random.choice(feedback_dict['PositiveFeedback']))
        # _output.append({"type":"text", "content": feedback_tmp, 'end':0})
        # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})
    
    if target is not None:
        collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'end':0})
        # select a hint
        hint_keys = [k for k in message_tmp['Expectation'+str(target)].keys() if 'Hint' in k]
        if str(target) != str(last_attempt_id):
            hint_key_tmp = 'Hint1'
        else:
            # try: 
                last_hint = collection.find_one({'session': session_id, 'speaker': 'system', 'target':target}, sort=[("_id", -1)])['target2']

                last_hint = int(re.findall('Hint(\d)', last_hint)[0])
            # except:
            #     last_hint = 0
                hint_key_tmp = 'Hint' + str(last_hint + 1)

        if not hint_key_tmp in message_tmp['Expectation'+str(target)].keys():
            _output = closing_output(question, session_id, user_input, message_tmp, expectation_log, _output)
        else:
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
        _output = closing_output(question, session_id, user_input, message_tmp, expectation_log, _output)
    return _output

def summarize_output(question, session_id, user_input, message_tmp, expectation_log, _output):
    exp_tmp = '; '.join(["Expectation {}: ".format(str(d)) + str(message_tmp['Expectation'+str(d)]) for d in range(5) if ("Expectation{}".format(str(d)) in message_tmp.keys())])
    question_tmp = '; '.join([msg for msg in message_tmp['Prompt']])
    stack = collection.find({'session': session_id, 'speaker':'user', 'type':'text'},{'content':1}, sort=[('_id', -1)])
    statement_tmp = str([item['content'] for item in stack])

    main_input = "# Question: {}. # User Statements: {}. # Expectation: {}".format(question_tmp, statement_tmp, exp_tmp)
    response_tmp =  summarize(main_input)
    # _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
    return response_tmp

def closing_output(question, session_id, user_input, expectation_log, _output):
    path = os.path.join('/var/www/tutor/app/json')
    for file in os.listdir(path): 
        if question in file:
            with open(os.path.join(path, file), 'r') as f:    message_tmp = json.load(f)
    message_tmp = message_tmp[list(message_tmp.keys())[0]] # get the main content
    # feedback_tmp = str(random.choice(feedback_dict['PositiveFeedback']))
    
    # _output.append({"type":"text", "content": feedback_tmp, 'end':1})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})

    closing_message = []

    # ###summary of the whole dialogue
    # summarize_msg = 'TEST_ending: '+ summarize_output(question, session_id, user_input, message_tmp, expectation_log, _output)
    # _output.append({"type":"text", "content":summarize_msg, 'reached':list(expectation_log), 'end':1})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':summarize_msg, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})

    for closing_k in ["Conclusion", "Closing"]:
        if closing_k in message_tmp.keys():
                closing_message.extend(message_tmp[closing_k])
    for conclusion_content in closing_message:
        if not conclusion_content.endswith(')'): # text conclusion
            _output.append({"type":"text", "content":conclusion_content, 'reached':list(expectation_log), 'end':1})
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':conclusion_content, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
        else:
            _output.append({"type":'action', "content":str(conclusion_content), 'reached':list(expectation_log), 'end':1})
            collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(conclusion_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
    if "Summary Content" in message_tmp.keys():
        summary = ['<strong style="color: red;">Summary</strong>'] + ["&#8226 {}".format(item) for item in message_tmp["Summary Content"]]
        summary_content = "<br>".join(summary)
        _output.append({"type":"summary", "content":summary_content, 'reached':list(expectation_log), 'end':1})
        collection.insert_one({'session':session_id, 'question':question, 'type':'summary', 'content':summary_content, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
    return _output

def dialogue_output2(question, session_id, user_input, main_input, message_tmp, expectations):
    _output = []
    expectation_log, last_attempt_id = get_reached_exp(session_id)
    # feedback_tmp = str(random.choice(feedback_dict['NegativeFeedback']))
    # _output.append({"type":"text", "content": feedback_tmp, 'end':0})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

    dialogue_hist = list(collection.find({'session': session_id,}, {'_id': 0, 'speaker': 1, 'content': 1}, sort=[('_id', -1)], limit=5))[::-1]
    collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})

    if count_unreach_records(collection, session_id, limit = 3):
        expectation_output = json.loads(expectations)
        full_exp_order = [int(d) for d in expectation_output.keys()]
        expectation_log, last_attempt_id = get_reached_exp(session_id)
        target = induce_exp_idx(expectation_log, full_exp_order)
        main_input += '# Expectation to Teach: {}'.format(str(target))
        expectation_log.add(int(target))
        response_tmp =  teach(main_input)
        _output.append({"type":"text", "content":response_tmp, 'end':0})
        collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
    else:
        main_input += "# Dialogue: "+str(dialogue_hist)
        response_tmp = answer(main_input)
        _output.append({"type":"text", "content":response_tmp, 'end':0})
        collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})
    return _output
    
    