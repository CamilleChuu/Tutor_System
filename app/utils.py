# timecontrol decorator
import functools
import signal
import time, re
import openai

def timeout(sec):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            def _handle_timeout(signum, frame):
                err_msg = f'Function {func.__name__} timed out after {sec} seconds'
                raise TimeoutError(err_msg)
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapped_func
    return decorator

def find_match_in_sentence(input_sentence, choices):
    input_sentence = re.sub('[^\w\s]', '', input_sentence)
    words = input_sentence.split()
    choices_lower = [str(choice).lower() for choice in choices]
    for word in words:
        if word.lower()   in choices_lower:
            return [choice for choice, choice_lower in zip(choices, choices_lower) if choice_lower == word.lower()][0]
    return 'ERROR'

def llm_predict(messages, temperature = 0.5, max_tokens = 2):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens
            )
        predict = completion.choices[0].message['content']
    except openai.error.Timeout:
        print('time sleep')
        time.sleep(10)
    return predict

def llm_answer(messages, temperature = 0.5, max_tokens = 2):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens
            )
        predict = completion.choices[0].message['content']
    except openai.error.Timeout:
        print('time sleep')
        time.sleep(10)
    return predict

def symbol_control(_input):
    out = _input
    replacements = {'â€™': "\'",    'â€œ': '\"',    'â€': '\"',    'â€˜': "\'",    'â€¦': '…', }
    for k, v in replacements.items():
        out = out.replace(k ,v)
    return out