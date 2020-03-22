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
    south = 17 
    east = 27
    west = 22
    try:
        db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    except Exception as e:
        print("ERROR EN: connect db local",str(e))
        codRes= 'ERROR'
        menRes = str(e)
    try:
        db2=mysql.connector.connect(host='5.189.148.10',user='slave',passwd='sup3rPw#',database='hidroponia',port='23306',
                            ssl_ca='/etc/certs/ca.pem',ssl_cert='/etc/certs/client-cert.pem',ssl_key='/etc/certs/client-key2.pem')
    except Exception as e:
        print("ERROR EN: connect db web",str(e))
        codRes= 'ERROR'
        menRes = str(e)
    try:
        print(fullpath)
        print('seleccion de opcion')
        if ubi == "north":
                print ("opcion north")
                cursor=db.cursor() 
                #Se obtiene pin gpio
                sql="select gpio from sensor where ubi=%s"
                nombre=(ubi,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                north=(y)
                db.commit()
                print(north)
                humidity, temperature = dht.read_retry(sensor, north)
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
                #Base de datos local
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                #al=(temperature,humidity,z)
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente local")
                #Base de datos Wweb
                cursor=db2.cursor() 
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                val=(temperature,humidity,z)
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db2.commit()
                db2.close()
                print(cursor.rowcount,"insertado correctamente WEB")
        elif ubi == "south":
                print ("opcion south")
                cursor=db.cursor() 
                #Se obtiene pin gpio
                sql="select gpio from sensor where ubi=%s"
                nombre=(ubi,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                south=(y)
                db.commit()
                print(south)
                humidity, temperature = dht.read_retry(sensor, south)
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
                val=(temperature,humidity,z)
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente local")
                #Base de datos Wweb
                cursor=db2.cursor() 
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                val=(temperature,humidity,z)
                #val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db2.commit()
                db2.close()
                print(cursor.rowcount,"insertado correctamente WEB")
        elif ubi == "east":
                print ("opcion east")
                cursor=db.cursor() 
                #Se obtiene pin gpio
                sql="select gpio from sensor where ubi=%s"
                nombre=(ubi,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                east=(y)
                db.commit()
                print(east)
                humidity, temperature = dht.read_retry(sensor, east)
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
                val=(temperature,humidity,z)
                #val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente local")
                #Base de datos Wweb
                cursor=db2.cursor() 
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                #val=(temperature,humidity,z)
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db2.commit()
                db2.close()
                print(cursor.rowcount,"insertado correctamente WEB")
        elif ubi == "west":
                print ("opcion west")
                cursor=db.cursor() 
                #Se obtiene pin gpio
                sql="select gpio from sensor where ubi=%s"
                nombre=(ubi,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                west=(y)
                db.commit()
                print(west)
                humidity, temperature = dht.read_retry(sensor, west)
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
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db.commit()
                db.close()
                print(cursor.rowcount,"insertado correctamente local")
                #Base de datos Wweb
                cursor=db2.cursor() 
                sql="insert into DHT11 (temperatura,humedad,id_sensor) values(%s,%s,%s)"
                #val=(temperature,humidity,z)
                val=(temperature,humidity,z)
                cursor.execute(sql,val)
                db2.commit()
                db2.close()
                print(cursor.rowcount,"insertado correctamente WEB")
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


