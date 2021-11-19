# -*- coding: utf-8 -*-
'''
Created on 27 mar. 2021

@author: Patxi Juaristi
'''

import utils

class Requisitos:

    def cargarRequisitos():
        requisitos=[]
        with open(utils.resource_path("requisitos.txt")) as f:
            listaRequisitos = f.read().splitlines()
        f.close()

        for req in listaRequisitos:
            if('cookies=' in req):
                requisitos.append(req.replace('cookies=',''))
            elif('linkXpath=' in req):
                requisitos.append(req.replace('linkXpath=',''))
            elif('imgXpath=' in req):
                requisitos.append(req.replace('imgXpath=',''))
            elif('masImg=' in req):
                requisitos.append(req.replace('masImg=',''))
            else:
                print('Some error occurred with the requirements')
                return
        
        return requisitos