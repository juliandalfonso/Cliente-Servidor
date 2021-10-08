
#todo:--------------------------------------------------
    #implementar lógica de cluster de servidores 🔥
#todo:--------------------------------------------------

import zmq # libreria sockets 
import json #diccionario python a json 
import uuid #unique-id -> encuentra identificador unico
import os #para crear las nuevas carpetas y checkear su existencia
import time #libreria para usar time.sleep() mas que todo para hacer pruebas


#?-----------Conexion con Proxy-------------
context = zmq.Context()
proxy_socket = context.socket(zmq.REQ)
proxy_socket.connect('tcp://localhost:5555')
#?-----------Conexion con Proxy-------------

#!-----------Conexion con Client-------------
context = zmq.Context()
client_socket = context.socket(zmq.REP)
client_socket.bind('tcp://*:1111')
#!-----------Conexion con Client-------------


#!-----comunicacion con proxy inicial---------------------
msg = 'server'
server = {"server1":
    {
        "ip":"tcp://localhost:1111",
        "storaged":"0",
        "max_storage":"200",
        "running":True,
        "parts":
        {}
    }}
jsserver = json.dumps(server)

msgencoded = msg.encode('utf-8')
serverencoded = jsserver.encode('utf-8')
proxy_socket.send_multipart([msgencoded,serverencoded])
response = proxy_socket.recv_multipart()
print(response[0])
print('[SERV1]: Esperando Clientes...')
#!-----comunicacion con proxy inicial---------------------




#Bittorrent block = 250KB -> 250000B
CHUNK_SIZE = 250000 #establecemos una constante de particion de archivos en memoria

#?-----------------------------FUNCIONES-----------------------------------------
#lee el contenido de DB y retorna su contenido
def leeDB(file):
    file = open(file, "r")
    data=file.read()
    DATABASE = json.loads(data)
    file.close()
    return DATABASE

#sobreescribe el nuevo contenido en la BD ingresada
def actualizaDB(file,DB):
    file = open(file, "w")
    appendjson = json.dumps(DB, indent=4)
    file.write(appendjson)
    file.close()

#crea un nuevo diccionario con el numero del hash/parte y el hash
def nuevoHash(jsonHash):
    newdic ={jsonHash['chunkCounter']:jsonHash['hash']}
    return newdic

#crea nuevo diccionario con el nombre del usuario, el link, el archivo y sus partes
def nuevoUsuario(json_dic, link):
    nombre = json_dic["usuario"]
    filename = json_dic["filename"]
    newuser =   { nombre : {
              filename : {
                  'parts':{
                      jsonHash['chunkCounter']:jsonHash['hash']
                  },
                  'link' : link,
                  }}}
    return newuser

#crea nuevo diccionario con el nombre del usuario, el link, el archivo y la coleccion parts vacia
def nuevoDict(json_dic, link):
    filename = json_dic["filename"]
    newdic =  {
              filename : {
                  'parts':{},
                  'link' : link,
              }}
    return newdic

#decodifica el json y lo convierte a diccionario
def procesaJson(mensjson):
    #decodifica multipart a utf-8
    jsondecoded = mensjson.decode('utf-8')
    finaljson = json.loads(jsondecoded)
    return finaljson

#revisa la existencia de un archivo y devuelve booleano 
def checkFilename(json_dict, DATABASE):
    existe = False
    nombreasubir = json_dict["usuario"]
    archivoasubir = json_dict["filename"]
    for nombres, archivos in DATABASE.items():
        for filename, link in archivos.items():
            if nombreasubir == nombres and archivoasubir == filename:
                existe = True
    return existe

#busca en HASH_DATABASE si ese archivo ya se habia subido antes
def checkHash(jsonHash, HASH_DATABASE):
    existe = False
    file_hash = jsonHash['file_hash']
    for hashes, archivos in HASH_DATABASE.items():
        if file_hash == hashes:
            existe = True
    return existe

#funcion que devuelve el link y el filename de un archivo dado un hash
def actualizapuntero(jsonHash, HASH_DATABASE, DATABASE):
    file_hash = jsonHash['file_hash']
    filename=''
    #todo: encontrar el hash en HASH_DATABASE.json
    for hashes, archivos in HASH_DATABASE.items():
        if file_hash == hashes:
            file_hash =hashes
            filename=archivos            
    #todo: Encontrar el usuario que subio ese archivo
    #todo: encontrar el link del archivo
    usuarioOriginal = ''
    link = ''    
    for nombres, archivossubidos in DATABASE.items():
        for archivo, contenido in archivossubidos.items():
            for partolink, parts in contenido.items():
                if partolink == 'parts':
                    for hashnumber,file_hashes in parts.items():
                        if filename == archivo and file_hash==file_hashes:
                            usuarioOriginal = nombres
                if partolink == 'link':
                    if filename == archivo and usuarioOriginal==nombres:
                        link=parts
    return filename, link

