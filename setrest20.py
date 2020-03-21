#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:27:18 2020

Modulos    : DHT11
Sub-Modulos: DHT11
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/03/2020

Nombre     : setrest20
Objetivo   : se encarga de devolver temperatura y humedad ambiente

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest20 por apache
http://192.168.137.220:5000/setrest20 por flask
{
	"mod":"DHT11"
}

Respeusta de servicio:
    {"ParmOut": {
   "hum": 39,
   "temp": 31.5
}}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
 
setrest20 = Blueprint('setrest20', __name__)

@setrest20.route('/setrest20', methods=['POST'])
def llamarServicioSet():
    global mod
    ##try:
    mod =request.json['mod']
    inicializarVariables(mod)
    
     
    salida = {'temp':r2,'hum':r3}
    return jsonify({'ParmOut':salida})

def inicializarVariables(mod):
    global codRes, menRes,r2,r3
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    mainpath="/var/www/html/scraping/"
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod)


def accesoSet(fullpath,mod):
    global menRes,codRes,r2,r3
    f = Path(fullpath)
    f.exists()
    db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    try:
        print(fullpath)
        print('seleccion de opcion')
        if mod == "DHT11":
                print ("opcion DHT11")
                cursor=db.cursor() 
                sql="select temperatura from DHT11 order by id_dh desc limit 4"
                cursor.execute(sql)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                z=float(y)
                b=(result[1])
                w = ''.join(map(str,b))
                x=float(w)
                r=z+x;
                a=(result[2])
                y = ''.join(map(str,a))
                z=float(y)
                b=(result[3])
                w = ''.join(map(str,b))
                x=float(w)
                r2=((r+z+x)/4);
                print(r2)
                db.commit()
                cursor=db.cursor() 
                sql="select humedad from DHT11 order by id_dh desc limit 4"
                cursor.execute(sql)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                z=float(y)
                b=(result[1])
                w = ''.join(map(str,b))
                x=float(w)
                r=z+x;
                a=(result[2])
                y = ''.join(map(str,a))
                z=float(y)
                b=(result[3])
                w = ''.join(map(str,b))
                x=float(w)
                r3=((r+z+x)/4);
                print(r3)
                db.commit()
                db.close()
                return r2,r3
                print("promedio finalizado")
        elif mod == "south":
                print ("opcion south")
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)