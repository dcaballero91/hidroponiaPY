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
    "ubi":"north"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
import Adafruit_DHT as dht
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
    # Configuracion del tipo de sensor DHT
    sensor = dht.DHT22

    # Configuracion del puerto GPIO al cual esta conectado  (GPIO 23)
    north = 4
    south = 6 
    east = 7
    west = 8
    db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    try:
        print(fullpath)
        print('seleccion de opcion')
        
		
        if ubi == "north":
                print ("opcion north")
                #humidity, temperature = dht.read_retry(sensor, north)
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
                #val=(temperature,humidity,z)
                val=('30','30',z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente")
        elif ubi == "south":
                print ("opcion south")
                #humidity, temperature = dht.read_retry(sensor, south)
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
                #val=(temperature,humidity,z)
                val=('31','41',z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
        elif ubi == "east":
                print ("opcion east")
                #umidity, temperature = dht.read_retry(sensor, east)
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
                #val=(temperature,humidity,z)
                val=('32','42',z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
        elif ubi == "west":
                print ("opcion west")
                #umidity, temperature = dht.read_retry(sensor, west)
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
                #val=(temperature,humidity,z)
                val=('33','43',z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