#actualizamos la DATABASE.json con el nuevo archivo
def upload(json_dic,jsonHash):

    #cargamos el usuario y el archivo 
    nombre = json_dic["usuario"]
    filename = json_dic["filename"] 
    
    #creaamos un nuevo id (link de descarga) - tipo string
    link = str(uuid.uuid4())
        
    #verificamos la existencia del usuario en DB
    if nombre in DATABASE:
        
        #validamos la existencia del hash para optimizar almacenamiento
        hash_existe = checkHash(jsonHash, HASH_DATABASE)
        #en caso de que el archivo ya lo haya subido otro usuario
        if hash_existe and jsonHash['chunkCounter']==0:
            #cuando el usuario intenta subir un hash que ya existe
            #se crea un link-copy como puntero al archivo original
            filename, link = actualizapuntero(jsonHash, HASH_DATABASE, DATABASE)
            newlinkcopyjson={filename:{'link_copy':link}}
            #actualizamos la base de datos con el nuevo link_copy
            DATABASE[nombre].update(newlinkcopyjson)
            actualizaDB('../DATABASE/DATABASE.json', DATABASE)
            print('[SERV]archivo ya existe, puntero actualizado')
            client_socket.send_string('actualizapuntero')
        #caso en que nadie haya subido ese archivo antes
        else:
            #Validamos la existencia del archivo
            if checkFilename(json_dic, DATABASE):    
                newjson = nuevoHash(jsonHash)
                DATABASE[nombre][filename]['parts'].update(newjson)
            #caso en que se vaya a subir un archivo-parte por primera vez
            else:
                #creamos el diccionario basico
                newdic=nuevoDict(json_dic, link)
                DATABASE[nombre].update(newdic)
                #le agregamos el primer hash o la parte cero
                newjson = nuevoHash(jsonHash)
                DATABASE[nombre][filename]['parts'].update(newjson)
            
            #actualizamos la base de datos DB
            actualizaDB('../DATABASE/DATABASE.json', DATABASE)
            #creamos un nuevo diccionario para HASH_DATABASE.json y lo agregamos
            newdbhash ={jsonHash['hash']:filename}
            #!UPDATE SERVERS_DATABASE
            SERVERS_DATABASE['server1']['parts'].update(newdbhash)
            actualizaDB('../DATABASE/SERVERS_DATABASE.json',SERVERS_DATABASE)
            HASH_DATABASE.update(newdbhash)
            actualizaDB('../DATABASE/HASH_DATABASE.json',HASH_DATABASE)
            
            #enviamos la respuesta al cliente
            response = f'\nSe agregó el archivo:{filename} al usuario {nombre}\n'
            client_socket.send_string(response)
            print('[SERV] archivo agregado')
    
    #caso en que el usuario no esté en la BD
    else:
        #validamos la existencia del hash para optimizar almacenamiento
        hash_existe = checkHash(jsonHash, HASH_DATABASE)
        #si el usuario no existe pero el archivo si -> se actualiza el puntero link_copy
        if hash_existe:
            #guardamos el link del archivo existente en link_copy
            filename, link = actualizapuntero(jsonHash, HASH_DATABASE, DATABASE)
            #creamos el nuevo usuario y le agregamos el archivo existente como link_copy
            newlinkcopyjson =   { nombre : {
              filename : {
                  'link_copy' : link,
                  }}}
            
            #actualizamos la base de datos con el nuevo usuario    
            DATABASE.update(newlinkcopyjson)
            actualizaDB('../DATABASE/DATABASE.json',DATABASE)
            #enviamos la respuesta al cliente
            print('[SERV]archivo ya existe, puntero actualizado')
            client_socket.send_string('actualizapuntero')
        #si el usuario no existe y el archivo tampoco
        else:
            #creamos el diccionario del nuevo usuario
            newuser = nuevoUsuario(json_dic, link)
            #actualizamos el nuevo usuario en la BD
            DATABASE.update(newuser)
            actualizaDB('../DATABASE/DATABASE.json',DATABASE)
            #agregamos el hash a HASH_DATABASE
            newdbhash ={jsonHash['hash']:filename}
            #!UPDATE SERVERS_DATABASE
            SERVERS_DATABASE['server1']['parts'].update(newdbhash)
            actualizaDB('../DATABASE/SERVERS_DATABASE.json',SERVERS_DATABASE)
            
            HASH_DATABASE.update(newdbhash)
            actualizaDB('../DATABASE/HASH_DATABASE.json',HASH_DATABASE)
            #respondemos al cliente
            response = f'\nnuevo usuario {nombre} con archivo {filename}\n'
            client_socket.send_string(response)
            print('[SERV] usuario y carpeta creados y archivo agregado')


