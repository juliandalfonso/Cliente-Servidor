import zmq
import sys
import json
import time
#Creamos un contexto de sockets
context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
socket = context.socket(zmq.REQ)
# nos conectamos por medio de tcp por el puerto 5555 
#localhost-> sistema operativo
#quiero CONECTAR esta máquina en el puerto 5555 por medio del S.O localhost
socket.connect('tcp://localhost:5555')

# crear cueenta gustavo 10mil
# transferir gustavo 10mil julian
# gustavo saldo
def menu():
    print('1.Crear cuenta\n2.Transferir saldo\n3.Mostrar saldo')
    print('Seleccione una opcion: ')
    selector = str(input())
    return selector

def JSON_crear():
    nombre = input("\nnombre: ")
    saldo = input("saldo: ")
    crear = json.dumps(
            {
                "tipo" : "crear",
                "nombre" : nombre,
                "saldo" : saldo
            }
        )  
    return crear       

def JSON_mostrar():
    nombre = input("\nnombre: ")
    mostrar = json.dumps(
            {
                "tipo" : "mostrar",
                "nombre" : nombre,
            }
        )
    return mostrar
    
'''
transferir = json.dumps(
    
    {
        "solicitud": transferir,
        "remitente": remitente,
        "destinatario" : destinatario,
        "saldo": saldo
    }
)

mostrar = json.dumps(
    {
        "solicitud" : mostrar,
        "nombre": nombre
    }
)
'''     

while True:
    
    selector = menu()
    
    if selector == '1':
        request_crear = JSON_crear()
        socket.send_json(request_crear)
        
    elif selector == '2':
        print('transf')
        
    elif selector == '3':
        request_mostrar = JSON_mostrar()
        socket.send_json(request_mostrar)        
    else:
        print('error')
    
    
    response = socket.recv_string()
    print(response)
    time.sleep(3)
    