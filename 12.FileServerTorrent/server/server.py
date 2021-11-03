
#todo: ----------------------------------------------------
#crea logica de rangos para cada servidor

#! idea de implementacion json por servidor
# {
#     "server1":{
#     "add":"192.16.31.32",
#     "port":"4000",
#     "range":[0,105312291668557186697918027683670432318895095400549111254310977536]}
# }
#todo: ----------------------------------------------------

import json
import os
import socket
import uuid
import random
import string
import hashlib
import zmq


#!-----------Conexion con Client-------------
context = zmq.Context()
client_socket = context.socket(zmq.REP)
client_socket.bind('tcp://*:1111')
#!-----------Conexion con Client-------------

DECIMALID = 0


def idGenerator():
    #MAC address
    MAC=str(hex(uuid.getnode()))
    #IP address
    IP=socket.gethostbyname(socket.gethostname())
    #Process ID
    PID=str(os.getpid())
    #string de 100 caracteres aleatorios
    RAND=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
    #String concatenado
    S=IP+MAC+PID+RAND
    #objeto que permite encriptar un archivo a 160bits - 20 bytes
    sha1 = hashlib.sha1()
    sha1.update(S.encode('utf-8')) 
    Shashed= sha1.hexdigest()
    #convertimos a decimal el String Hasheado 
    dec=int(Shashed, 16)
    print(f'String = IP + MAC + PID + RAND \n')
    print(f'String = {S} \n')
    print(f'Hash = {Shashed} \n')
    print(f'decimal = {dec} \n')
    DECIMALID = dec
    #esperamos que el usuario digite enter para volver al menu
    str(input('\n\npresione enter para continuar'))
    


#lee el contenido de DB y retorna su contenido
def leeDB(file):
    file = open(file, "r")
    data=file.read()
    DATABASE = json.loads(data)
    file.close()
    return DATABASE

#sobreescribe el nuevo contenido en la BD ingresada
def actualizaDB(file,DB):
    file = open(file, "w")
    appendjson = json.dumps(DB, indent=4)
    file.write(appendjson)
    file.close()


#funcion que inicializa un servidor por primera vez
def inicializar(server,ip, port):
    #crear json
    newserver =   {
        "add":ip,
        "port":port,
        "range":[0,105312291668557186697918027683670432318895095400549111254310977536]
        }
    serverdb.update(newserver)
    actualizaDB('./serverdb.json',serverdb)
    #subir a serverdb
    
    ipport = ip+':'+port
    server = '1'
    range = '[0,2^160]'
    return ipport, server, range

#funcion que valida la existencia de una ip y un puerto
def validarExistenciaIP(ip,port):
    
    pass
    

#logica del menú para mejor experiencia de usuario
def menuDatos():
    #borramos la pantalla para mejor interfaz
    os.system('cls||clear')
    print('1.Inicializar\n2.Conectar\n')
    print('Seleccione una opcion: ')
    selector = str(input())
    
    os.system('cls||clear')#borra la pantalla 
    
    if selector == '1':
        os.system('cls||clear')
        ip= str(input('\n ingrese ip: '))
        port= str(input('\n ingrese port: '))
        existe = validarExistenciaIP(ip,port)

        if existe:
            print('esta direccion ya esta ocupada')
        else:
            #inicializamos el primer servidor
            ipport,server,range = inicializar('server1',ip,port)            
            print(f'\nAddress: {ipport}\n')
            print(f'Servidor No: {server}\n')
            print(f'Rango asignado {range}\n')
        
    elif selector == '2':
        os.system('cls||clear')
        ipport = str(input('\n ingrese ip:puerto: '))
        existe = validarExistenciaIP(ipport)

        if existe:
            print('esta direccion ya esta ocupada')
        else:
            
            ipport,server,range = inicializar(ipport)            
            print(f'\nAddress: {ipport}\n')
            print(f'Servidor No: {server}\n')
            print(f'Rango asignado {range}\n')
    else:
        print('digite correctamente el comando')
        

#antes de empezar el ciclo encontramos el rango 
idGenerator()

while True:
    #cargamos la base de datos en DATABASE
    serverdb = leeDB('./serverdb.json')
    menuDatos()

    #esperamos que el usuario digite enter para volver al menu
    str(input('\n\npresione enter para continuar'))
