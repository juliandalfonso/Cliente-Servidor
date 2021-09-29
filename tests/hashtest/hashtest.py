import hashlib

inputFile = str(input('\n\nNombre del archivo: '))
openedFile = open(inputFile)
readFile = openedFile.read()
FileEncoded = readFile.encode('utf-8')


sha1Hash = hashlib.sha1(FileEncoded)
sha1Hashed = sha1Hash.hexdigest()


print(f"\nArchivo: {inputFile}")
print(f"Hash: {sha1Hashed}")