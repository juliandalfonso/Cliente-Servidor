#
#   Hello World server en Python
#   Espera un mensaje del cliente
#   bind(escucha) 
#
#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes (sockets)
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
    # Espera un mensaje del cliente y lo almacena en m
    request_json = x.recv_json()
    
    print(type(request_json))
    
    
    #una vez recibido el mensaje, imprime Servidor recibe y
    # el mensaje de la linea de comandos
    print(request_json)    
    x.send_json(request_json)
