from os import pipe
import socket 
import json


socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketServer.bind(('localhost',8000))
socketServer.listen(5)

while True:
    conexion, addr = socketServer.accept()
    print("conexión establecida")
    print(addr)
    dato = conexion.recv(1024)
    print(dato)
    conexion.send("Saludos desde python")
    conexion.close


# print(f'Esperando conexicones en {ip}:{puerto}')
# cliente, dir = socketServer.accept()
# print(f'Conexion con {cliente} en {dir}')
# datos = cliente.recv()
# print(datos.find('hola'))

# socketServer.send(socketServer.makefile('w',newline='Hola'))

# socketServer.close()
# while True:
#     pass

