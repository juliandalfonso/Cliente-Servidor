
#todo:-----------------------------------------
    #python client.py username upload hola.txt #!LISTO
        #crear funcionalidad upload ----------LISTO
    #python client.py username sharelink hola.txt#!LISTO
        #crear funcionalidad sharelink
    #python client.py username downloadlink link#!LISTO
    #python client.py username list hola.txt#!LISTO
    
    #arreglar usuario al listar (pedir opcion todos o solo usuario antes de pedir el usuario)#!LISTO
#todo:-----------------------------------------

import zmq
import json
import sys
import os
import time

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


def menuDatos():
    
    os.system('cls||clear')
    print('1.Upload\n2.Sharelink\n3.List\n4.Download\n')
    print('Seleccione una opcion: ')
    selector = str(input())

    
    user=''
    tipo=''
    file_dir=''
    
    os.system('cls||clear')
    if selector == '1':
        print('Ingrese usuario: ')
        user = str(input())
        print('\nIngrese archivo a subir: ')
        file_dir = str(input())
        tipo='upload'
    #sharelink
    elif selector == '2':
        print('Ingrese usuario que subió el archivo: ')
        user = str(input())
        print('\nIngrese nombre del archivo que desea compartir: ')
        file_dir = str(input())
        tipo = 'sharelink'
    
    #list
    elif selector == '3':    
        print('\n1.Solo archivos de un usuario\n2.Todos los archivos\n')
        print('Seleccione una opcion: ')
        select = str(input())
        tipo = 'list'
        if select == '1':
            file_dir = 'aaa'
            print('Ingrese usuario a buscar: ')
            user = str(input())
        elif select =='2':
            file_dir = 'todo'
            user='aaa'
        else:
            print('seleccione una opcion valida') 
    #download
    elif selector == '4':
        user = ''
        print('\nIngrese el link de descarga: ')
        file_dir = str(input())
        tipo = 'downloadlink'
    print('\n')
    return selector, user, tipo, file_dir

#!-------------------Logica del CLIENT -------------------------
while True:

    selector, user,tipo,file_dir = menuDatos()
    
    #creamos un json con la informacion que suministra el usuario
    newjson = convertToJson(user, tipo, file_dir)
    jsonencoded = newjson.encode('utf-8')

    #upload
    if selector == '1':
        
        #procesa la direccion del archivo lo lee y devuelve su informacion en binario
        archivobinario = procesaArchivo(file_dir)
        #enviamos la peticion al server
        socket.send_multipart([jsonencoded, archivobinario])
        #esperamos la respuesta y la imprimimos
        response = socket.recv_string()
        print(response)

    #sharelink
    elif selector == '2':
        #enviamos la peticion al server
        socket.send_multipart([jsonencoded])
        #esperamos la respuesta y la imprimimos
        response = socket.recv_string()
        print(response)

    #list
    elif selector == '3':
        #enviamos la peticion al server
        socket.send_multipart([jsonencoded])
        #esperamos la respuesta y la imprimimos
        response = socket.recv_string()
        print(response)
    #download
    elif selector == '4':
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
    
    nada = str(input())
#!-------------------Logica del cliente -------------------------