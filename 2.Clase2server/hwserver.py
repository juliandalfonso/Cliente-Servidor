#
#   Hello World server en Python
#   Espera un mensaje del cliente
#   bind(escucha) 
#
#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes (sockets)
import zmq
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
    m = x.recv_string()
    
    #una vez recibido el mensaje, imprime Servidor recibe y
    # el mensaje de la linea de comandos
    print('Servidor recibe: ' + m)    
    x.send_string(m)
    #mostramos las pateiciones y respuestas que se han hecho en un contador
    #es decir, guardamos las peticiones en "cola" en el contador
    i = i+1
    print("se atendio el mensaje {}".format(i))