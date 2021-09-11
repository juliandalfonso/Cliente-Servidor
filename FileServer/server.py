
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

def nuevoUsuario(json_dic, link):
    
    # newjson = json.dumps(
    #         {
    #             link : json_dic["filename"]
    #         }
    #     )
    # return newjson
    pass
    

def procesaJson(mensjson):
    jsondecoded = mensjson.decode('utf-8')
    finaljson = json.loads(jsondecoded)
    return finaljson

def crear():
    #creamos un nuevo objeto en python
    nombre = json_dic["usuario"]
    file_dir = json_dic["filename"]  
    link = uuid.uuid4()
    
    #!link = linkscreator()
    #verificamos la existencioa del nuevo contacto
    if nombre in DATABASE:
        socket.send_string('\nUsuario Ya Existente')
        #!agregarLink(link)
        #!guardaArchivo(link)
        
    else:
        #!nuevoUsuario()
        jsonlink = nuevoUsuario(json_dic, link)
        #!guardaArchivo(link)
        DATABASE[nombre] = file_dir
        file = open("./DATABASE.json", "w")
        appendjson = json.dumps(DATABASE)
        file.write(appendjson)
        file.close()
        
        response = f'\nagregado->{file_dir} de {nombre}\n'
        socket.send_string(response)

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
    
    if json_dic["tipo"] == 'upload':
        crear()
    
    print('guardado')
#!-------------------Logica del SERVER -------------------------
