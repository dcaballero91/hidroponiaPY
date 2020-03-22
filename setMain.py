#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from flask import Flask, jsonify, request
from setrest01 import setrest01
from setrest02 import setrest02
from setrest20 import setrest20
from setrest21 import setrest21
from setrest03 import setrest03
from setrest04 import setrest04
from setrest05 import setrest05
from setrest06 import setrest06
app = Flask(__name__) 

##servicios rest
app.register_blueprint(setrest01)
app.register_blueprint(setrest02)
app.register_blueprint(setrest20)
app.register_blueprint(setrest21)
app.register_blueprint(setrest03)
app.register_blueprint(setrest04)
app.register_blueprint(setrest05)
app.register_blueprint(setrest06)
@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    ##app.run(host = '127.0.0.1', debug = True, port = 5000)
    app.run(host = '0.0.0.0', debug = True, port = 5000)
    app.run(debug = True)
