#!/usr/bin/env python
# -*- Coding: utf-8 -*-
"""
Modulos    : iGDoc, V360
Sub-Modulos: P. al Toque, CRC
Empresa    : Vision Banco S.A.E.C.A

Autor      : Arturo Irala
Fecha      : 02/12/2019

Nombre     : bcprest03
Objetivo   : Se encarga de realizar scraping en la pagina del BCP para
descargar el PDF de la Califiacion diaria del cliente por Entidad Bancaria

Tipo       : Servicio REST

Ej. llamada:
{
  	"tipoDoc":"CI", 
    "nroDoc":"3823043",
  	"periodoDesde":"201901",
  	"periodoHasta":"201902" 	
}
"""
from flask import Blueprint, request, jsonify, g ##la g es una lib que permite ejecutar codigo despues del request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time, os, sys, datetime, signal
from funciones.credencialesBcp import credencialesBCP 
from funciones.loginSitioBCP import loginSitioBCP
from funciones.logoutSitioBCP import logoutSitioBCP
from funciones.descargasSandbox import enable_downoad_headless

bcprest03 = Blueprint('bcprest03', __name__)

@bcprest03.route('/bcprest03', methods=['POST']) 
def llamarServiciobcprest03():
    global tipoDoc, nroDoc, periodoDesde, periodoHasta, salida, sesionBcp
    sesionBcp = 'N'

    tipoDoc = str(request.json['tipoDoc'].encode('utf-8')).upper()
    nroDoc = str(request.json['nroDoc'].encode('utf-8')).upper()
    periodoDesde = str(request.json['periodoDesde'].encode('utf-8')).upper()
    periodoHasta = str(request.json['periodoHasta'].encode('utf-8')).upper()
    print('tipoDoc: ' + tipoDoc)
    print('nroDoc: ' + nroDoc)
    print('periodoDesde: ' + periodoDesde)
    print('periodoHasta: ' + periodoHasta)

    inicializarVariables() 
        
    salida = {'codRes': codRes, 'menRes': menRes, 'path': path}
    print('salida: ' + str(salida))

    return jsonify({'ParmOut':salida})


def inicializarVariables():
    global codRes, menRes, driver, path, pdf, sesionBcp, PID
    global usuarioBCP, contrasenhaBCP, urlv
    codRes = 'SIN_ERROR'
    menRes = 'OK'
    
    ##download = 'C:\\tmp\\'
    download = '/tmp/'
    now = datetime.datetime.now()
    periodoActual = str(now.strftime("%Y%m"))
    print('peridoActual: ' + periodoActual)

    ##Creacion de directorios de descarga
    path = download + tipoDoc
    if not os.path.exists(path):
        os.mkdir( path, 0755 )

    ##path = path + '\\' + nroDoc
    path = path + '/' + nroDoc
    if not os.path.exists(path):
        os.mkdir( path, 0755 )

    ##path = path + '\\' + periodoDesde + '_' + periodoHasta
    path = path + '/' + periodoDesde + '_' + periodoHasta
    print('path: ' + path)
    if not os.path.exists(path):
        os.mkdir( path, 0755 )    

    ##Verifico si el PDF del periodo ya fue descargado con anterioridad
    ##pdf = path + '\\' + 'Estado_de_deuda.pdf'
    ##pdf = path + '/' + 'entidad_acreedora_titular_afectado.pdf'
    ##pdf = path + '/' + 'Estado_de_deuda.pdf'
    pdf = path + '/' + 'Estado_de_deuda_diario.pdf'
    print('pdf: ' + pdf)
    if os.path.exists(pdf):
        ##os.remove(pdf)
        print('Ya se habia descargado el PDF anteriormente: ' + pdf)    
    else:
        print('Se procede al login y descarga del PDF en BCP')  

        usuarioBCP, contrasenhaBCP, urlv = credencialesBCP('bcprest03') ##funcion llamada desde credencialesBCP.py

        ##Cargo valores para ejecutar Chrome y valores para config descarga PDF
        options = webdriver.ChromeOptions() 

        prefs = {'download.default_directory': path,
            'plugins.always_open_pdf_externally': True}
        options.add_experimental_option("prefs",prefs)
                
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument('--headless') ##para linux
        options.add_argument('--no-sandbox')##para linux
        ##options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" ##solo pruebas en windows
        driver = webdriver.Chrome(chrome_options=options, executable_path=r'/opt/chrome/chromedriver') ##para linux
        ##driver = webdriver.Chrome(chrome_options=options, executable_path=r"D:\\pc01681\\jirala\\Desktop\\Arturo\\SVT\\2019\\Abril 2019\\2019-00531 - PRS AL TOQUE BCP 6 MESES ATRAS\\chromedriver.exe") ##para windows
        PID = driver.service.process.pid ##ID proceso Chromedriver
        print('PID: ' + str(PID))
        ##driver.implicitly_wait(10)
        driver.set_page_load_timeout(4)
        enable_downoad_headless(driver, path) ##habilita las descargas en modo sandbox
        ##driver.get('https://192.168.78.9/ords/f?p=1109:132')

        try:
            
            try:
                driver.get(urlv)
                ##Logeo en BCP
                sesionBcp = loginSitioBCP(driver, usuarioBCP, contrasenhaBCP)
                descargarCalificacionPDF()
            except TimeoutException as e:
                driver.close()
                driver.quit()
                matarChromeDriver()
                print("bcprest03 Page load Timeout Occured EN: get a BCP. Quiting !!!")

        except:
            print("bcprest03 ERROR EN: get a BCP, intento driver.close() - driver.quit")
            menRes = 'No se pudo ir a la pagina del BCP'
            try:
                driver.close()
                driver.quit()
            except:
                print("bcprest03 ERROR EN: get a BCP, no se llego a crear la sesion")

            matarChromeDriver()
            print("bcprest03 ERROR EN: get a BCP, termine driver.close() - driver.quit")

        


