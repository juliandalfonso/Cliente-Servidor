import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

file = open("./files/hola.txt", "rb")
data=file.read()
file.close()
print(type(data))

socket.send(data)
response = socket.recv_string()
print(response)