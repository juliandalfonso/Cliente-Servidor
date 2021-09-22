
#todo:-----------------------------------------
    #Nuevo metodo de envio por chunks #!FALTA
    #recibir por chunks#!FALTA
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

CHUNK_SIZE = 1

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
            "filename": file_dir,
            "chunk":0
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

def downloadFile(user,file_dir,response, archivo):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './Clientfiles/'+user+'/'+file_dir
    #si existe la carpeta del usuario la sobre escribe, sino la crea
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    size=response["size"]
    chunk = 0
    
    while chunk <= size:
        file = open(newfilepath, "ab")
        file.write(archivo)
        chunk += CHUNK_SIZE
        #imprimimos el porcentaje enviado hasta ahora
        porcentaje = (chunk*100)/size
        print(str("{:.1f}".format(porcentaje)) + '%')
        chunkjson = json.dumps({'chunk': chunk })
        chunkencoded = chunkjson.encode('utf-8')
        #enviamos el primer chunk al server
        socket.send_multipart([jsonencoded, chunkencoded])
        #recibimos la respuesta del server
        mens,archivo_respuesta = socket.recv_multipart()
        archivo = archivo_respuesta
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

def sizeArchivo(file):
    # Dice el tamano del archivo
    file.seek(0, os.SEEK_END)
    print("Size of file is :", file.tell(), "bytes")
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size


#!-------------------Logica del CLIENT -------------------------
while True:

    selector, user,tipo,file_dir = menuDatos()
    
    #creamos un json con la informacion que suministra el usuario
    newjson = convertToJson(user, tipo, file_dir)
    jsonencoded = newjson.encode('utf-8')

    #upload
    if selector == '1':
        #abrimos el archivo en lectura binaria
        file = open(file_dir, "rb")
        #retorna el peso del archivo
        file_size = sizeArchivo(file)
        #calculamos el porcentaje segun el peso del archivo y el chunksize
        porcentaje = (CHUNK_SIZE*100)/file_size
        #lleva la cuenta del porcentaje
        contador = 0
        chunk = file.read(CHUNK_SIZE)
        while chunk:
            #enviamos el primer chunk al server
            socket.send_multipart([jsonencoded, chunk])
            #recibimos la respuesta del server
            mensaje = socket.recv_string()
            #leemos el siguiente chunk
            chunk = file.read(CHUNK_SIZE)
            #imprimimos el porcentaje enviado hasta ahora
            contador += porcentaje
            print(str("{:.1f}".format(contador)) + '%')
        file.close()

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
        chunkjson = json.dumps({'chunk': 0})
        chunkencoded = chunkjson.encode('utf-8')
        socket.send_multipart([jsonencoded,chunkencoded])
        mens = socket.recv_multipart()
        response = procesaJson(mens[0])
        
        if response["encontrado"]:
            print(response["response"])
            file_dir = response["filename"]
            downloadFile(user,file_dir,response, mens[1])
        else:
            print(response["response"])

    else:
        print('digite correctamente el comando')
    
    nada = str(input('\n\npresione enter para continuar'))
#!-------------------Logica del cliente -------------------------