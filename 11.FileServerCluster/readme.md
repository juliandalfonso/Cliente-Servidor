## File Server con Proxy y Servers

Programa tipo "google Drive" que corre un servidor que escucha uno o varios clientes y almacena archivos.

## Chunks: partes de archivo

El servidor recibe el archivo por partes para optimizar la memoria, al igual que la descarga del archivo también se hace por partes

## funcion de los hashes

se implementa la libreria hashlib para "encriptar" un archivo, básicamente es una función que recibe información (un archivo leido en binario por ejemplo) y lo convierte en un hash de 160-bits (20-bytes) sin importar el tamaño del archivo que se le pase

![](../Screenshots/sha1.png)

esto permite que si un usuario va a subir un archivo que el servidor ya tiene, no se guarda para evitar redundancia, es decir optimizar el almacenamiento

## Como usar el programa
  
- upload: sube un archivo al servidor
- list: lista los archivos subidos por un usuario o de todos
- sharelink comparte el link para descargar un archivo existente
- download: descarga el archivo solicitado al ingresar el link descarga del archivo correspondiente

---

Este programa se ejecuta corriendo dos archivos server.py  y client.py

Para correr el servidor ejecutamos

```console
python server.py
```

Para correr el cliente ejecutamos

```console
python client.py
```

## Manejo de los archivos

para subir un archivo este debe estar en la misma carpeta de client.py

al subir un archivo en el servidor, se crea una carpeta ServerFiles que contine el archivo separado por partes

al descargar un archivo del servidor, se crea una carpeta Clientfiles donde se guarda el archivo solicitado

## Screenshots

![](../Screenshots/10_MenuCliente.png)

![](../Screenshots/10_MenuCliente2.png)

![](../Screenshots/10_DATABASE.png)