def descargarCalificacionPDF():
    global menRes, seleccion

    try:

        print('entro descarga')
        seleccion = "CEDULA DE IDENTIDAD"
        if tipoDoc == 'CI':
    	    seleccion = 'CEDULA DE IDENTIDAD'
        elif tipoDoc == 'RUC':
	        seleccion = 'REGISTRO UNICO DE CONTRIBUYENTES'
        elif tipoDoc == 'CRC':
    	    seleccion = 'CODIGO PARA PERSONAS NO RESIDENTES'
        elif tipoDoc == 'CRP':
	        seleccion = 'CARNE DE RESIDENCIA PERMANENTE'

        print('seleccion: ' + seleccion)
        # una vez dentro ingreso el doc
        tipoDocumento = Select(driver.find_element_by_id('P165_RF_TIPO_IDENT'))      
        tipoDocumento.select_by_visible_text(seleccion)
        nroDocumento = driver.find_element_by_id('P165_RF_NUMERO')
        nroDocumento.send_keys(nroDoc) ## 3823043, 4214182, 3386889
        print('periodoDesde2:' + periodoDesde)
        perDesde = driver.find_element_by_id('P165_ANOMES_DESDE')
        perDesde.clear()
        perDesde.send_keys(periodoDesde) 
        print('periodoHasta2:' + periodoHasta)
        perHasta = driver.find_element_by_id('P165_ANOMES_HASTA')
        perHasta.clear()
        perHasta.send_keys(periodoHasta) 

        descargarPDF_button = driver.find_element_by_id('B24822840193067598')
        descargarPDF_button.click() 

        print('Salio descarga')
    except:
        print("bcprest03 ERROR EN: descarga, intento driver.close() - driver.quit")
        menRes = 'No se pudo realizar la descarga'
        driver.close()
        driver.quit()
        matarChromeDriver()
        print("bcprest03 ERROR EN: descarga, termine driver.close() - driver.quit")

########################Funciones interesantes##########################
##a. Sirve para ejecutar codigo luego de la respuesta del servicio
@bcprest03.after_request
def after_request(response):
    ##renombrarPDF(response)
    print ('sesionBcp: ' + sesionBcp)
    if sesionBcp == 'S':
        try:
            
            try:
                logoutSitioBCP(driver, urlv) ##funcion llamada desde logoutSitioBCP.py
            except TimeoutException as e:
                driver.close()
                driver.quit()
                matarChromeDriver()
                print("bcprest03 Page load Timeout Occured EN: logout a BCP. Quiting !!!")
        except:
            global menRes
            print("bcprest03 ERROR EN: logout a BCP, intento driver.close() - driver.quit")
            menRes = 'No se pudo ir a la pagina del BCP'
            try:
                driver.close()
                driver.quit()
            except:
                print("bcprest03 ERROR EN: logout a BCP, no se llego a crear la sesion")

            matarChromeDriver()
            print("bcprest03 ERROR EN: gelogoutt a BCP, termine driver.close() - driver.quit")
      
        
    for callback in getattr(g, 'after_request_callbacks', ()):
        result = callback(response)
        if result is not None:
            response = result

    return response ##retorna el json del ParmOut

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