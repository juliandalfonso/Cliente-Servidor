import zmq
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')


mens = socket.recv()
file = open('./files/hola_nuevo.txt', 'wb' )
file.write(mens)
# save(DATABASE, file)

file.close()
print('guardado')
socket.send_string('guardado en DB')
