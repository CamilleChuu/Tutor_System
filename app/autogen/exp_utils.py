import re, json, os, pickle

def json_converter(data):
    try:
        d1 = json.loads(re.findall('\[[\d\s,]*\]', data)[0])
        d2 = json.loads(re.sub('\n', '', re.findall(r'\{.*?\}', data, re.DOTALL)[0]))
        d3 = json.loads(re.sub('\n', '', re.findall(r'\{.*?\}', data, re.DOTALL)[1]))
        return d1, d2, d3
    except:
        try:
            data2 = data.replace("\'output\'", '\"output\"').replace("\'evidence\'", '\"evidence\"')
            d1 = json.loads(re.findall('\[[\d\s,]*\]', data2)[0])
            d2 = json.loads(re.sub('\n', '', re.findall(r'\{.*?\}', data2, re.DOTALL)[0]))
            d3 = json.loads(re.sub('\n', '', re.findall(r'\{.*?\}', data2, re.DOTALL)[1]))
            return d1, d2, d3
        except:
            try:
                d2 = re.sub('\n', '', re.findall(r'\{.*?\}', data, re.DOTALL)[0])
                try: d2a = re.findall('["\']output["\']\s*:\s.*(\[[\d\s,]*\])', d2)[0]
                except: d2a = []
                try: d2b = re.findall('[\'"]evidence[\'"]\s*:(.*)', d2)[0]
                except: d2b =''
                a2 = {'output':json.loads(d2a), 'evidence':d2b} 
                try:
                    d3 = re.sub('\n', '', re.findall(r'\{.*?\}', data, re.DOTALL)[1])
                    try: d3a = re.findall('["\']output["\']\s*:\s.*(\[[\d\s,]*\])', d3)[0]
                    except: d3a = []
                    try: d3b = re.findall('[\'"]evidence[\'"]\s*:(.*)', d3)[0]
                    except: d3b = ''
                    d3 = {'output':json.loads(d3a), 'evidence':d3b} 
                except:
                    if 'AGREEMENT' in data:
                        a3 = {'output':d2['evidence'], 'evidence':'no evidence'} 
                try: 
                    a1 = json.loads(re.findall('\[[\d\s,]*\]', data)[0])
                except: 
                    if 'AGREEMENT' in data:
                        a1 = d2['output']
                return a1, a2, a3
            except:
                print(data)
                return 0
                # return [], {"output":[], "evidence":"on evidence provided."}, {"output":[], "evidence":"on evidence provided."}
            
def process_output(dir):
    with open(dir, 'rb') as f:  data = pickle.load(f)
    return json_converter(data)