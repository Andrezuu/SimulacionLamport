import socket
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0' ,  5001))

def handleClient(data, addr):
    print(f"Mensaje recibido: {data.decode()} de {addr}")

while True:
    data, addr = sock.recvfrom(1024) 
    thread = Thread(target=handleClient, args=(data,addr))
    thread.start()
