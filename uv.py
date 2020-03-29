#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 19:19:16 2020

@author: root
"""

import pyfirmata
import time

board = pyfirmata.Arduino("/dev/ttyACM0")
pin1 = board.get_pin('a:0:i')

iterator = pyfirmata.util.Iterator(board)
iterator.start()
pin1.enable_reporting()

while True:
    if pin1.read() == None:
        pass
    else:
        x=(pin1.read()/1024*5)
        print("UV es: " +str(x))
        pin1.disable_reporting()
        time.sleep (5)