
#todo:--------------------------------------------------
    #DOCUMENTACION Y ORDEN #!FALTA
        #falta corregir print cuando server envia archivo
        #falta documentar download y sus funciones
    
    #UPLOAD #!LISTO
    #SHARELINK #!LISTO
    #DOWNLOAD #!LISTO
    #LIST #!LISTO

#todo:--------------------------------------------------



import zmq # libreria sockets 
import json #diccionario python a json 
import uuid #unique-id -> encuentra identificador unico
import os #para crear las nuevas carpetas y checkear su existencia

#-----------Conexion con CLIENT-------------
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')
#-----------Conexion con CLIENT-------------


CHUNK_SIZE = 1000 #establecemos una constante de particion de archivos en memoria

#?-----------------------------FUNCIONES-----------------------------------------
#lee el contenido de DATABASE.json y retorna su contenido
def leeDATABASE():
    file = open("./DATABASE.json", "r")
    data=file.read()
    DATABASE = json.loads(data)
    file.close()
    return DATABASE
    
#escribe el nuevo contenido en la BD DATABASE.json
def actualizaDB():
    file = open("./DATABASE.json", "w")
    appendjson = json.dumps(DATABASE, indent=4)
    file.write(appendjson)
    file.close()

#crea un nuevo diccionario con el link y el archivo
def nuevoDict(json_dic, link):
    filename = json_dic["filename"]
    newdic = {link : filename}
    return newdic

#crea nuevo diccionario con el nombre del usuario, el link y el archivo
def nuevoUsuario(json_dic, link):
    nombre = json_dic["usuario"]
    filename = json_dic["filename"]
    newuser =   { nombre : {link : filename}}
    return newuser

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
        for link, filename in archivos.items():
            if nombreasubir == nombres and archivoasubir == filename:
                existe = True
    return existe

#actualizamos la DATABASE.json con el nuevo archivo
def upload(json_dic):
    #cargamos el usuario y el archivo 
    nombre = json_dic["usuario"]
    file_dir = json_dic["filename"] 
    
    #creaamos un nuevo id (link de descarga) - tipo string
    link = str(uuid.uuid4())
        
    #verificamos la existencia del usuario
    if nombre in DATABASE:
        #en caso de que el usuario ya exista solo se carga el archivo
        #creamos el diccionario a agregar al usuario existente en la BD
        newjson = nuevoDict(json_dic, link)
        
        #agregamos el nuevo diccionario al usuario con update
        DATABASE[nombre].update(newjson)
        #abrimos el archivo de DATABASE.json y lo actualizamos con DATABASE
        actualizaDB()
        
        #enviamos la respuesta al cliente
        response = f'\nSe agregó el archivo:{file_dir} al usuario {nombre}\n'
        socket.send_string(response)
        print('[SERV] archivo agregado')
    
    #caso en que el usuario no esté en la BD
    else:
        #creamos el diccionario del nuevo usuario
        newuser = nuevoUsuario(json_dic, link)
        #actualizamos el nuevo usuario en la BD
        DATABASE.update(newuser)
        actualizaDB()
        #respondemos al cliente
        response = f'\nnuevo usuario {nombre} con archivo {file_dir}\n'
        socket.send_string(response)
        print('[SERV] usuario y carpeta creados y archivo agregado')

# funcion que devuelve el tamaño de un archivo
def sizeArchivo(usuario,nombrearchivo):
    newfilepath = './Serverfiles/'+usuario+'/'+nombrearchivo
    #si existe la carpeta del usuario la sobre escribe, sino la crea 
    file = open(newfilepath, "rb")
    # Dice el tamano del archivo
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0, os.SEEK_SET)
    return size


#encuentra el archivo solicitado dentro de las carpetas existentes y devuelve su contenido
def encuentraArchivo(usuario, nombrearchivo):
    newfilepath = './Serverfiles/'+usuario+'/'+nombrearchivo
    #si existe la carpeta del usuario la sobre escribe, sino la crea 
    file = open(newfilepath, "rb")
    data = file.read()
    file.close()
    return data

#encuentra el archivo solicitado dentro de las carpetas existentes y devuelve su contenido
def segmentaArchivo(usuario, nombrearchivo, chunk):
    newfilepath = './Serverfiles/'+usuario+'/'+nombrearchivo
    #si existe la carpeta del usuario la sobre escribe, sino la crea 
    file = open(newfilepath, "rb")
    file.seek(chunk)
    data= file.read(CHUNK_SIZE)
    file.seek(0, os.SEEK_SET)
    file.close()
    return data


