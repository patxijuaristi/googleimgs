# -*- coding: utf-8 -*-

import os
import random
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from requisitos import Requisitos

class GoogleImagesScraper:

    def __init__(self, ruta, formato):
        self.rutaFicheros = ruta
        self.requisitos = Requisitos.cargarRequisitos()
        self.driver = None
        self.format = formato
    
    def checkRequisitos(self):
        if(len(self.requisitos) != 4):
            return False
        else:
            return True
    
    def initDriver(self, headless):
        try:
            chrome_options = webdriver.ChromeOptions()
            if(headless):
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            s=Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=s, options=chrome_options)
            self.driver.get('https://www.google.com/')            
            self.driver.find_element_by_xpath(self.requisitos[0]).click()
            return True
        except:
            print('Error with the Chrome Driver')
            return False
    
    def scrapearImagen(self, kw, bgTransp, cantidad):
        transp=''
        if(bgTransp):
            transp='%2Cic:trans'
        try:
            time.sleep(random.randint(1,3))
            url = 'https://www.google.com/search?q='+kw.replace(' ','+')+'&tbm=isch&tbs=ift:'+self.format+transp
            self.driver.get(url)
            nImg = 0
            nImgNombre = 1
            completado = False
            while(nImg < (cantidad + 4) and (completado == False)):
                nImg += 1
                try:
                    time.sleep(random.randint(2,4))   
                    self.driver.find_element_by_xpath(self.requisitos[1].replace('CONTIMG',str(nImg))).click()    
                    time.sleep(random.randint(2,4))
                    xpathImg = self.requisitos[2]
                    if(nImg > 1):
                        xpathImg = self.requisitos[3]
                    img = self.driver.find_element_by_xpath(xpathImg)
                    src = img.get_attribute('src')
                    if(cantidad != 1):
                        nombreFichero = kw.replace(' ','-')+'-'+str(nImgNombre)
                    else:
                        nombreFichero = kw.replace(' ','-')
                    if('.svg' in src):
                        urllib.request.urlretrieve(src, "./temp.svg")
                        drawing = svg2rlg("./temp.svg")
                        renderPM.drawToFile(drawing, self.rutaFicheros+nombreFichero+'.'+self.format, fmt=self.format.upper())
                        os.remove("./temp.svg")
                    else:
                        urllib.request.urlretrieve(src, self.rutaFicheros+nombreFichero+'.'+self.format)
                    print(str(nImgNombre)+'/'+str(cantidad)+' - '+kw+' - Downloaded')
                    nImgNombre += 1
                except:
                    print(str(nImgNombre - 1)+'/'+str(cantidad)+' - Error with this '+kw+' image. Retrying')
                    pass
                if(nImgNombre == cantidad + 1):
                    completado = True
            return True
        except:
            print('Some error occurred')
            return False
    
    def endDriver(self):
        self.driver.quit()
