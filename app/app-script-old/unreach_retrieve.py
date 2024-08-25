from bson.objectid import ObjectId
def get_unreach_records(collection, session_id='0', length = 99):
    results = collection.find({'session': session_id, 'speaker': 'user', 'target': -1}, sort=[('_id', -1)])
    last_record_satisfies_condition = True
    filtered_results = []
    i = 0
    for result in results:
        last_record_satisfies_condition = (result['session'] == session_id and result['speaker'] == 'user' and result['target'] == -1)
        if last_record_satisfies_condition:
            filtered_results.append(result['content'])
            i += 1
        if (not last_record_satisfies_condition) or (i >=length):
            break
    return '. '.join(filtered_results)    