#funcion que devuelve la parte solicitada de un archivo
def getPart(usuario,nombrearchivo,part,DATABASE):
    hash_solicitado=''#aqui guardamos el hash que de la parte solicitada
    for nombres, archivossubidos in DATABASE.items():
        for archivo, contenido in archivossubidos.items():
            for partolink, parts in contenido.items():
                if partolink == 'parts':
                    for hashnumber,file_hash in parts.items():
                        if usuario == nombres and nombrearchivo==archivo:
                            if int(hashnumber)==int(part):
                                hash_solicitado = file_hash
    
    #encontramos la parte del archivo que fue solicitada           
    newfilepath = './Serverfiles/'+hash_solicitado
    #abrimos el archivo en lectura binaria y retornamos su data
    file = open(newfilepath, "rb")
    data = file.read()
    file.close()
    return data

#funcion que devuelve el numero de partes de un archivo
def numberOfParts(usuario, nombrearchivo):
    numberofparts=0 #iniciamos en cero partes
    
    #iteramos hasta encontrar el documento 'parts' del archivo y guardamos el numero de partes que contiene
    for nombres, items in DATABASE.items():
        for filename, content in items.items():
            for files, parts in content.items():
                if usuario == nombres and nombrearchivo==filename:
                    if files == 'parts':
                        numberofparts = len(parts)
    return numberofparts

#busca un archivo segun el link y se lo envia al cliente en caso de encontrarlo
def download(DATABASE,dllink,part):
    
    encontrado = False #iniciamos la bandera en falso, si la encuentra sera verdadero
    nombrearchivo =''
    usuario = ''
    #revisamos si el link solicitado existe
    for nombres, items in DATABASE.items():
        for filename, content in items.items():
            for links, dblink in content.items():
                if links == 'link' and dllink==dblink:
                    nombrearchivo = filename
                    usuario = nombres
                    response = f'\nHa solicitado descargar {filename} de {nombres}\n'
                    encontrado = True
                
    
    #en caso de encontrar el archivo con el link
    if encontrado:
        #guardamos el numero de partes que contiene el archivo para enviarlo
        numberofparts = numberOfParts(usuario, nombrearchivo)
        #cramos el json respuesta
        json_response = json.dumps(
            {
                'encontrado': True,
                'response': response,
                'filename': nombrearchivo,
                'numberofparts': numberofparts
            }
        )
        json_response_encoded = json_response.encode('utf-8')
        #obtenemos la parte del archivo solicitada
        filePart = getPart(usuario,nombrearchivo, part,DATABASE)
        #enviamos la respuesta con la parte del archivo al cliente
        client_socket.send_multipart([json_response_encoded,filePart])
    
    #en caso de no haber encontrado el link
    else:
        response = '\nlink no encontrado'
        json_response = json.dumps(
            {
                'encontrado': False,
                'response': response
            }
        )
        json_response_encoded = json_response.encode('utf-8')
        client_socket.send_multipart([json_response_encoded])
        print('[SERV] link no encontrado descarga no exitosa')

#SHARELINK -> verifica que el archivo exista y devuelve el link de descarga
def shareLink(json_dic, DATABASE):
    linkshare=''
    nombreacompartir = json_dic["usuario"]
    archivoacompartir = json_dic["filename"]
    #iteramos para encontrar el link
    for nombres, archivos in DATABASE.items():
        for filename, values in archivos.items():
            for claves, link in values.items():
                #comparamos el usuario y el archivo solicitado con el usuario encontrado y el archivo encontrado
                if nombreacompartir == nombres and archivoacompartir == filename:
                    if claves=='link' or claves=='link_copy':
                        linkshare = link
    return linkshare

#lista los archivos de la base de datos y los envia al cliente
def listadorArchivos(DATABASE):
    #encontramos todos los archivos en DATABASE y los organiza en un string
    lista ='Todos los archivos: \n'
    for nombres, archivos in DATABASE.items():
        lista += nombres+':\n'
        for filename, values in archivos.items():
            lista += '      -'+filename + '\n'
    #envia los archivos existentes en el server como string al cliente
    client_socket.send_string(lista)
    print('[SERV] enviada lista de archivos')

