import json
import zmq


context = zmq.Context()

socket = context.socket(zmq.REP)

socket.bind('tcp://*:5555')

while True:
    mensaje = socket.recv_string()
    print(mensaje)
    file = open("./DATABASE.json", "r")
    data=file.read()
    data_json = json.loads(data)
    print(data_json)
    file.close()
    socket.send_string('listo')
    