# Importamos la libreria para mensajeria
import zmq

# Necesitamos un contexto para correr sockets
context = zmq.Context()

# Creamos el socket
socket = context.socket(zmq.REP)

# Escuchamos en el puerto 5555
socket.bind('tcp://*:5555')

# Ciclo que mantiene el server escuchando siempre
while True:

    # Almacenamos el mensaje que reciba del cliente
    mensaje = socket.recv_string()
    # Imprimimos el mensaje recibido
    print('server recibe' + ' ' + mensaje)
    #procesamos el mensaje
    if mensaje=='1':
    
        m='usted selecciono suma'
        socket.send_string(m)
    
    else:
    
        m='usted selecciono resta'
        socket.send_string(m)
    
    
    