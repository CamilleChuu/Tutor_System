# from app.autogen.brieffeedback import feedback_dict
from app.autogen.myutils import get_user_input, is_valid_num_input, update_chat_log, process_exp, induce_exp_idx
import random, json, os, re
from datetime import datetime
from app.autogen.generate_response import rephrase, answer, teach, courage, summarize, check_partial
from app.autogen.unreach_retrieve import count_unreach_records

from app.autogen.autogen_support2 import closing_output
from app.dialogue_open import opening_prompts
from pymongo import MongoClient
# db = MongoClient('localhost', 27017)['tutor_sys']
# collection = db['demo']
mongo_uri = os.getenv('MONGODB_URI')  
client = MongoClient(mongo_uri)
db = client['tutor_sys'] 
collection = db['demo'] 

def get_reached_exp(session_id):
    # prepare the expectation log set
    try:
        if int(collection.find_one({'session': session_id, 'speaker': 'system'}, sort=[('_id', -1)])['end']) ==0: # last record is the middle step
            expectation_log = set(collection.find_one({'session': session_id, 'speaker': 'system'}, sort=[('_id', -1)])['reached'])
            last_attempt_id = collection.find_one({'session': session_id, 'speaker': 'system'}, sort=[('_id', -1)])['target']
        else:
            expectation_log = set()
            last_attempt_id = -1
    except: 
        expectation_log = set()
        last_attempt_id = -1
    return expectation_log, last_attempt_id


def courage_output(question, session_id, user_input, reached_exp, message_tmp, expectations):
    exp_tmp = '; '.join(["Expectation {}: ".format(str(d)) + str(message_tmp['Expectation'+str(d)]) for d in reached_exp])
    question_tmp = '; '.join([msg for msg in message_tmp['Prompt']])
    main_input = "# Question: {}. # User Response : {}. # Expectation: {}".format(question_tmp, user_input, exp_tmp)
    response_tmp =  courage(main_input)
    # _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
    return response_tmp

def hint_output(question, session_id, user_input, reached_exp, message_tmp, expectations, stage_now, max_stage):
    _output = []
    # feedback_tmp = str(random.choice(feedback_dict['PositiveFeedback']))
    # previous reached exp
    expectation_output = json.loads(expectations)
    full_exp_order = [int(d) for d in expectation_output.keys()]
    expectation_log, last_attempt_id = get_reached_exp(session_id)
    for d in reached_exp: expectation_log.add(int(d))
    # if there are new expectation to cover
    target = induce_exp_idx(expectation_log, full_exp_order)

    if target is not None:
        encourage_msg = courage_output(question, session_id, user_input, reached_exp, message_tmp[stage_now], expectations)
        _output.append({"type":"text", "content": encourage_msg, 'reached':list(expectation_log), 'end':0})
        collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'text', 'content':str(encourage_msg), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
        _output += rephraser_block(question, session_id, user_input, message_tmp, expectations, expectation_log, last_attempt_id, target, stage_now, max_stage)
    else: # target is None; end of the stage of dialogue
        stage_order = int(re.findall('\d', stage_now)[0])
        if max_stage == stage_order:
            # transit_msg = 'END OF ALL STAGES'
            # collection.insert_one({'session':session_id, 'question':question, 'type':'transit', 'stage_now':stage_now, 'content':transit_msg, 'time':datetime.utcnow().timestamp(), 'end':0})
            # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':1})
            # _output += [{"type":"text", "content":transit_msg , 'end':0}]
            ending_message = [{"type":"text", "content":"Great! You've mastered all the knowledge in this activity!", 'reached':list(expectation_log), 'end':1}]
            _output = _output + ending_message
            _output = closing_output(question, session_id, user_input, expectation_log, _output)
            _output = _output
        else: 
            stage_order += 1
            stage_now = "Stage" + str(stage_order)
            transit_msg = 'TRANSIT TO NEW {}'.format(stage_now) ## transit message
            _output += [{"type":"text", "content":transit_msg , 'end':0}]
            collection.insert_one({'session':session_id, 'question':question, 'type':'transit', 'stage_now':stage_now, 'content':transit_msg, 'time':datetime.utcnow().timestamp(), 'end':0})

            _output += opening_prompts(message_tmp, stage_now, question, session_id, )

        """collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':1})

        # _output.append({"type":"text", "content": feedback_tmp, 'end':1})
        # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})

        for conclusion_content in message_tmp['Conclusion']:
            if not conclusion_content.endswith(')'): # text conclusion
                _output.append({"type":"text", "content":conclusion_content, 'reached':list(expectation_log), 'end':1})
                collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':conclusion_content, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})
            else:
                _output.append({"type":'action', "content":str(conclusion_content), 'reached':list(expectation_log), 'end':1})
                collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(conclusion_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':1})"""
    return _output

