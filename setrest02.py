#!/usr/bin/env python
# -*- Coding: utf-8 -*-
"""
Modulos    : DHT11
Sub-Modulos: DHT11
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/03/2020

Nombre     : setrest02
Objetivo   : se encarga de tomcar temperatura y humedad ambiente

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest02 por apache
http://192.168.137.220:5000/setrest02 por flask
{
	"mod":"DHT11",
    "ubi":"entrada"
}
"""
from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import os, signal
from time import sleep
import pandas as pd
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
 
setrest02 = Blueprint('setrest02', __name__)

@setrest02.route('/setrest02', methods=['POST'])
def llamarServicioSet():
    global mod, ubi
    ##try:
    mod =request.json['mod']
    ubi =request.json['ubi']
    inicializarVariables(mod,ubi)
    
     
    salida = {'codRes': codRes, 'menRes': menRes}
    return jsonify({'ParmOut':salida})

def inicializarVariables(mod,ubi):
    global codRes, menRes
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    mainpath="/var/www/html/scraping/"
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod,ubi)


def accesoSet(fullpath,mod,ubi):
    global menRes,codRes
    f = Path(fullpath)
    f.exists()
    db=mysql.connector.connect(host='localhost',user='root',passwd='tecnologia',database='hidroponia')
    try:
        print(fullpath)
        print('seleccion de opcion')
        if ubi == "interior":
                print ("opcion interior")
                cursor=db.cursor() 
                sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
                nombre=(mod,ubi)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                z=int(y)
                print(z)
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                val=("1","2",z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente")
        elif ubi == "semillero":
                print ("opcion semillero")
                
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


