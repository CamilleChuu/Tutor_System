import re, json, time, os
from generate_response import rephrase

for file in os.listdir("../json"):
    if file.endswith("json") and (not os.path.exists(os.path.join("./app/json", 'rephrase', file))):
        if 'SM2' in file:
            with open(os.path.join("../json", file), 'r') as f: msg = json.load(f)
            print('processing ...', file)
            q = list(msg.keys())[0]
            msg = msg[q]
            new_msg = {}
            new_msg[q] = {}
            for k1 in msg.keys():
                if "Stage" in k1:
                    s = msg[k1]
                    new_msg[q][k1] = {}
                    for k2 in s.keys():
                        if "Expectation" in k2:
                            e = s[k2]
                            new_msg[q][k1][k2] = {}
                            for k3 in e.keys():
                                if "Hint" in k3:
                                    hint = e[k3]
                                    hint_list = []
                                    if not isinstance(hint, list):
                                        hint = [hint]
                                    for step in range(10):
                                        hint_tmp = []
                                        for hint_content in hint:
                                            if not hint_content.endswith(')'): # text hint
                                                hint_step = rephrase(str(hint_content))
                                            else: # action hint
                                                hint_step = hint_content
                                            hint_tmp.append(hint_step)
                                        hint_list.append(hint_tmp)
                                        new_msg[q][k1][k2][k3] = hint_list
                                        with open(os.path.join("../json", 'rephrase', file), 'w') as g: json.dump(new_msg, g)
            print('ended ...', file)