#busca un archivo segun el link y se lo envia al cliente en caso de encontrarlo
def download(DATABASE,dllink,chunk):
    
    encontrado = False
    nombrearchivo =''
    usuario = ''
    for nombres, items in DATABASE.items():
        for link, filename in items.items():
            if link == dllink:
                nombrearchivo = filename
                usuario = nombres
                response = f'\nHa solicitado descargar {filename} de {nombres}\n'
                encontrado = True
                
    
    #en caso de encontrar el archivo con el link
    if encontrado:
        size = sizeArchivo(usuario, nombrearchivo)
        
        json_response = json.dumps(
            {
                'encontrado': True,
                'response': response,
                'filename': nombrearchivo,
                'size': size
            }
        )
        json_response_encoded = json_response.encode('utf-8')
        
        filesegment = segmentaArchivo(usuario,nombrearchivo, chunk)
        socket.send_multipart([json_response_encoded,filesegment])
        
    else:
        response = '\nlink no encontrado'
        json_response = json.dumps(
            {
                'encontrado': False,
                'response': response
            }
        )
        json_response_encoded = json_response.encode('utf-8')
        socket.send_multipart([json_response_encoded])
        print('[SERV] link no encontrado descarga no exitosa')

#verifica que el archivo exista y devuelve el link de descarga                
def shareLink(json_dic, DATABASE):
    linkshare=''
    nombreacompartir = json_dic["usuario"]
    archivoacompartir = json_dic["filename"]
    for nombres, archivos in DATABASE.items():
        for link, filename in archivos.items():
            if nombreacompartir == nombres and archivoacompartir == filename:
                linkshare = link
    return linkshare

#lista los archivos de la base de datos y los envia al servidor
def listadorArchivos(DATABASE):
    lista = ''
    for nombres, archivos in DATABASE.items():
        lista += nombres+':\n'
        for link, filename in archivos.items():
            lista += '      -'+filename + '\n'
    socket.send_string(lista)
    print('[SERV] enviada lista de archivos')

def listadorArchivosUsuario(json_dic,DATABASE):
    usuario = json_dic["usuario"]
    lista = f'archivos de {usuario}: \n'
    encontrado = False
    for nombres, archivos in DATABASE.items():
        if usuario == nombres:
            lista += nombres+':\n'
            encontrado = True
        for link, filename in archivos.items():
            if usuario == nombres:
                lista += '      -'+filename + '\n'
    if encontrado:
        print('[SERV] enviando archivos al cliente ')
        socket.send_string(lista)
    else:
        print('[SERV] Usuario no encontrado')
        socket.send_string('Usuario no encontrado')

#recibe chunks (el archivo por partes) y los va guardando a medida que los recibe            
def cargaChunks(json_dic, archivo):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './Serverfiles/'+json_dic["usuario"]+'/'+json_dic["filename"]
    #si existe la carpeta del usuario la sobre escribe, sino la crea
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    file = open(newfilepath, "ab")
    file.write(archivo)
    file.close()
#?-----------------------------FUNCIONES-----------------------------------------



#!-------------------Logica del SERVER -------------------------
while True:
    #Recibimos un archivo binario
    mens = socket.recv_multipart()
    #cargamos la base de datos en DATABASE
    DATABASE= leeDATABASE()

    #primera parte del mensaje
    json_dic = procesaJson(mens[0])
    
    #caso en que el cliente haga upload
    if json_dic["tipo"] == 'upload':
        #segunda parte del mensaje
        chunk = mens[1]
        #revisamos si el archivo existe
        existe = checkFilename(json_dic, DATABASE)
        if existe:
            cargaChunks(json_dic, chunk)
            socket.send_string('True')
        else:
            upload(json_dic)
            cargaChunks(json_dic, chunk)
    
    #caso que el cliente solicite una descarga
    if json_dic["tipo"] == 'sharelink':
        if checkFilename(json_dic, DATABASE):
            linkshare = shareLink(json_dic, DATABASE)
            socket.send_string(f'\nlink para descargar {json_dic["filename"]} es: \n    {linkshare}\n')
            print('[SERV] link compartido')
        else:
            socket.send_string('archivo no encontrado')
            print('[SERV] archivo no encontrado')
    
    #caso que el cliente solicite la lista de los archivos
    if json_dic["tipo"] == 'list':
        if json_dic["filename"] == 'todo':
            listadorArchivos(DATABASE)
        else:
            listadorArchivosUsuario(json_dic, DATABASE)
    
    #caso que el cliente solicite una descarga
    if json_dic["tipo"] == 'downloadlink':
        dllink = json_dic["filename"]
        chunkjson = json.loads(mens[1])
        chunk = chunkjson["chunk"]
        download(DATABASE, dllink, chunk)
    
#!-------------------Logica del SERVER -------------------------