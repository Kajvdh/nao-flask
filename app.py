#!flask/bin/python
from flask import Flask, abort, jsonify, request
import naoqi

from naoqi import ALProxy
import logger


app = Flask(__name__)

nao_host = "192.168.0.154"
nao_port = 9559
logger = logger.Logger(4) # Initialize logger with level "debug"


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

@app.route('/volume', methods=['GET'])
def get_volume():
    logger.debug("set_volume() called")
    audioDeviceProxy = ALProxy("ALAudioDeviceProxy", nao_host, nao_port)
    level = str(audioDeviceProxy.getOutputVolume())
    return jsonify({"volume": level}), 200

@app.route('/volume/<int:volume>', methods=['POST'])
def set_volume(volume):
    logger.debug("set_volume() called")
    vol = int(volume)
    if ((vol <= 100) and (vol >= 0)):
        audioDeviceProxy = ALProxy("ALAudioDeviceProxy", nao_host, nao_port)
        audioDeviceProxy.setOutputVolume(vol)
        return jsonify({"volume": vol}), 200
    else:
        return jsonify({"error": "Volume out of range [0,100]"}), 400


@app.route('/temperature', methods=['GET'])
def get_temperature_diagnosis():
    logger.debug("get_temperature_diagnosis() called")
    bodyTemperatureProxy = ALProxy("ALBodyTemperatureProxy", nao_host, nao_port)
    level = str(bodyTemperatureProxy.getTemperatureDiagnosis())
    return jsonify({"temperature": level}), 200

@app.route('/battery', methods=['GET'])
def get_battery_level():
    logger.debug("get_batteryLevel() called")
    batteryProxy = ALProxy("ALBattery", nao_host, nao_port)
    level = str(batteryProxy.getBatteryCharge())
    return jsonify({"battery": level}), 200

@app.route('/behaviors', methods=['GET'])
def get_behaviors():
    logger.debug("get_behaviors() called")
    managerProxy = ALProxy("ALBehaviorManager", nao_host, nao_port)
    behaviors = managerProxy.getInstalledBehaviors()
    return jsonify({"behaviors": behaviors}), 200

@app.route('/behaviors/start', methods=['POST'])
def start_behavior():
    logger.debug("start_behavior() called")
    if not request.json or not 'behavior' in request.json:
        abort(400)
    behavior = str(request.json['behavior'])
    managerProxy = ALProxy("ALBehaviorManager", nao_host, nao_port)

    if (managerProxy.isBehaviorInstalled(behavior)):
        logger.debug("Behavior "+behavior+" is present on the robot, starting behavior...")
        managerProxy.post.runBehavior(behavior)
        return jsonify({"started": behavior}), 200
    else:
        logger.debug("Behavior "+behavior+" is NOT present on the robot")
        return jsonify({"error": "Behavior not found"}), 404

@app.route('/behaviors/stop', methods=['POST'])
def stop_behavior():
    logger.debug("stop_behavior() called")
    if not request.json or not 'behavior' in request.json:
        abort(400)
    behavior = str(request.json['behavior'])
    managerProxy = ALProxy("ALBehaviorManager", nao_host, nao_port)

    if (managerProxy.isBehaviorRunning(behavior)):
        logger.debug("Behavior "+behavior+" is running on the robot, stopping behavior...")
        managerProxy.stopBehavior(behavior)
        return jsonify({"stopped": behavior}), 200
    else:
        logger.debug("Behavior "+behavior+" is NOT running on the robot")
        return jsonify({"error": "Behavior not running"}), 404

@app.route('/behaviors/stop/all', methods=['GET'])
def stop_behaviors():
    logger.debug("stop_behaviors() called")
    managerProxy = ALProxy("ALBehaviorManager", nao_host, nao_port)
    behaviors = managerProxy.getRunningBehaviors()

    if (len(behaviors) > 0):
        managerProxy.stopAllBehaviors()
        return jsonify({"stopped": behaviors}), 200
    else:
        return jsonify({"error": "No running behaviors"}), 400


@app.route('/say', methods=['POST'])
def say():
    if not request.json or not 'text' in request.json:
        abort(400)
    tts = ALProxy("ALTextToSpeech", nao_host, nao_port)
    tts.say(str(request.json['text']))
    return jsonify({'text': request.json['text']}), 200

@app.route('/ask/<string:question>', methods=['GET'])
def ask(question):
    tts = ALProxy("ALTextToSpeech", nao_host, nao_port)
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
