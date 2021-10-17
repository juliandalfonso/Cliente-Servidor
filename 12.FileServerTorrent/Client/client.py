
#todo: -----------------------------------------------------------------------------------
#leer archivo .torrent con direcciones a los servidores con la ubicacion del archivo

#todo: -----------------------------------------------------------------------------------

import sys
import hashlib
import zmq
import os

CHUNK_SIZE = 10

def hashear():    
    sha1 = hashlib.sha1()
    filename = sys.argv[1]
    file = open(filename, "rb")
    while True:
        data = file.read(CHUNK_SIZE)
        if not data:
            break
        sha1.update(data)
        chunkHash= sha1.hexdigest()    
        print(data)
        print(chunkHash)
        print(int(chunkHash,16))
    
    
    print(f"SHA1: {sha1.hexdigest()}")


#logica del menú para mejor experiencia de usuario
def menuDatos():
    #borramos la pantalla para mejor interfaz
    os.system('cls||clear')
    print('1.upload\n2.Download\n')
    print('Seleccione una opcion: ')
    selector = str(input())
    op=''
    if selector == '1':
        os.system('cls||clear')
        print('Ingresa el archivo subida:\n') 
        op = str(input())
    elif selector == '2':
        os.system('cls||clear')
        print('Ingresa el archivo descarga:\n') 
        op = str(input())
    
    return op

while True:
    op = menuDatos()