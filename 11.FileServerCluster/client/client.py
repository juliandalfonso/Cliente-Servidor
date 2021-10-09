
#todo:-----------------------------------------
    #documentar y organizar codigo #!LISTO
#todo:-----------------------------------------

import zmq # libreria sockets 
import json #diccionario python a json 
import os #sistema operativo para las rutas de los archivos
import hashlib #maneja encriptacion de archivos sha1-sha256



#?-----------Conexion con Proxy-------------
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')
#?-----------Conexion con Proxy-------------

#Bittorrent block = 250KB -> 250000B
CHUNK_SIZE = 250000 #establecemos una constante de particion de archivos en memoria

#objeto que permite encriptar un archivo a 160bits - 20 bytes
sha1 = hashlib.sha1()

clientrequestid = 'client'
CLIENT = clientrequestid.encode('utf-8')


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
    
    #numero de partes que contiene el archivo
    numberofparts=response["numberofparts"]
    
    #contador para iterar todas las partes del archivo
    counterofparts = 1
    
    #escribimos la primera parte solicitada del archivo, la parte o hash "cero"
    file = open(newfilepath, "ab")
    file.write(archivo)

    #hasta que el puntero lee todas las partes o hashes   
    while counterofparts < numberofparts:
        
        #imprimimos el porcentaje de descarga
        porcentaje = (counterofparts*100)/(numberofparts-1)
        print(str("{:.1f}".format(porcentaje)) + '%')
        
        
        #Actualizamos el puntero/contador y lo codificamos
        partjson = json.dumps({'part': counterofparts })
        partencoded = partjson.encode('utf-8')
        
        #solicitamos la parte al server
        socket.send_multipart([CLIENT,jsonencoded, partencoded])
        #recibimos la respuesta del server
        mens,archivo_respuesta = socket.recv_multipart()
        
        #guardamos la nueva parte del archivo e iteramos nuevamente
        archivo = archivo_respuesta
        #abre el nuevo archivo en modo append y escribimos
        file = open(newfilepath, "ab")
        file.write(archivo)
        
        #incrementamos el contador de partes para la siguiente iteracion
        counterofparts += 1
        
    #si el archivo solo contiene una parte imprime 100%
    if numberofparts == 1:
        print(str("{:.1f}".format(100)) + '%')
    #cerramos el archivo
    file.close()

#logica del menú para mejor experiencia de usuario
def menuDatos():

    os.system('cls||clear')
    print('1.Upload\n2.Sharelink\n3.List\n4.Download\n5.Salir\n')
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
    #Salir
    elif selector == '5':
        user = ''
        file_dir=''
        tipo=''
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
            "hash" : chunkHash, #hash del chunk o parte
            "chunkCounter" : chunkCounter, #contador del numero de partes enviadas
            "file_hash":file_hash #hash definitivo o final del archivo
        }
    )
    return crearJson

#recibe el archivo y retorna su hash
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
        #obtenemos el hash del archivo completo
        file_hash = getFileHash(readfile)
        
        sizeencoded = (str(file_size)).encode('utf-8')
        hashencoded = file_hash.encode('utf-8')
        socket.send_multipart([CLIENT,jsonencoded,sizeencoded,hashencoded])
        response = socket.recv_multipart()
        
        directions = procesaJson(response[0])
        
        #calculamos el porcentaje segun el peso del archivo y el chunksize
        porcentaje = (CHUNK_SIZE*100)/file_size
        contador = 0 #lleva la cuenta del porcentaje
        #leemos solo el numero de bytes especificados en CHUNK_SIZE
        chunk = file.read(CHUNK_SIZE)
        chunkCounter = 0 #cuenta cuantas partes se envian al servidor
        servercounter=0
        while chunk:
            #iteramos entre 4 servidores que hay
            if servercounter<4:
                ip=directions[str(servercounter)]
                servercounter+=1
            else:
                servercounter=0
            
            #?-----------Conexion con Proxy-------------
            temporal_socket = context.socket(zmq.REQ)
            temporal_socket.connect(ip)
            #?-----------Conexion con Proxy-------------
            
            #manejo de hashes
            #hasheamos solo el pedazo/chunk del archivo
            sha1.update(chunk) 
            chunkHash= sha1.hexdigest()#retorna hash tipo string
            
            #si el archivo se separa en mas de una parte
            if file_size>CHUNK_SIZE:
                jsonHash = convertToJsonHash(chunkHash,chunkCounter,file_hash).encode('utf-8')
            #caso en que el arvhivo solo sea un chunk
            elif file_size<=CHUNK_SIZE:
                jsonHash = convertToJsonHash(file_hash,chunkCounter,file_hash).encode('utf-8')
            
            #enviamos la parte del archivo al server
            temporal_socket.send_multipart([jsonencoded, chunk, jsonHash, response[0]])
            #leemos el siguiente chunk
            chunk = file.read(CHUNK_SIZE)
            #incrementamos contador de chunks
            chunkCounter +=1
            
            #recibimos la respuesta del server
            mensaje = temporal_socket.recv_string()
            #si el usuario ya subio un archivo con ese nombre
            if mensaje=='archivoexiste':
                print(f'{user} ya subio un archivo con el nombre {file_dir}')
                chunk=False
            #si el archivo ya existia en el server y se actualiza el puntero
            elif mensaje=='actualizapuntero':
                print('el archivo existia en [SERV], puntero actualizado -> subido correctamente')
                chunk=False
            else:
                #imprimimos el porcentaje enviado hasta ahora
                contador += porcentaje
                if contador>100:
                    contador=100
                print(str("{:.1f}".format(contador)) + '%')
        #cerramos el archivo
        file.close()

    #sharelink
    elif selector == '2':
        #enviamos la peticion al server
        socket.send_multipart([CLIENT,jsonencoded])
        #esperamos la respuesta y la imprimimos
        response = socket.recv_string()
        print(response)

    #list
    elif selector == '3':
        #enviamos la peticion al server
        socket.send_multipart([CLIENT,jsonencoded])
        #esperamos la respuesta y la imprimimos
        response = socket.recv_string()
        print(response)
    
    #download
    elif selector == '4':
        #inicializamos el apuntador en cero
        partjson = json.dumps({'part': 0})
        #lo codificamos para enviarlo
        partencoded = partjson.encode('utf-8')
        socket.send_multipart([CLIENT,jsonencoded,partencoded])
        
        #recibimos la respuesta del server con la primera parte a descargar
        mens = socket.recv_multipart()
        response = procesaJson(mens[0])
        
        #en caso de que el servidor haya encontrado el archivo lo descarga
        if response["encontrado"]:
            file_dir = response["filename"]
            downloadFile(user,file_dir,response, mens[1])
        #cuando el archivo no fue encontrado o el link es invalido
        else:
            print(response["response"])
    
    #Salir
    elif selector == '5':
        break
    else:
        print('digite correctamente el comando')
    
    #esperamos que el usuario digite enter para volver al menu
    str(input('\n\npresione enter para continuar'))
#!-------------------Logica del cliente ------------------------- 