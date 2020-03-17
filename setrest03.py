#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 22:52:11 2020
Modulos    : Rele
Sub-Modulos: Rele
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/03/2020

Nombre     : Rele
Objetivo   : modoulo para activar reles

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest03 por apache
http://192.168.137.220:5000/setrest03 por flask
{
	"mod":"fan",
    "est":"north"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector

 
setrest03 = Blueprint('setrest03', __name__)

@setrest03.route('/setrest03', methods=['POST'])
def llamarServicioSet():
    global mod, est
    ##try:
    mod =request.json['mod']
    est =request.json['est']
    inicializarVariables(mod,est)
    
     
    salida = {'codRes': codRes, 'menRes': menRes}
    return jsonify({'ParmOut':salida})
def inicializarVariables(mod,est):
    global codRes, menRes
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    mainpath="/var/www/html/scraping/"
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod,est)
def accesoSet(fullpath,mod,ubi):
    global menRes,codRes
    f = Path(fullpath)
    f.exists()
    db=mysql.connector.connect(host='localhost',user='root',passwd='tecnologia',database='hidroponia')
    try:
        print(fullpath)
        print('seleccion de opcion')
        if mod == "fan":
            print ("opcion fan")
            cursor=db.cursor() 
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_fan=(y)
            print(pin_fan)
            #Exportamos el PIN deseado
            os.system ('sudo echo %s > /sys/class/gpio/export'%pin_fan)
            mainpath="/sys/class/gpio/"
            fullpath= os.path.join(mainpath,"gpio"+pin_fan)
            #Establecemos la direccion (salida o entrada)
            os.system('sudo echo out > %s/direction'%fullpath)
            #Activamos la salida del rele dandole un valor de 1 al bit
            os.system('sudo echo 1 > %s/value'%fullpath)
        elif mod == "light":
            print ("opcion light")
            cursor=db.cursor() 
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_light=int(y)
            print(pin_light)
            #Exportamos el PIN deseado
            os.system ('sudo echo %s > /sys/class/gpio/export'%pin_fan)
            mainpath="/sys/class/gpio/"
            fullpath= os.path.join(mainpath,"gpio"+pin_fan)
            #Establecemos la direccion (salida o entrada)
            os.system('sudo echo out > %s/direction'%fullpath)
            #Activamos la salida del rele dandole un valor de 1 al bit
            os.system('sudo echo 1 > %s/value'%fullpath)
        elif mod == "motor":
            print ("opcion motor")
            cursor=db.cursor() 
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_motor=int(y)
            print(pin_motor)
            #Exportamos el PIN deseado
            os.system ('sudo echo %s > /sys/class/gpio/export'%pin_fan)
            mainpath="/sys/class/gpio/"
            fullpath= os.path.join(mainpath,"gpio"+pin_fan)
            #Establecemos la direccion (salida o entrada)
            os.system('sudo echo out > %s/direction'%fullpath)
            #Activamos la salida del rele dandole un valor de 1 al bit
            os.system('sudo echo 1 > %s/value'%fullpath)
        elif mod == "sprintkler":
            print ("opcion sprintkler")
            cursor=db.cursor() 
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_sprintkler=int(y)
            print(pin_sprintkler)
            #Exportamos el PIN deseado
            os.system ('sudo echo %s > /sys/class/gpio/export'%pin_fan)
            mainpath="/sys/class/gpio/"
            fullpath= os.path.join(mainpath,"gpio"+pin_fan)
            #Establecemos la direccion (salida o entrada)
            os.system('sudo echo out > %s/direction'%fullpath)
            #Activamos la salida del rele dandole un valor de 1 al bit
            os.system('sudo echo 1 > %s/value'%fullpath)
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)
