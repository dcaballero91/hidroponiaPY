# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 08:55:12 2020

@author: dcaballe
Modulos    : Rele
Sub-Modulos: Rele
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 17/03/2020

Nombre     : Rele
Objetivo   : modoulo para desactivar el rele

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest04 por apache
http://192.168.137.220:5000/setrest04 por flask
{
	"mod":"fan",
    "est":"D"
}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector

 
setrest04 = Blueprint('setrest04', __name__)

@setrest04.route('/setrest04', methods=['POST'])
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
            print(pin_fan)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=(y)
            db.commit()
            print(id_sensor)
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
            if estado == 'P' or estado=='D':
                cursor=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                nombre=(est,id_sensor)
                cursor.execute(sql,nombre)
                db.commit()
                print(cursor.rowcount, "record(s) affected")
            
                #Apagamos la salida del rele
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_fan)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo 0 > %s/value'%fullpath)
                #Liberamos el pin activasdo
                os.system('sudo echo %s > /sys/class/gpio/unexport'%pin_fan)
            elif estado =='A':
                codRes= 'ERROR'
                menRes = "ACTVIE"
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
            pin_fan=(y)
            db.commit()
            print(pin_fan)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=(y)
            db.commit()
            print(id_sensor)
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
            if estado == 'P' or estado=='D':
                cursor=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                nombre=(est,id_sensor)
                cursor.execute(sql,nombre)
                db.commit()
                print(cursor.rowcount, "record(s) affected")
            
                #Apagamos la salida del rele
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_fan)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo 0 > %s/value'%fullpath)
                #Liberamos el pin activasdo
                os.system('sudo echo %s > /sys/class/gpio/unexport'%pin_fan)
            elif estado =='A':
                codRes= 'ERROR'
                menRes = "ACTVIE"
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
            pin_fan=(y)
            db.commit()
            print(pin_fan)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=(y)
            db.commit()
            print(id_sensor)
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
            if estado == 'P' or estado=='D':
                cursor=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                nombre=(est,id_sensor)
                cursor.execute(sql,nombre)
                db.commit()
                print(cursor.rowcount, "record(s) affected")
            
                #Apagamos la salida del rele
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_fan)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo 0 > %s/value'%fullpath)
                #Liberamos el pin activasdo
                os.system('sudo echo %s > /sys/class/gpio/unexport'%pin_fan)
            elif estado =='A':
                codRes= 'ERROR'
                menRes = "ACTVIE"
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
            pin_fan=(y)
            db.commit()
            print(pin_fan)
            #Se obtiene id sensor
            sql="select id_sensor from sensor where descrip=%s"
            nombre=(mod,)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            #Se convierte a string el resultado del select para poder insertar 
            x=(result[0])
            y = ''.join(map(str,x))
            id_sensor=(y)
            db.commit()
            print(id_sensor)
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
            if estado == 'P' or estado=='D':
                cursor=db.cursor() 
                sql="update Rele set estado=%s where id_sensor=%s"
                nombre=(est,id_sensor)
                cursor.execute(sql,nombre)
                db.commit()
                print(cursor.rowcount, "record(s) affected")
            
                #Apagamos la salida del rele
                mainpath="/sys/class/gpio/"
                fullpath= os.path.join(mainpath,"gpio"+pin_fan)
                #Establecemos la direccion (salida o entrada)
                os.system('sudo echo 0 > %s/value'%fullpath)
                #Liberamos el pin activasdo
                os.system('sudo echo %s > /sys/class/gpio/unexport'%pin_fan)
            elif estado =='A':
                codRes= 'ERROR'
                menRes = "ACTVIE"
            else:
                codRes= 'ERROR'
                menRes = "ESTADO INVALIDO"
    except Exception as e:
        print("ERROR EN:",str(e))
        codRes= 'ERROR'
        menRes = str(e)
