#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:03:20 2020

@author: dcaballe
Modulos    : Rele
Sub-Modulos: Rele
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 17/03/2020

Nombre     : Rele
Objetivo   : modoulo saber si esta activo el rele

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest05 por apache
http://192.168.137.220:5000/setrest05 por flask
{
	"mod":"fan",
    "est":"status"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector

 
setrest05 = Blueprint('setrest05', __name__)

@setrest05.route('/setrest05', methods=['POST'])
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
    db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
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
            pin_fan=(y)
            print(pin_fan)
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
            pin_fan=(y)
            print(pin_fan)
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
            pin_fan=(y)
            print(pin_fan)
    except Exception as e:
        print("ERROR EN:",str(e))
        codRes= 'ERROR'
        menRes = str(e)


