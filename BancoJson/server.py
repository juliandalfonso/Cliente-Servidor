import json
import zmq


context = zmq.Context()

socket = context.socket(zmq.REP)

socket.bind('tcp://*:5555')

while True:
    #Manejo de archivos 
    file = open("./DATABASE.json", "r")
    data=file.read()
    DATABASE = json.loads(data)
    file.close()
    
    request = socket.recv_json()
    #pasamos a diccionario
    request_dict = json.loads(request)

    if request_dict["tipo"] == 'crear':
        #creamos un nuevo objeto en python
        nombre = request_dict["nombre"]
        saldo = request_dict["saldo"]  
        #verificamos la existencioa del nuevo contacto
        if nombre in DATABASE:
            socket.send_string('\nUsuario Ya Existente')
        else:
            DATABASE[nombre] = saldo
            file = open("./DATABASE.json", "w")
            append = json.dumps(DATABASE)
            file.write(append)
            file.close()
            response = f'\nagregado->{nombre} con saldo {saldo}\n'
            socket.send_string(response)
        
    elif request_dict["tipo"] == 'transf':
        
        remitente = request_dict["remitente"]
        destinatario = request_dict["destinatario"]
        saldo = request_dict["saldo"]
        
        #verificamos la existencia de los usuarios
        if remitente in DATABASE and destinatario in DATABASE:
                #verificamos la disponibilidad del remitente
            check_saldo = DATABASE[remitente] - saldo
            if check_saldo < 0:
                socket.send_string('\nSaldo insuficiente')
            else:
                #creamos una nueva lista y la actualizamos al DATABASE
                nuevo_saldo_remitente = DATABASE[remitente]-saldo
                DATABASE[remitente] = nuevo_saldo_remitente
                
                nuevo_saldo_destinatario = DATABASE[destinatario]+saldo
                DATABASE[destinatario] = nuevo_saldo_destinatario
                
                file = open("./DATABASE.json", "w")
                append = json.dumps(DATABASE)
                file.write(append)
                file.close()
                
                response= f'\nTransferencia de {remitente} a {destinatario} por {saldo}\n'
                socket.send_string(response)
        #caso en que no exista algun usuario
        else:
            socket.send_string('\nusuario no encontrado')
        
        
        
    elif request_dict["tipo"] == 'mostrar':
        
        nombre = request_dict["nombre"]
        #verificamos la existencia de los usuarios
        if nombre in DATABASE:
            response= f'\nEl saldo de {nombre} es: {DATABASE[nombre]}\n'
            socket.send_string(response)
        else:
            socket.send_string('\nusuario no encontrado')
    
    elif request_dict["tipo"] == 'deposito':
        if nombre in DATABASE:
            nombre = request_dict["nombre"]
            nuevo_saldo = DATABASE[nombre]+request_dict["saldo"]
            depositado = {nombre:nuevo_saldo}
            DATABASE.update(depositado)
            response= f'\nNuevo saldo de {nombre} es {DATABASE[nombre]}\n'
            socket.send_string(response)
        else:
            socket.send_string('\nusuario no encontrado')
    
    elif request_dict["tipo"] == 'retirar':
        nombre = request_dict["nombre"]
        #verificamos la existencia de los usuarios
        if nombre in DATABASE:
            
            nuevo_saldo = DATABASE[nombre]-request_dict["retiro"]
            if nuevo_saldo < 0:
                socket.send_string('\nSaldo insuficiente')
            else:
                retirado = {nombre:nuevo_saldo}
                DATABASE.update(retirado)
                response= f'\nNuevo saldo de {nombre} es {DATABASE[nombre]}\n'
                socket.send_string(response)
        else:
            socket.send_string('\nusuario no encontrado')
    else:
        print('error')
    
    print(DATABASE)
    
