#
#   Hello World server en Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#


#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes
import zmq


context = zmq.Context()

# creamos un socket llamado x
x = context.socket(zmq.REP)



x.bind('tcp://*:5555')



while True:
    
    m = x.recv_string()
    
    print('Servidor recibe ' + m)
    
    x.send_string('Recibido' + m)