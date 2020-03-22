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
http://192.168.137.220/scrapgin/setrest06 por apache
http://192.168.137.220:5000/setrest06 por flask
{
	"mod":"fan",
    "est":"A"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector

 
setrest06 = Blueprint('setrest06', __name__)

@setrest06.route('/setrest06', methods=['POST'])
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
def accesoSet(fullpath,mod,est):
    global menRes,codRes
    f = Path(fullpath)
    f.exists()
    try:
        db=mysql.connector.connect(host='5.189.148.10',user='slave',passwd='sup3rPw#',database='hidroponia',port='23306',
                            ssl_ca='/etc/certs/ca.pem',ssl_cert='/etc/certs/client-cert.pem',ssl_key='/etc/certs/client-key2.pem')
    except Exception as e:
        print("ERROR EN: connect db web",str(e))
        codRes= 'ERROR'
        menRes = str(e)
    try:
        print(fullpath)
        print('seleccion de opcion')
        if mod == "fan":
            print ("opcion fan")
            cursor=db.cursor() 
            #Se obtiene pin gpio
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_fan=(y)
            db.commit()
            print("pin fan:",pin_fan)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            db.commit()
            print("id sensor",id_sensor)
            #Encontrar estado
            sql="select estado from Rele where id_sensor=%s"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            estado=(y)
            print("Estado:",estado)
            db.commit()
            if estado =="P":
                codRes= 'ERROR'
                menRes = "PROCESO"
                
            elif estado == "A":
                #Actualizamos estado
                cursorUpdate=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                val=(est,id_sensor)
                cursorUpdate.execute(sql,val)
                db.commit()
                db.close()
                print(cursorUpdate.rowcount, "record(s) affected")
                #Exportamos el PIN deseado
                os.system ('sudo echo %s > /sys/class/gpio/export'%pin_fan)
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_fan)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo out > %s/direction'%fullpath)
                #Activamos la salida del rele dandole un valor de 1 al bit
                os.system('sudo echo 1 > %s/value'%fullpath)
            elif estado == "D":
                codRes= 'ERROR'
                menRes = "DESACT OF MARKET FOR DESACT"
            else:
                codRes= 'ERROR'
                menRes = "ESTADO INVALIDO"
        elif mod == "light":
            print ("opcion light")
            cursor=db.cursor() 
            #Se obtiene pin gpio
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_light=(y)
            db.commit()
            print("pin light:",pin_light)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            db.commit()
            print("id sensor",id_sensor)
            #Encontrar estado
            sql="select estado from Rele where id_sensor=%s"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            estado=(y)
            print("Estado:",estado)
            db.commit()
            if estado =="P":
                codRes= 'ERROR'
                menRes = "PROCESO"
                
            elif estado == "A":
                #Actualizamos estado
                cursorUpdate=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                val=(est,id_sensor)
                cursorUpdate.execute(sql,val)
                db.commit()
                db.close()
                print(cursorUpdate.rowcount, "record(s) affected")
                #Exportamos el PIN deseado
                os.system ('sudo echo %s > /sys/class/gpio/export'%pin_light)
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_light)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo out > %s/direction'%fullpath)
                #Activamos la salida del rele dandole un valor de 1 al bit
                os.system('sudo echo 1 > %s/value'%fullpath)
            elif estado == "D":
                codRes= 'ERROR'
                menRes = "DESACT OF MARKET FOR DESACT"
            else:
                codRes= 'ERROR'
                menRes = "ESTADO INVALIDO"
        elif mod == "motor":
            print ("opcion motor")
            cursor=db.cursor() 
            #Se obtiene pin gpio
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_motor=(y)
            db.commit()
            print("pin light:",pin_motor)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            db.commit()
            print("id sensor",id_sensor)
            #Encontrar estado
            sql="select estado from Rele where id_sensor=%s"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            estado=(y)
            print("Estado:",estado)
            db.commit()
            if estado =="P":
                codRes= 'ERROR'
                menRes = "PROCESO"
                
            elif estado == "A":
                #Actualizamos estado
                cursorUpdate=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                val=(est,id_sensor)
                cursorUpdate.execute(sql,val)
                db.commit()
                db.close()
                print(cursorUpdate.rowcount, "record(s) affected")
                #Exportamos el PIN deseado
                os.system ('sudo echo %s > /sys/class/gpio/export'%pin_motor)
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_motor)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo out > %s/direction'%fullpath)
                #Activamos la salida del rele dandole un valor de 1 al bit
                os.system('sudo echo 1 > %s/value'%fullpath)
            elif estado == "D":
                codRes= 'ERROR'
                menRes = "DESACT OF MARKET FOR DESACT"
            else:
                codRes= 'ERROR'
                menRes = "ESTADO INVALIDO"
        elif mod == "sprintkler":
            print ("opcion sprintkler")
            cursor=db.cursor() 
            #Se obtiene pin gpio
            sql="select gpio from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            pin_sprintkler=(y)
            db.commit()
            print("pin light:",pin_sprintkler)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=int(y)
            db.commit()
            print("id sensor",id_sensor)
            #Encontrar estado
            sql="select estado from Rele where id_sensor=%s"
            nombre=(id_sensor,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            estado=(y)
            print("Estado:",estado)
            if estado =="P":
                codRes= 'ERROR'
                menRes = "PROCESO"
                
            elif estado == "A":
                #Actualizamos estado
                cursorUpdate=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                val=(est,id_sensor)
                cursorUpdate.execute(sql,val)
                db.commit()
                db.close()
                print(cursorUpdate.rowcount, "record(s) affected")
                #Exportamos el PIN deseado
                os.system ('sudo echo %s > /sys/class/gpio/export'%pin_sprintkler)
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_sprintkler)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo out > %s/direction'%fullpath)
                #Activamos la salida del rele dandole un valor de 1 al bit
                os.system('sudo echo 1 > %s/value'%fullpath)
            elif estado == "D":
                codRes= 'ERROR'
                menRes = "DESACT OF MARKET FOR DESACT"
            else:
                codRes= 'ERROR'
                menRes = "ESTADO INVALIDO"
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)
