#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:27:18 2020

Modulos    : ph
Sub-Modulos: ph
Empresa    : UNIDA PY

Autor      : Derlis Caballero
Fecha      : 28/03/2020

Nombre     : setrest23
Objetivo   : se encarga de devolver estados ph

Tipo       : Servicio Rest

Ej. llamada:
http://192.168.137.220/scrapgin/setrest23 por apache
http://192.168.137.107:5000/setrest23 por flask
{
	"mod":"uv"
}

Respeusta de servicio:
    {"ParmOut": {
   "uv": 0.137921
}}
"""
from flask import Blueprint, request, jsonify
import os
from unipath import Path
"""python -m pip install mysql-connector"""
import mysql.connector
 
setrest23 = Blueprint('setrest23', __name__)

@setrest23.route('/setrest23', methods=['POST'])
def llamarServicioSet():
    global mod
    ##try:
    mod =request.json['mod']
    inicializarVariables(mod)
    
     
    salida = {'uv':r2}
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
        if mod == "uv":
                print ("opcion uv")
                cursor=db.cursor() 
                sql="select uv from UV order by id_uv desc limit 1"
                cursor.execute(sql)
                result=cursor.fetchall()
                #Se convierte a string el resultado del select para poder insertar 
                a=(result[0])
                y = ''.join(map(str,a))
                z=float(y)
                print(z)
                db.commit()
                r2=z
                return r2
                print("finalizado")
        
        
       
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)
