import zmq
import sys


context = zmq.Context()


# creamos un socket como la variable s

# REQ establece el protocolo con el que interactuan los componentes
s = context.socket(zmq.REQ)

# nos conectamos por medio de tcp por el puerto 5555
s.connect('tcp://localhost:5555')


# a traves del socket s enviamos la cadena 'hola mundo'
s.send_string('Hola mundo')

# Recibimos la respuesta del mensaje y la guardamos en la variable m
m = s.recv_string()
