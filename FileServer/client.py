import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')



socket.send_string('oli')
response = socket.recv_string()
print(response)