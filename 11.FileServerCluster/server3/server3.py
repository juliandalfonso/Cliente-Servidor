
#todo:--------------------------------------------------
    #implementar lógica de cluster de servidores 🔥

#todo:--------------------------------------------------

import zmq # libreria sockets 
import json #diccionario python a json 
import uuid #unique-id -> encuentra identificador unico
import os #para crear las nuevas carpetas y checkear su existencia
import time #libreria para usar time.sleep() mas que todo para hacer pruebas


#?-----------Conexion con Proxy-------------
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
#?-----------Conexion con Proxy-------------

#Bittorrent block = 250KB -> 250000B
CHUNK_SIZE = 250000 #establecemos una constante de particion de archivos en memoria