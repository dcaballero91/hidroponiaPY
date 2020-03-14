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
http://192.168.137.220/scrapgin/setrest02
{
	"mod":"DHT11",
    "ubi":"entrada"
}
"""
from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import os, signal
from time import sleep
import pandas as pd
from unipath import Path
 
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

    try:
        print(fullpath)
        print('seleccion de opcion')
        if ubi == "entrada":
                print ("opcion entrada")
        elif ubi == "semillero":
                print ("opcion semillero")
                
        
             
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        codRes= 'ERROR'
        menRes = str(e)


