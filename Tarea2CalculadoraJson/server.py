#
#   Hello World server en Python
#   Espera un mensaje del cliente
#   bind(escucha) 
#
#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes (sockets)
from typing import Dict
import zmq
#importamos la libreria para leer json
import json
#para usar sockets, necesitan un contexto
context = zmq.Context()
# creamos un socket llamado x
x = context.socket(zmq.REP)
# REP (RESPONSE) envia una respuesta por el puerto 5555
#Voy a ESCUCHAR(BIND) todo lo que ocurra en el puerto 5555
x.bind('tcp://*:5555')

i=0
while True:    
    # Recibo un JSON
    request_json = x.recv_json()    
    
    
    request_dict = json.loads(request_json)
    print("la operacion es: ", request_dict["operacion"])
    
    #lo convertimos nuevamente a json y lo imprimimos
    print(type(json.dumps(request_json)))
    
    # Lo enviamos como json
    x.send_json(request_json)
