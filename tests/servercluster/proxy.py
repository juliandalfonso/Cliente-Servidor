import zmq # libreria sockets 
import json #diccionario python a json 


from zmq.sugar import socket #libreria para usar time.sleep() mas que todo para hacer pruebas


#!-------Conexion con CLIENTS Y SERVERS -------------
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')
#!-------Conexion con CLIENTS Y SERVERS-------------

SERVER = {} #datos del servidor

def client():

    serverip = json.dumps(SERVER)
    msgencoded = serverip.encode('utf-8')
    socket.send_multipart([msgencoded])

def server(decodeddata):
    serverjson = json.loads(decodeddata)
    SERVER.update(serverjson)
    print(SERVER)
    msg = 'servidor corriendo'
    msgencoded = msg.encode('utf-8')
    socket.send_multipart([msgencoded])
    

#!-------------------Logica del SERVER -------------------------
while True:
    #Recibimos un multipart del cliente
    mens = socket.recv_multipart()
    
    msgdecoded = mens[0].decode('utf-8')
    
    
    if msgdecoded == 'client':
        client()
    if msgdecoded == 'server':
        serverdata = mens[1]
        decodeddata = serverdata.decode('utf-8')
        server(decodeddata)
#!-------------------Logica del SERVER -------------------------
