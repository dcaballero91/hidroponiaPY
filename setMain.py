#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from flask import Flask, jsonify, request
from setrest01 import setrest01
from setrest02 import setrest02
from bcprest01 import bcprest01
from bcprest02 import bcprest02
app = Flask(__name__) 

##servicios rest
app.register_blueprint(setrest01)
app.register_blueprint(setrest02)
app.register_blueprint(bcprest01)
app.register_blueprint(bcprest02)
@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    ##app.run(host = '127.0.0.1', debug = True, port = 5000)
    app.run(host = '0.0.0.0', debug = True, port = 5000)
    app.run(debug = True)
