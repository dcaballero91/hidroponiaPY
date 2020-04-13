#!/usr/bin/env python
# -*- Coding: utf-8 -*-
"""
Modulos    : DS18B20
Sub-Modulos: DS18B20
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 12/03/2020

Nombre     : ds18b20
Objetivo   : se encarga de tomcar tempratura del agua

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scraping/ds18b20 por apache
http://192.168.137.220:5000/ds18b20 por flask
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
import time
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 

 
def read_temp_raw(fol):
    base_dir = '/sys/bus/w1/devices/'
    #device_folder = glob.glob(base_dir + '28*')[0]
    base_dir = '/sys/bus/w1/devices/'+fol
    device_file = base_dir + '/w1_slave'
    
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(fol):
    lines = read_temp_raw(fol)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
ds18b20 = Blueprint('ds18b20', __name__)

@ds18b20.route('/ds18b20', methods=['POST'])

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
    
 
    
    #device_folder = glob.glob(base_dir + '28*')[0]
    
    fullpath= os.path.join(mainpath)
    accesoSet(fullpath,mod,ubi)



def accesoSet(fullpath,mod,ubi):
    global menRes,codRes
    f = Path(fullpath)
    f.exists()
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
            sql="select sensor.descrip from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            descrip=(y)
            print(descrip)
            fol=descrip
            temp=(read_temp(fol))
            print(temp)
            db.commit()
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor.execute(sql,val)
            db.commit()
            db.close()
            print(cursor.rowcount,"insertado correctamente local")
            cursor2=db2.cursor() 
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor2.execute(sql,val)
            db2.commit()
            db2.close()
            print(cursor.rowcount,"insertado correctamente para la web")
            
        elif ubi == "semillero":
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
            sql="select sensor.descrip from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            descrip=(y)
            print(descrip)
            fol=descrip
            temp=(read_temp(fol))
            print(temp)
            db.commit()
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor.execute(sql,val)
            db.commit()
            db.close()
            print(cursor.rowcount,"insertado correctamente local")
            cursor2=db2.cursor() 
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor2.execute(sql,val)
            db2.commit()
            db2.close()
            print(cursor.rowcount,"insertado correctamente para la web")
        
        elif ubi == "zona1":
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
            sql="select sensor.descrip from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            descrip=(y)
            print(descrip)
            fol=descrip
            temp=(read_temp(fol))
            print(temp)
            db.commit()
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor.execute(sql,val)
            db.commit()
            db.close()
            print(cursor.rowcount,"insertado correctamente local")
            cursor2=db2.cursor() 
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor2.execute(sql,val)
            db2.commit()
            db2.close()
            print(cursor.rowcount,"insertado correctamente para la web")
        elif ubi == "zona2":
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
            sql="select sensor.descrip from sensor inner join station on sensor.id_est = station.id_est where sensor.nombre= %s and sensor.ubi=%s"
            nombre=(mod,ubi)
            cursor.execute(sql,nombre)
            result=cursor.fetchall()
            x=(result[0])
            y = ''.join(map(str,x))
            descrip=(y)
            print(descrip)
            fol=descrip
            temp=(read_temp(fol))
            print(temp)
            db.commit()
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor.execute(sql,val)
            db.commit()
            db.close()
            print(cursor.rowcount,"insertado correctamente local")
            cursor2=db2.cursor() 
            sql="insert into DS18B20 (temperatura,id_sensor) values(%s,%s)"
            val=(temp,id_sensor)
            cursor2.execute(sql,val)
            db2.commit()
            db2.close()
            print(cursor.rowcount,"insertado correctamente para la web")
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


