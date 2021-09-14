
#todo:-----------------------------------------
    #python client.py username upload hola.txt #!LISTO
        #crear funcionalidad upload ----------LISTO
    #python client.py username sharelink hola.txt#!LISTO
        #crear funcionalidad sharelink
    #python client.py username downloadlink link#!LISTO
    #python client.py username list hola.txt#!FALTA
#todo:-----------------------------------------

import zmq
import json
import sys

#-----------Conexion con SERVER-------------
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
#-----------Conexion con SERVER-------------



#------------Funciones--------------
def arguments():
    usuario = sys.argv[1]
    tipo = sys.argv[2]
    dir_archivo = sys.argv[3]
    
    return usuario, tipo, dir_archivo

def convertToJson(user, tipo, file_dir):
    crearJson = json.dumps(
        {
            "usuario" : user,
            "tipo" : tipo,
            "filename": file_dir
        }
    )
    return crearJson

def procesaArchivo(file_dir):
    file = open(file_dir, "rb")
    data=file.read()
    file.close()
    return data

def uneJsonyArchivo(byte_json, byte_archivo):
    unido = byte_json + byte_archivo
    return unido

def procesaJson(mensjson):
    jsondecoded = mensjson.decode('utf-8')
    finaljson = json.loads(jsondecoded)
    return finaljson

def downloadFile(response, archivo):
    filename = response["filename"]
    file = open(filename, "wb")
    file.write(archivo)
    file.close()

#!-------------------Logica del CLIENT -------------------------
#recibimos los argumentos del usuario y los guardamos en variables
user, tipo, file_dir = arguments()

#creamos un json con la informacion que suministra el usuario
newjson = convertToJson(user, tipo, file_dir)
jsonencoded = newjson.encode('utf-8')

if tipo == 'upload':
    #procesa la direccion del archivo lo lee y devuelve su informacion en binario
    archivobinario = procesaArchivo(file_dir)
    #enviamos la peticion al server
    socket.send_multipart([jsonencoded, archivobinario])
    #esperamos la respuesta y la imprimimos
    response = socket.recv_string()
    print(response)

elif tipo == 'sharelink':
    #enviamos la peticion al server
    socket.send_multipart([jsonencoded])
    #esperamos la respuesta y la imprimimos
    response = socket.recv_string()
    print(response)

elif tipo == 'list':
    #enviamos la peticion al server
    socket.send_multipart([jsonencoded])
    #esperamos la respuesta y la imprimimos
    response = socket.recv_string()
    print(response)
    
elif tipo == 'downloadlink':
    socket.send_multipart([jsonencoded])
    mens = socket.recv_multipart()
    response = procesaJson(mens[0])
    
    if response["encontrado"]:
        print(response["response"])
        downloadFile(response, mens[1])
    else:
        print(response["response"])

else:
    print('digite correctamente el comando')
#!-------------------Logica del cliente -------------------------