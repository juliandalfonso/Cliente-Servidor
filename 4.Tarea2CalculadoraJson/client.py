import zmq
import sys
import json
#Creamos un contexto de sockets
context = zmq.Context()
# creamos un socket como la variable s
# REQ (REQUEST) establece el protocolo con el que interactuan los componentes
s = context.socket(zmq.REQ)
# nos conectamos por medio de tcp por el puerto 5555 
#localhost-> sistema operativo
#quiero CONECTAR esta máquina en el puerto 5555 por medio del S.O localhost
s.connect('tcp://localhost:5555')
# guardamos un argumento (DESDE LA LINEA DE COMANDOS) y lo guardamos en un JSON
numero1 = int(sys.argv[1])
operacion = sys.argv[2]
numero2 = int(sys.argv[3])
#usamos json.dumps para convertir la informacion a JSON
request_json = json.dumps(
    {
    "operador1":numero1,
    "operacion":operacion,
    "operador2":numero2
}
)
#enviamos el objeto json al servidor y esperamos la respuesta
s.send_json(request_json)
#Recibimos un string como respuesta
response = s.recv_string()
#Imprimimos el resultado devuelto por el servidor
print(response)