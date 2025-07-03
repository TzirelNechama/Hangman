from functools import wraps
from random import shuffle
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

from User import User
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

def get_users():
    return json.loads(open('./allUsers.json').read())


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.cookies.get('id'):
            return func(*args, **kwargs)
        res = make_response("time is up!", 403)
        return res
    # wrapper.__name__ = func.__name__
    return wrapper

@cross_origin(app, supports_credentials=True)
@app.route('/login', methods=["GET"])
def login():
    obj = request.json
    users = get_users()
    if users.__contains__(obj['id']):
        if (users.get(obj['id']).get("user_name") == obj['name'] and
                users.get(obj['id']).get("password") == obj['password']):
            return "found"
        if (users.get(obj['id']).get("user_name") == obj['name'] and
                users.get(obj['id']).get("password") != obj['password']):
            return users.get(obj['id']).get("password")
        else:
            return "error"
    elif not users.__contains__(obj['id']):
        return "no"
    return "llleee"

@cross_origin(app, supports_credentials=True)
@app.route('/start_game', methods=["POST"])
def start_game():
    obj = request.json
    response = make_response(f"hello {obj['name']} you are ready to start the game!")
    # max_age - the number of seconds that you want the cookie to last.
    response.set_cookie('id', obj['id'], max_age=600, httponly=True, secure=False)
    return response

@cross_origin(app, supports_credentials=True)
@app.route('/add_user', methods=["POST"])
def add_user():
    print("add user in")
    obj = request.json
    file = open('allUsers.json').read()
    text = file[0:file.__len__() - 1]
    u = User(obj["name"], obj["id"], obj["pas"])
    file = open('allUsers.json', 'w')
    file.write(text + f',\n  "{obj['id']}": {str(u)}')
    file.close()
    return jsonify(f"Hello {obj['name']}")

# @decorator
# @cross_origin(app, supports_credentials=True)
# @app.route('/get_game_time', methods=["GET"])
# def get_game_time():
#     user_name = request.cookies.get('user_name')
#     if user_name:
#         return jsonify(f"Got cookie: {user_name}")

@cross_origin(app, supports_credentials=True)
@app.route('/get_word', methods=["GET"])
@decorator
def get_word():
    num = int(request.json["num"])
    fl = open('words.txt').read().split(", ")
    shuffle(fl)
    return fl[num % fl.__len__()]

@cross_origin(app, supports_credentials=True)
@app.route('/end_game', methods=["POST"])
@decorator
def end_game():
    users = get_users()
    win = request.json["win"]
    print(win)
    word = request.json["word"]
    print(word)
    idn = request.cookies.get('id')
    user = users.get(idn)
    if user:
        if win == 1:
            user['num_win'] += 1
        user['play_times'] += 1
        if not user['word_list'].__contains__(word):
            user['word_list'].append(word)
        users.update({idn: user})
        f = open('allUsers.json', 'w')
        u = str(users).replace("'", '"')
        f.write(u)
        f.close()
        return user
    return users


@cross_origin(app, supports_credentials=True)
@app.route('/get_history', methods=["GET"])
@decorator
def get_history():
    users = get_users()
    d = request.cookies.get('id')
    if d:
        return users[d]
    return "invalid id"

@cross_origin(app, supports_credentials=True)
@app.route('/relogin', methods=["GET"])
def relogin():
    users = get_users()
    obj = request.json
    if users.__contains__(obj['id']):
        res = make_response("found id")
        res.set_cookie('id', obj['id'], max_age=600, httponly=True, secure=False)
    return res


if __name__ == "__main__":
    app.run(debug=True)