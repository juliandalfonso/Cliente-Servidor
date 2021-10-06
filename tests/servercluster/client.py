

import zmq # libreria sockets 
import json #diccionario python a json 


#?-----------Conexion con Proxy-------------
context = zmq.Context()
proxy_socket = context.socket(zmq.REQ)
proxy_socket.connect('tcp://localhost:5555')
#?-----------Conexion con Proxy-------------



msg = 'client'
msgencoded = msg.encode('utf-8')
proxy_socket.send_multipart([msgencoded])
proxy_response = proxy_socket.recv_multipart()

serverip = json.loads(proxy_response[0])
print(serverip['ip'])
#?-----------Conexion con Proxy-------------
server_socket = context.socket(zmq.REQ)
server_socket.connect(serverip['ip'])
#?-----------Conexion con Proxy-------------

parte = 'parte 1'
parteencoded = parte.encode('utf-8')

server_socket.send_multipart([parteencoded])
server_response = server_socket.recv_multipart()

print(server_response)