
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
proxy_socket = context.socket(zmq.REQ)
proxy_socket.connect('tcp://localhost:5555')
#?-----------Conexion con Proxy-------------

#!-----------Conexion con Client-------------
context = zmq.Context()
client_socket = context.socket(zmq.REP)
client_socket.bind('tcp://*:1111')
#!-----------Conexion con Client-------------

msg = 'server'
msgencoded = msg.encode('utf-8')
proxy_socket.send_multipart([msgencoded])
response = proxy_socket.recv_string()
print(response)

#Bittorrent block = 250KB -> 250000B
CHUNK_SIZE = 250000 #establecemos una constante de particion de archivos en memoria

