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
        
        remitente = request_dict["remitente"]
        destinatario = request_dict["destinatario"]
        saldo = request_dict["saldo"]

        #logica de la transferencia
        #creamos una nueva lista y la actualizamos al DATABASE
        nuevo_saldo_remitente = DATABASE[remitente]-saldo
        nuevo_remitente = {remitente : nuevo_saldo_remitente}
        DATABASE.update(nuevo_remitente)
        
        nuevo_saldo_destinatario = DATABASE[destinatario]+saldo
        nuevo_destinatario = {destinatario : nuevo_saldo_destinatario}
        DATABASE.update(nuevo_destinatario)
        
        response= f'\nTransferencia de {remitente} a {destinatario} por {saldo}\n'
        socket.send_string(response)
        
    elif request_dict["tipo"] == 'mostrar':
        nombre = request_dict["nombre"]
        response= f'\nEl saldo de {nombre} es: {DATABASE[nombre]}\n'
        socket.send_string(response)
    else:
        print('error')
    
    print(DATABASE)
    
