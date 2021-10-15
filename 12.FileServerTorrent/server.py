import os
import socket
import uuid
import random
import string

#MAC address
MAC=str(hex(uuid.getnode()))
#IP address
IP=socket.gethostbyname(socket.gethostname())
#Process ID
PID=str(os.getpid())
#string de 100 caracteres aleatorios
RAND=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
#String concatenado
S=IP+MAC+PID+RAND

print(S)