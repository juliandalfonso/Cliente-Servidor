import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')


mens = socket.recv_string()
print('llego '+ mens)
socket.send_string('oli x2')
    