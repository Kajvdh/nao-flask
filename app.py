#!flask/bin/python
from flask import Flask, abort, jsonify, request
import naoqi

from naoqi import ALProxy


app = Flask(__name__)

nao_host = "localhost"
nao_port = 39726

@app.route('/')
def index():
    return "Hello, World!"

robots = [
    {
        'id': 1,
        'title': u'Nao',
        'description': u'The default Nao robot'
    },
    {
        'id': 2,
        'title': u'Zora',
        'description': u'An advanced Nao robot that takes care of your health'
    }
]

@app.route('/say', methods=['POST'])
def say():
    if not request.json or not 'text' in request.json:
        abort(400)
    tts = ALProxy("ALTextToSpeech", "localhost", 39726)
    tts.say(str(request.json['text']))
    return jsonify({'text': request.json['text']}), 200

@app.route('/ask/<string:question>', methods=['GET'])
def ask(question):
    tts = ALProxy("ALTextToSpeech", "localhost", 39726)
    tts.say(str(question))
    return jsonify({'question': question}), 200

@app.route('/robots', methods=['GET'])
def get_robots():
    return jsonify({'robots': robots}), 200

@app.route('/robots/<int:robot_id>', methods=['GET'])
def get_robot(robot_id):
    robot = [robot for robot in robots if robot['id'] == robot_id]
    if len(robot) == 0:
        abort(404)
    return jsonify({'robot': robot[0]}), 200

if __name__ == '__main__':
    app.run(debug=True)
