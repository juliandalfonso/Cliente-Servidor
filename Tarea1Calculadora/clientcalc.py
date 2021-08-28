# Importamos la libreria de mensajeria
import zmq
import sys

#creamos un contexto para sockets
context = zmq.Context()

#creamos un socket de tipo request (Peticion - cliente)
socket = context.socket(zmq.REQ)

#conectamos el socket al puerto 5555
socket.connect('tcp://localhost:5555')


menu = '1.sum 2.rest'
print(menu)
selector = str(input())

socket.send_string(selector)
#Ahora recibimos el mensaje de vuelta del servidor y lo almacenamos
response = socket.recv_string()
print(f'la respuesta es: {response}')