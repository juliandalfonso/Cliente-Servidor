import hashlib

inputFile = str(input('\n\nNombre del archivo: '))
openedFile = open(inputFile, "rb")
readFile = openedFile.read()



sha1Hash = hashlib.sha1(readFile)
sha1Hashed = sha1Hash.hexdigest()


print(f"\nArchivo: {inputFile}")
print(f"Hash: {sha1Hashed}")