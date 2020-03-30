#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulos    : ACS
Sub-Modulos: ACS
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 28/03/2020

Nombre     : setrest09
Objetivo   : se encarga de tomar consumo de la llave

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest09 por apache
http://192.168.137.220:5000/setrest09 por flask
{
	"mod":"acs",
    "ubi":"llave"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
import pyfirmata
 
setrest09 = Blueprint('setrest09', __name__)

@setrest09.route('/setrest09', methods=['POST'])
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
    board = pyfirmata.Arduino("/dev/ttyACM0")

    
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
        if ubi == "llave":
                print ("opcion tanque")
                cursor=db.cursor() 
                #Se obtiene pin gpio
                sql="select gpio from sensor where ubi=%s and nombre=%s"
                nombre=(ubi,mod)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                x=(result[0])
                y = ''.join(map(str,x))
                s=(y)
                db.commit()
                print("Pin",s)
                pin="pin"+s
                pin = board.get_pin('a:0:i')
                iterator = pyfirmata.util.Iterator(board)
                iterator.start()
                pin.enable_reporting()
                if pin.read() == None:
                    pass
                else:
                    average=0
                    for i in range(1000):
            #       print(i)
            
                        average=average+((0.0264 * pin.read())-13.51)/1000
                        """esto es 
                        para 5Amperes, para sensor de20A o 30A modifica con:
                        (.19 * analogRead(A0) -25) para 20A 
                        (.044 * analogRead(A0) -3.78) para  30A """
                    print("Corriente: " +str(average))
                    pin.disable_reporting()
                    cursor=db.cursor() 
                    sql="select sensor.id_sensor from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
                    nombre=(mod,ubi,)
                    cursor.execute(sql,nombre)
                    result=cursor.fetchall()
                    #Se convierte a string el resultado del select para poder insertar 
                    x=(result[0])
                    y = ''.join(map(str,x))
                    z=int(y)
                    print("Id sensor",z)
                    print("Corriente: ", average)
                    #Base de datos local
                    sql="insert into ACS (volt,id_sensor) values(%s,%s)"
                    val=(average,z)
                    cursor.execute(sql,val)
                    db.commit()
                    db.close()
                    print(cursor.rowcount,"insertado correctamente local")
                    #Base de datos Wweb
                    cursor=db2.cursor() 
                    sql="insert into ACS (volt,id_sensor) values(%s,%s)"
                    val=(average,z)
                    cursor.execute(sql,val)
                    db2.commit()
                    db2.close()
                    print(cursor.rowcount,"insertado correctamente WEB")
         
        
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)

