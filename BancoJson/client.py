import zmq
import os
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
    os.system('cls||clear')
    print('1.Crear cuenta\n2.Transferir saldo\n3.Mostrar saldo\n4.Depositar saldo\n5.Retirar saldo')
    print('Seleccione una opcion: ')
    selector = str(input())
    return selector

def JSON_crear():
    nombre = input("\nnombre: ")
    saldo = int(input("saldo: "))
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

def JSON_transferir():
    remitente = input("\nremitente: ")
    destinatario = input("\ndestinatario: ")
    saldo = int(input("\nsaldo: "))
    
    mostrar = json.dumps(
            {
                "tipo": 'transf',
                "remitente": remitente,
                "destinatario" : destinatario,
                "saldo": saldo
            }
        )
    return mostrar

def JSON_depositar():
    nombre = input("\nnombre: ")
    saldo = int(input("\nsaldo a depositar: "))
    
    depositar = json.dumps(
            {
                "tipo": 'deposito',
                "nombre": nombre,
                "saldo": saldo
            }
        )
    return depositar

def JSON_retirar():
    nombre = input("\nnombre: ")
    retiro = int(input("\nsaldo a retirar: "))
    
    retirar = json.dumps(
            {
                "tipo": 'retirar',
                "nombre" : nombre,
                "retiro": retiro
            }
        )
    return retirar
    

while True:
    
    selector = menu()
    
    if selector == '1':
        request_crear = JSON_crear()
        socket.send_json(request_crear)
        
    elif selector == '2':
        request_transferir = JSON_transferir()
        socket.send_json(request_transferir) 
        
    elif selector == '3':
        request_mostrar = JSON_mostrar()
        socket.send_json(request_mostrar)        
    
    elif selector == '4':
        request_depositar = JSON_depositar()
        socket.send_json(request_depositar)        
    
    elif selector == '5':
        request_retirar = JSON_retirar()
        socket.send_json(request_retirar)        
    else:
        print('seleccion no valida')
    
    
    response = socket.recv_string()
    print(response)
    time.sleep(3)
    