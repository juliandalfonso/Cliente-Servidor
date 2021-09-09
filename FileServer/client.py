
#todo:-----------------------------------------
    #python client.py username upload hola.txt
        #crear funcionalidad upload ----------LISTO
    #python client.py username sharelink hola.txt
        #crear funcionalidad sharelink
    #python client.py username downloadlink link
    #python client.py username list hola.txt
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

def convertToJson(user, tipo):
    crearJson = json.dumps(
        {
            "usuario" : user,
            "tipo" : tipo
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





#!-------------------Logica del CLIENT -------------------------
#recibimos los argumentos del usuario y los guardamos en variables
user, tipo, file_dir = arguments()

#creamos un json con la informacion que suministra el usuario
newjson = convertToJson(user, tipo)
#convierto el json a binario y le agregamos un salto de linea
byte_json = bytes(newjson, 'utf-8')
byte_jump = bytes('\n', 'utf-8')
jsonbinario = byte_json + byte_jump

#procesa la direccion del archivo lo lee y devuelve su informacion en binario
archivobinario = procesaArchivo(file_dir)

#unimos el jsonbinario(informacion de cliente) y el archivo en binario
request = uneJsonyArchivo(jsonbinario, archivobinario)

#enviamos la peticion al server
socket.send(request)
#esperamos la respuesta y la imprimimos
response = socket.recv_string()
print(response)
#!-------------------Logica del cliente -------------------------