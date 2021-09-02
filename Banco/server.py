import zmq
import json #importamos la libreria para leer json
#para usar sockets, necesitan un contexto
context = zmq.Context()
# creamos un socket llamado x
# REP (RESPONSE) envia una respuesta por el puerto 5555
socket = context.socket(zmq.REP)
#Voy a ESCUCHAR(BIND) todo lo que ocurra en el puerto 5555
socket.bind('tcp://*:5555')


DATABASE= {}
    

while True:
    
    request = socket.recv_json()
    #pasamos a diccionario
    request_dict = json.loads(request)

    if request_dict["tipo"] == 'crear':
        #creamos un nuevo objeto en python
        nombre = request_dict["nombre"]
        saldo = request_dict["saldo"]
        nuevo_dato = {nombre:saldo}
        DATABASE.update(nuevo_dato)
        response = f'\nagregado->{nombre} con saldo {DATABASE[nombre]}\n'
        socket.send_string(response)
        
    elif request_dict["tipo"] == 'transf':
        pass
    elif request_dict["tipo"] == 'mostrar':
        nombre = request_dict["nombre"]
        response= f'\nEl saldo de {nombre} es: {DATABASE[nombre]}\n'
        socket.send_string(response)
    else:
        print('error')
    
    print(DATABASE)
    
