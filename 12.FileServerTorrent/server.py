import os
import socket
import uuid
import random
import string
import hashlib
            

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


#objeto que permite encriptar un archivo a 160bits - 20 bytes
sha1 = hashlib.sha1()
sha1.update(S.encode('utf-8')) 
Shashed= sha1.hexdigest()

#convertimos a decimal el String Hasheado
dec=int(Shashed, 16)


print(f'String = {S} \n')
print(f'Hash = {Shashed} \n')
print(f'decimal = {dec} \n')


