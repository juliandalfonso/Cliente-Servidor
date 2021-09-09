
#todo:--------------------------------------------------
    #UPLOAD
    #separar archivo json de binario
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

#-----------Conexion con CLIENT-------------
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')
#-----------Conexion con CLIENT-------------


#!-------------------Logica del SERVER -------------------------
while True:
    #Recibimos un archivo binario
    mens = socket.recv()
    #creamos un nuevo archivo en binario
    file = open('./files/hola_nuevo.txt', 'wb')
    #le escribimos lo que contiene el mensaje
    file.write(mens)
    #imprimimos el mensaje recibido
    print(mens)
    # save(DATABASE, file)
    #cerramos el archivo
    file.close()
    print('guardado')
    socket.send_string('guardado en DB')
#!-------------------Logica del SERVER -------------------------
