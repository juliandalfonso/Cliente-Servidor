

import zmq # libreria sockets 
import json

from zmq.sugar import socket #diccionario python a json 



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
serverip = {'ip': 'tcp://localhost:1111'}
jsserverip = json.dumps(serverip)

msgencoded = msg.encode('utf-8')
serveripencoded = jsserverip.encode('utf-8')
proxy_socket.send_multipart([msgencoded,serveripencoded])
response = proxy_socket.recv_multipart()
print(response[0])

while True:
    request = client_socket.recv_multipart()
    requestdecoded = request[0].decode('utf-8')
    print(requestdecoded+' guardada')
    
    response = 'recibida y guardada'
    msgencoded = msg.encode('utf-8')
    client_socket.send_multipart([msgencoded])

