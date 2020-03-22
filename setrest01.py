#!/usr/bin/env python
# -*- Coding: utf-8 -*-
"""
Modulos    : DS18B20
Sub-Modulos: DS18B20
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/03/2020

Nombre     : setrest01
Objetivo   : se encarga de tomcar tempratura del agua tanque

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest01 por apache
http://192.168.137.220:500/setrest01 por flask
{
	"mod":"DS18B20",
    "ubi":"tanque"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
 
setrest01 = Blueprint('setrest01', __name__)

@setrest01.route('/setrest01', methods=['POST'])
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
    db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    db2=mysql.connector.connect(host='5.189.148.10',user='slave',passwd='sup3rPw#',database='hidroponia',port='23306',
                                ssl_ca='/etc/certs/ca.pem',ssl_cert='/etc/certs/client-cert.pem',ssl_key='/etc/certs/client-key2.pem')
    try:
        print(fullpath)
        print('seleccion de opcion')
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
            z=int(y)
            print(z)
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=("1",z)
            cursor.execute(sql,val)
            db.commit()
            db.close()
            print(cursor.rowcount,"insertado correctamente local")
            cursor=db2.cursor() 
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=("1",z)
            cursor.execute(sql,val)
            db2.commit()
            db2.close()
            print(cursor.rowcount,"insertado correctamente para la web")
            
        elif ubi == "semillero":
                print ("opcion semillero")
                
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


