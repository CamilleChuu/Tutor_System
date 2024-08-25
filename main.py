from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
# from app.dialogue_new import process_input
from app.dialogue_open import opening
from app.action_saving import action_saving
from app.session_generate import generate_session_id
from app.account import register_account, login_account
from app.progress import retrieve_progress
from app.autogen.autogen_dialogue import process_input
import os

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_tutor'  # Replace with your MongoDB connection URI
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/welcomepage')
def welcomepage():
    return render_template('./index2.html')

@app.route('/progress')
def progress():
    return render_template('./progress.html')

@app.route('/progress2')
def progress2():
    return render_template('./progress2.html')

@app.route('/get_progress',  methods=['POST', 'GET'])
def get_progress():
    data = request.json
    username = data.get('user')
    output = retrieve_progress(username)
    return output

@app.route('/test')
def test():
    return 'test'

@app.route('/register', methods=['POST', 'GET'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname')
    output_code = register_account(username, password, nickname)
    return output_code

@app.route('/login', methods=['POST', 'GET'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    output_code = login_account(username, password)
    return output_code

@app.route('/dialogue_new', methods=['POST', 'GET'])
def dialogue():
    data = request.json
    user_input = data.get('userInput')
    question_input = data.get('question')
    session_id = data.get('sessionID')
    bot_output = process_input(user_input, question_input, session_id)
    # Echoes back the user input
    return jsonify(bot_output)

@app.route('/dialogue_open', methods=['POST', 'GET'])
def dialogue_open():
    data = request.json
    question_input = data.get('question')
    session_id = data.get('sessionID')
    bot_output = opening(question_input, session_id)
    return jsonify(bot_output)
    # response = [{'content':'test content 1'}, {'content':'test content 2'}]
    # response = jsonify(response)
    # return response

# @app.route('/dialogue_close', methods=['POST', 'GET'])
# def dialogue_close():
#     data = request.json
#     question_input = data.get('question')
#     session_id = data.get('sessionID')
#     bot_output =closing(question_input, session_id)
#     return jsonify(bot_output)

@app.route('/get_sessionid', methods=['POST', 'GET'])
def get_sessionid():
    data = request.json
    question_input = data.get('question')
    user_input = data.get('user')
    id_output = generate_session_id(topic=question_input, user=user_input)
    return jsonify(id_output)

@app.route('/action_return', methods=['POST', 'GET'])
def action_return():
    data = request.json
    action_type = data.get('action')
    action_content = data.get('content')
    session_id = data.get('sessionID')
    bot_output = action_saving(action_type, action_content, session_id)
    return jsonify(bot_output)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)

