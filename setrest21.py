#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:27:18 2020

Modulos    : rele
Sub-Modulos: rele
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 17/03/2020

Nombre     : setrest20
Objetivo   : se encarga de devolver temperatura y humedad ambiente

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest21 por apache
http://192.168.137.107:5000/setrest21 por flask
{
	"mod":"fan"
}

Respeusta de servicio:
    {"ParmOut": {
   "est": act
}}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
 
setrest21 = Blueprint('setrest21', __name__)

@setrest21.route('/setrest21', methods=['POST'])
def llamarServicioSet():
    global mod
    ##try:
    mod =request.json['mod']
    inicializarVariables(mod)
    
     
    salida = {'est':r2}
    return jsonify({'ParmOut':salida})

def inicializarVariables(mod):
    global codRes, menRes,r2
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    mainpath="/var/www/html/scraping/"
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod)


def accesoSet(fullpath,mod):
    global menRes,codRes,r2
    f = Path(fullpath)
    f.exists()
    db=mysql.connector.connect(host='localhost',user='root',passwd='sup3rPw#',database='hidroponia')
    try:
        print(fullpath)
        print('seleccion de opcion')
        if mod == "fan":
                print ("opcion fan")
                cursor=db.cursor() 
                sql="select Rele.estado from sensor inner join Rele on sensor.id_sensor=Rele.id_sensor where sensor.descrip=%s"
                nombre=(mod,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                r2=(y)
                print(r2)
                db.commit()
                return r2
                print("promedio finalizado")
        elif mod == "light":
                print ("opcion light")
                cursor=db.cursor() 
                sql="select Rele.estado from sensor inner join Rele on sensor.id_sensor=Rele.id_sensor where sensor.descrip=%s"
                nombre=(mod,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                r2=(y)
                print(r2)
                db.commit()
                return r2
        elif mod == "motor":
                print ("opcion motor")
                cursor=db.cursor() 
                sql="select Rele.estado from sensor inner join Rele on sensor.id_sensor=Rele.id_sensor where sensor.descrip=%s"
                nombre=(mod,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                r2=(y)
                print(r2)
                db.commit()
                return r2
        elif mod == "sprintkler":
                print ("opcion sprintkler")
                cursor=db.cursor() 
                sql="select Rele.estado from sensor inner join Rele on sensor.id_sensor=Rele.id_sensor where sensor.descrip=%s"
                nombre=(mod,)
                cursor.execute(sql,nombre)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                r2=(y)
                print(r2)
                db.commit()
                return r2
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)