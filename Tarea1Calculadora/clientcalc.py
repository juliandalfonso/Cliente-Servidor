# Importamos la libreria de mensajeria
import zmq
import sys

#creamos un contexto para sockets
context = zmq.Context()

#creamos un socket de tipo request (Peticion - cliente)
socket = context.socket(zmq.REQ)

#conectamos el socket al puerto 5555
socket.connect('tcp://localhost:5555')


while True:
    menu = '1.sum\n2.rest\n3.multip\n4.div'
    print(menu)
    selector = str(input())
    socket.send_string(selector)
    #Ahora recibimos el mensaje de vuelta del servidor y lo almacenamos
    response1 = socket.recv_string()
    print(response1)
    num1 = str(input())
    socket.send_string(num1)
    response2 = socket.recv_string()
    print(response2)
    num2 = str(input())
    socket.send_string(num2)
    result = socket.recv_string()
    print(result)
    print('-------FIN------\n\n')