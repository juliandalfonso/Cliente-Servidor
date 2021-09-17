import zmq
import json #importamos la libreria para leer json
import os

#para usar sockets, necesitan un contexto
context = zmq.Context()
# creamos un socket llamado x
# REP (RESPONSE) envia una respuesta por el puerto 5555
socket = context.socket(zmq.REP)
#Voy a ESCUCHAR(BIND) todo lo que ocurra en el puerto 5555
socket.bind('tcp://*:5555')


#crea una carpeta o la actualiza con el nuevo archivo subido
def guardaArchivo(json_dic, archivo):
    #crea un directorio con el nombre del usuario y el archivo
    # /files/usuario/archivo.txt
    newfilepath = './files/'+json_dic["usuario"]+'/'+json_dic["filename"]
    #si existe la carpeta del usuario la sobre escribe, sino la crea
    os.makedirs(os.path.dirname(newfilepath), exist_ok=True)
    file = open(newfilepath, "ab")
    file.write(archivo)
    file.close()


while True:
    json_enconded, chunk = socket.recv_multipart()

    json_decoded = json_enconded.decode('utf-8')
    json_dic = json.loads(json_decoded)
    print(json_dic)
    
    guardaArchivo(json_dic,chunk)
    print(chunk)
    print('\n')
    
    socket.send_string('True')