


import zmq
import sys

context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
s = context.socket(zmq.REQ)

# nos conectamos por medio de tcp por el puerto 5555 
s.connect('tcp://localhost:5555')

# guardamos un argumento (DESDE LA LINEA DE COMANDOS) y lo guardamos en message
message = sys.argv[1]


# a traves del socket s enviamos la cadena 'hola mundo'
s.send_string(message)

# Recibimos la nueva respuesta del servidor y la guardamos en la variable m
m = s.recv_string()

#Imprimimos un mensaje que dice Cliente Recibe: seguido del mensaje que envio el servidor
print('Cliente Recibe: ' + m)
