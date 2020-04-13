#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:27:18 2020

Modulos    : DS18B20
Sub-Modulos: DS18B20
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/04/2020

Nombre     : ds18b20cons
Objetivo   : se encarga de devolver temperatura agua

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/scraping/ds18b20cons por apache
http://192.168.137.220:5000/ds18b20cons por flask
{
	"mod":"tanque"
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
 
ds18b20cons = Blueprint('ds18b20cons', __name__)

@ds18b20cons.route('/ds18b20cons', methods=['POST'])
def llamarServicioSet():
    global mod
    ##try:
    mod =request.json['mod']
    ubi =request.json['ubi']
    inicializarVariables(mod,ubi)
    
     
    salida = {'temp':r2,'codRes':codRes,'menRes':menRes}
    return jsonify({'ParmOut':salida})

def inicializarVariables(mod,ubi):
    global codRes, menRes,r2
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    r2='Null'
    mainpath="/var/www/html/scraping/"
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod,ubi)


def accesoSet(fullpath,mod,ubi):
    global menRes,codRes,r2
    f = Path(fullpath)
    f.exists()
    try:
        db=mysql.connector.connect(host='5.189.148.10',user='slave',passwd='sup3rPw#',database='hidroponia',port='23306',
                            ssl_ca='/etc/certs/ca.pem',ssl_cert='/etc/certs/client-cert.pem',ssl_key='/etc/certs/client-key2.pem')
    except Exception as e:
        print("ERROR EN: connect db local",str(e))
        codRes= 'ERROR'
        menRes = str(e)
    try:
        print(fullpath)
        print('seleccion de opcion')
        print(ubi)
        if ubi == "tanque":
            print ("opcion tanque")
            cursor=db.cursor() 
            sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            print(id_sensor)
            db.commit()
            sql="select temperatura from DS18B20 where id_sensor=%s order by id_ds desc limit 1"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            r2=(y)
            print(r2)  
            return r2
            
        if ubi == "semillero":
            print ("opcion semillero")
            cursor=db.cursor() 
            sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            print(id_sensor)
            db.commit()
            sql="select temperatura from DS18B20 where id_sensor=%s order by id_ds desc limit 1"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            r2=(y)
            print(r2)  
            return r2
        if ubi == "zona1":
            print ("opcion zona1")
            cursor=db.cursor() 
            sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            print(id_sensor)
            db.commit()
            sql="select temperatura from DS18B20 where id_sensor=%s order by id_ds desc limit 1"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            r2=(y)
            print(r2)  
            return r2
        if ubi == "zona2":
            print ("opcion zona2")
            cursor=db.cursor() 
            sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            print(id_sensor)
            db.commit()
            sql="select temperatura from DS18B20 where id_sensor=%s order by id_ds desc limit 1"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            r2=(y)
            print(r2)  
            return r2
        else:
            codRes= 'ERROR'
            menRes = 'Item no value'
            
            
                
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)