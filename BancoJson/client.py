import json
import zmq
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')

socket.send_string('enviado desde el cliente')
respuesta = socket.recv_string()
print(respuesta)