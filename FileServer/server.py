
#todo:--------------------------------------------------
    #UPLOAD
    #separar archivo json de binario (leer primera linea)
        #convertir binario a string
        #guardar json en una variable
        #guardar archivo recibido

    #SHARELINK
    #crear DATABASE json
        #guardar usuario en DATABASE
    #crear sistema de ID's personalizado para los links
        # {
        #     "juan":
        #         {
        #             "123-abc" : "./files/hola.txt",
        #             "456-def" : "./files/song.mp3"
        #         }
        # }

    #DOWNLOADLINK
        #verificar existencia de link
        #devolver archivo binario
#todo:--------------------------------------------------



import zmq
import json
import uuid
import os

#-----------Conexion con CLIENT-------------
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')
#-----------Conexion con CLIENT-------------


def actualizaDB():
    file = open("./DATABASE.json", "w")
    appendjson = json.dumps(DATABASE, indent=4)
    file.write(appendjson)
    file.close()

def nuevoDict(json_dic, link):
    filename = json_dic["filename"]
    newjson = {link : filename}
    return newjson

def nuevoUsuario(json_dic, link):
    nombre = json_dic["usuario"]
    filename = json_dic["filename"]
    newuser =   { nombre : {link : filename}}
    return newuser

def guardaArchivo(archivo, json_dict):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './files/'+json_dic["usuario"]+'/'+json_dic["filename"]
    #si existe la carpeta del usuario la sobre escribe, sino la crea 
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    file = open(newfilepath, "wb")
    file.write(archivo)
    file.close()

def procesaJson(mensjson):
    jsondecoded = mensjson.decode('utf-8')
    finaljson = json.loads(jsondecoded)
    return finaljson

def upload():
    #creamos un nuevo objeto en python
    nombre = json_dic["usuario"]
    file_dir = json_dic["filename"]  
    #creaamos un nuevo id (link)
    link = str(uuid.uuid4())
    
    #verificamos la existencioa del nuevo contacto
    if nombre in DATABASE:
        #creamos el diccionario a agregar al usuario existente en la BD
        newjson = nuevoDict(json_dic, link)
        #agregamos el nuevo diccionario al usuario
        DATABASE[nombre].update(newjson)
        #abrimos el archivo de base de datos y lo agregamos
        actualizaDB()
        #enviamos la respuesta al cliente
        response = f'\nSe agregó el archivo:{file_dir} al usuario {nombre}'
        socket.send_string(response)
        #! agregar archivo a carpeta de usuario
    
    #caso en que el usuario no esté en la BD
    else:
        #creamos el diccionario del nuevo usuario
        newuser = nuevoUsuario(json_dic, link)
        #actualizamos el nuevo usuario en la BD
        DATABASE.update(newuser)
        actualizaDB()
        #respondemos al cliente
        response = f'\nnuevo usuario {nombre} con archivo {file_dir}'
        socket.send_string(response)
        
        #!crear carpeta de usuario
        #!agregar archivo a carpeta de  usuario

def encuentraArchivo(usuario, nombrearchivo):
    newfilepath = './files/'+usuario+'/'+nombrearchivo
    #si existe la carpeta del usuario la sobre escribe, sino la crea 
    file = open(newfilepath, "rb")
    data = file.read()
    file.close()
    return data

def download(DATABASE,dllink):
    
    encontrado = False
    nombrearchivo =''
    usuario = ''
    for nombres, items in DATABASE.items():
        for link, filename in items.items():
            if link == dllink:
                nombrearchivo = filename
                usuario = nombres
                response = f'\nHa solicitado descargar {filename} de {nombres}'
                encontrado = True
                
    
    #en caso de encontrar el archivo con el link
    if encontrado:
        json_response = json.dumps(
            {
                'encontrado': True,
                'response': response,
                'filename': nombrearchivo
            }
        )
        json_response_encoded = json_response.encode('utf-8')
        #cargamos el archivo en file
        file = encuentraArchivo(usuario, nombrearchivo)
        socket.send_multipart([json_response_encoded,file])
        
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
                
                
            



#!-------------------Logica del SERVER -------------------------
while True:
    #Recibimos un archivo binario
    mens = socket.recv_multipart()
    
    #Manejo de base de datos 
    file = open("./DATABASE.json", "r")
    data=file.read()
    DATABASE = json.loads(data)
    file.close()

    json_dic = procesaJson(mens[0])
    #caso en que el usuario haga upload
    if json_dic["tipo"] == 'upload':
        upload()
        archivo = mens[1]
        guardaArchivo(archivo, json_dic)
    if json_dic["tipo"] == 'downloadlink':
        dllink = json_dic["filename"]
        download(DATABASE, dllink)
    
    print('[SERV] Terminado')
#!-------------------Logica del SERVER -------------------------