def dialogue_output(question, session_id, user_input, main_input, message_tmp, expectations, stage_now, max_stage):
    _output = []
    expectation_log, last_attempt_id = get_reached_exp(session_id)
    # feedback_tmp = str(random.choice(feedback_dict['NegativeFeedback']))
    # _output.append({"type":"text", "content": feedback_tmp, 'end':0})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

    dialogue_hist = list(collection.find({'session': session_id,}, {'_id': 0, 'speaker': 1, 'content': 1}, sort=[('_id', -1)], limit=5))[::-1]
    collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})

    question_tmp = '; '.join([msg for msg in message_tmp[stage_now]['Prompt'] if not msg.endswith(")")])
    checking_input = "## User Statement: {}; Math Question: {};".format(user_input, message_tmp[stage_now]['Prompt'])
    checking_result = 'yes' in check_partial(checking_input).lower()

    if checking_result: # related to question, although incorrect
        expectation_output = json.loads(expectations)
        full_exp_order = [int(d) for d in expectation_output.keys()]
        expectation_log, last_attempt_id = get_reached_exp(session_id)
        target = induce_exp_idx(expectation_log, full_exp_order)
        if count_unreach_records(collection, session_id, limit = 3): # too many attempts; teach it
            main_input += '# Expectation to Teach: {}'.format(str(target))
            expectation_log.add(int(target))
            response_tmp =  teach(main_input)
            _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':-1, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0}) # add an empty user message to update the reached list
            if set(expectation_log) == set(full_exp_order):
                _output = closing_output(question, session_id, user_input, expectation_log, _output)
                _output = _output
            else:
                response_tmp = "Then what else can you say about this question?"
                _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
                collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
        else: # no enough attempt, give pre-defined hint by rephrasing
            _output += rephraser_block(question, session_id, user_input, message_tmp, expectations, expectation_log, last_attempt_id, target, stage_now, max_stage)
            _output = _output
    else: # totally NOT related to question
        if count_unreach_records(collection, session_id, limit = 5): # too many attempts; teach it
            expectation_output = json.loads(expectations)
            full_exp_order = [int(d) for d in expectation_output.keys()]
            expectation_log, last_attempt_id = get_reached_exp(session_id)
            target = induce_exp_idx(expectation_log, full_exp_order)
            main_input += '# Expectation to Teach: {}'.format(str(target))
            expectation_log.add(int(target))
            response_tmp =  teach(main_input)
            _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content':-1, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0}) # add an empty user message to update the reached list
            if set(expectation_log) == set(full_exp_order):
                _output = closing_output(question, session_id, user_input, expectation_log, _output)
                _output = _output
            else:
                response_tmp = "Then what else can you say about this question?"
                _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
                collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})
        else:
            main_input += "\n# Math Question: " + str(message_tmp[stage_now]['Prompt']) +"\n# Dialogue: "+str(dialogue_hist) 
            response_tmp = answer(main_input)
            _output.append({"type":"text", "content":response_tmp, 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'type':'action', 'content':str(response_tmp), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':-1, 'target2':-1, 'end':0})
    return _output
    
    
def rephraser_block(question, session_id, user_input, message_tmp, expectations, expectation_log, last_attempt_id, target, stage_now, max_stage):
    _output = []
    collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})

    # _output.append({"type":"text", "content": feedback_tmp, 'end':0})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

    # select a hint
    hint_keys = [k for k in message_tmp[stage_now]['Expectation'+str(target)].keys() if 'Hint' in k]
    if str(target) != str(last_attempt_id):
        # hint_key_tmp = random.choice(hint_keys)
        hint_key_tmp = 'Hint1'
    else:
        try: 
            last_hint = collection.find_one({'session': session_id, 'speaker': 'system', 'stage_now':stage_now, 'target':target}, sort=[('_id', -1)])['target2']
            last_hint = str(last_hint)
        except:
            last_hint = 'Hint0'
        last_hint_order = int(re.findall('\d', last_hint)[0])
        hint_key_tmp = 'Hint' + str(last_hint_order+1)
        if hint_key_tmp not in message_tmp[stage_now]['Expectation'+str(target)].keys(): # run out hints
            hint_key_tmp = random.choice([e for e in hint_keys if e != last_hint])
        # hint_key_tmp = random.choice([e for e in hint_keys if e != last_hint])

    # for file in os.listdir('/var/www/tutor/app/json/rephrase'):
    #     if question in file:
    #         with open(os.path.join('/var/www/tutor/app/json/rephrase', file), 'r') as f: new_msg = json.load(f)
    # hint_list_tmp = new_msg[list(new_msg.keys())[0]][stage_now]['Expectation'+str(target)][hint_key_tmp]
    # hint_list_tmp = random.choice(hint_list_tmp)

    rephrase_path = os.environ.get('REPHRASE_JSON_PATH', './app/json/rephrase')
    
    for file in os.listdir(rephrase_path):
        if question in file:
            with open(os.path.join(rephrase_path, file), 'r') as f:
                new_msg = json.load(f)
                
    hint_list_tmp = new_msg[list(new_msg.keys())[0]][stage_now]['Expectation'+str(target)][hint_key_tmp]
    hint_list_tmp = random.choice(hint_list_tmp)


    for hint_content in hint_list_tmp:
        if not hint_content.endswith(')'): # text hint
            hint_tmp = hint_content
            # _output.append({"type":"text", "content": "Rephraser: EXP{}, {}, last{}".format(target, hint_key_tmp, last_attempt_id), 'reached':list(expectation_log), 'end':0})
            _output.append({"type":"text", "content": hint_tmp, 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
        else: # action hint
            _output.append({"type":'action', "content":str(hint_content), 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'action', 'content':str(hint_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
    return _output


"""BACKUP def rephraser_block(question, session_id, user_input, message_tmp, expectations, expectation_log, last_attempt_id, target, stage_now, max_stage):
    _output = []
    collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'text', 'content':user_input, 'speaker':'user', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':-1, 'end':0})

    # _output.append({"type":"text", "content": feedback_tmp, 'end':0})
    # collection.insert_one({'session':session_id, 'question':question, 'type':'text', 'content': feedback_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'end':0})

    # select a hint
    hint_keys = [k for k in message_tmp[stage_now]['Expectation'+str(target)].keys() if 'Hint' in k]
    if str(target) != str(last_attempt_id):
        # hint_key_tmp = random.choice(hint_keys)
        hint_key_tmp = 'Hint1'
    else:
        try: 
            last_hint = collection.find_one({'session': session_id, 'speaker': 'system', 'stage_now':stage_now, 'target':target}, sort=[('_id', -1)])['target2']
        except:
            last_hint = 'Hint0'
        last_hint_order = int(re.findall('\d', last_hint)[0])
        hint_key_tmp = 'Hint' + str(last_hint_order+1)
        if hint_key_tmp not in message_tmp[stage_now]['Expectation'+str(target)].keys(): # run out hints
            hint_key_tmp = random.choice([e for e in hint_keys if e != last_hint])
        # hint_key_tmp = random.choice([e for e in hint_keys if e != last_hint])

    if isinstance(message_tmp[stage_now]['Expectation'+str(target)][hint_key_tmp], list):
        hint_list_tmp = message_tmp[stage_now]['Expectation'+str(target)][hint_key_tmp]
    else:
        hint_list_tmp = [message_tmp[stage_now]['Expectation'+str(target)][hint_key_tmp]]

    for hint_content in hint_list_tmp:
        if not hint_content.endswith(')'): # text hint
            hint_tmp = rephrase(str(hint_content))
            _output.append({"type":"text", "content": "Rephraser: EXP{}, {}, last{}".format(target, hint_key_tmp, last_attempt_id), 'reached':list(expectation_log), 'end':0})
            _output.append({"type":"text", "content": hint_tmp, 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'text', 'content':hint_tmp, 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
        else: # action hint
            _output.append({"type":'action', "content":str(hint_content), 'reached':list(expectation_log), 'end':0})
            collection.insert_one({'session':session_id, 'question':question, 'stage_now':stage_now, 'type':'action', 'content':str(hint_content), 'speaker':'system', 'time':datetime.utcnow().timestamp(), 'reached':list(expectation_log), 'target':target, 'target2':hint_key_tmp, 'end':0})
    return _output"""