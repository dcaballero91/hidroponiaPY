#!/usr/bin/env python
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
	"tipo":"Saldos", 
    "arc":"CRC03-1039-20200129.txt"
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
 
bcprest01 = Blueprint('bcprest01', __name__)

@bcprest01.route('/bcprest01', methods=['POST'])
def llamarServicioBcp():
    
##@bcprest01.route('/bcprest01/<string:nroDoc>', methods=['GET'])
    global tipo,arc
    ##try:
    tipo =request.json['tipo']
    arc = request.json['arc']
    print('tipo: ' + tipo)
    print('arc: ' + arc)
    inicializarVariables(tipo,arc)
    
     
    salida = {'codRes': codRes, 'menRes': menRes}
    return jsonify({'ParmOut':salida})

def inicializarVariables(tipo,arc):
    global codRes, menRes, driver, PID
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    #Ruta para windows
    #mainpath= "C:\\Users\\dcaballe\\CursoPython\\python-ml-course\\datasets\\titanic\\"
    #Ruta para Linux
    mainpath="/mnt/bcp/"
    fullpath= os.path.join(mainpath,arc)
    
    print("Se procede al login y descarga del PDF en BCP")
    ##Cargo valores para ejecutar Chrome y valores para config descarga PDF
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    #Driver para linux
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'/opt/chrome/chromedriver')
    #Driver para Windows
    #driver = webdriver.Chrome(chrome_options=options, executable_path=r'E:\\Compartida\\chrome\\chromedriver.exe')
    
    print(driver)
    PID = driver.service.process.pid ##ID proceso Chromedriver
    print('PID: ' + str(PID))
    ##driver.implicitly_wait(10)
    driver.set_page_load_timeout(15)            
    try:
            driver.get('https://bcp003.bcp.gov.py/ords/f?p=1109:LOGIN:100623018562732:::::')
            ##Logeo en BCP
            loginSitioBCP(fullpath)
    except TimeoutException:
            driver.close()
            driver.quit()
            print("Page load Timeout Occured EN: get a BCP. Quiting !!!")


def loginSitioBCP(fullpath):
    global menRes,codRes
    f = Path(fullpath)
    f.exists()
    #data = pd.read_txt(fullpath)
    #Prueba la lectura del csv
    #data.head(10)
    try:
        
        
        print("incio login")
        print(fullpath)
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
        sleep(3)
        try:
            
            print('seleccion de opcion')
            
            if tipo == "Operaciones":
                print ("Pagina de Operaciones")
                operaciones=driver.find_element_by_link_text('Operaciones')
                operaciones.click()
                archivo=driver.find_element_by_id('P2_ARCHIVO_CRC01').send_keys(fullpath)
                #Boton para enviar 
                enviar= driver.find_element_by_id("B55214923069156266")
                enviar.click()
            elif tipo == "Relaciones":
                print ("Pagina de Relaciones")
                realaciones=driver.find_element_by_link_text('Relaciones')
                realaciones.click()
                archivo=driver.find_element_by_id('P9_ARCHIVO_CRC02').send_keys(fullpath)
                #Boton para enviar 
                enviar= driver.find_element_by_id("B38727296343463895")
                enviar.click()
            elif tipo == "Saldos":
                print ("Pagina de Saldos")
                saldos=driver.find_element_by_link_text('Saldos')
                saldos.click()
                archivo=driver.find_element_by_id('P14_ARCHIVO_CRC03').send_keys(fullpath)
                #Boton para enviar 
                enviar= driver.find_element_by_id("B39073620434839353")
                enviar.click()
            elif tipo == "Clasifica":
                print ("Pagina de Clasifica")
                clasific=driver.find_element_by_link_text('Clasifica')
                clasific.click()
                archivo=driver.find_element_by_id('P47_ARCHIVO_CRC06').send_keys(fullpath)
                #Boton para enviar 
                enviar= driver.find_element_by_id("B40239402532278161")
                enviar.click()
            elif tipo == "Garantias":
                print ("Pagina de Garantías")
                garantias=driver.find_element_by_link_text('Garantías')
                garantias.click()
                archivo=driver.find_element_by_id('P52_ARCHIVO_CRC04').send_keys(fullpath)
                #Boton para enviar 
                enviar= driver.find_element_by_id("B39732125778053336")
                enviar.click()
            elif tipo == "Opegaran":
                print ("Pagina de Opegaran")
                opegaran=driver.find_element_by_link_text("Opegaran")
                opegaran.click()
                archivo=driver.find_element_by_id('P55_ARCHIVO_CRC10').send_keys(fullpath)   
                #Boton para enviar 
                enviar= driver.find_element_by_id("B39748519659330358")
                enviar.click()
            elif tipo == "Movimientos":
                print ("Pagina de Movimientos")
                movimientos=driver.find_element_by_link_text("Movimientos")
                movimientos.click()
                archivo=driver.find_element_by_id('P19_ARCHIVO_CRC07').send_keys(fullpath)
                #Boton para enviar 
                #enviar= driver.find_element_by_id("B39173517804849822")
                #enviar.click()
            elif tipo == "B'DESVINCULACIONES'":
                print ("Pagina de Desvinculaciones")
                desv=driver.find_element_by_link_text("Desvinculaciones")
                desv.click()
            elif tipo == "B'SEGMENTOS'":
                print ("Pagina de Segmentos")
                segment=driver.find_element_by_link_text("Segmentos")
                segment.click()
            elif tipo == "B'ACTORES'":
                print ("Pagina Actores Vinculados a la Cadena Agrícola")
                actores=driver.find_element_by_link_text("Actores Vinculados a la Cadena Agrícola")
                actores.click()
            elif tipo == "B'ALTA'":
                print ("Pagin Alta de Personas")
                alta=driver.find_element_by_link_text("Alta de Personas")
                alta.click()
            elif tipo == "B'RESULTADOALTA'":
                print ("Resultado Alta Persona")
                resultado=driver.find_element_by_link_text("Resultado Alta Persona")
                resultado.click()
            elif tipo == "B'RESULTADODISP'":
                print ("Resultados Disponibles")
                reslutadodis=driver.find_element_by_link_text("Resultados Disponibles")
                reslutadodis.click()
            #Cierra session    
            logout=driver.find_element_by_link_text("Logout")
            logout.click()
        except Exception as e:
                print('error en seleccionar item',str(e))
                codRes= 'ERROR'
                menRes = str(e)
                driver.close()
                driver.quit()
                matarChromeDriver()       
    except Exception as e:
        print("ERROR EN: login, intento driver.close() - driver.quit",str(e))
        driver.close()
        driver.quit()
        matarChromeDriver()
        print("ERROR EN: login, termine driver.close() - driver.quit")


def matarChromeDriver():
    print('El PID quedo vivo: ' + str(PID))
    try:
        os.kill(PID, signal.SIGTERM) 
        print('Mate el proceso chromedriver: ' + str(PID))
    except OSError:
        print('Error al intentar matar el PID: ' + str(PID))
        pass
