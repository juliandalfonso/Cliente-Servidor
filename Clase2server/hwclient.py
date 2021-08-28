#   Hello World client en Python
#   envia, solcicita mensaje
#   connect (envía, solicita)
import zmq
import sys
import time
from random import seed
from random import randint

#seed random number generator
seed(1)

context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
s = context.socket(zmq.REQ)
# nos conectamos por medio de tcp por el puerto 5555 
#localhost-> sistema operativo
#quiero CONECTAR esta máquina en el puerto 5555 por medio del S.O localhost
s.connect('tcp://localhost:5555')
# guardamos un argumento (DESDE LA LINEA DE COMANDOS) y lo guardamos en message
name = sys.argv[1]

# for itera 10 veces
for _ in range(10):
    #generamos num aleatorio entre 0 y 10
    value = randint(0,10)
    # concatenamos el mensaje con el argumento en consola + el numero aleatorio
    message = name + ' ' + str(value) 
    # a traves del socket s enviamos la cadena message 
    s.send_string(message)
    # Recibimos la nueva respuesta del servidor y la guardamos en la variable m
    m = s.recv_string()
    #Imprimimos un mensaje que dice Cliente Recibe: seguido del mensaje que envio el servidor
    print('Cliente Recibe: ' + m)
    time.sleep(value)


