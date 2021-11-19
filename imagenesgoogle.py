# -*- coding: utf-8 -*-
'''
Created on 27 mar. 2021

@author: Patxi Juaristi
'''
from tkinter import Tk, Frame, Text, Scrollbar, Label, Button, filedialog, \
    PhotoImage, Radiobutton, IntVar, StringVar, Entry, messagebox
from tkinter.constants import END
from threading import Thread
import utils

from google_images_scraper import GoogleImagesScraper


raiz = Tk()
icono = PhotoImage(file = utils.resource_path("imagenes-icono.png"))
raiz.iconphoto(False, icono)
raiz.title("Google Image Downloader")

miFrame=Frame(raiz, width=1200, height=700)
miFrame.pack()

rutaCarpeta=StringVar()
directorioPath=StringVar()
esHeadless=True
bgTransparente=False
formatoImg='jpg'

textResults=Text(miFrame, width=50, height=15)
textResults.grid(row=4, column=4, padx=5, pady=5)

scrollResults=Scrollbar(miFrame, command=textResults.yview)
scrollResults.grid(row=4, column=5, sticky="nsew")

textResults.config(yscrollcommand=scrollResults.set)

resultsLabel=Label(miFrame, text="Result: ", font=('Arial', 12 ))
resultsLabel.grid(row=4, column=3, padx=5, pady=5)

######33

textKeywords=Text(miFrame, width=50, height=15)
textKeywords.grid(row=4, column=1, padx=5, pady=5)

scrollKws=Scrollbar(miFrame, command=textKeywords.yview)
scrollKws.grid(row=4, column=2, sticky="nsew")

textKeywords.config(yscrollcommand=scrollKws.set)

keywordsLabel=Label(miFrame, text="Keywords: ", font=('Arial', 12 ))
keywordsLabel.grid(row=4, column=0, padx=5, pady=5)

####################################
opcionesFrame=Frame(miFrame)
opcionesFrame.grid(row=1, column=0, columnspan=5, padx=20, pady=15)

def selec():
    global esHeadless
    if(opcion.get()==2):
        esHeadless = False
    else:
        esHeadless = True

opcion = IntVar()
opcion.set(1)
monitor = Label(opcionesFrame, text='Hide Chrome window', font=('Arial', 12 ))
monitor.pack(side='left')

headed = Radiobutton(opcionesFrame, text="Yes", variable=opcion, value=1, command=selec, font=('Arial', 12 )).pack(side='left')
headless = Radiobutton(opcionesFrame, text="No", variable=opcion, value=2, command=selec, font=('Arial', 12 )).pack(side='left')

#########

formatoFrame=Frame(miFrame)
formatoFrame.grid(row=2, column=0, columnspan=5, padx=20, pady=(5,10))

def selecF():
    global formatoImg
    global bgTransparente
    bgTransparente=False
    if(opcionF.get()==2):
        formatoImg = 'png'
    elif(opcionF.get()==3):
        formatoImg = 'png'
        bgTransparente=True
    elif(opcionF.get()==4):
        formatoImg = 'gif'
    else:
        formatoImg = 'jpg'

opcionF = IntVar()
opcionF.set(1)
formatoLabel = Label(formatoFrame, text='Images Format', font=('Arial', 12 ))
formatoLabel.pack(side='left')

jpgRadio = Radiobutton(formatoFrame, text="JPG", variable=opcionF, value=1, command=selecF, font=('Arial', 12 )).pack(side='left')
pngRadio = Radiobutton(formatoFrame, text="PNG", variable=opcionF, value=2, command=selecF, font=('Arial', 12 )).pack(side='left')
gifRadio = Radiobutton(formatoFrame, text="PNG (Transparent BG.)", variable=opcionF, value=3, command=selecF, font=('Arial', 12 )).pack(side='left')
gifRadio = Radiobutton(formatoFrame, text="GIF", variable=opcionF, value=4, command=selecF, font=('Arial', 12 )).pack(side='left')

####

cantidadFrame=Frame(miFrame)
cantidadFrame.grid(row=3, column=0, columnspan=5, padx=20, pady=(5,10))

cantidadLabel = Label(cantidadFrame, text='Number of Images per each Keyword:', font=('Arial', 12 ))
cantidadLabel.pack(side='left')

cantidadEntry = Entry(cantidadFrame, font=('Arial', 12 ), width=5)
cantidadEntry.pack(side='left')

def validateNumber():
    try:
        int(cantidadEntry.get())
        return True
    except:
        return False

####

def split_list(a, n):
    k, m = divmod(len(a), n)
    return list((a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))

def scrapearImg(kwList, cantidad):
    scraper = GoogleImagesScraper(directorioPath.get()+'/', formatoImg)
    i = 1
    if(scraper.checkRequisitos()):
        if(scraper.initDriver(esHeadless)):
            for kw in kwList:
                if(scraper.scrapearImagen(kw, bgTransparente, cantidad)):                 
                    textResults.insert(float(i), kw + ' ' + str(cantidad) + '/' +str(cantidad)+ ' OK\n')
                    raiz.update()
                else:
                    textResults.insert(float(i), kw + ' ERROR\n')
                i+=1
        else:
            messagebox.showwarning(title='Chrome Driver Error', message='Error with the Chrome Driver. Probably you should need to update it')
    else:
        messagebox.showwarning(title='Google Block', message='Google has blocked the bot')
    scraper.endDriver()
    

def empezarScraping():
    texto = textKeywords.get("1.0", END)
    kwList = texto.split('\n')
    kwList = list(filter(('').__ne__, kwList))
    textResults.delete(1.0,"end")
    
    if(len(kwList) == 0):
        messagebox.showwarning(title='Empty Keywords', message='You need to introduce the keywords to download the images')
        return
    
    if(directorioPath.get() != ''):
        if(validateNumber() != False):
            hilos = 5
            divididos = split_list(kwList, hilos)
            
            hiloCont = 1
            for lista in divididos:
                if(len(lista) > 0):
                    Thread(target = scrapearImg, args=(lista, int(cantidadEntry.get()))).start()
                    hiloCont += 1
        else:
            messagebox.showwarning(title='Incorrect Quantity', message='The number of images to download is incorrect')
    else:
        textResults.delete(1.0,"end")
        messagebox.showwarning(title='Path Not Set', message='Set the path to storage the output files')

def establecerDirectorio():
    path = filedialog.askdirectory(initialdir="/", title="Select file")
    directorioPath.set(path)
    rutaCarpeta.set(path)

ficheroFrame=Frame(miFrame)
ficheroFrame.grid(row=0, column=0, columnspan=5, padx=20, pady=(20,5))

nameCarpeta=Label(ficheroFrame, text="Image output folder", font=('Arial', 12 )).pack(side='left')

nameCarpetaEntry=Entry(ficheroFrame, textvariable=rutaCarpeta, width=70)
nameCarpetaEntry.config(fg="red", justify="center", font=('Arial', 12 ))
nameCarpetaEntry.pack(side='left')

botonDir=Button(ficheroFrame, text="Folder", command=establecerDirectorio, bg='white', fg='black', font=('Arial', 12 )).pack(side='left')

botonBuscar=Button(miFrame, text="Download", command=empezarScraping, bg='red', fg='white', font=('Arial', 14 ))
botonBuscar.grid(row=5, column=0, columnspan=5, pady=(15,15))

raiz.mainloop()