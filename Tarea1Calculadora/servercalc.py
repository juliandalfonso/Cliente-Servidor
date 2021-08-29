# Importamos la libreria para mensajeria
import zmq

# Necesitamos un contexto para correr sockets
context = zmq.Context()

# Creamos el socket
socket = context.socket(zmq.REP)

# Escuchamos en el puerto 5555
socket.bind('tcp://*:5555')


def suma():
    socket.send_string('digite el primer numero a sumar')
    num1 = socket.recv_string()
    socket.send_string('digite el segundo numero a sumar')
    num2 = socket.recv_string()
    result = int(num1) + int(num2)
    socket.send_string(f'la respuesta es: {result}')

def resta():
    socket.send_string('digite el primer numero a restar')
    num1 = socket.recv_string()
    socket.send_string('digite el segundo numero a restar')
    num2 = socket.recv_string()
    result = int(num1) - int(num2)
    socket.send_string(f'la respuesta es: {result}')
    
def multi():
    socket.send_string('digite el primer numero a multiplicar')
    num1 = socket.recv_string()
    socket.send_string('digite el segundo numero a multiplicar')
    num2 = socket.recv_string()
    result = int(num1) * int(num2)
    socket.send_string(f'la respuesta es: {result}')
    
def divi():
    socket.send_string('digite el primer numero a dividir')
    num1 = socket.recv_string()
    socket.send_string('digite el segundo numero a dividir')
    num2 = socket.recv_string()
    result = int(num1) / int(num2)
    socket.send_string(f'la respuesta es: {result}')
# Ciclo que mantiene el server escuchando siempre
while True:
    
    # Almacenamos el mensaje que reciba del cliente
    mensaje = socket.recv_string()
    # Imprimimos el mensaje recibido
    print('server recibe' + ' ' + mensaje)
    #procesamos el mensaje
    if mensaje=='1':
    
        suma()
    
    elif mensaje=='2':
    
        resta()
        
    elif mensaje=='3':
    
        multi()
    
    elif mensaje=='4':
    
        divi()
    else:
        socket.send_string('error')
    
    
    
    