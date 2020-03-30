#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 22:41:30 2020

@author: root
"""

import pyfirmata
import time
board=pyfirmata.Arduino('/dev/ttyACM0')
flame_pin = board.get_pin('d:6:i')
indicator_pin=board.get_pin('d:7:o')
it=pyfirmata.util.Iterator(board)
it.start()
flame_pin.enable_reporting()
while True:
    flame_state=flame_pin.read()#read digital pin
    print(str(flame_state))
    if flame_state == False: #check conditio
        print('No obstacle')
        indicator_pin.write(1)
        time.sleep(0.2)
    else:
        print("Obstacule Found")
        indicator_pin.write(0)
        time.sleep(0.2)
        