#lista los archivos de un usuario en especifico y los envia al cliente
def listadorArchivosUsuario(json_dic,DATABASE):
    usuario = json_dic["usuario"]
    lista = f'archivos de {usuario}: \n'
    encontrado = False
    #iteramos por todos los archivos hasta encontrar el usuario
    for nombres, archivos in DATABASE.items():
        if usuario == nombres:
            lista += nombres+':\n'
            encontrado = True
        for filename, values in archivos.items():
            if usuario == nombres:
                # guardamos los archivos que ha subido
                lista += '      -'+filename + '\n'
    #en caso de encontrar el usuario
    if encontrado:
        print('[SERV] enviando archivos al cliente ')
        client_socket.send_string(lista)
    #caso de no encontrar el usuario
    else:
        print('[SERV] Usuario no encontrado')
        client_socket.send_string('Usuario no encontrado')

#recibe chunks (el archivo por partes) y los va guardando a medida que los recibe            
def cargaChunks(archivo, jsonHash):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './Serverfiles/'+ jsonHash['hash']
    #si existe la carpeta del usuario la sobre escribe, sino la crea
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    file = open(newfilepath, "ab")
    file.write(archivo)
    file.close()
    
#?-----------------------------FUNCIONES-----------------------------------------

#cargamos la base de datos en DATABASE
DATABASE= leeDB('../DATABASE/DATABASE.json')
#cargamos la base de datos de hashes en HASH_DATABASE
HASH_DATABASE= leeDB('../DATABASE/HASH_DATABASE.json')
#cargamos la base de datos de hashes en HASH_DATABASE
SERVERS_DATABASE= leeDB('../DATABASE/SERVERS_DATABASE.json')


#!-------------------Logica del SERVER -------------------------
while True:
    #Recibimos un multipart del cliente
    mens = client_socket.recv_multipart()
    #cargamos la base de datos en DATABASE
    DATABASE= leeDB('../DATABASE/DATABASE.json')
    #cargamos la base de datos de hashes en HASH_DATABASE
    HASH_DATABASE= leeDB('../DATABASE/HASH_DATABASE.json')
    #cargamos la base de datos de hashes en SERVERS_DATABASE
    SERVERS_DATABASE= leeDB('../DATABASE/SERVERS_DATABASE.json')
    #primera parte del mensaje
    json_dic = procesaJson(mens[0])
    
    #caso en que el cliente haga upload
    if json_dic["tipo"] == 'upload':
        #segunda parte del mensaje es el chunk
        chunk = mens[1]
        #la tercera parte es el jsonhash
        jsonHash = procesaJson(mens[2])
        
        #revisamos si el archivo existe y si ya se encuentra en la BD del usuario
        archivo_existe = checkFilename(json_dic, DATABASE)
        #si el usuario intenta subir un archivo que ya subio antes con ese nombre
        if archivo_existe and jsonHash['chunkCounter']==0:
            client_socket.send_string('archivoexiste')
        #si el archivo es nuevo y el nombre no esta repetido lo carga
        else:
            #guardamos el archivo en la base de datos
            upload(json_dic,jsonHash)
            #guardamos el archivo fisicamente
            cargaChunks(chunk,jsonHash)
    
    #caso que el cliente solicite una descarga
    if json_dic["tipo"] == 'sharelink':
        #revisamos que el arvhivo exista
        if checkFilename(json_dic, DATABASE):
            #guardamos el link en linkshare
            linkshare = shareLink(json_dic, DATABASE)
            client_socket.send_string(f'\nlink para descargar {json_dic["filename"]} es: \n    {linkshare}\n')
            print('[SERV] link compartido')
        #si el archivo no existe o no se encuentra
        else:
            client_socket.send_string('archivo no encontrado')
            print('[SERV] archivo no encontrado')
    
    #caso que el cliente solicite la lista de los archivos
    if json_dic["tipo"] == 'list':
        #si solicito todos los archivos
        if json_dic["filename"] == 'todo':
            listadorArchivos(DATABASE)
        #si solicito un usuario en especifico
        else:
            listadorArchivosUsuario(json_dic, DATABASE)
    
    #caso que el cliente solicite una descarga
    if json_dic["tipo"] == 'downloadlink':
        #guardamos el link pedido por el cliente
        dllink = json_dic["filename"]
        #guardamos partjson que contiene la parte(contador) a descargar
        partjson = json.loads(mens[1])
        #guardamos el contador o la parte solicitada
        part = partjson["part"]
        #llama la funcion download que envia el archivo al cliente
        download(DATABASE, dllink, part)
    
#!-------------------Logica del SERVER -------------------------