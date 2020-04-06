#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:41:30 2020

@author: root
"""

import pyfirmata
import time

board = pyfirmata.Arduino("/dev/ttyACM0")
pin0 = board.get_pin('a:0:i')

iterator = pyfirmata.util.Iterator(board)
iterator.start()
pin0.enable_reporting()

while True:
    if pin0.read() == None:
        pass
    else:
        x=(1023*pin0.read())/73.07
        print("El ph es: " +str(x))
        time.sleep (5)