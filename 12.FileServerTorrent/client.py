import sys
import hashlib

CHUNK_SIZE = 10
sha1 = hashlib.sha1()
filename = sys.argv[1]
file = open(filename, "rb")

while True:
    data = file.read(CHUNK_SIZE)
    if not data:
        break
    sha1.update(data)
    chunkHash= sha1.hexdigest()    
    print(data)
    print(chunkHash)
    print(int(chunkHash,16))
    
    
print(f"SHA1: {sha1.hexdigest()}")