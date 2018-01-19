from flask import Flask, jsonify, request
import math

app = Flask(__name__)

@app.route('/seed/<int:id>')
def seed(id):
    return '%09d' % id

def logrange(p, min, max):
    return min * math.exp(p * math.log(max/min))

@app.route('/sample')
def sample():
    system = {
        'w': 67*4,
        'h': 126*4,
        'axiom': 'A',
        'limit': 5000,
        'lineLength': 5*4,
        'lineWidth': 3*4,
        'scaleStep': 1.0 + logrange(.5, 0.001, 0.5),
        'angle': logrange(.5, 5, 200),
        'angle0': 0,
        'iterations': 3,
        'rules': {
            'S': 'SJSJ',
            'J': 'JJ',
        }
    }
    return jsonify(system)

@app.route('/preferences', methods=['POST'])
def preferences():
    data = request.get_json()
    print('going to store', data)
    return jsonify(data)
