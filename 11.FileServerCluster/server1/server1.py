
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
server = {"server1":
    {
        "ip":"tcp://localhost:5555",
        "storaged":"0",
        "max_storage":"200",
        "running":True,
        "parts":
        {}
    }}
jsserver = json.dumps(server)

msgencoded = msg.encode('utf-8')
serverencoded = jsserver.encode('utf-8')
proxy_socket.send_multipart([msgencoded,serverencoded])
response = proxy_socket.recv_multipart()
print(response[0])

while True:
    request = client_socket.recv_multipart()
    requestdecoded = request[0].decode('utf-8')
    print(requestdecoded+' guardada')
    
    response = 'recibida y guardada'
    msgencoded = msg.encode('utf-8')
    client_socket.send_multipart([msgencoded])


