
#todo:-----------------------------------------
#python client.py username upload hola.txt
#python client.py username sharelink hola.txt
#python client.py username downloadlink link
#python client.py username list hola.txt
#todo:-----------------------------------------

import zmq
import json
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

#------------Recive Argumentos --------------
def arguments():
    usuario = sys.argv[1]
    tipo = sys.argv[2]
    dir_archivo = sys.argv[3]
    
    return usuario, tipo, dir_archivo




#----------MANEJO DE ARCHIVOS-------------
file = open("./files/hola.txt", "rb")
data=file.read()
file.close()
print(type(data))
#----------MANEJO DE ARCHIVOS-------------


def convertToJson(user, tipo):
    crearJson = json.dumps(
        {
            "usuario" : user,
            "tipo" : tipo
        }
    )
    return crearJson

def procesaArchivo():
    pass

while True:
    
    user, tipo, file_dir = arguments()
    
    #devuelve el json
    newjson = convertToJson(user, tipo)
    print(type(newjson))
    #procesa la direccion 
    archivo = procesaArchivo(file_dir)
    
    print(user, tipo, dir)
    socket.send(data)
    response = socket.recv_string()
    print(response)