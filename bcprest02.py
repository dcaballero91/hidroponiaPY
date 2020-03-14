#!/usr/bin/env python3
# -*- Coding: utf-8 -*-
"""
Modulos    : Reportes para BCP
Sub-Modulos: CRC
Empresa    : Vision Banco S.A.E.C.A

Autor      : Derlis Caballero
Fecha      : 30/01/2020

Nombre     : bcprest01
Objetivo   : Se encarga de realizar scraping en la pagina del BCP para
subir csv generados por controlm

Tipo       : Servicio REST

Ej. llamada:
{
	"tipo":"Reporte", 
    "fec":"20200129"
}
"""
from flask import Blueprint, request, jsonify
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import os, sys, datetime, signal
from time import sleep
import pandas as pd
import requests
import lxml.html as lh
from bs4 import BeautifulSoup
 
bcprest02 = Blueprint('bcprest02', __name__)

@bcprest02.route('/bcprest02', methods=['POST'])
def llamarServicioBcp():
    
    codRes = 'SIN_ERROR'
    menRes = 'OK'
##@bcprest02.route('/bcprest02/<string:nroDoc>', methods=['GET'])
    global tipo,arc
    ##try:
    tipo =request.json['tipo']
    fec = request.json['fec']
    act = request.json['act']
    print('tipo: ' + tipo)
    print('fec: ' + fec)
    print('act: ' + act)
    inicializarVariables(tipo,fec,act)
    
     
    salida = {'codRes': codRes, 'menRes': menRes}
    return jsonify({'ParmOut':salida})

def inicializarVariables(tipo,fec,act):
    global codRes, menRes, driver, PID
    
    print("Se procede al login y descarga del PDF en BCP")
    ##Cargo valores para ejecutar Chrome y valores para config descarga PDF
    options = webdriver.ChromeOptions()

    #driver = webdriver.Chrome(chrome_options=options, executable_path=r'/opt/chrome/chromedriver')
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'E:\\Compartida\\chrome\\chromedriver.exe')
    
    print(driver)
    PID = driver.service.process.pid ##ID proceso Chromedriver
    print('PID: ' + str(PID))
    ##driver.implicitly_wait(10)
    driver.set_page_load_timeout(15)            
    try:
            driver.get('https://bcp003.bcp.gov.py/ords/f?p=1109:LOGIN:100623018562732:::::')
            ##Logeo en BCP
            loginSitioBCP(fec,act)
    except TimeoutException:
            driver.close()
            driver.quit()
            print("Page load Timeout Occured EN: get a BCP. Quiting !!!")


def loginSitioBCP(fec,act):
    global menRes
    #data = pd.read_txt(fullpath)
    #Prueba la lectura del csv
    #data.head(10)
    try:
        
        
        print("incio login")
        
        # type text
        usuario = driver.find_element_by_id('P101_USERNAME')
        usuario.send_keys('e1039cvarela')

        contrasenha = driver.find_element_by_id('P101_PASSWORD')
        contrasenha.send_keys('ruizurss2020.T')

        # click submit button
        LOGIN_button = driver.find_element_by_id('P101_LOGIN')
        LOGIN_button.click()
        print("Login OK")
        archivos=driver.find_element_by_link_text('Transferir Archivos')
        archivos.click()
        print("Se ingreso en la menu de transferir archivos")
        #Menu para seleccionar items
        try:
            
            print('seleccion de opcion')
            print(fec)
            print ("Resultados Disponibles")
            sleep(2)
            archivos=driver.find_element_by_link_text('Resultados Disponibles')
            archivos.click()
            sleep(2)
            driver.find_element_by_id('P38_PERIODO').send_keys(fec)
            sleep(2)
            #Boton para Buscar 
            enviar= driver.find_element_by_id("P38_FILTRAR")
            enviar.click()
            soup = BeautifulSoup(html_source, 'html.parser')
            for name_list in soup.find_all(class_ ='dropdown-row'):
                print(name_list.text)
                
            print('Preparar descarga')
            
            
            """
            correo = driver.find_element_by_id('R75169270633622983_download_EMAIL')
            correo.click()
            to=driver.find_element_by_id('R75169270633622983_email_to')
            to.send_keys('dcaballero@visionbanco.com')
            Send=driver.find_element_by_link_text('Send')
            Send.click()
            print("Se envio correctamente el correo")
            """
        except Exception as e:
                print('error en seleccionar item',str(e))
                #driver.close()
                #driver.quit()
                #matarChromeDriver()       
    except:
        print("ERROR EN: login, intento driver.close() - driver.quit")
        menRes = 'No se realizo el login en BCP'
        driver.close()
        driver.quit()
        matarChromeDriver()
        print("ERROR EN: login, termine driver.close() - driver.quit")
   

def logoutSitioBCP():
    
    try:
        
        try:
            print("Cierro Sesion yendo a pagina de inicio")
            driver.get('https://192.168.78.9/ords/f?p=1109:134')

            driver.close()
            driver.quit()
            print("Completo logout con quit()")
        except TimeoutException as e:
            driver.close()
            driver.quit()
            print("Page load Timeout Occured EN: logout a BCP. Quiting !!!")


    except:
        print("ERROR EN: logout, intento driver.close() - driver.quit")
        driver.close()
        driver.quit()
        matarChromeDriver()
        print("ERROR EN: logout, termine driver.close() - driver.quit")
    

def enable_downoad_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


def matarChromeDriver():
    print('El PID quedo vivo: ' + str(PID))
    global menRes
    menRes = 'No se pudo descargar el PDF'
    try:
        os.kill(PID, signal.SIGTERM) 
        print('Mate el proceso chromedriver: ' + str(PID))
    except OSError:
        print('Error al intentar matar el PID: ' + str(PID))
        pass
