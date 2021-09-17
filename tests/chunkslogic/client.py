import zmq
import sys
import json
import time
import os
#Creamos un contexto de sockets
context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
socket = context.socket(zmq.REQ)
# nos conectamos por medio de tcp por el puerto 5555
#localhost-> sistema operativo
#quiero CONECTAR esta máquina en el puerto 5555 por medio del S.O localhost
socket.connect('tcp://localhost:5555')

usuario = sys.argv[1]
filename = sys.argv[2]


def convertToJson(user, file_dir):
    crearJson = json.dumps(
        {
            "usuario" : user,
            "filename": file_dir
        }
    )
    return crearJson



CHUNK_SIZE = 10
json_dic = convertToJson(usuario, filename)
jsonencoded = json_dic.encode('utf-8')

file = open(filename, "rb")

# Dice el tamano del archivo
file.seek(0, os.SEEK_END)
print("Size of file is :", file.tell(), "bytes")
file.seek(0, os.SEEK_SET)


chunk = file.read(CHUNK_SIZE)
while chunk:
    print(chunk)
    socket.send_multipart([jsonencoded, chunk])
    ok = socket.recv_string()
    chunk = file.read(CHUNK_SIZE)
    
file.close()



