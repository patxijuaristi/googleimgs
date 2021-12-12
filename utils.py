import sys
import os
from os import listdir
from os.path import isfile, join

def resource_path(relative_path):
    """ To get resources path for creating the .exe with PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def readFolderFiles(rutaFicheros):
    onlyfiles = [f for f in listdir(rutaFicheros) if isfile(join(rutaFicheros, f))]
    return onlyfiles

def convertirKwEnFilename(s):
        replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),(" ","-"),("|",""),(".",""),(",",""),("'",""),("´",""),("`",""),("¿",""),("¡",""),("?",""),("!",""),("@",""),("*",""),("/",""),("\\",""),("\"",""),("$",""),("%",""),("&",""),("(",""),(")",""),("ö","o"),("ü","u"),("ä","a"),("ë","e"),("è","e"),("à","a"),("ì","i"),("ù","u"),("ò","o"),("’",""),("ğ","g"),("„",""),("“",""),("ć","c"),("ß","s"))
        s = s.lower()
        for a, b in replacements:
            s = s.replace(a, b)
        return s

def split_list(a, n):
    k, m = divmod(len(a), n)
    lista =  list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))
    listaSinVacios = []
    for i in lista:
        if len(i) > 0:
            listaSinVacios.append(i)
    return listaSinVacios

def leerFichero(fichero):
    archivo = open(fichero,'r', encoding='utf-8')
    kwList = archivo.read().splitlines()
    archivo.close()

    return kwList

def escribirFichero(fichero, lineas):
    with open(fichero, 'w', encoding='utf-8') as f:
        for line in lineas:
            f.write(line)
            f.write('\n')