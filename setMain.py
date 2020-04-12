#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from flask import Flask, jsonify, request
from ds18b20 import ds18b20
from setrest02 import setrest02
from setrest03 import setrest03
from setrest04 import setrest04
from setrest05 import setrest05
from setrest06 import setrest06
from setrest07 import setrest07
from setrest08 import setrest08
from setrest09 import setrest09
from setrest20 import setrest20
from setrest21 import setrest21
from setrest22 import setrest22
from setrest23 import setrest23
from setrest24 import setrest24
app = Flask(__name__) 

##servicios rest
app.register_blueprint(ds18b20)
app.register_blueprint(setrest02)
app.register_blueprint(setrest03)
app.register_blueprint(setrest04)
app.register_blueprint(setrest05)
app.register_blueprint(setrest06)
app.register_blueprint(setrest07)
app.register_blueprint(setrest08)
app.register_blueprint(setrest09)
app.register_blueprint(setrest20)
app.register_blueprint(setrest21)
app.register_blueprint(setrest22)
app.register_blueprint(setrest23)
app.register_blueprint(setrest24)
@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


if __name__ == "__main__":
    ##app.run(host = '127.0.0.1', debug = True, port = 5000)
    app.run(host = '0.0.0.0', debug = True, port = 5000)
    app.run(debug = True)
