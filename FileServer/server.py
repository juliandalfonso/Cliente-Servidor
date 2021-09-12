
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
    newjson = {filename : link}
    return newjson

def nuevoUsuario(json_dic, link):
    nombre = json_dic["usuario"]
    filename = json_dic["filename"]
    newuser =   { nombre : {filename : link}}
    return newuser

def guardaArchivo(archivo, json_dict):
    newfilepath = './files/'+json_dic["filename"]
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
    archivo = mens[1]
    guardaArchivo(archivo, json_dic)
    #caso en que el usuario haga upload
    if json_dic["tipo"] == 'upload':
        upload()
    
    print('guardado')
#!-------------------Logica del SERVER -------------------------
