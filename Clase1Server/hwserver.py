#
#   Hello World server en Python
#   Espera un mensaje del cliente
#


#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes
import zmq


context = zmq.Context()

# creamos un socket llamado x

x = context.socket(zmq.REP)

# REP (RESPONSE) envia una respuesta por el puerto 5555
x.bind('tcp://*:5555')

while True:
    
    # Espera un mensaje del cliente y lo almacena en m
    m = x.recv_string()
    
    #una vez recibido el mensaje, imprime Servidor recibe y
    # el mensaje de la linea de comandos
    print('Servidor recibe: ' + m)
    
    
    x.send_string(m)