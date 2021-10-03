
#todo:-----------------------------------------
    #Implmentar funcion que saca hash a un archivo #!LISTO
    #agregar hash al json que se envia #!LISTO
    #implementar descarga por hashes
#todo:-----------------------------------------

import zmq # libreria sockets 
import json #diccionario python a json 
import os #sistema operativo para las rutas de los archivos
import hashlib #maneja encriptacion de archivos sha1-sha256

#?-----------Conexion con SERVER-------------
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
#?-----------Conexion con SERVER-------------

#Bittorrent block = 250KB -> 250000B
CHUNK_SIZE = 250000 #establecemos una constante de particion de archivos en memoria

#objeto que permite encriptar un archivo a 160bits - 20 bytes
sha1 = hashlib.sha1()

#?-----------------------------FUNCIONES-----------------------------------------
#recibe los argumentos del usuario y los convierte en json
def convertToJson(user, tipo, file_dir):
    crearJson = json.dumps(#json.dumps convierte dict a json
        {
            "usuario" : user,
            "tipo" : tipo, #tipo (upload, download, list, share)
            "filename": file_dir,
            "chunk":0 #posicion del chunk a descargar
        }
    )
    return crearJson

#recibe el json utf-8 del server y lo procesa a diccionario
def procesaJson(mensjson):
    jsondecoded = mensjson.decode('utf-8') #decodifica utf-8
    finaljson = json.loads(jsondecoded)#carga el json a dict
    return finaljson

#descarga un documento por chunks
def downloadFile(user,file_dir,response, archivo):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './Clientfiles/'+user+'/'+file_dir
    #si existe la carpeta del usuario la sobre escribe, sino la crea
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    #tamaño del archivo respondido por el server
    size=response["size"]
    
    #posicion (puntero) del chunk que se le solicita al servidor
    chunk = 0
    #hasta que el puntero llegue al final del archivo
    while chunk <= size:
        #abre el nuevo archivo en modo append y escribimos
        file = open(newfilepath, "ab")
        file.write(archivo)
        
        #actualizamos el puntero chunk
        chunk += CHUNK_SIZE
        
        #imprimimos el porcentaje enviado hasta ahora
        porcentaje = (chunk*100)/size
        print(str("{:.1f}".format(porcentaje)) + '%')
        
        #Actualizamos el puntero y lo codificamos
        chunkjson = json.dumps({'chunk': chunk })
        chunkencoded = chunkjson.encode('utf-8')
        
        #enviamos el chunk al server
        socket.send_multipart([jsonencoded, chunkencoded])
        #recibimos la respuesta del server
        mens,archivo_respuesta = socket.recv_multipart()
        #guardamos la nueva parte del archivo e iteramos nuevamente
        archivo = archivo_respuesta
    file.close()

#logica del menú para mejor experiencia de usuario
def menuDatos():

    os.system('cls||clear')
    print('1.Upload\n2.Sharelink\n3.List\n4.Download\n')
    print('Seleccione una opcion: ')
    selector = str(input())
    
    #variables que retorna la funcion
    user=''
    tipo=''
    file_dir=''
    
    os.system('cls||clear')#borra la pantalla 
    
    #upload
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

#Recibe un archivo y retorna su tamaño
def sizeArchivo(file):
    # Dice el tamano del archivo
    file.seek(0, os.SEEK_END)
    print("Size of file is :", file.tell(), "bytes")
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size

def convertToJsonHash(chunkHash,chunkCounter,file_hash):
    crearJson = json.dumps(#json.dumps convierte dict a json
        {
            "hash" : chunkHash,
            "chunkCounter" : chunkCounter,
            "file_hash":file_hash
        }
    )
    return crearJson

def getFileHash(file):
    sha1Hash = hashlib.sha1(file)
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed
#?-----------------------------FUNCIONES-----------------------------------------


#!-------------------Logica del CLIENT -------------------------
while True:

    selector, user,tipo,file_dir = menuDatos()
    
    #creamos un json con la informacion que suministra el usuario
    newjson = convertToJson(user, tipo, file_dir)
    #lo codificamos para enviarlo al server
    jsonencoded = newjson.encode('utf-8')

    #upload
    if selector == '1':
        #abrimos el archivo en lectura binaria
        file = open(file_dir, "rb")
        readfile=file.read()
        #calculamos el peso del archivo
        file_size = sizeArchivo(file)
        file_hash = getFileHash(readfile)
        #calculamos el porcentaje segun el peso del archivo y el chunksize
        porcentaje = (CHUNK_SIZE*100)/file_size
        contador = 0 #lleva la cuenta del porcentaje
        
        #leemos solo el numero de bytes especificados en CHUNK_SIZE
        chunk = file.read(CHUNK_SIZE)
        chunkCounter = 0 #cuenta cuantas partes se envian al servidor
        while chunk:
            
            #manejo de hashes
            sha1.update(chunk)
            chunkHash= sha1.hexdigest()#retorna hash tipo string
            jsonHash = convertToJsonHash(chunkHash,chunkCounter,file_hash).encode('utf-8')
            
            #enviamos la parte del archivo al server
            socket.send_multipart([jsonencoded, chunk, jsonHash])
            #leemos el siguiente chunk
            chunk = file.read(CHUNK_SIZE)
            #incrementamos contador de chunks
            chunkCounter +=1
            
            #recibimos la respuesta del server
            mensaje = socket.recv_string()
            if mensaje=='archivoexiste':
                print('el archivo ya existe')
                chunk=False
            elif mensaje=='actualizapuntero':
                print('el archivo ya existe, puntero actualizado')
                chunk=False
            else:
                #imprimimos el porcentaje enviado hasta ahora
                contador += porcentaje
                if contador>100:
                    contador=100
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
        #inicializamos el apuntador en cero
        chunkjson = json.dumps({'chunk': 0})
        #lo codificamos para enviarlo
        chunkencoded = chunkjson.encode('utf-8')
        socket.send_multipart([jsonencoded,chunkencoded])
        
        #recibimos la respuesta del server
        mens = socket.recv_multipart()
        response = procesaJson(mens[0])
        
        #en caso de que el servidor haya encontrado el archivo
        if response["encontrado"]:
            file_dir = response["filename"]
            downloadFile(user,file_dir,response, mens[1])
        else:
            print(response["response"])

    else:
        print('digite correctamente el comando')
    
    #esperamos que el usuario digite enter para volver al menu
    str(input('\n\npresione enter para continuar'))
#!-------------------Logica del cliente -------------------------