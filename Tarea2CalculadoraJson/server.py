#llamamos la libreria zmq permite crear nuestra propia infraestructura de mensajes (sockets)
from typing import Dict
import zmq
import json #importamos la libreria para leer json
#para usar sockets, necesitan un contexto
context = zmq.Context()
# creamos un socket llamado x
x = context.socket(zmq.REP)
# REP (RESPONSE) envia una respuesta por el puerto 5555
#Voy a ESCUCHAR(BIND) todo lo que ocurra en el puerto 5555
x.bind('tcp://*:5555')
#Ciclo infinito esperando peticiones
while True:    
    # Recibo un JSON desde el cliente
    request_json = x.recv_json()    
    
    #convierto el JSON a diccionario
    request_dict = json.loads(request_json)
    
    #logica del programa
    if request_dict["operacion"] == '+':
        #convierto a entero y lo  guardo en op1 y op2 
        op1 = int(request_dict["operador1"])
        op2 = int(request_dict["operador2"])
        #Calculamos el resultado
        result = op1 + op2
        #imprimimos lo que se esta haciendo del lado del server
        print(f"sumando: {op1} + {op2}")
        #enviamos como string
        x.send_string(f"la respuesta es: {result}")
        
        
    elif request_dict["operacion"] == '-':
        op1 = int(request_dict["operador1"])
        op2 = int(request_dict["operador2"])
        result = op1 - op2
        print(f"restando: {op1} - {op2}")
        x.send_string(f"la respuesta es: {result}")
        
        
    elif request_dict["operacion"] == '*':
        op1 = int(request_dict["operador1"])
        op2 = int(request_dict["operador2"])
        result = op1 * op2
        print(f"multiplicando: {op1} * {op2}")
        x.send_string(f"la respuesta es: {result}")
        
        
    elif request_dict["operacion"] == '/':
        op1 = int(request_dict["operador1"])
        op2 = int(request_dict["operador2"])
        result = op1 / op2
        print(f"dividiendo: {op1} / {op2}")
        x.send_string(f"la respuesta es: {result}")
        
        
    else:
        print("error")
        x.send_string("ingresa una operacion valida")
        
        
    
