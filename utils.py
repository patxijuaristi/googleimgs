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