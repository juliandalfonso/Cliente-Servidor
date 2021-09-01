#   Hello World client en Python
#   envia, solcicita mensaje
#   connect (envía, solicita)
import zmq
import sys
import time
import json


context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
s = context.socket(zmq.REQ)
# nos conectamos por medio de tcp por el puerto 5555 
#localhost-> sistema operativo
#quiero CONECTAR esta máquina en el puerto 5555 por medio del S.O localhost
s.connect('tcp://localhost:5555')
# guardamos un argumento (DESDE LA LINEA DE COMANDOS) y lo guardamos en message
numero1 = sys.argv[1]
operacion = sys.argv[2]
numero2 = sys.argv[3]

request_json = """{
    "operador1":numero1,
    "operacion":operacion,
    "operador2":numero2
}"""

print(type(request_json))
s.send_json(request_json)
response = s.recv_json()
print(response)