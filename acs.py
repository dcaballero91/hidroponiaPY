#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 22:05:45 2020

@author: root
"""
import pyfirmata
import time

board = pyfirmata.Arduino("/dev/ttyACM0")
pin0 = board.get_pin('a:0:i')


iterator = pyfirmata.util.Iterator(board)
iterator.start()
pin0.enable_reporting()
pin=str(pin0.read())
print("pin0: "+pin)


def drummer(x):
    counter = 0
    inst_current=0
    av_current=0
    nMuestras=100
    # time.sleep(time.time() * 8 % 1 / 8) # enable to sync clock for demo
    for counter in range(nMuestras):
       
        #print (time.time())
        inst_current= 0.0254*(float(x) - 512);
        if inst_current < 0:
            #maximo valor del muestreo
            inst_current= - inst_current;
    av_current = av_current + inst_current / float(nMuestras) ;
    print("Av_current: " + str(av_current))
    return av_current
        
while True:
    if pin0.read() == None:
        pass
    else:
        sensor_max=drummer()
        print(str(sensor_max))
        Irms= float(1.1107) * float(sensor_max);
        print("Irms: " + str(Irms)+" [A]")
        s=220*float(Irms)
        print("S: " + str(s) + "[VA]")
        #pin2.disable_reporting
        pin0.disable_reporting
        time.sleep (5)

