# TODO:: Declarar UTF-8 para poner tildes y tal
import requests
import shutil
import sys
import hashlib
import datetime
import time
import os
# BUF_SIZE para el calculo del hash
BUF_SIZE = 65536
# Workaround para evitar la comparacion de ficheros en la primera iteracion
primeraIteracion = True

# Funcion para la descarga de la imagen de camara
def descargaFichero(url,destino):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(destino, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

# Calculo del md5 del fichero para eliminar duplicados
def compruebaHash(fich1):
    md5 = hashlib.md5()
    with open(fich1, 'rb') as fichero:
        while True:
            data = fichero.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

# Diccionario con las camaras y la URL de las imagenes
camaras = { 'cuatrocaminos' : 'http://informo.munimadrid.es/informo/Camaras/Camara00005.jpg',
            'sorangela' : 'http://informo.munimadrid.es/informo/Camaras/Camara00084.jpg',
            'castellana-sinesio' : 'http://informo.munimadrid.es/informo/Camaras/Camara00092.jpg',
            'pzacastilla-norte' : 'http://informo.munimadrid.es/informo/Camaras/Camara00001.jpg',
            'pzacastilla-sur' : 'http://informo.munimadrid.es/informo/Camaras/Camara00002.jpg',
            'cuzco' : 'http://informo.munimadrid.es/informo/Camaras/Camara00003.jpg',
            'lima' : 'http://informo.munimadrid.es/informo/Camaras/Camara00004.jpg',
            'raimundo' : 'http://informo.munimadrid.es/informo/Camaras/Camara00090.jpg',
            'pabloiglesias' : 'http://informo.munimadrid.es/informo/Camaras/Camara00062.jpg',
            'sangerman' : 'http://informo.munimadrid.es/informo/Camaras/Camara00063.jpg',
            'cibeles' : 'http://informo.munimadrid.es/informo/Camaras/Camara00028.jpg',
            'cristorey' : 'http://informo.munimadrid.es/informo/Camaras/Camara00007.jpg',
            'bailen': 'http://informo.munimadrid.es/informo/Camaras/Camara00009.jpg',
            'granvia-pespana': 'http://informo.munimadrid.es/informo/Camaras/Camara00010.jpg',
            'granvia-callao': 'http://informo.munimadrid.es/informo/Camaras/Camara00011.jpg',
            'gmaranon': 'http://informo.munimadrid.es/informo/Camaras/Camara00013.jpg',
            'bilbao': 'http://informo.munimadrid.es/informo/Camaras/Camara00018.jpg',
            'alc-goya': 'http://informo.munimadrid.es/informo/Camaras/Camara00021.jpg',
            'legazpi': 'http://informo.munimadrid.es/informo/Camaras/Camara00024.jpg',
            'granvia-alcala': 'http://informo.munimadrid.es/informo/Camaras/Camara00029.jpg',
            'canalejas': 'http://informo.munimadrid.es/informo/Camaras/Camara00030.jpg',
            'quevedo': 'http://informo.munimadrid.es/informo/Camaras/Camara00031.jpg',
            'alonsomartinez': 'http://informo.munimadrid.es/informo/Camaras/Camara00032.jpg'
            }
# Diccionario para almacenar los nombres de los ultimos ficheros descargados para cada camara
# Seguramente haya una manera mas elegante de hacerlo
ficherosAnteriores = { 'cuatrocaminos' : '',
            'sorangela' : '',
            'castellana-sinesio' : '',
            'pzacastilla-norte' : '',
            'pzacastilla-sur' : '',
            'cuzco' : '',
            'lima' : '',
            'raimundo' : '',
            'pabloiglesias' : '',
            'sangerman' : '',
            'cibeles' : '',
            'cristorey' : '',
            'bailen': '',
            'granvia-pespana': '',
            'granvia-callao': '',
            'gmaranon': '',
            'bilbao': '',
            'alc-goya': '',
            'legazpi': '',
            'granvia-alcala': '',
            'canalejas': '',
            'quevedo': '',
            'alonsomartinez': ''
            }

# Hora de arranque del programa como referenci para ejecutar el bucle cada N segundos
horaInicio = time.time()

while True:
    # Iteramos el diccinonario de camaras
    for camara in camaras:
        fecha = datetime.datetime.now()
        # Construimos el nombre del fichero con la camara y el timestamp
        nombreFichero = camara + fecha.strftime("-%Y%m%d-%H%M%S") + ".jpg"
        print "[" + fecha.strftime("%H:%M") + "] Descargando " + camara
        # Ojo con el MD5 c58490da7b9059ab240d4be93fd0fd2f
        # Es la imagen de "Camara no disponible"
        descargaFichero(camaras[camara],nombreFichero)
        # A partir de la segunda iteracion comparamos el fichero descargado con el anterior
        if (not primeraIteracion):
            print "[" + fecha.strftime("%H:%M") + "] Comparando hashes"
            hashAnterior = compruebaHash(ficherosAnteriores[camara])
            hashActual = compruebaHash(nombreFichero)
            print hashAnterior
            print hashActual
            # Si los hashes coinciden el contenido es el mismo y eliminamos la descarga
            if (hashActual == hashAnterior):
                print "[" + fecha.strftime("%H:%M") + "] Imagen duplicada - Eliminando: " + ficherosAnteriores[camara]
                os.remove(ficherosAnteriores[camara])
        # Introducimos el nombre actual en el diccionario de ficheros anteriores
        ficherosAnteriores[camara] = nombreFichero
    primeraIteracion = False # Una vez se ejecuta por primera vez se queda a False
    # Esperamos N segundos y repetimos
    # Ojo, que parece que las imagenes se refrescan con mas frecuencia durante el dia
    time.sleep(30.0 - ((time.time() - horaInicio) % 30.0))
