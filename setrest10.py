#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:44:05 2020

@author: root
"""

# the sensor has to be connected to pin 1 for power, pin 6 for ground
# and pin 7 for signal(board numbering!).
 
import time, sys
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
def action(pin):
    print('Sensor detected action!')
    return
 
GPIO.add_event_detect(19, GPIO.RISING)
GPIO.add_event_callback(19, action)
 
try:
    while True:
        print('alive')
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()